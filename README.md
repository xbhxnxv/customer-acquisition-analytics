# Customer Acquisition Response Predictor

Predicting which customers respond to a marketing campaign, and segmenting them for
targeting. Built as a portfolio project for a data analytics role in marketing /
customer-acquisition analytics.

## Problem
Given a bank's direct-marketing campaign data, predict whether a customer will
subscribe to the offered product, and group customers into segments to inform targeting.

## Dataset
UCI Bank Marketing dataset (bank-additional-full.csv, ~41k rows). Downloaded at runtime.

## Methods
- Exploratory data analysis
- Logistic Regression (interpretable baseline)
- XGBoost (higher-accuracy model)
- Model comparison on ROC-AUC, precision, recall, F1
- K-Means customer segmentation

## Results
_To be filled in with real numbers after running the notebook._

## How to run
```
pip install -r requirements.txt
jupyter notebook notebook.ipynb
```
Run all cells top to bottom.
