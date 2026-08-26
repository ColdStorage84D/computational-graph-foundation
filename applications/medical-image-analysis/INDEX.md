# Medical Image Analysis Application Index

Medical Image Analysis is a CGF application example. It demonstrates how
reusable Architecture frameworks can be composed for a high-separation review
workflow.

It does not own the reusable concepts. It composes them.

## Reading Path

Use this order:

```text
README.md
-> walkthrough.md
-> review-template.md
-> claim-boundary.md
-> index.html
-> synthetic_review.py
-> BENCHMARK_RESOURCES.md
```

Then follow the owning reusable concepts:

```text
../../architecture/multimodal-outcome-stack.md
../../architecture/granular-analysis.md
../../architecture/frameworks/registry.md
../../architecture/frameworks/cards/README.md
```

## Documents

| Document | Purpose |
| --- | --- |
| [README.md](README.md) | Application landing page and framework mix. |
| [walkthrough.md](walkthrough.md) | Step-by-step medical image analysis review flow using reusable CGF patterns. |
| [review-template.md](review-template.md) | Copyable template for a medical image analysis evidence review case. |
| [claim-boundary.md](claim-boundary.md) | What this application can and cannot claim. |
| [index.html](index.html) | Static browser fixture demo. |
| [demo-data.js](demo-data.js) | Generated fixture trace payload used by the browser demo. |
| [synthetic_review.py](synthetic_review.py) | Tiny synthetic application example, not a medical implementation. |
| [benchmark_resources.py](benchmark_resources.py) | Optional local benchmark-resource loader. |
| [BENCHMARK_RESOURCES.md](BENCHMARK_RESOURCES.md) | External benchmark resource setup and usage boundary. |
| [test_synthetic_review.py](test_synthetic_review.py) | Tests for the synthetic application contract. |

## What To Look For

- Source evidence stays external.
- Decoded records stay bounded.
- Labels and later outcomes stay out of live feature paths.
- Views and routes are explicit.
- Processor output is proposal state.
- Human or policy review is separate from source evidence.
- Trace preserves selected and rejected proposals.
- The committed browser demo uses only local CGF fixture assets.
- Optional benchmark records stay local and uncommitted.
- No medical, clinical, safety, or production claim is made.
