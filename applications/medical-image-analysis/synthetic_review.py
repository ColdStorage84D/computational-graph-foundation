"""Synthetic medical image analysis CGF review example.

This is a tiny application example, not a medical implementation.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping
import sys

ROOT = Path(__file__).resolve().parents[2]
ARCH_REF = ROOT / "architecture" / "reference" / "python"
if str(ARCH_REF) not in sys.path:
    sys.path.insert(0, str(ARCH_REF))

from cgf_architecture import AnalysisNode, GranularAnalysisEngine, HypergraphEncoder, Lens  # noqa: E402


APP_DIR = Path(__file__).resolve().parent
FIXTURE_RECORDS = APP_DIR / "data" / "fixture" / "records.json"

TRAINING_ONLY_KEYS = frozenset(
    {"answer", "expected_decision", "label", "future_outcome", "review_decision", "diagnosis"}
)


@dataclass(frozen=True)
class SourceEvidence:
    evidence_ref: str
    evidence_type: str
    bounded_summary: Mapping[str, Any]
    raw_payload_present: bool = True


@dataclass
class MedicalImageAnalysisGraph:
    case_id: str
    nodes: dict[str, dict[str, Any]] = field(default_factory=dict)
    edges: list[tuple[str, str, str]] = field(default_factory=list)
    later_records: dict[str, Any] = field(default_factory=dict)

    def add_node(self, node_id: str, node_type: str, **fields: Any) -> None:
        self.nodes[node_id] = {"type": node_type, **fields}

    def add_edge(self, source: str, target: str, relation: str) -> None:
        if source not in self.nodes or target not in self.nodes:
            raise ValueError("edge endpoint missing")
        self.edges.append((source, target, relation))

    def add_later_record(self, key: str, value: Any) -> None:
        self.later_records[key] = value

    def encoded_hypergraph(self):
        encoder = HypergraphEncoder(self.case_id)
        for node_id, fields in sorted(self.nodes.items()):
            node_type = str(fields.get("type", "record"))
            features = {
                key: value
                for key, value in sorted(fields.items())
                if key != "type" and key != "evidence_ref" and key not in TRAINING_ONLY_KEYS
            }
            evidence_ref = fields.get("evidence_ref")
            evidence_refs = () if evidence_ref is None else (str(evidence_ref),)
            encoder.add_node(
                node_id,
                node_type,
                features=features,
                evidence_refs=evidence_refs,
            )
        for index, (source, target, relation) in enumerate(self.edges):
            encoder.add_hyperedge(
                f"edge:{index}:{relation}",
                relation,
                (source, target),
            )
        return encoder.build()

    def live_record(self) -> dict[str, Any]:
        record: dict[str, Any] = {}
        for node_id, fields in sorted(self.nodes.items()):
            for key, value in sorted(fields.items()):
                if key == "type" or key in TRAINING_ONLY_KEYS:
                    continue
                record[f"{node_id}.{key}"] = value
        return record


def _float_record_value(record: Mapping[str, Any], key: str, default: float) -> float:
    try:
        return float(record.get(key, default))
    except (TypeError, ValueError):
        return default


def build_case_from_record(record: Mapping[str, Any]) -> tuple[list[SourceEvidence], MedicalImageAnalysisGraph]:
    case_id = str(record.get("case_id", "fixture-case"))
    image_ref = f"evidence:image:{case_id}"
    morphology_ref = f"evidence:morphology:{case_id}"
    context_ref = f"evidence:context:{case_id}"
    evidence = [
        SourceEvidence(
            image_ref,
            "image",
            {
                "image": str(record.get("image", "")),
                "texture_contrast": _float_record_value(record, "texture_contrast", 0.0),
                "region_quality": _float_record_value(record, "region_quality", 0.0),
            },
        ),
        SourceEvidence(
            morphology_ref,
            "measurement",
            {
                "cell_density": _float_record_value(record, "cell_density", 0.0),
                "boundary_clarity": _float_record_value(record, "boundary_clarity", 0.0),
            },
        ),
        SourceEvidence(
            context_ref,
            "metadata",
            {
                "source_quality": _float_record_value(record, "source_quality", 0.0),
                "collection_flag": str(record.get("collection_flag", "fixture")),
                "question": str(record.get("question", "")),
            },
        ),
    ]

    graph = MedicalImageAnalysisGraph(f"medical-image-analysis:{case_id}")
    graph.add_node(
        "case",
        "case",
        sample_id=case_id,
        question=str(record.get("question", "")),
        image=str(record.get("image", "")),
    )
    graph.add_node(
        "texture",
        "bounded-record",
        texture_contrast=_float_record_value(record, "texture_contrast", 0.0),
        region_quality=_float_record_value(record, "region_quality", 0.0),
        evidence_ref=image_ref,
    )
    graph.add_node(
        "morphology",
        "bounded-record",
        cell_density=_float_record_value(record, "cell_density", 0.0),
        boundary_clarity=_float_record_value(record, "boundary_clarity", 0.0),
        evidence_ref=morphology_ref,
    )
    graph.add_node(
        "context",
        "bounded-record",
        source_quality=_float_record_value(record, "source_quality", 0.0),
        collection_flag=str(record.get("collection_flag", "fixture")),
        evidence_ref=context_ref,
    )
    graph.add_edge("case", "texture", "has_record")
    graph.add_edge("case", "morphology", "has_record")
    graph.add_edge("case", "context", "has_record")
    graph.add_later_record("review_decision", "accepted-only-after-review")
    for key in sorted(TRAINING_ONLY_KEYS):
        if key in record:
            graph.add_later_record(key, record[key])
    return evidence, graph


def build_case() -> tuple[list[SourceEvidence], MedicalImageAnalysisGraph]:
    return build_case_from_record(
        {
            "case_id": "synthetic-1",
            "image": "data/fixture/images/texture-review.svg",
            "question": "Which review route has the strongest visible support?",
            "texture_contrast": 0.79,
            "region_quality": 0.82,
            "cell_density": 0.68,
            "boundary_clarity": 0.73,
            "source_quality": 0.86,
            "collection_flag": "synthetic",
        }
    )


def build_engine() -> GranularAnalysisEngine:
    return GranularAnalysisEngine(
        lenses=(
            Lens(
                "texture",
                "aggregate",
                lambda row: {
                    "texture_contrast": row["texture.texture_contrast"],
                    "region_quality": row["texture.region_quality"],
                },
                (),
            ),
            Lens(
                "morphology",
                "domain-specific",
                lambda row: {
                    "cell_density": row["morphology.cell_density"],
                    "boundary_clarity": row["morphology.boundary_clarity"],
                },
                (),
            ),
            Lens(
                "context",
                "aligned",
                lambda row: {
                    "source_quality": row["context.source_quality"],
                    "collection_flag": row["context.collection_flag"],
                },
                (),
            ),
        ),
        analysis_nodes=(
            AnalysisNode(
                "texture-proposer",
                ("texture",),
                lambda outputs: {
                    "outcome_ref": "review-item:texture-supported",
                    "score": (
                        outputs[0].features["texture_contrast"] + outputs[0].features["region_quality"]
                    )
                    / 2,
                    "confidence": max(0.0, outputs[0].features["region_quality"] - 0.06),
                    "uncertainty": max(0.0, 1.0 - outputs[0].features["region_quality"]),
                    "metadata": {"route": "texture-route"},
                    "evidence_refs": ("evidence:sample-image",),
                },
            ),
            AnalysisNode(
                "morphology-proposer",
                ("morphology",),
                lambda outputs: {
                    "outcome_ref": "review-item:morphology-supported",
                    "score": (
                        outputs[0].features["cell_density"] + outputs[0].features["boundary_clarity"]
                    )
                    / 2,
                    "confidence": max(0.0, outputs[0].features["boundary_clarity"] - 0.05),
                    "uncertainty": max(0.0, 1.0 - outputs[0].features["boundary_clarity"]),
                    "metadata": {"route": "morphology-route"},
                    "evidence_refs": ("evidence:region-measurement",),
                },
            ),
            AnalysisNode(
                "combined-review-proposer",
                ("texture", "morphology", "context"),
                lambda outputs: {
                    "outcome_ref": "review-item:combined-evidence",
                    "score": min(
                        0.99,
                        (
                            outputs[0].features["texture_contrast"]
                            + outputs[0].features["region_quality"]
                            + outputs[1].features["cell_density"]
                            + outputs[1].features["boundary_clarity"]
                            + outputs[2].features["source_quality"]
                        )
                        / 5
                        + 0.08,
                    ),
                    "confidence": max(0.0, outputs[2].features["source_quality"] - 0.09),
                    "uncertainty": max(0.0, 1.0 - outputs[2].features["source_quality"]),
                    "metadata": {"route": "combined-review-route", "review_state": "review"},
                    "evidence_refs": (
                        "evidence:sample-image",
                        "evidence:region-measurement",
                        "evidence:case-metadata",
                    ),
                },
            ),
        ),
        commit_threshold=0.92,
        review_threshold=0.50,
        training_only_keys=TRAINING_ONLY_KEYS,
    )


def run_synthetic_review():
    evidence, graph = build_case()
    return run_review_for_graph(evidence, graph)


def run_review_for_record(record: Mapping[str, Any]):
    evidence, graph = build_case_from_record(record)
    return run_review_for_graph(evidence, graph)


def run_review_for_graph(evidence: list[SourceEvidence], graph: MedicalImageAnalysisGraph):
    live = graph.live_record()
    hidden = dict(graph.later_records)
    engine = build_engine()
    result = engine.run(graph.case_id, live | hidden)
    return evidence, graph, result


def load_fixture_records() -> list[dict[str, Any]]:
    return json.loads(FIXTURE_RECORDS.read_text(encoding="utf-8"))


def _result_payload(result) -> dict[str, Any]:
    proposals_by_id = {proposal.proposal_id: proposal for proposal in result.trace.proposals}
    rejected = [
        proposals_by_id[proposal_id]
        for proposal_id in result.trace.rejected_proposal_ids
        if proposal_id in proposals_by_id
    ]
    return {
        "decision": result.decision,
        "outcome_ref": result.outcome_ref,
        "reason": result.trace.reason,
        "selected_proposal_id": result.trace.selected_proposal_id,
        "rejected_proposal_ids": list(result.trace.rejected_proposal_ids),
        "rejected_proposals": [
            {
                "proposal_id": proposal.proposal_id,
                "proposer_id": proposal.proposer_id,
                "outcome_ref": proposal.outcome_ref,
                "score": proposal.score,
                "confidence": proposal.confidence,
            }
            for proposal in rejected
        ],
        "hidden_keys_excluded": list(result.trace.hidden_keys_excluded),
        "lenses": [
            {
                "lens_id": output.lens_id,
                "kind": output.kind,
                "features": dict(output.features),
                "evidence_refs": list(output.evidence_refs),
            }
            for output in result.trace.lens_outputs
        ],
        "proposals": [
            {
                "proposal_id": proposal.proposal_id,
                "proposer_id": proposal.proposer_id,
                "outcome_ref": proposal.outcome_ref,
                "score": proposal.score,
                "confidence": proposal.confidence,
                "uncertainty": proposal.uncertainty,
                "lens_ids": list(proposal.lens_ids),
                "evidence_refs": list(proposal.evidence_refs),
                "metadata": dict(proposal.metadata),
            }
            for proposal in result.trace.proposals
        ],
    }


def _visual_graph_payload(record: Mapping[str, Any], result) -> dict[str, Any]:
    texture_score = _float_record_value(record, "texture_contrast", 0.0)
    morphology_score = _float_record_value(record, "boundary_clarity", 0.0)
    source_score = _float_record_value(record, "source_quality", 0.0)
    selected = result.trace.selected_proposal_id or "none"
    return {
        "regions": [
            {
                "id": "texture-region",
                "label": "texture field",
                "x": 16,
                "y": 20,
                "w": 36,
                "h": 30,
                "score": texture_score,
                "route": "texture-proposer",
            },
            {
                "id": "morphology-region",
                "label": "morphology path",
                "x": 42,
                "y": 34,
                "w": 38,
                "h": 36,
                "score": morphology_score,
                "route": "morphology-proposer",
            },
            {
                "id": "quality-region",
                "label": "source quality",
                "x": 20,
                "y": 66,
                "w": 58,
                "h": 18,
                "score": source_score,
                "route": "combined-review-proposer",
            },
        ],
        "stages": [
            "image evidence",
            "region graph",
            "visual lenses",
            "proposal routes",
            "verifier",
            result.decision,
        ],
        "selected_route": selected.split(":")[-1] if selected != "none" else "none",
    }


def build_demo_payload() -> dict[str, Any]:
    cases = []
    for record in load_fixture_records():
        _, _, result = run_review_for_record(record)
        cases.append(
            {
                "case_id": record["case_id"],
                "display_name": record.get("display_name", record["case_id"]),
                "case_summary": record.get("case_summary", ""),
                "review_goal": record.get("review_goal", ""),
                "image": f"data/fixture/{record['image']}",
                "question": record["question"],
                "capability": "one image case -> region graph -> lenses -> competing proposals -> verifier trace",
                "visual_graph": _visual_graph_payload(record, result),
                "result": _result_payload(result),
            }
        )
    return {
        "claim_boundary": "fixture workflow only; no medical or benchmark claim",
        "cases": cases,
    }


def write_demo_data(path: Path | None = None) -> Path:
    output = path or APP_DIR / "demo-data.js"
    payload = build_demo_payload()
    output.write_text(
        "window.CGF_MEDICAL_IMAGE_DEMO = "
        + json.dumps(payload, indent=2, sort_keys=True)
        + ";\n",
        encoding="utf-8",
    )
    return output


if __name__ == "__main__":
    write_demo_data()
