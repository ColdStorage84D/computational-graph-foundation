"""Toy cortical-column world-model eval for CGF.

This is a small mechanism test, not a biological simulation. It models a few
ideas from cortical-column and Thousand Brains style descriptions:

- feature input is bound to a location in a local reference frame;
- movement updates the local reference-frame position by path integration;
- each column holds ambiguous object hypotheses from local evidence;
- lateral voting reinforces the object hypothesis shared across columns;
- the selected object model predicts the next feature after an action.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping


Coord = tuple[int, int]
UNKNOWN_FEATURE = "unknown"


def add_coord(left: Coord, right: Coord) -> Coord:
    return (left[0] + right[0], left[1] + right[1])


def sub_coord(left: Coord, right: Coord) -> Coord:
    return (left[0] - right[0], left[1] - right[1])


@dataclass(frozen=True)
class WorldObject:
    object_ref: str
    features: Mapping[Coord, str]

    def feature_at(self, position: Coord) -> str:
        return str(self.features.get(position, UNKNOWN_FEATURE))


@dataclass(frozen=True)
class LearningEvent:
    column_id: str
    object_ref: str
    action_delta: Coord
    position: Coord
    feature: str
    layer4_feature_input: str
    layer5_action_output: Coord
    layer6_reference_position: Coord


@dataclass(frozen=True)
class Observation:
    column_id: str
    position: Coord
    feature: str
    candidate_object_refs: tuple[str, ...]


@dataclass(frozen=True)
class VoteRound:
    round_index: int
    column_scores: Mapping[str, Mapping[str, float]]


@dataclass(frozen=True)
class VotingResult:
    selected_object_ref: str | None
    aggregate_scores: Mapping[str, float]
    vote_rounds: tuple[VoteRound, ...]
    rejected_object_refs: tuple[str, ...]
    selected_margin: float


@dataclass(frozen=True)
class Prediction:
    column_id: str
    object_ref: str
    from_position: Coord
    action_delta: Coord
    target_position: Coord
    predicted_feature: str | None
    observed_feature: str

    @property
    def matched(self) -> bool:
        return self.predicted_feature == self.observed_feature


@dataclass(frozen=True)
class WorldModelRun:
    training_events: tuple[LearningEvent, ...]
    observations: tuple[Observation, ...]
    voting: VotingResult
    prediction: Prediction
    claim_boundary: str


@dataclass
class CorticalColumn:
    """Local feature-location model with path integration.

    The names mirror the concept being tested:

    - layer 4 receives the current feature;
    - layer 5 emits movement as a local action delta;
    - layer 6 stores the current reference-frame position;
    - layers 2/3 are represented by object hypotheses used in voting.
    """

    column_id: str
    position: Coord = (0, 0)
    object_maps: dict[str, dict[Coord, str]] = field(default_factory=dict)

    def reset(self, position: Coord = (0, 0)) -> None:
        self.position = position

    def move(self, action_delta: Coord) -> Coord:
        self.position = add_coord(self.position, action_delta)
        return self.position

    def observe(self, world_object: WorldObject) -> str:
        return world_object.feature_at(self.position)

    def bind(self, object_ref: str, feature: str) -> None:
        self.object_maps.setdefault(object_ref, {})[self.position] = feature

    def learn_from(
        self,
        world_object: WorldObject,
        path: tuple[Coord, ...] | None = None,
    ) -> tuple[LearningEvent, ...]:
        positions = path or tuple(sorted(world_object.features))
        if not positions:
            return ()

        events: list[LearningEvent] = []
        self.reset(positions[0])
        for index, target in enumerate(positions):
            if index == 0:
                action_delta = (0, 0)
                self.reset(target)
            else:
                action_delta = sub_coord(target, self.position)
                self.move(action_delta)
            feature = self.observe(world_object)
            self.bind(world_object.object_ref, feature)
            events.append(
                LearningEvent(
                    column_id=self.column_id,
                    object_ref=world_object.object_ref,
                    action_delta=action_delta,
                    position=self.position,
                    feature=feature,
                    layer4_feature_input=feature,
                    layer5_action_output=action_delta,
                    layer6_reference_position=self.position,
                )
            )
        return tuple(events)

    def matching_hypotheses(self, position: Coord, feature: str) -> tuple[str, ...]:
        matches = [
            object_ref
            for object_ref, feature_map in self.object_maps.items()
            if feature_map.get(position) == feature
        ]
        return tuple(sorted(matches))

    def predict(self, object_ref: str, action_delta: Coord) -> str | None:
        target = add_coord(self.position, action_delta)
        return self.object_maps.get(object_ref, {}).get(target)


class ColumnVotingNetwork:
    """Lateral voting over local column hypotheses."""

    def __init__(self, *, vote_gain: float = 0.80, unsupported_decay: float = 0.35) -> None:
        self.vote_gain = float(vote_gain)
        self.unsupported_decay = float(unsupported_decay)

    def vote(self, observations: tuple[Observation, ...], *, rounds: int = 3) -> VotingResult:
        current: dict[str, dict[str, float]] = {
            observation.column_id: {
                object_ref: 1.0 for object_ref in observation.candidate_object_refs
            }
            for observation in observations
        }
        vote_rounds = [VoteRound(0, freeze_scores(current))]

        for round_index in range(1, rounds + 1):
            next_scores: dict[str, dict[str, float]] = {}
            for observation in observations:
                column_scores: dict[str, float] = {}
                for object_ref, previous_score in current[observation.column_id].items():
                    lateral_support = sum(
                        current[other.column_id].get(object_ref, 0.0)
                        for other in observations
                        if other.column_id != observation.column_id
                    )
                    if lateral_support > 0.0:
                        column_scores[object_ref] = 1.0 + self.vote_gain * lateral_support
                    else:
                        column_scores[object_ref] = previous_score * self.unsupported_decay
                next_scores[observation.column_id] = column_scores
            current = next_scores
            vote_rounds.append(VoteRound(round_index, freeze_scores(current)))

        aggregate = aggregate_scores(current)
        if not aggregate:
            return VotingResult(None, {}, tuple(vote_rounds), (), 0.0)

        ordered = sorted(aggregate.items(), key=lambda item: (-item[1], item[0]))
        selected_object_ref, selected_score = ordered[0]
        runner_up = ordered[1][1] if len(ordered) > 1 else 0.0
        rejected = tuple(object_ref for object_ref, _score in ordered[1:])
        return VotingResult(
            selected_object_ref=selected_object_ref,
            aggregate_scores=aggregate,
            vote_rounds=tuple(vote_rounds),
            rejected_object_refs=rejected,
            selected_margin=selected_score - runner_up,
        )


def freeze_scores(scores: Mapping[str, Mapping[str, float]]) -> dict[str, dict[str, float]]:
    return {
        column_id: {
            object_ref: round(float(score), 6)
            for object_ref, score in object_scores.items()
        }
        for column_id, object_scores in scores.items()
    }


def aggregate_scores(scores: Mapping[str, Mapping[str, float]]) -> dict[str, float]:
    aggregate: dict[str, float] = {}
    for object_scores in scores.values():
        for object_ref, score in object_scores.items():
            aggregate[object_ref] = aggregate.get(object_ref, 0.0) + float(score)
    return {object_ref: round(score, 6) for object_ref, score in aggregate.items()}


OBJECT_LIBRARY: dict[str, WorldObject] = {
    "object:cup": WorldObject(
        "object:cup",
        {
            (0, 0): "handle_curve",
            (1, 0): "smooth_wall",
            (2, 0): "rim_arc",
            (2, 1): "hollow_ceramic",
        },
    ),
    "object:saucer": WorldObject(
        "object:saucer",
        {
            (0, 0): "flat_ceramic",
            (1, 0): "shallow_dish",
            (2, 0): "rim_arc",
        },
    ),
    "object:wine-glass": WorldObject(
        "object:wine-glass",
        {
            (0, 0): "thin_stem",
            (1, 0): "smooth_glass",
            (2, 0): "rim_arc",
            (2, 1): "empty_bowl",
        },
    ),
    "object:drawer": WorldObject(
        "object:drawer",
        {
            (0, 0): "handle_curve",
            (1, 0): "wood_panel",
            (2, 0): "flat_front",
        },
    ),
    "object:teapot": WorldObject(
        "object:teapot",
        {
            (0, 0): "handle_curve",
            (1, 0): "round_body",
            (2, 0): "spout_tip",
        },
    ),
}


def train_columns(column_ids: tuple[str, ...] = ("thumb-column", "index-column")) -> tuple[
    tuple[CorticalColumn, ...], tuple[LearningEvent, ...]
]:
    columns = tuple(CorticalColumn(column_id) for column_id in column_ids)
    events: list[LearningEvent] = []
    for column in columns:
        for world_object in OBJECT_LIBRARY.values():
            events.extend(column.learn_from(world_object))
    return columns, tuple(events)


def observe_object(
    columns: tuple[CorticalColumn, ...],
    world_object: WorldObject,
    contacts: Mapping[str, Coord],
) -> tuple[Observation, ...]:
    observations: list[Observation] = []
    for column in columns:
        position = contacts[column.column_id]
        column.reset(position)
        feature = column.observe(world_object)
        observations.append(
            Observation(
                column_id=column.column_id,
                position=position,
                feature=feature,
                candidate_object_refs=column.matching_hypotheses(position, feature),
            )
        )
    return tuple(observations)


def predict_after_action(
    column: CorticalColumn,
    world_object: WorldObject,
    object_ref: str,
    action_delta: Coord,
) -> Prediction:
    from_position = column.position
    target_position = add_coord(from_position, action_delta)
    return Prediction(
        column_id=column.column_id,
        object_ref=object_ref,
        from_position=from_position,
        action_delta=action_delta,
        target_position=target_position,
        predicted_feature=column.predict(object_ref, action_delta),
        observed_feature=world_object.feature_at(target_position),
    )


def run_fixture() -> WorldModelRun:
    columns, training_events = train_columns()
    by_id = {column.column_id: column for column in columns}
    cup = OBJECT_LIBRARY["object:cup"]

    observations = observe_object(
        columns,
        cup,
        {
            "thumb-column": (0, 0),
            "index-column": (2, 0),
        },
    )
    voting = ColumnVotingNetwork().vote(observations)

    index_column = by_id["index-column"]
    index_column.reset((2, 0))
    if voting.selected_object_ref is None:
        raise AssertionError("fixture should produce a selected object")
    prediction = predict_after_action(
        index_column,
        cup,
        voting.selected_object_ref,
        (0, 1),
    )

    return WorldModelRun(
        training_events=training_events,
        observations=observations,
        voting=voting,
        prediction=prediction,
        claim_boundary=(
            "Toy graph mechanism only: local feature-location memory, "
            "path integration, lateral voting, and one-step prediction. "
            "No biological, AGI, or real-world performance claim."
        ),
    )
