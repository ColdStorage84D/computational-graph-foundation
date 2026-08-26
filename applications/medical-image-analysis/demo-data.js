window.CGF_MEDICAL_IMAGE_DEMO = {
  "cases": [
    {
      "capability": "one image case -> region graph -> lenses -> competing proposals -> verifier trace",
      "case_id": "fixture-texture-1",
      "case_summary": "A generated image tile where the texture route has the strongest evidence.",
      "display_name": "Texture-supported fixture",
      "image": "data/fixture/images/texture-review.svg",
      "question": "Which evidence route should be reviewed first?",
      "result": {
        "decision": "review",
        "hidden_keys_excluded": [
          "expected_decision",
          "review_decision"
        ],
        "lenses": [
          {
            "evidence_refs": [],
            "features": {
              "region_quality": 0.8,
              "texture_contrast": 0.82
            },
            "kind": "aggregate",
            "lens_id": "texture"
          },
          {
            "evidence_refs": [],
            "features": {
              "boundary_clarity": 0.62,
              "cell_density": 0.58
            },
            "kind": "domain-specific",
            "lens_id": "morphology"
          },
          {
            "evidence_refs": [],
            "features": {
              "collection_flag": "fixture",
              "source_quality": 0.86
            },
            "kind": "aligned",
            "lens_id": "context"
          }
        ],
        "outcome_ref": "review-item:combined-evidence",
        "proposals": [
          {
            "confidence": 0.74,
            "evidence_refs": [
              "evidence:sample-image"
            ],
            "lens_ids": [
              "texture"
            ],
            "metadata": {
              "route": "texture-route"
            },
            "outcome_ref": "review-item:texture-supported",
            "proposal_id": "proposal:medical-image-analysis:fixture-texture-1:texture-proposer",
            "proposer_id": "texture-proposer",
            "score": 0.81,
            "uncertainty": 0.19999999999999996
          },
          {
            "confidence": 0.57,
            "evidence_refs": [
              "evidence:region-measurement"
            ],
            "lens_ids": [
              "morphology"
            ],
            "metadata": {
              "route": "morphology-route"
            },
            "outcome_ref": "review-item:morphology-supported",
            "proposal_id": "proposal:medical-image-analysis:fixture-texture-1:morphology-proposer",
            "proposer_id": "morphology-proposer",
            "score": 0.6,
            "uncertainty": 0.38
          },
          {
            "confidence": 0.77,
            "evidence_refs": [
              "evidence:sample-image",
              "evidence:region-measurement",
              "evidence:case-metadata"
            ],
            "lens_ids": [
              "texture",
              "morphology",
              "context"
            ],
            "metadata": {
              "review_state": "review",
              "route": "combined-review-route"
            },
            "outcome_ref": "review-item:combined-evidence",
            "proposal_id": "proposal:medical-image-analysis:fixture-texture-1:combined-review-proposer",
            "proposer_id": "combined-review-proposer",
            "score": 0.816,
            "uncertainty": 0.14
          }
        ],
        "reason": "best_proposal_needs_review",
        "rejected_proposal_ids": [
          "proposal:medical-image-analysis:fixture-texture-1:texture-proposer",
          "proposal:medical-image-analysis:fixture-texture-1:morphology-proposer"
        ],
        "rejected_proposals": [
          {
            "confidence": 0.74,
            "outcome_ref": "review-item:texture-supported",
            "proposal_id": "proposal:medical-image-analysis:fixture-texture-1:texture-proposer",
            "proposer_id": "texture-proposer",
            "score": 0.81
          },
          {
            "confidence": 0.57,
            "outcome_ref": "review-item:morphology-supported",
            "proposal_id": "proposal:medical-image-analysis:fixture-texture-1:morphology-proposer",
            "proposer_id": "morphology-proposer",
            "score": 0.6
          }
        ],
        "selected_proposal_id": "proposal:medical-image-analysis:fixture-texture-1:combined-review-proposer"
      },
      "review_goal": "Show how one visual branch can lead the graph toward human review without becoming an automatic medical answer.",
      "visual_graph": {
        "regions": [
          {
            "h": 30,
            "id": "texture-region",
            "label": "texture field",
            "route": "texture-proposer",
            "score": 0.82,
            "w": 36,
            "x": 16,
            "y": 20
          },
          {
            "h": 36,
            "id": "morphology-region",
            "label": "morphology path",
            "route": "morphology-proposer",
            "score": 0.62,
            "w": 38,
            "x": 42,
            "y": 34
          },
          {
            "h": 18,
            "id": "quality-region",
            "label": "source quality",
            "route": "combined-review-proposer",
            "score": 0.86,
            "w": 58,
            "x": 20,
            "y": 66
          }
        ],
        "selected_route": "combined-review-proposer",
        "stages": [
          "image evidence",
          "region graph",
          "visual lenses",
          "proposal routes",
          "verifier",
          "review"
        ]
      }
    },
    {
      "capability": "one image case -> region graph -> lenses -> competing proposals -> verifier trace",
      "case_id": "fixture-morphology-1",
      "case_summary": "A generated image tile where boundary and shape evidence is stronger than texture evidence.",
      "display_name": "Morphology-supported fixture",
      "image": "data/fixture/images/morphology-review.svg",
      "question": "Which evidence route should be reviewed first?",
      "result": {
        "decision": "review",
        "hidden_keys_excluded": [
          "expected_decision",
          "review_decision"
        ],
        "lenses": [
          {
            "evidence_refs": [],
            "features": {
              "region_quality": 0.6,
              "texture_contrast": 0.51
            },
            "kind": "aggregate",
            "lens_id": "texture"
          },
          {
            "evidence_refs": [],
            "features": {
              "boundary_clarity": 0.84,
              "cell_density": 0.78
            },
            "kind": "domain-specific",
            "lens_id": "morphology"
          },
          {
            "evidence_refs": [],
            "features": {
              "collection_flag": "fixture",
              "source_quality": 0.82
            },
            "kind": "aligned",
            "lens_id": "context"
          }
        ],
        "outcome_ref": "review-item:morphology-supported",
        "proposals": [
          {
            "confidence": 0.54,
            "evidence_refs": [
              "evidence:sample-image"
            ],
            "lens_ids": [
              "texture"
            ],
            "metadata": {
              "route": "texture-route"
            },
            "outcome_ref": "review-item:texture-supported",
            "proposal_id": "proposal:medical-image-analysis:fixture-morphology-1:texture-proposer",
            "proposer_id": "texture-proposer",
            "score": 0.5549999999999999,
            "uncertainty": 0.4
          },
          {
            "confidence": 0.7899999999999999,
            "evidence_refs": [
              "evidence:region-measurement"
            ],
            "lens_ids": [
              "morphology"
            ],
            "metadata": {
              "route": "morphology-route"
            },
            "outcome_ref": "review-item:morphology-supported",
            "proposal_id": "proposal:medical-image-analysis:fixture-morphology-1:morphology-proposer",
            "proposer_id": "morphology-proposer",
            "score": 0.81,
            "uncertainty": 0.16000000000000003
          },
          {
            "confidence": 0.73,
            "evidence_refs": [
              "evidence:sample-image",
              "evidence:region-measurement",
              "evidence:case-metadata"
            ],
            "lens_ids": [
              "texture",
              "morphology",
              "context"
            ],
            "metadata": {
              "review_state": "review",
              "route": "combined-review-route"
            },
            "outcome_ref": "review-item:combined-evidence",
            "proposal_id": "proposal:medical-image-analysis:fixture-morphology-1:combined-review-proposer",
            "proposer_id": "combined-review-proposer",
            "score": 0.7899999999999999,
            "uncertainty": 0.18000000000000005
          }
        ],
        "reason": "best_proposal_needs_review",
        "rejected_proposal_ids": [
          "proposal:medical-image-analysis:fixture-morphology-1:texture-proposer",
          "proposal:medical-image-analysis:fixture-morphology-1:combined-review-proposer"
        ],
        "rejected_proposals": [
          {
            "confidence": 0.54,
            "outcome_ref": "review-item:texture-supported",
            "proposal_id": "proposal:medical-image-analysis:fixture-morphology-1:texture-proposer",
            "proposer_id": "texture-proposer",
            "score": 0.5549999999999999
          },
          {
            "confidence": 0.73,
            "outcome_ref": "review-item:combined-evidence",
            "proposal_id": "proposal:medical-image-analysis:fixture-morphology-1:combined-review-proposer",
            "proposer_id": "combined-review-proposer",
            "score": 0.7899999999999999
          }
        ],
        "selected_proposal_id": "proposal:medical-image-analysis:fixture-morphology-1:morphology-proposer"
      },
      "review_goal": "Show competing analysis routes and a verifier-selected review path.",
      "visual_graph": {
        "regions": [
          {
            "h": 30,
            "id": "texture-region",
            "label": "texture field",
            "route": "texture-proposer",
            "score": 0.51,
            "w": 36,
            "x": 16,
            "y": 20
          },
          {
            "h": 36,
            "id": "morphology-region",
            "label": "morphology path",
            "route": "morphology-proposer",
            "score": 0.84,
            "w": 38,
            "x": 42,
            "y": 34
          },
          {
            "h": 18,
            "id": "quality-region",
            "label": "source quality",
            "route": "combined-review-proposer",
            "score": 0.82,
            "w": 58,
            "x": 20,
            "y": 66
          }
        ],
        "selected_route": "morphology-proposer",
        "stages": [
          "image evidence",
          "region graph",
          "visual lenses",
          "proposal routes",
          "verifier",
          "review"
        ]
      }
    },
    {
      "capability": "one image case -> region graph -> lenses -> competing proposals -> verifier trace",
      "case_id": "fixture-low-confidence-1",
      "case_summary": "A generated image tile where all analysis routes are weak.",
      "display_name": "Low-confidence fixture",
      "image": "data/fixture/images/low-confidence-review.svg",
      "question": "Should weak visual support create an automatic answer?",
      "result": {
        "decision": "abstain",
        "hidden_keys_excluded": [
          "expected_decision",
          "review_decision"
        ],
        "lenses": [
          {
            "evidence_refs": [],
            "features": {
              "region_quality": 0.31,
              "texture_contrast": 0.22
            },
            "kind": "aggregate",
            "lens_id": "texture"
          },
          {
            "evidence_refs": [],
            "features": {
              "boundary_clarity": 0.26,
              "cell_density": 0.28
            },
            "kind": "domain-specific",
            "lens_id": "morphology"
          },
          {
            "evidence_refs": [],
            "features": {
              "collection_flag": "fixture",
              "source_quality": 0.34
            },
            "kind": "aligned",
            "lens_id": "context"
          }
        ],
        "outcome_ref": null,
        "proposals": [
          {
            "confidence": 0.25,
            "evidence_refs": [
              "evidence:sample-image"
            ],
            "lens_ids": [
              "texture"
            ],
            "metadata": {
              "route": "texture-route"
            },
            "outcome_ref": "review-item:texture-supported",
            "proposal_id": "proposal:medical-image-analysis:fixture-low-confidence-1:texture-proposer",
            "proposer_id": "texture-proposer",
            "score": 0.265,
            "uncertainty": 0.69
          },
          {
            "confidence": 0.21000000000000002,
            "evidence_refs": [
              "evidence:region-measurement"
            ],
            "lens_ids": [
              "morphology"
            ],
            "metadata": {
              "route": "morphology-route"
            },
            "outcome_ref": "review-item:morphology-supported",
            "proposal_id": "proposal:medical-image-analysis:fixture-low-confidence-1:morphology-proposer",
            "proposer_id": "morphology-proposer",
            "score": 0.27,
            "uncertainty": 0.74
          },
          {
            "confidence": 0.25,
            "evidence_refs": [
              "evidence:sample-image",
              "evidence:region-measurement",
              "evidence:case-metadata"
            ],
            "lens_ids": [
              "texture",
              "morphology",
              "context"
            ],
            "metadata": {
              "review_state": "review",
              "route": "combined-review-route"
            },
            "outcome_ref": "review-item:combined-evidence",
            "proposal_id": "proposal:medical-image-analysis:fixture-low-confidence-1:combined-review-proposer",
            "proposer_id": "combined-review-proposer",
            "score": 0.36200000000000004,
            "uncertainty": 0.6599999999999999
          }
        ],
        "reason": "best_proposal_below_review_threshold",
        "rejected_proposal_ids": [
          "proposal:medical-image-analysis:fixture-low-confidence-1:texture-proposer",
          "proposal:medical-image-analysis:fixture-low-confidence-1:morphology-proposer",
          "proposal:medical-image-analysis:fixture-low-confidence-1:combined-review-proposer"
        ],
        "rejected_proposals": [
          {
            "confidence": 0.25,
            "outcome_ref": "review-item:texture-supported",
            "proposal_id": "proposal:medical-image-analysis:fixture-low-confidence-1:texture-proposer",
            "proposer_id": "texture-proposer",
            "score": 0.265
          },
          {
            "confidence": 0.21000000000000002,
            "outcome_ref": "review-item:morphology-supported",
            "proposal_id": "proposal:medical-image-analysis:fixture-low-confidence-1:morphology-proposer",
            "proposer_id": "morphology-proposer",
            "score": 0.27
          },
          {
            "confidence": 0.25,
            "outcome_ref": "review-item:combined-evidence",
            "proposal_id": "proposal:medical-image-analysis:fixture-low-confidence-1:combined-review-proposer",
            "proposer_id": "combined-review-proposer",
            "score": 0.36200000000000004
          }
        ],
        "selected_proposal_id": null
      },
      "review_goal": "Show that weak evidence should abstain instead of creating authority.",
      "visual_graph": {
        "regions": [
          {
            "h": 30,
            "id": "texture-region",
            "label": "texture field",
            "route": "texture-proposer",
            "score": 0.22,
            "w": 36,
            "x": 16,
            "y": 20
          },
          {
            "h": 36,
            "id": "morphology-region",
            "label": "morphology path",
            "route": "morphology-proposer",
            "score": 0.26,
            "w": 38,
            "x": 42,
            "y": 34
          },
          {
            "h": 18,
            "id": "quality-region",
            "label": "source quality",
            "route": "combined-review-proposer",
            "score": 0.34,
            "w": 58,
            "x": 20,
            "y": 66
          }
        ],
        "selected_route": "none",
        "stages": [
          "image evidence",
          "region graph",
          "visual lenses",
          "proposal routes",
          "verifier",
          "abstain"
        ]
      }
    }
  ],
  "claim_boundary": "fixture workflow only; no medical or benchmark claim"
};
