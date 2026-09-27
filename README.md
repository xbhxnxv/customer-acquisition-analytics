# Customer Acquisition Response Predictor

Predicting which customers respond to a bank's direct-marketing campaign, and segmenting
customers to guide targeting. Built as a portfolio project on marketing / customer-acquisition
analytics.

## Problem
A Portuguese bank ran direct-marketing (phone) campaigns for a term-deposit product. Given
what is known about a customer *before* the call, predict whether they will subscribe, and
group customers into segments so marketing can target the ones worth calling.

## Dataset
UCI Bank Marketing dataset (`bank-additional-full.csv`, 41,188 rows, 20 input features).
A copy is included in `data/` so the notebook runs offline. Source:
https://archive.ics.uci.edu/dataset/222/bank+marketing

## Approach
- **EDA** on class balance and response drivers (the target is imbalanced — 11.3% subscribe).
- **Data prep with two anti-leakage steps:** dropped `duration` (known only after the call ends),
  and converted `pdays = 999` ("never contacted") into a clean `previously_contacted` flag.
- **Logistic Regression** — interpretable baseline, class-weighted for the imbalance.
- **XGBoost** — stronger model, `scale_pos_weight` for a fair comparison.
- **Evaluation** on ROC-AUC (the right metric for imbalanced ranking), plus a business-facing
  top-decile lift.
- **K-Means** customer segmentation, with k chosen by the elbow method.

## Results (test set, 20% hold-out)

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---|---|---|---|---|
| Logistic Regression | 0.835 | 0.368 | 0.646 | 0.469 | **0.801** |
| XGBoost | 0.848 | 0.392 | 0.644 | 0.488 | **0.809** |

- **Top-decile lift: 4.85x** — the top 10% of customers by model score subscribe at ~54.7%
  versus an 11.3% base rate. Calling that tenth first finds nearly five times as many
  subscribers per call.
- **Top drivers:** national employment level (`nr.employed`), a prior successful contact
  (`poutcome_success`, `previously_contacted`), and contact month.
- **Segmentation:** one segment — customers with a prior successful contact — subscribes at
  ~63% versus ~9% for the rest; a heavily over-called segment barely converts.

AUC is modest by design: dropping the leaky `duration` feature (which inflates online results
past 0.93) gives a realistic model. XGBoost only edges the logistic baseline, so the simpler,
more explainable model is a reasonable choice too.

## How to run
```
pip install -r requirements.txt
jupyter notebook notebook.ipynb
```
Run all cells top to bottom. The dataset in `data/` means no download is needed.

## Files
- `notebook.ipynb` — full analysis, executed with outputs and charts
- `data/bank-additional-full.csv` — dataset
- `requirements.txt` — dependencies
