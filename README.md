# Automated Vulnerability Pattern Analysis for IoT Inspection Prioritization

Master's thesis project analyzing \~266,000 CVE records from the European Union
Vulnerability Database (EUVD) to help identify patterns in vulnerability severity,
exploitability, and product category, supporting data-driven inspection
prioritization for IoT products under the EU Radio Equipment Directive (RED).

## Overview

The project combines three analytical pipelines on a large, messy, real-world
vulnerability dataset:

1. **LLM-based product categorization** — using an LLM (Mistral Large, via
Azure batch API) to classify unique raw product labels into a
structured taxonomy, since no reliable ground-truth categories exist for
CVE-affected products at scale.
2. **Statistical analysis** — Kruskal-Wallis tests with Dunn's post-hoc
comparisons to test whether CVSS/EPSS scores differ
significantly across product categories.
3. **Topic modelling** — per-category LDA (scikit-learn + Gensim coherence
scoring, grid search over k/alpha/beta) on CVE descriptions, to check
whether vulnerability themes differ between high- and low-risk categories.

## Key findings

* Both CVSS and EPSS scores differ significantly across product categories,
with **large effect sizes** (ε² ≈ 0.24 and ≈ 0.22 respectively).
* Topic modelling found **no consistent thematic distinction** between
high-risk and low-risk categories. The severity differences are not explained
by different kinds of vulnerabilities being reported.
* Built a two-tier taxonomy (a broad \~100-category version and a curated
30-category version) from \~21,700 unique raw product labels with no
existing standard classification. A pre-determined taxonomy from the RDI resulted
in larger effect sizes.

## Pipeline

```
01\\\_Pulling data API.ipynb           → pull raw records from the EUVD API
02\\\_Initial data creation.ipynb      → clean and prepare the raw dataset
03\\\_Data\\\_exploration.ipynb           → initial EDA on the cleaned dataset
04\\\_Mistral call.ipynb               → LLM batch calls for product categorization
05\\\_First/Second/Third\\\_API\\\_call\\\_
    extraction.ipynb                → parse raw LLM batch output into usable data
06\\\_Kruskal wallis\\\*.ipynb            → statistical testing across categories
07\\\_Individual LDA\\\*.ipynb            → per-category topic modelling
07\\\_LDA topic analysis.ipynb         → aggregate/compare topic modelling results
08\\\_Html converter.py                → generates the HTML to visually display the topic analysis
```

*(Files with an `\\\_IoT` suffix repeat the analysis on the IoT-specific subset
of the data.)*

## Tech stack

`pandas` · `scikit-learn` · `Gensim` · `SciPy` (Kruskal-Wallis, Dunn's test)
· Mistral Large via Azure API · `matplotlib`/`seaborn` (boxenplots)

## Data

Source: [European Union Vulnerability Database (EUVD)](https://euvd.enisa.europa.eu/),
\~266,000 CVE records (2016–2026). Known dataset biases are discussed in the
thesis, including WordPress plugin over-representation and geographic
CSIRT-reporting skew.

## Limitations

* LLM-based categorization introduces some label noise; deduplication and
validation steps were used to mitigate this, but it isn't ground truth.
* The topic-modelling null result is itself informative but means LDA topics
should not be read as a severity predictor.

## Setup

```bash
pip install -r requirements.txt
```

*(add a `requirements.txt` — pandas, scikit-learn, gensim, scipy, seaborn,
matplotlib, and the Azure/Mistral client library you used)*

\---

Full methodology and results can be found in the [corresponding thesis (Kevin Rijnders, 2026)](https://studenttheses.uu.nl/items/1e296969-f143-441c-9c28-46fa88bddcb5)

