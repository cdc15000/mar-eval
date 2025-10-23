# mar-eval
![CI](https://github.com/cdc15000/mar-eval/actions/workflows/tests.yml/badge.svg)

`mar-eval` is an open Python toolkit for evaluating Metal Artifact Reduction (MAR)
performance in computed tomography (CT) imaging.

It implements the quantitative analysis framework described in **Annex GG** of
IEC 60601-2-44 Ed. 4, including Channelized Hotelling Observer (CHO) analysis,
AUC computation, statistical comparison, and bias assessment.

---

## Features
- CHO model observer and AUC computation
- Paired ΔAUC and one-tailed t-test
- Bias and reproducibility metrics
- Ready for benchmarking MAR algorithms

## Example

```bash
python examples/synthetic_demo.py
```

© 2025 Christopher D. Cocchiaraley. MIT License.
