# Online Sales Data Cleansing (Python / Pandas)

Cleans a raw online-sales dataset: finds and fixes missing values, removes duplicates,
standardises text, corrects data types, checks outliers and saves a clean CSV.

## Structure
- `data/online_sales_raw.csv` - raw data (1,025 rows, 11 columns)
- `data/online_sales_clean.csv` - cleaned data (1,000 rows, 0 missing values)
- `data_cleaning.py` - the cleansing script
- `generate_dataset.py` - creates the raw sample data (skip if you use a Kaggle file)
- `screenshots/` - code and output screenshots used in the report

## Run
```bash
pip install -r requirements.txt
python data_cleaning.py
```

## Result
| | Before | After |
|---|---|---|
| Rows | 1,025 | 1,000 |
| Missing values | 367 | 0 |
| Duplicate orders | 25 | 0 |
