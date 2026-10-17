import pandas as pd
from pathlib import Path

# load original customer dataset
customers = pd.read_csv("customer.csv")

# identify customers with missing transaction dates
missing_customers = customers[
    customers["first_transaction_date"].isna()
].copy()

# remove the column containing missing dates
missing_customers.drop(
    columns=["first_transaction_date"],
    inplace=True
)

# specifying where to save the csv
file_path = Path(r"C:\python_learning\customers_missing_dates.csv")

# save the csv file
missing_customers.to_csv(file_path, index=False)

# verify the results
print("Missing customers:", len(missing_customers))
print("Columns:", missing_customers.columns.tolist())
print("CSV FILE LOCATION:", file_path)
print("FILE EXISTS:", file_path.exists())