"""CGF Multimodal Outcome Stack eval."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping
import sys

ROOT = Path(__file__).resolve().parents[3]
ARCH_REF = ROOT / "architecture" / "reference" / "python"
if str(ARCH_REF) not in sys.path:
    sys.path.insert(0, str(ARCH_REF))

from cgf_architecture import AnalysisNode, GranularAnalysisEngine, Lens  # noqa: E402


TRAINING_ONLY = frozenset({"label", "future_outcome", "review_decision"})


@dataclass(frozen=True)
class EvidenceRecord:
    evidence_ref: str
    record_id: str
    record_type: str
    decoded: Mapping[str, Any]
    raw_payload: str | None = None


@dataclass
class TypedCaseGraph:
    graph_id: str
    nodes: dict[str, dict[str, Any]] = field(default_factory=dict)
    edges: list[tuple[str, str, str]] = field(default_factory=list)
    labels: dict[str, Any] = field(default_factory=dict)
    training_only_keys: set[str] = field(default_factory=set)

    def add_node(self, node_id: str, node_type: str, **attrs: Any) -> None:
        self.nodes[node_id] = {"type": node_type, **attrs}

    def add_edge(self, source: str, target: str, edge_type: str) -> None:
        if source not in self.nodes or target not in self.nodes:
            raise ValueError("edge endpoint missing")
        self.edges.append((source, target, edge_type))

    def add_training_label(self, key: str, value: Any) -> None:
        self.labels[key] = value
        self.training_only_keys.add(key)

    def feature_record(self) -> dict[str, Any]:
        record: dict[str, Any] = {}
        for node_id, node in sorted(self.nodes.items()):
            for key, value in sorted(node.items()):
                if key == "type" or key in self.training_only_keys:
                    continue
                record[f"{node_id}.{key}"] = value
        return record


@dataclass(frozen=True)
class FeatureView:
    view_id: str
    kind: str
    fields: tuple[str, ...]

    def select(self, record: Mapping[str, Any]) -> dict[str, Any]:
        return {field: record[field] for field in self.fields if field in record}


@dataclass(frozen=True)
class Processor:
    processor_id: str
    invariant_to: tuple[str, ...] = ()


@dataclass(frozen=True)
class TaskSpec:
    task_id: str
    sensitive_to: tuple[str, ...] = ()


def processor_allowed(processor: Processor, task: TaskSpec) -> bool:
    return not bool(set(processor.invariant_to) & set(task.sensitive_to))


def build_fixture() -> tuple[list[EvidenceRecord], TypedCaseGraph, dict[str, FeatureView], dict[str, Processor], dict[str, TaskSpec]]:
    records = [
        EvidenceRecord(
            "evidence:image-a",
            "record:texture",
            "texture-summary",
            {"texture_contrast": 0.82, "texture_uniformity": 0.71},
            raw_payload="not-copied-image-bytes",
        ),
        EvidenceRecord(
            "evidence:layout-a",
            "record:layout",
            "layout-summary",
            {"orientation_score": 0.91, "position_bias": 0.67},
            raw_payload="not-copied-layout-map",
        ),
        EvidenceRecord(
            "evidence:metadata-a",
            "record:metadata",
            "metadata-summary",
            {"source_quality": 0.88, "operator_confidence": 0.74},
            raw_payload="not-copied-metadata-doc",
        ),
    ]

    graph = TypedCaseGraph("case:synthetic-1")
    graph.add_node("case", "case", sample_id="synthetic-1")
    graph.add_node("texture", "record", texture_contrast=0.82, texture_uniformity=0.71, evidence_ref="evidence:image-a")
    graph.add_node("layout", "record", orientation_score=0.91, position_bias=0.67, evidence_ref="evidence:layout-a")
    graph.add_node("metadata", "record", source_quality=0.88, operator_confidence=0.74, evidence_ref="evidence:metadata-a")
    graph.add_edge("case", "texture", "has_record")
    graph.add_edge("case", "layout", "has_record")
    graph.add_edge("case", "metadata", "has_record")
    graph.add_training_label("label", "training-only-class")

    views = {
        "texture": FeatureView("texture", "invariant", ("texture.texture_contrast", "texture.texture_uniformity")),
        "layout": FeatureView("layout", "raw", ("layout.orientation_score", "layout.position_bias")),
        "metadata": FeatureView("metadata", "aligned", ("metadata.source_quality", "metadata.operator_confidence")),
    }
    processors = {
        "texture-invariant": Processor("texture-invariant", invariant_to=("orientation",)),
        "layout-direct": Processor("layout-direct"),
        "metadata-quality": Processor("metadata-quality"),
    }
    tasks = {
        "texture-task": TaskSpec("texture-task"),
        "orientation-task": TaskSpec("orientation-task", sensitive_to=("orientation",)),
    }
    return records, graph, views, processors, tasks


def build_engine(views: Mapping[str, FeatureView]) -> GranularAnalysisEngine:
    return GranularAnalysisEngine(
        lenses=(
            Lens("texture", "invariant", lambda row: views["texture"].select(row), ("evidence:image-a",)),
            Lens("layout", "raw", lambda row: views["layout"].select(row), ("evidence:layout-a",)),
            Lens("metadata", "aligned", lambda row: views["metadata"].select(row), ("evidence:metadata-a",)),
        ),
        analysis_nodes=(
            AnalysisNode(
                "texture-proposer",
                ("texture",),
                lambda outputs: {
                    "outcome_ref": "proposal:texture-supported",
                    "score": outputs[0].features["texture.texture_contrast"],
                    "confidence": 0.72,
                    "uncertainty": 0.25,
                    "metadata": {"route": "texture-invariant"},
                },
            ),
            AnalysisNode(
                "layout-proposer",
                ("layout",),
                lambda outputs: {
                    "outcome_ref": "proposal:layout-supported",
                    "score": outputs[0].features["layout.orientation_score"],
                    "confidence": 0.80,
                    "uncertainty": 0.18,
                    "metadata": {"route": "layout-direct"},
                },
            ),
            AnalysisNode(
                "combined-review-proposer",
                ("texture", "layout", "metadata"),
                lambda outputs: {
                    "outcome_ref": "proposal:combined-review",
                    "score": 0.94,
                    "confidence": 0.76,
                    "uncertainty": 0.16,
                    "metadata": {"route": "combined", "review_state": "review"},
                },
            ),
        ),
        commit_threshold=0.90,
        review_threshold=0.50,
        training_only_keys=TRAINING_ONLY,
    )


def run_eval():
    records, graph, views, processors, tasks = build_fixture()
    engine = build_engine(views)
    result = engine.run(graph.graph_id, graph.feature_record() | graph.labels)
    return records, graph, views, processors, tasks, result


if __name__ == "__main__":
    _, _, _, _, _, result = run_eval()
    print(result.decision)
    print(result.outcome_ref)
