# E-Commerce Business Intelligence & Performance Analytics

## Project Overview

This project is an end-to-end business analytics case study for a multi-channel e-commerce operation. It simulates the work of a Business Analyst/Data Analyst supporting management decisions around revenue growth, profitability, product performance, pricing, and operations.

Rather than treating the dataset only as a dashboard exercise, the project follows a full business analytics workflow: business understanding, data preparation, exploratory analysis, KPI design, dashboard development, and business recommendations.

## Business Problem

The company sells products through multiple online channels. Management wants to understand:

- Which channels and products generate the strongest revenue and profit
- Which products sell well but have weak margins
- Whether pricing differs meaningfully across platforms
- How cancellations and fulfilment issues affect performance
- Where the business should focus to improve profitability

## Dataset

This project uses the **Unlock Profits with E-Commerce Sales Data** dataset from Kaggle.

The dataset contains multiple business-related tables, including:

- Sales transactions
- Product information
- Pricing data
- Profit & Loss reports
- Warehouse information
- Expense and operational data

Because the data comes from different sources, an important first step is cleaning, standardizing, and preparing the files for analysis.

## Current Scope

- Raw dataset extraction
- Data cleaning and standardization
- Data quality profiling
- Cleaned CSV outputs for analysis
- Reproducible cleaning script

## Tools & Technologies

- Python
- Pandas
- SQL
- Power BI
- Git & GitHub

## Project Workflow

1. Business Understanding
2. Data Understanding
3. Data Preparation
4. Exploratory Data Analysis
5. KPI Framework
6. Sales Analytics
7. Product Analytics
8. Pricing Analytics
9. Operations Analytics
10. Profitability Analytics
11. Dashboard Development
12. Business Recommendations

## Key Business KPIs

- Revenue
- Profit
- Gross Margin
- Net Margin
- Average Order Value
- Order Cancellation Rate
- Fulfilment Rate
- Product Profitability
- Sales Growth

## Project Structure

```text
data/
  raw/          Original extracted source CSVs
  cleaned/      Analysis-ready cleaned CSVs
reports/        Data quality report and cleaned dataset package
scripts/        Reproducible data cleaning pipeline
```

## Key Outputs

- `reports/data_quality_report.md`
- `reports/data_quality_profile.json`
- `reports/cleaned_ecommerce_datasets.zip`
- `scripts/clean_ecommerce_data.py`

## Next Steps

- Build the analytical data model
- Define KPI calculations
- Perform sales, product, pricing, supply chain, and profitability analysis
- Create a Power BI executive dashboard
- Develop final business recommendations using:

```text
Observation -> Insight -> Recommendation -> Expected Business Impact
```
