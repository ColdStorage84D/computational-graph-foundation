# Basis-Mode Representation Results

Status: `contract-pass`

Eval layer: `isolated`

Reviewed command:

```powershell
python -m unittest discover -s labs/evals/basis-mode-representation -p "test_*.py"
```

Reviewed result:

```text
Ran 7 tests
OK
```

Claim boundary: this result covers a tiny Fourier-like fixture only. It proves
that the local CGF declaration contract can expose mode labels, coefficient
placement, selection rules, operator support, readout, and truncation residuals.
It does not prove domain accuracy, solver quality, or model performance.
