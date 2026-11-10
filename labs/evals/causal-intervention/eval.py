"""CGF causal intervention eval.

Two layers live here:

- a small structural causal model with exact enumeration, so observation,
  intervention, and counterfactual queries are computed rather than labeled;
- the record discipline that keeps those three kinds of statement separate
  once they leave the model.

Everything is finite and enumerated. Nothing here discovers causal structure
from data: the graph and the mechanisms are declared by the fixture.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Callable, Mapping


Values = dict[str, object]


@dataclass(frozen=True)
class Mechanism:
    """One structural equation: value = function(parent values, noise)."""

    variable: str
    parents: tuple[str, ...]
    noise: Mapping[object, float]
    function: Callable[[Mapping[str, object], object], object]


class StructuralCausalModel:
    """Finite structural causal model solved by enumerating exogenous noise."""

    def __init__(self, mechanisms: tuple[Mechanism, ...]) -> None:
        seen: set[str] = set()
        for mechanism in mechanisms:
            if mechanism.variable in seen:
                raise ValueError(f"duplicate mechanism: {mechanism.variable}")
            missing = [parent for parent in mechanism.parents if parent not in seen]
            if missing:
                raise ValueError(
                    f"{mechanism.variable} uses parents declared later or never: {missing}"
                )
            if not mechanism.noise:
                raise ValueError(f"{mechanism.variable} needs a noise distribution")
            if any(weight < 0.0 for weight in mechanism.noise.values()):
                raise ValueError("noise probabilities must be nonnegative")
            if abs(sum(mechanism.noise.values()) - 1.0) > 1e-9:
                raise ValueError(f"{mechanism.variable} noise must normalize")
            seen.add(mechanism.variable)
        self.mechanisms = tuple(mechanisms)
        self.variables = tuple(mechanism.variable for mechanism in mechanisms)

    def _noise_settings(self) -> list[tuple[float, tuple[object, ...]]]:
        settings = []
        supports = [tuple(mechanism.noise.items()) for mechanism in self.mechanisms]
        for combination in product(*supports):
            weight = 1.0
            for _, probability in combination:
                weight *= probability
            if weight > 0.0:
                settings.append((weight, tuple(value for value, _ in combination)))
        return settings

    def _solve(self, noise: tuple[object, ...], do: Mapping[str, object] | None) -> Values:
        do = do or {}
        unknown = set(do) - set(self.variables)
        if unknown:
            raise ValueError(f"intervention on undeclared variables: {sorted(unknown)}")
        values: Values = {}
        for mechanism, noise_value in zip(self.mechanisms, noise):
            if mechanism.variable in do:
                # An intervention replaces the mechanism. Parents no longer matter.
                values[mechanism.variable] = do[mechanism.variable]
                continue
            parent_values = {parent: values[parent] for parent in mechanism.parents}
            values[mechanism.variable] = mechanism.function(parent_values, noise_value)
        return values

    @staticmethod
    def _matches(values: Mapping[str, object], event: Mapping[str, object]) -> bool:
        return all(values[name] == expected for name, expected in event.items())

    def probability(
        self,
        event: Mapping[str, object],
        *,
        given: Mapping[str, object] | None = None,
        do: Mapping[str, object] | None = None,
    ) -> float:
        """P(event | given) in the observational or the do-regime."""

        given = given or {}
        numerator = 0.0
        denominator = 0.0
        for weight, noise in self._noise_settings():
            values = self._solve(noise, do)
            if not self._matches(values, given):
                continue
            denominator += weight
            if self._matches(values, event):
                numerator += weight
        if denominator <= 0.0:
            raise ValueError("conditioning event has probability zero")
        return numerator / denominator

    def counterfactual_probability(
        self,
        event: Mapping[str, object],
        *,
        evidence: Mapping[str, object],
        do: Mapping[str, object],
    ) -> float:
        """Abduction, action, prediction.

        The evidence is observed in the factual world. It updates the noise
        distribution. The intervention is then applied with that noise held
        fixed, which is what separates a counterfactual from an intervention on
        a fresh unit.
        """

        numerator = 0.0
        denominator = 0.0
        for weight, noise in self._noise_settings():
            if not self._matches(self._solve(noise, None), evidence):
                continue
            denominator += weight
            if self._matches(self._solve(noise, do), event):
                numerator += weight
        if denominator <= 0.0:
            raise ValueError("evidence has probability zero")
        return numerator / denominator


def backdoor_adjustment(
    model: StructuralCausalModel,
    *,
    treatment: Mapping[str, object],
    outcome: Mapping[str, object],
    adjustment: tuple[str, ...],
    adjustment_values: tuple[object, ...],
) -> float:
    """Estimate P(outcome | do(treatment)) from observational quantities only.

    Computes the sum over z of P(outcome | treatment, z) P(z). It equals the
    interventional probability only when `adjustment` blocks every backdoor
    path, which the caller must justify from the declared graph.
    """

    total = 0.0
    for combination in product(adjustment_values, repeat=len(adjustment)):
        stratum = dict(zip(adjustment, combination))
        weight = model.probability(stratum)
        if weight <= 0.0:
            continue
        total += weight * model.probability(outcome, given={**treatment, **stratum})
    return total


def confounded_model(effect_of_treatment: int = 1) -> StructuralCausalModel:
    """Z causes both X and Y; X also causes Y.

    P(X=1 | Z) is 0.9 when Z=1 and 0.1 when Z=0.
    P(Y=1 | X, Z) is (2 + effect_of_treatment * X + 6 * Z) / 10, shifted so it
    stays a probability when the effect is negative.
    """

    if effect_of_treatment not in (-1, 0, 1):
        raise ValueError("effect_of_treatment must be -1, 0, or 1")
    base = 3 if effect_of_treatment < 0 else 2

    def treatment(parents: Mapping[str, object], noise: object) -> int:
        if noise == "follow":
            return int(parents["Z"])
        return 1 if noise == "one" else 0

    def outcome(parents: Mapping[str, object], noise: object) -> int:
        threshold = base + effect_of_treatment * int(parents["X"]) + 6 * int(parents["Z"])
        return 1 if int(noise) < threshold else 0

    return StructuralCausalModel(
        (
            Mechanism("Z", (), {0: 0.5, 1: 0.5}, lambda parents, noise: int(noise)),
            Mechanism("X", ("Z",), {"follow": 0.8, "one": 0.1, "zero": 0.1}, treatment),
            Mechanism("Y", ("X", "Z"), {level: 0.1 for level in range(10)}, outcome),
        )
    )


# --- Record discipline -------------------------------------------------------


@dataclass(frozen=True)
class Record:
    record_id: str
    kind: str
    subject: str
    value: object
    scope: tuple[str, ...] = ()
    source_refs: tuple[str, ...] = ()


def observe(record_id: str, subject: str, value: object, source_refs: tuple[str, ...] = ()) -> Record:
    return Record(record_id, "observation", subject, value, (), source_refs)


def intervene(record_id: str, subject: str, value: object, scope: tuple[str, ...], source_refs: tuple[str, ...] = ()) -> Record:
    if not scope:
        raise ValueError("intervention scope is required")
    return Record(record_id, "intervention", subject, value, scope, source_refs)


def mark_counterfactual(record_id: str, subject: str, value: object) -> Record:
    return Record(record_id, "counterfactual", subject, value)


def block_counterfactual_promotion(record: Record) -> bool:
    return record.kind == "counterfactual"


def score_attribution(candidate: Record, outcome: Record, causal_scope: tuple[str, ...]) -> float:
    if candidate.kind != "intervention":
        return 0.0
    if candidate.subject != outcome.subject:
        return 0.0
    return 1.0 if set(candidate.scope) == set(causal_scope) else 0.0


def trace_attribution(candidate: Record, outcome: Record, causal_scope: tuple[str, ...]) -> dict[str, object]:
    score = score_attribution(candidate, outcome, causal_scope)
    return {
        "candidate_ref": candidate.record_id,
        "outcome_ref": outcome.record_id,
        "score": score,
        "allowed": score > 0.0,
    }


def effect_record(
    model: StructuralCausalModel,
    record_id: str,
    *,
    treatment: str,
    outcome: str,
) -> Record:
    """Package an average causal effect as an intervention record.

    The record carries the interventional contrast, never the observational
    one, and names the intervened variable as its scope.
    """

    effect = model.probability({outcome: 1}, do={treatment: 1}) - model.probability(
        {outcome: 1}, do={treatment: 0}
    )
    return intervene(record_id, outcome, effect, (treatment,), (f"do:{treatment}",))
