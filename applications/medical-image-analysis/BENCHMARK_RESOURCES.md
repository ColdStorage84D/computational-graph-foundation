# Benchmark Resources

CGF does not ship benchmark medical images, full datasets, checkpoints, or
generated benchmark artifacts in this application.

Developers who want to run optional benchmark smoke tests can use an external
benchmark resource page and place the downloaded files in a local ignored
folder.

## Resource Page

- MedBLINK dataset page: <https://huggingface.co/datasets/MahtabBg/MedBLINK>
- MedBLINK paper page: <https://huggingface.co/papers/2508.02951>

Before using any benchmark data, check the dataset page for current license,
terms of use, allowed redistribution, and any medical-data restrictions.

## Local Folder

Set this environment variable:

```powershell
$env:CGF_MEDICAL_BENCHMARK_DIR="<local-benchmark-folder>"
```

Expected local shape:

```text
medical-benchmark/
  records.jsonl
  images/
    case-001.png
    case-002.png
```

Each `records.jsonl` row should contain:

```json
{"case_id":"case-001","image":"images/case-001.png","question":"...","answer":"..."}
```

The optional benchmark loader treats `answer` as an evaluation-only field. It
must not become live lens evidence.

## Optional Smoke Test

When `CGF_MEDICAL_BENCHMARK_DIR` is set, the app can:

- validate the local folder shape;
- load a small number of local records;
- create bounded graph cases;
- run the same lens / proposal / verifier flow used by the fixture demo;
- report local smoke-test decisions and trace shape.

This path is intentionally small. It is meant to confirm that local records can
enter the CGF workflow, not to score a benchmark.

## Claim Boundary

The optional benchmark path only checks that the CGF graph/lens/proposal/review
pipeline can run on locally supplied records. It does not claim medical
validity, clinical safety, diagnostic correctness, dataset representativeness,
or benchmark performance.
