"""Optional stdlib reference for CGF Architecture contracts.

The module is intentionally small. It is a teaching implementation of execution
graph contracts, not a required framework.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Mapping


@dataclass(frozen=True)
class Event:
    event_id: str
    event_type: str
    correlation_id: str
    payload: Mapping[str, Any] = field(default_factory=dict)
    caused_by: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_json(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "correlation_id": self.correlation_id,
            "payload": dict(self.payload),
            "caused_by": self.caused_by,
            "metadata": dict(self.metadata),
        }


class EventLog:
    """Append-only event log used as replay source."""

    def __init__(self) -> None:
        self._events: list[Event] = []

    def append(
        self,
        event_type: str,
        correlation_id: str,
        payload: Mapping[str, Any] | None = None,
        *,
        caused_by: str | None = None,
        metadata: Mapping[str, Any] | None = None,
    ) -> Event:
        event = Event(
            event_id=f"event:{len(self._events) + 1}",
            event_type=str(event_type),
            correlation_id=str(correlation_id),
            payload=dict(payload or {}),
            caused_by=caused_by,
            metadata=dict(metadata or {}),
        )
        self._events.append(event)
        return event

    def all(self) -> tuple[Event, ...]:
        return tuple(self._events)

    def by_type(self, event_type: str) -> tuple[Event, ...]:
        return tuple(event for event in self._events if event.event_type == event_type)

    def by_correlation(self, correlation_id: str) -> tuple[Event, ...]:
        return tuple(event for event in self._events if event.correlation_id == correlation_id)

    def to_json(self) -> list[dict[str, Any]]:
        return [event.to_json() for event in self._events]

    @classmethod
    def from_json(cls, rows: list[Mapping[str, Any]]) -> "EventLog":
        log = cls()
        for row in rows:
            log._events.append(
                Event(
                    event_id=str(row["event_id"]),
                    event_type=str(row["event_type"]),
                    correlation_id=str(row["correlation_id"]),
                    payload=dict(row.get("payload", {})),
                    caused_by=None if row.get("caused_by") is None else str(row.get("caused_by")),
                    metadata=dict(row.get("metadata", {})),
                )
            )
        return log


@dataclass(frozen=True)
class GraphNode:
    node_id: str
    node_type: str
    features: Mapping[str, Any] = field(default_factory=dict)
    attrs: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Edge:
    edge_id: str
    source: str
    target: str
    edge_type: str
    attrs: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class HypergraphNode:
    node_id: str
    node_type: str
    features: Mapping[str, Any] = field(default_factory=dict)
    evidence_refs: tuple[str, ...] = ()


@dataclass(frozen=True)
class Hyperedge:
    edge_id: str
    edge_type: str
    endpoint_ids: tuple[str, ...]
    features: Mapping[str, Any] = field(default_factory=dict)
    evidence_refs: tuple[str, ...] = ()


@dataclass(frozen=True)
class EncodedHypergraph:
    graph_id: str
    nodes: Mapping[str, HypergraphNode] = field(default_factory=dict)
    hyperedges: Mapping[str, Hyperedge] = field(default_factory=dict)

    def to_json(self) -> dict[str, Any]:
        return {
            "graph_id": self.graph_id,
            "nodes": [
                {
                    "node_id": node.node_id,
                    "node_type": node.node_type,
                    "features": dict(node.features),
                    "evidence_refs": list(node.evidence_refs),
                }
                for node in self.nodes.values()
            ],
            "hyperedges": [
                {
                    "edge_id": edge.edge_id,
                    "edge_type": edge.edge_type,
                    "endpoint_ids": list(edge.endpoint_ids),
                    "features": dict(edge.features),
                    "evidence_refs": list(edge.evidence_refs),
                }
                for edge in self.hyperedges.values()
            ],
        }

    def flatten_features(self, *, prefix: str = "hypergraph") -> dict[str, Any]:
        record: dict[str, Any] = {}
        for node_id, node in sorted(self.nodes.items()):
            for key, value in sorted(node.features.items()):
                record[f"{prefix}.node.{node_id}.{key}"] = value
        for edge_id, edge in sorted(self.hyperedges.items()):
            for key, value in sorted(edge.features.items()):
                record[f"{prefix}.edge.{edge_id}.{key}"] = value
        return record


class HypergraphEncoder:
    """Generic evidence-to-hypergraph encoder.

    The encoder is domain-neutral. Applications supply bounded evidence nodes
    and relations; the encoder preserves typed nodes, n-ary hyperedges,
    features, and evidence references without owning domain semantics.
    """

    def __init__(self, graph_id: str) -> None:
        self.graph_id = str(graph_id)
        self._nodes: dict[str, HypergraphNode] = {}
        self._hyperedges: dict[str, Hyperedge] = {}

    def add_node(
        self,
        node_id: str,
        node_type: str,
        *,
        features: Mapping[str, Any] | None = None,
        evidence_refs: tuple[str, ...] = (),
    ) -> "HypergraphEncoder":
        self._nodes[str(node_id)] = HypergraphNode(
            str(node_id),
            str(node_type),
            dict(features or {}),
            tuple(str(ref) for ref in evidence_refs),
        )
        return self

    def add_hyperedge(
        self,
        edge_id: str,
        edge_type: str,
        endpoint_ids: tuple[str, ...] | list[str],
        *,
        features: Mapping[str, Any] | None = None,
        evidence_refs: tuple[str, ...] = (),
    ) -> "HypergraphEncoder":
        endpoints = tuple(str(endpoint_id) for endpoint_id in endpoint_ids)
        if len(endpoints) < 2:
            raise ValueError("hyperedge needs at least two endpoints")
        missing = [endpoint_id for endpoint_id in endpoints if endpoint_id not in self._nodes]
        if missing:
            raise ValueError(f"hyperedge endpoint missing: {', '.join(missing)}")
        self._hyperedges[str(edge_id)] = Hyperedge(
            str(edge_id),
            str(edge_type),
            endpoints,
            dict(features or {}),
            tuple(str(ref) for ref in evidence_refs),
        )
        return self

    def build(self) -> EncodedHypergraph:
        return EncodedHypergraph(
            self.graph_id,
            dict(self._nodes),
            dict(self._hyperedges),
        )


@dataclass(frozen=True)
class GraphState:
    graph_id: str
    nodes: Mapping[str, GraphNode] = field(default_factory=dict)
    edges: Mapping[str, Edge] = field(default_factory=dict)

    def with_node(self, node: GraphNode) -> "GraphState":
        nodes = dict(self.nodes)
        nodes[node.node_id] = node
        return GraphState(self.graph_id, nodes, dict(self.edges))

    def with_edge(self, edge: Edge) -> "GraphState":
        if edge.source not in self.nodes or edge.target not in self.nodes:
            raise ValueError("edge endpoints must exist before adding an edge")
        edges = dict(self.edges)
        edges[edge.edge_id] = edge
        return GraphState(self.graph_id, dict(self.nodes), edges)


@dataclass(frozen=True)
class Path:
    path_id: str
    node_ids: tuple[str, ...]
    edge_ids: tuple[str, ...] = ()


def validate_path(graph: GraphState, path: Path) -> list[str]:
    """Validate a path fail-closed against a graph view."""

    errors: list[str] = []
    for node_id in path.node_ids:
        if node_id not in graph.nodes:
            errors.append(f"missing node {node_id}")
    if len(path.node_ids) <= 1:
        if path.edge_ids:
            errors.append("fact path cannot carry edges")
        return errors
    if len(path.edge_ids) != len(path.node_ids) - 1:
        errors.append("edge count must equal node count minus one")
        return errors
    for index, edge_id in enumerate(path.edge_ids):
        edge = graph.edges.get(edge_id)
        if edge is None:
            errors.append(f"missing edge {edge_id}")
            continue
        expected_source = path.node_ids[index]
        expected_target = path.node_ids[index + 1]
        if edge.source != expected_source or edge.target != expected_target:
            errors.append(f"edge {edge_id} does not connect path step {index}")
    return errors


@dataclass(frozen=True)
class GateDecision:
    gate_id: str
    passed: bool
    reason: str = ""
    hard: bool = True
    evidence_refs: tuple[str, ...] = ()


@dataclass(frozen=True)
class Proposal:
    proposal_id: str
    action_ref: str
    score: float = 0.0
    risk: float = 0.0
    confidence: float = 0.0
    uncertainty: float = 1.0
    path: Path | None = None
    policy_required: str | None = None
    gates: tuple[GateDecision, ...] = ()
    evidence_refs: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def hard_violations(self) -> tuple[str, ...]:
        return tuple(gate.gate_id for gate in self.gates if gate.hard and not gate.passed)

    def feasible(self, policy_basis: frozenset[str] = frozenset()) -> bool:
        if self.hard_violations:
            return False
        if self.policy_required and self.policy_required not in policy_basis:
            return False
        return True


@dataclass(frozen=True)
class CommitDecision:
    decision: str
    selected_proposal_id: str | None
    reason: str
    proposal_ids: tuple[str, ...]

    @property
    def committed(self) -> bool:
        return self.decision == "commit" and self.selected_proposal_id is not None


class CommitOperator:
    """Deterministic commit authority for proposal sets."""

    def commit(
        self,
        proposals: tuple[Proposal, ...] | list[Proposal],
        *,
        policy_basis: frozenset[str] = frozenset(),
    ) -> CommitDecision:
        ordered = tuple(proposals)
        feasible = [proposal for proposal in ordered if proposal.feasible(policy_basis)]
        if not feasible:
            return CommitDecision(
                "reject",
                None,
                "no_feasible_proposal",
                tuple(proposal.proposal_id for proposal in ordered),
            )
        selected = min(feasible, key=lambda proposal: (proposal.score, proposal.proposal_id))
        return CommitDecision(
            "commit",
            selected.proposal_id,
            "lowest_feasible_score",
            tuple(proposal.proposal_id for proposal in ordered),
        )


PENDING = "pending"
RESOLVED = "resolved"
EXPIRED = "expired"


@dataclass(frozen=True)
class EligibilityTrace:
    trace_id: str
    proposal_id: str
    path_id: str | None
    cycle_id: str
    status: str = PENDING
    succeeded: bool | None = None


class EligibilityStore:
    def __init__(self) -> None:
        self._traces: dict[str, EligibilityTrace] = {}

    def create(self, trace_id: str, *, proposal: Proposal, cycle_id: str) -> EligibilityTrace:
        trace = EligibilityTrace(
            trace_id=trace_id,
            proposal_id=proposal.proposal_id,
            path_id=None if proposal.path is None else proposal.path.path_id,
            cycle_id=str(cycle_id),
        )
        self._traces[trace_id] = trace
        return trace

    def resolve(self, trace_id: str, succeeded: bool | None) -> EligibilityTrace:
        trace = self._require_pending(trace_id)
        resolved = EligibilityTrace(
            trace.trace_id,
            trace.proposal_id,
            trace.path_id,
            trace.cycle_id,
            RESOLVED,
            succeeded,
        )
        self._traces[trace_id] = resolved
        return resolved

    def expire(self, trace_id: str) -> EligibilityTrace:
        trace = self._require_pending(trace_id)
        expired = EligibilityTrace(
            trace.trace_id,
            trace.proposal_id,
            trace.path_id,
            trace.cycle_id,
            EXPIRED,
            None,
        )
        self._traces[trace_id] = expired
        return expired

    def get(self, trace_id: str) -> EligibilityTrace | None:
        return self._traces.get(trace_id)

    def _require_pending(self, trace_id: str) -> EligibilityTrace:
        trace = self._traces.get(trace_id)
        if trace is None:
            raise ValueError(f"unknown eligibility trace {trace_id}")
        if trace.status != PENDING:
            raise ValueError(f"eligibility trace {trace_id} is not pending")
        return trace


@dataclass(frozen=True)
class OutcomeObservation:
    outcome_id: str
    eligibility_trace_id: str
    succeeded: bool | None
    evidence_refs: tuple[str, ...] = ()


@dataclass(frozen=True)
class ValueMemory:
    key: str
    success_count: int = 0
    failure_count: int = 0
    risk: float = 0.0
    uncertainty: float = 1.0
    sample_count: int = 0
    evidence_refs: tuple[str, ...] = ()


@dataclass(frozen=True)
class MemoryUpdate:
    key: str
    kind: str
    before: ValueMemory
    after: ValueMemory


class ValueMemoryStore:
    def __init__(self) -> None:
        self._memory: dict[str, ValueMemory] = {}

    def get(self, key: str) -> ValueMemory:
        return self._memory.get(key, ValueMemory(key))

    def apply(self, outcome: OutcomeObservation, *, key: str) -> MemoryUpdate:
        before = self.get(key)
        refs = tuple(dict.fromkeys((*before.evidence_refs, *outcome.evidence_refs)))[-16:]
        if outcome.succeeded is True:
            after = ValueMemory(
                key,
                before.success_count + 1,
                before.failure_count,
                max(0.0, before.risk * 0.75),
                max(0.0, before.uncertainty * 0.70),
                before.sample_count + 1,
                refs,
            )
            kind = "reinforce"
        elif outcome.succeeded is False:
            after = ValueMemory(
                key,
                before.success_count,
                before.failure_count + 1,
                min(1.0, before.risk + 0.25),
                min(1.0, before.uncertainty + 0.10),
                before.sample_count + 1,
                refs,
            )
            kind = "inhibit"
        else:
            after = ValueMemory(
                key,
                before.success_count,
                before.failure_count,
                before.risk,
                min(1.0, before.uncertainty + 0.20),
                before.sample_count + 1,
                refs,
            )
            kind = "uncertainty"
        self._memory[key] = after
        return MemoryUpdate(key, kind, before, after)


@dataclass(frozen=True)
class Trace:
    correlation_id: str
    event_ids: tuple[str, ...]
    event_types: tuple[str, ...]

    @classmethod
    def from_log(cls, log: EventLog, correlation_id: str) -> "Trace":
        events = log.by_correlation(correlation_id)
        return Trace(
            correlation_id,
            tuple(event.event_id for event in events),
            tuple(event.event_type for event in events),
        )


DEFAULT_TRAINING_ONLY_KEYS = frozenset({"label", "labels", "target", "outcome", "ground_truth", "answer"})


@dataclass(frozen=True)
class LensOutput:
    lens_id: str
    kind: str
    input_id: str
    features: Mapping[str, Any] = field(default_factory=dict)
    evidence_refs: tuple[str, ...] = ()


@dataclass(frozen=True)
class Lens:
    lens_id: str
    kind: str
    handler: Callable[[Mapping[str, Any]], Mapping[str, Any]]
    evidence_refs: tuple[str, ...] = ()

    def run(
        self,
        input_id: str,
        input_record: Mapping[str, Any],
        *,
        training_only_keys: frozenset[str] = DEFAULT_TRAINING_ONLY_KEYS,
    ) -> LensOutput:
        sanitized = {
            key: value
            for key, value in input_record.items()
            if str(key) not in training_only_keys
        }
        features = dict(self.handler(sanitized))
        leaked = sorted(str(key) for key in features if str(key) in training_only_keys)
        if leaked:
            raise ValueError(f"lens {self.lens_id} emitted training-only keys: {', '.join(leaked)}")
        return LensOutput(
            lens_id=self.lens_id,
            kind=self.kind,
            input_id=str(input_id),
            features=features,
            evidence_refs=self.evidence_refs,
        )


@dataclass(frozen=True)
class AnalysisProposal:
    proposal_id: str
    proposer_id: str
    outcome_ref: str
    score: float
    confidence: float
    uncertainty: float
    lens_ids: tuple[str, ...]
    evidence_refs: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class AnalysisNode:
    node_id: str
    required_lens_ids: tuple[str, ...]
    handler: Callable[[tuple[LensOutput, ...]], Mapping[str, Any]]

    def run(self, input_id: str, lens_outputs: Mapping[str, LensOutput]) -> AnalysisProposal:
        missing = [lens_id for lens_id in self.required_lens_ids if lens_id not in lens_outputs]
        if missing:
            raise ValueError(f"analysis node {self.node_id} missing lenses: {', '.join(missing)}")
        selected = tuple(lens_outputs[lens_id] for lens_id in self.required_lens_ids)
        row = dict(self.handler(selected))
        if "outcome_ref" not in row:
            raise ValueError(f"analysis node {self.node_id} did not emit outcome_ref")
        evidence_refs: list[str] = []
        for output in selected:
            evidence_refs.extend(output.evidence_refs)
        evidence_refs.extend(str(ref) for ref in row.get("evidence_refs", ()) or ())
        return AnalysisProposal(
            proposal_id=f"proposal:{input_id}:{self.node_id}",
            proposer_id=self.node_id,
            outcome_ref=str(row["outcome_ref"]),
            score=float(row.get("score", 0.0)),
            confidence=float(row.get("confidence", 0.0)),
            uncertainty=float(row.get("uncertainty", 1.0)),
            lens_ids=tuple(self.required_lens_ids),
            evidence_refs=tuple(dict.fromkeys(evidence_refs)),
            metadata=dict(row.get("metadata", {}) or {}),
        )


@dataclass(frozen=True)
class GranularAnalysisTrace:
    trace_id: str
    input_id: str
    lens_outputs: tuple[LensOutput, ...]
    proposals: tuple[AnalysisProposal, ...]
    decision: str
    reason: str
    selected_proposal_id: str | None = None
    outcome_ref: str | None = None
    rejected_proposal_ids: tuple[str, ...] = ()
    hidden_keys_excluded: tuple[str, ...] = ()
    errors: tuple[str, ...] = ()


@dataclass(frozen=True)
class GranularAnalysisResult:
    decision: str
    outcome_ref: str | None
    selected_proposal: AnalysisProposal | None
    trace: GranularAnalysisTrace


class GranularAnalysisEngine:
    """Tiny engine for many lenses, many proposers, one traceable outcome."""

    def __init__(
        self,
        lenses: tuple[Lens, ...] | list[Lens],
        analysis_nodes: tuple[AnalysisNode, ...] | list[AnalysisNode],
        *,
        commit_threshold: float = 0.70,
        review_threshold: float = 0.40,
        training_only_keys: frozenset[str] = DEFAULT_TRAINING_ONLY_KEYS,
    ) -> None:
        self.lenses = tuple(lenses)
        self.analysis_nodes = tuple(analysis_nodes)
        self.commit_threshold = float(commit_threshold)
        self.review_threshold = float(review_threshold)
        self.training_only_keys = training_only_keys
        if self.review_threshold > self.commit_threshold:
            raise ValueError("review_threshold cannot exceed commit_threshold")

    def run(self, input_id: str, input_record: Mapping[str, Any]) -> GranularAnalysisResult:
        hidden_keys = tuple(
            sorted(str(key) for key in input_record if str(key) in self.training_only_keys)
        )
        outputs: dict[str, LensOutput] = {}
        errors: list[str] = []
        for lens in self.lenses:
            try:
                output = lens.run(
                    str(input_id),
                    input_record,
                    training_only_keys=self.training_only_keys,
                )
                outputs[output.lens_id] = output
            except Exception as exc:  # pragma: no cover - message path is tested through decisions
                errors.append(f"lens:{lens.lens_id}:{exc}")

        proposals: list[AnalysisProposal] = []
        for node in self.analysis_nodes:
            try:
                proposals.append(node.run(str(input_id), outputs))
            except Exception as exc:
                errors.append(f"node:{node.node_id}:{exc}")

        selected: AnalysisProposal | None = None
        if proposals:
            selected = max(
                proposals,
                key=lambda proposal: (
                    proposal.score,
                    proposal.confidence,
                    -proposal.uncertainty,
                    proposal.proposal_id,
                ),
            )

        decision: str
        reason: str
        if selected is None:
            decision = "defer" if errors else "abstain"
            reason = "analysis_errors" if errors else "no_proposals"
        elif selected.score >= self.commit_threshold and selected.confidence >= self.commit_threshold:
            decision = "commit"
            reason = "best_proposal_passed_commit_threshold"
        elif selected.score >= self.review_threshold:
            decision = "review"
            reason = "best_proposal_needs_review"
        else:
            decision = "abstain"
            reason = "best_proposal_below_review_threshold"

        selected_id = selected.proposal_id if selected is not None and decision in {"commit", "review"} else None
        outcome_ref = selected.outcome_ref if selected is not None and decision in {"commit", "review"} else None
        rejected = tuple(
            proposal.proposal_id
            for proposal in proposals
            if proposal.proposal_id != selected_id
        )
        trace = GranularAnalysisTrace(
            trace_id=f"granular-trace:{input_id}",
            input_id=str(input_id),
            lens_outputs=tuple(outputs[lens.lens_id] for lens in self.lenses if lens.lens_id in outputs),
            proposals=tuple(proposals),
            decision=decision,
            reason=reason,
            selected_proposal_id=selected_id,
            outcome_ref=outcome_ref,
            rejected_proposal_ids=rejected,
            hidden_keys_excluded=hidden_keys,
            errors=tuple(errors),
        )
        return GranularAnalysisResult(decision, outcome_ref, selected if selected_id else None, trace)


NodeHandler = Callable[[Any], Any]


@dataclass(frozen=True)
class GraphRoute:
    source_node_id: str
    target_node_id: str
    channel: str


@dataclass(frozen=True)
class GraphRelation:
    source_node_id: str
    target_node_id: str
    relation_type: str
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class BotNode:
    node_id: str
    surface: str
    handler: NodeHandler | None = None
    mode: str = "function"
    gates: tuple[GateDecision, ...] = ()
    subgraph: "BotGraph | None" = None


@dataclass(frozen=True)
class NodeRun:
    node_id: str
    channel: str
    payload: Any = None
    skipped: bool = False
    reason: str = ""
    trace_path: tuple[str, ...] = ()


class BotGraph:
    """Spine-routed surface graph for bot or processor applications."""

    def __init__(
        self,
        graph_id: str,
        *,
        nodes: Mapping[str, BotNode],
        routes: tuple[GraphRoute, ...],
        relations: tuple[GraphRelation, ...] = (),
        spine_node_id: str = "spine",
        brain_node_id: str = "brain",
    ) -> None:
        self.graph_id = str(graph_id)
        self.nodes = dict(nodes)
        self.routes = tuple(routes)
        self.relations = tuple(relations)
        self.spine_node_id = spine_node_id
        self.brain_node_id = brain_node_id
        self.validate()

    def validate(self) -> None:
        if self.spine_node_id not in self.nodes:
            raise ValueError("bot graph needs a spine node")
        if self.brain_node_id not in self.nodes:
            raise ValueError("bot graph needs a brain node")
        for route in self.routes:
            if route.source_node_id not in self.nodes or route.target_node_id not in self.nodes:
                raise ValueError("route endpoint must exist")
            if self.spine_node_id not in {route.source_node_id, route.target_node_id}:
                raise ValueError("runtime routes must pass through the spine")
        for relation in self.relations:
            if relation.source_node_id not in self.nodes or relation.target_node_id not in self.nodes:
                raise ValueError("relation endpoint must exist")

    def dispatch(self, channel: str, payload: Any, *, source_node_id: str | None = None) -> tuple[NodeRun, ...]:
        source = source_node_id or self.brain_node_id
        if source != self.spine_node_id and not self._has_route(source, self.spine_node_id, channel):
            raise ValueError(f"{source} has no route to spine for {channel}")
        runs: list[NodeRun] = []
        targets = [
            route.target_node_id
            for route in self.routes
            if route.source_node_id == self.spine_node_id and route.channel == channel
        ]
        for target in targets:
            if target == source:
                continue
            node = self.nodes[target]
            failed = tuple(gate for gate in node.gates if not gate.passed)
            trace_path = (source, self.spine_node_id, target)
            if failed:
                runs.append(NodeRun(target, channel, None, True, "gate_failed", trace_path))
                continue
            if node.subgraph is not None:
                child_runs = node.subgraph.dispatch(channel, payload, source_node_id=node.subgraph.brain_node_id)
                child_payload = tuple(run.payload for run in child_runs if not run.skipped)
                runs.append(NodeRun(target, channel, child_payload, False, "", trace_path))
                continue
            result = payload if node.handler is None else node.handler(payload)
            runs.append(NodeRun(target, channel, result, False, "", trace_path))
        return tuple(runs)

    def _has_route(self, source: str, target: str, channel: str) -> bool:
        return any(
            route.source_node_id == source
            and route.target_node_id == target
            and route.channel == channel
            for route in self.routes
        )


class BotGraphBuilder:
    def __init__(self, graph_id: str, *, spine_node_id: str = "spine", brain_node_id: str = "brain") -> None:
        self.graph_id = graph_id
        self.spine_node_id = spine_node_id
        self.brain_node_id = brain_node_id
        self._nodes: dict[str, BotNode] = {
            spine_node_id: BotNode(spine_node_id, "spine"),
            brain_node_id: BotNode(brain_node_id, "brain"),
        }
        self._routes: list[GraphRoute] = []
        self._relations: list[GraphRelation] = []

    def add_surface(self, node_id: str, surface: str, *, handler: NodeHandler | None = None) -> "BotGraphBuilder":
        self._nodes[node_id] = BotNode(node_id, surface, handler)
        return self

    def add_gated_surface(
        self,
        node_id: str,
        surface: str,
        *,
        gates: tuple[GateDecision, ...],
        handler: NodeHandler | None = None,
    ) -> "BotGraphBuilder":
        self._nodes[node_id] = BotNode(node_id, surface, handler, gates=gates)
        return self

    def add_subgraph(self, node_id: str, surface: str, subgraph: BotGraph) -> "BotGraphBuilder":
        self._nodes[node_id] = BotNode(node_id, surface, mode="graph", subgraph=subgraph)
        return self

    def add_route(self, source_node_id: str, target_node_id: str, channel: str) -> "BotGraphBuilder":
        if self.spine_node_id not in {source_node_id, target_node_id}:
            raise ValueError("runtime routes must pass through the spine")
        self._routes.append(GraphRoute(source_node_id, target_node_id, channel))
        return self

    def connect_to_spine(self, node_id: str, channel: str) -> "BotGraphBuilder":
        self.add_route(self.brain_node_id, self.spine_node_id, channel)
        self.add_route(self.spine_node_id, node_id, channel)
        return self

    def add_relation(self, source_node_id: str, target_node_id: str, relation_type: str) -> "BotGraphBuilder":
        self._relations.append(GraphRelation(source_node_id, target_node_id, relation_type))
        return self

    def build(self) -> BotGraph:
        return BotGraph(
            self.graph_id,
            nodes=self._nodes,
            routes=tuple(self._routes),
            relations=tuple(self._relations),
            spine_node_id=self.spine_node_id,
            brain_node_id=self.brain_node_id,
        )
