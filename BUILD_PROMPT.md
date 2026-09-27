# Build prompt (paste into Claude Code)

Build me a machine-learning portfolio project I can run and understand in one day, then put on my CV and GitHub. I'm a recent MSc Financial Technology grad applying for a Data Analytics role at American Express (marketing/customer-acquisition analytics). Everything must be real and reproducible — do not fabricate results or inflate anything.

PROJECT
A customer-acquisition response predictor: given a bank's marketing-campaign data, predict which customers will subscribe to the offer, then segment customers for targeting. This maps to prospect marketing analytics.

DATASET
Use the UCI Bank Marketing dataset ("bank-additional-full.csv", ~41k rows). Download it programmatically in the notebook (from the UCI repository). Target column is "y" (yes/no subscription). If the download fails, stop and tell me instead of inventing data.

WHAT TO BUILD
One clean, well-commented Jupyter notebook plus a GitHub-ready repo. In the notebook, in this order:
1. Load the data and do EDA — class balance, key feature distributions, 3-4 simple charts. Note that the target is imbalanced.
2. Preprocess — handle categoricals (one-hot), scale numerics where needed, train/test split (stratified, random_state=42).
3. Model 1: Logistic Regression as the interpretable baseline. Report accuracy, precision, recall, F1, ROC-AUC, and a confusion matrix.
4. Model 2: XGBoost classifier. Same metrics. Handle class imbalance (scale_pos_weight or class weights).
5. Compare the two models in a single table and one ROC-curve chart overlaying both.
6. Feature importance from XGBoost — which factors drive response — with a short plain-English read of the top drivers.
7. K-Means customer segmentation on a sensible subset of features. Pick k with the elbow method, describe each segment in one line, and one scatter/segment chart.
8. A short "So what" markdown cell: which model to use, which segments to target, honest limitations.

CODE STYLE — IMPORTANT
- Above every code block, add a markdown cell explaining in plain, layman English what it does and WHY, as if teaching someone who knows Python basics but is new to ML. I want to be able to explain this in an interview.
- Comment the tricky lines inline.
- Set random seeds everywhere for reproducibility.

TECH
Python, pandas, numpy, scikit-learn, xgboost, matplotlib, seaborn, jupyter.

REPO DELIVERABLES (this repo is already scaffolded — fill it in)
- notebook.ipynb (the above)
- README.md — update the RESULTS section with real numbers after running.
- requirements.txt (present)
- .gitignore (present)
- Runnable with: pip install -r requirements.txt then run the notebook top to bottom.

FINALLY
- Actually run the notebook end to end and paste the real metrics into the README — do not leave placeholders.
- Give me 2-3 honest CV bullet points describing what I built, using the real results (e.g. "compared logistic regression and XGBoost, AUC 0.79 vs 0.94").
- Tell me clearly anything that didn't work or any assumption you made.
