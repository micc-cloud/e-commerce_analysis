# E-Commerce Analysis

## Project Summary

This repository contains a business-focused e-commerce analytics workflow based on cleaned CSV datasets. The work covers data-quality validation, exploratory analysis, and insight generation for commercial and operational decision-making.

## What Was Completed

- Reviewed the cleaned datasets and verified their basic reliability.
- Performed a structured data-quality assessment covering duplicates, missing values, and suspicious values.
- Built a reusable Python-based exploratory analysis workflow using Pandas, NumPy, Matplotlib, Plotly, and Seaborn.
- Organized the analysis around business questions such as:
  - which products or categories are driving performance,
  - whether pricing and quantity patterns are stable,
  - where missing or unreliable data may affect conclusions,
  - and which areas should be prioritized for deeper business analysis.

## Key Outputs

- Cleaned datasets in the data/cleaned folder
- Data quality documentation in the reports folder
- Exploratory analysis workflow in the scripts folder
- Business-focused EDA visuals and summaries in the reports/eda_outputs folder

## How to Run the Analysis

1. Install the required Python packages:
   pip install pandas numpy matplotlib seaborn plotly

2. Run the analysis script from the repository root:
   python scripts/EDA.py

3. Review the generated outputs in the reports/eda_outputs folder.

## Business Focus

The analysis is designed to support operational and commercial decisions rather than only to visualize data. The next stage should concentrate on revenue contribution, profitability, product-level performance, and supply-chain or fulfillment reliability.
