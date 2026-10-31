# AI divergence reveals the shape of human cognition — supplementary data and code

**Reproducible secondary analysis of neural alignment in 55 visual models.**  
Associated manuscript: *AI divergence reveals the shape of human cognition* (Branda, Ahmed, Ceccarelli, Scarpa and Ciccozzi; under editorial consideration).  
This repository contains the material supporting the manuscript's controlled, exploratory comparison in **Figure 2A–B** and **Supplementary Table S1**.

> **Scope:** This is a **secondary reanalysis** of a public controlled *vision-only* dataset from Conwell et al. (2024). It is **not** the original, non-recoverable 21-evaluation cross-domain meta-regression and does not test the causal Constraint Identification Principle (CIP). Figure 2C–D in the manuscript are *conceptual simulations*, not reproduced by this dataset.

## Repository contents

| File or folder | Contents |
| --- | --- |
| `data/original/source_data.xlsx` | Source-data workbook distributed by Conwell et al. (2024), preserved without modification. See third-party attribution and license. |
| `data/derived/Supplementary_Table_S1.xlsx` | Supplementary Table S1: data dictionary, model-level values, four participant-specific scores, extraction references, audit and statistical results. |
| `reanalyze.py` | Deterministic extraction, validations, Welch comparisons and HC3 OLS regressions. |
| `output/verified_55_models.csv` | All 55 model-level averages (34 CNN, 21 Transformer). |
| `output/verified_52_performance_matched_models.csv` | 52 models with a matched ImageNet-1K top-1 accuracy (31 CNN, 21 Transformer). |
| `output/source_Figure2_440_subject_rows.csv` | 55 × 4 × 2 = 440 participant-specific source rows. |
| `output/source_Figure5C_198_rows.csv` | 198 source Figure5C rows used for accuracy matching and cross-checks. |
| `output/results.json` | Machine-readable results of the reproduction. |
| `figures/` | Figure 2A and 2B reanalysis illustrations (not the manuscript's simulated panels C–D). |
| `tests/verify_results.py` | Checks counts, available accuracy, key coefficients and dataset consistency. |
| `THIRD_PARTY_NOTICES.md` | Data provenance, reuse and source attribution. |
| `CITATION.cff` | Citation metadata for this analysis package (not a journal acceptance claim). |

## Reproduce the analysis

Use **Python 3.11 or later**. Install requirements in a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
python reanalyze.py data/original/source_data.xlsx
python tests/verify_results.py
```

The script writes or refreshes the four CSV files and `output/results.json`. It runs internal checks before writing results, including matching independently tabulated per-model source values.

## Analytical decisions

- **Unit of analysis:** an artificial model; the four participant-specific neural-alignment scores are averaged *within each model* before regression. Participants are not treated as independent model evaluations.
- **Comparison:** 34 CNNs and 21 visual Transformers with cRSA and veRSA measures; source uses the label **WRSA** for veRSA.
- **Outcome:** mean classical representational similarity analysis (**cRSA**) or voxel-encoding representational similarity analysis (**veRSA**) for each model.
- **Task performance:** ImageNet-1K top-1 accuracy. Available for 52/55 models. Missing accuracy for `eca_nfnet_l0`, `googlenet` and `semnasnet_100`; these models are kept in descriptive contrasts but excluded only from performance-adjusted regressions.
- **OLS predictors:** Transformer-vs-CNN indicator and `(ImageNet top-1 accuracy − 75)/10`; robust HC3 standard errors and two-sided tests. No causal inference is claimed.
- **Descriptive comparison:** Welch unequal-variance two-sided test on model-level means.
- **No multiple-domain pooling:** language and decision-making examples remain in the manuscript's *narrative* synthesis, not in this analysis.

## Selected reproduced results

| Measure | CNN average (34) | Transformer average (21) | Welch p | Adjusted Transformer coefficient (n = 52; HC3 95% CI) | Adjusted p |
| --- | ---: | ---: | ---: | ---: | ---: |
| **veRSA** | 0.6714 | 0.6615 | 0.1012 | −0.0134 (−0.02685, 0.00004) | 0.0507 |
| **cRSA** | 0.3694 | 0.3287 | 0.0014 | −0.0367 (−0.06570, −0.00775) | 0.0130 |

These estimates are **metric-dependent** and observational. In particular, the adjusted veRSA result is *not* significant at a two-sided α = 0.05. No result alone identifies a biologically causal mechanism.

## Primary-source attribution

**Conwell C, Prince JS, Kay KN, Alvarez GA, Konkle T.** A large-scale examination of inductive biases shaping high-level visual representation in brains and machines. *Nature Communications.* 2024;15:9383. DOI: [10.1038/s41467-024-53147-y](https://doi.org/10.1038/s41467-024-53147-y).

Original project: <https://github.com/ColinConwell/DeepNSD>. The associated paper states its deposited source data and code are available under **GNU GPL version 3**. This repository acknowledges that source and preserves the original `source_data.xlsx` separately. This secondary reanalysis is independent work by the associated manuscript authors, and must not be mistaken for the original authors' results or endorsement.

## Citation and archiving

Use the GitHub repository URL (once published) in the manuscript's Data Availability statement. For a stable citable archive, connect the **public** repository to Zenodo and create a tagged GitHub release (e.g. `v1.0.0`); Zenodo will assign a DOI. Do not enter a hypothetical DOI until one has actually been assigned.

## License and attribution

The repository contains third-party data subject to GPL-3.0 licensing statements provided with the original study; see `THIRD_PARTY_NOTICES.md` and `LICENSE`. Authors should verify that public release of the supplementary package is approved by all manuscript coauthors. The associated *journal manuscript is not included* in this repository.
