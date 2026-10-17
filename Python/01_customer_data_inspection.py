import pandas as pd

# To load the data

df = pd.read_csv("customer.csv")

# To know the dataset size
print(df.shape)

# To know the column titles/names
print(df.columns)

# To know the data types e.g. str, int
print(df.dtypes)

# To find missing values
print(df.isnull().sum())

# To know if there's any duplicated customer id
print(df["customer_id"].duplicated().sum())

# To find the age statistics i.e min and max age
print(df["age"].describe())

# number of male and female
print(df["gender"].value_counts())

print(df["customer_type"].value_counts())

print(df["plan"].value_counts())

print(df["status"].value_counts())

# To show how active vs inactive customers are distributed across basic, standard, and premium
print(pd.crosstab(df["status"], df["plan"]))

# To know the overall percentage of customers who are active vs inactive
print(df["status"].value_counts(normalize=True) * 100)

# To calculate the percentage of customers within each plan who are active
print(pd.crosstab(df["plan"], df["status"], normalize="index") * 100)

# To see how customers are distributed across customer_type i.e business or individual
print(df["customer_type"].value_counts())

print(df["customer_type"].value_counts(normalize=True) * 100)

# To know if the customer behaviour differ between individual and business customers
print(pd.crosstab(
    df["customer_type"],
    df["status"],
    normalize="index"
) * 100)



# To know what channels exist and how many customers came through each one
print(df["acquisition_channel_id"].value_counts())

print(df["acquisition_channel_id"].value_counts(normalize=True) * 100)

# To know which acquisition channels have the highest proportion of active customers
print(pd.crosstab(
    df["acquisition_channel_id"],
    df["status"],
    normalize="index"
) * 100)



print(df["age"].describe())

# To know how customers are distributed across age ranges
print(pd.cut(
    df["age"],
    bins=[17, 24, 34, 44, 54, 64, 70],
    labels=["18-24", "25-34", "35-44", "45-54", "55-64", "65-70"]
).value_counts().sort_index())

# To know whether active and inactive customers have noticeably different age profiles
print(df.groupby("status")["age"].agg(["count", "mean", "median", "min", "max"]))



# Checking gender
print(df["gender"].value_counts())

print(df["gender"].value_counts(normalize=True) * 100)

# To know the difference in activity status by gender
print(pd.crosstab(
    df["gender"],
    df["status"],
    normalize="index"
) * 100)



# To know the geographic distribution
print(df["state"].value_counts())

print(df["state"].value_counts(normalize=True).head(10) * 100)

# To know whether the active rate differs across states
print(pd.crosstab(
    df["state"],
    df["status"],
    normalize="index"
) * 100)



# To know how geographically concentrated the customers are at the city level
print(df["city"].value_counts())

# To know whether customer activity differs across cities
print(pd.crosstab(
    df["city"],
    df["status"],
    normalize="index"
) * 100)



print(df[["signup_date", "first_transaction_date"]].dtypes)

# To convert both columns to dates
df["signup_date"] = pd.to_datetime(df["signup_date"])
df["first_transaction_date"] = pd.to_datetime(df["first_transaction_date"])
print(df[["signup_date", "first_transaction_date"]].dtypes)

# To know the time period these customers where acquired
print("Earliext signup:", df["signup_date"].min())
print("Latest signup:", df["signup_date"].max())

# To know how many customers signed up each month
df["signup_month"] = df["signup_date"].dt.to_period("M")
print(df["signup_month"].value_counts().sort_index())

# To know how many days it took each customer to make their first transaction after signing up
df["days_to_first_transaction"] = (
    df["first_transaction_date"] - df["signup_date"]
).dt.days

print(df["days_to_first_transaction"].describe())

# To investigate the 3082 missing first-transaction dates
print(pd.crosstab(
    df["status"],
    df["first_transaction_date"].isna()
))

# Calculating the percentage of customers who have a first transaction date and the percentage who are missing one
print(df["first_transaction_date"].notna().mean() * 100)

print(df["first_transaction_date"].isna().mean() * 100)

# Comparing the two groups of customers who are currently active and inactive in how quickly they made their first transaction
print(df.groupby("status")["days_to_first_transaction"].describe())

# Proportion of active vs inactive customers across signup months
print(pd.crosstab(
    df["signup_month"],
    df["status"],
    normalize="index"
) * 100)


# To know customers who might have a first transaction before their signup date
print((df["first_transaction_date"] < df["signup_date"]).sum())









import numpy as np
import pandas as pd

# make sure date columns are in datetime format
df["signup_date"] = pd.to_datetime(df["signup_date"])
df["first_transaction_date"] = pd.to_datetime(
    df["first_transaction_date"]
)

# set up reproducible random data
rng = np.random.default_rng(42)

transaction_types = [
    "P2P Transfer",
    "Bill Payment",
    "Airtime",
    "Merchant Payment",
    "Bank Transfer"
]

payment_methods = [
    "Wallet",
    "Bank Account",
    "Card",
    "USSD"
]

statuses = ["Successful", "Failed", "Pending"]
status_weights = [0.92, 0.06, 0.02]

records = []
transaction_number = 1

for customer in df.itertuples(index=False):
    # Only customers with a recorded first transaction
    # will have transaction records
    if pd.isna(customer.first_transaction_date):
        continue

    first_date = customer.first_transaction_date

    # generate between 2 and 13 transactions per customer
    n = rng.integers(2, 13)

    # first transaction date plus later transactions
    offsets = [0] + sorted(
        rng.integers(1, 91, size=n - 1).tolist()
    )

    for i, offset in enumerate(offsets):
        # the first transaction is recorded as successful
        status = (
            "Successful" if i == 0
            else rng.choice(statuses, p=status_weights)
        )

        records.append({
            "transaction_id": f"TXN{transaction_number:07d}",
            "customer_id": customer.customer_id,
            "transaction_date": first_date + pd.Timedelta(days=int(offset)),
            "amount": round(float(rng.uniform(500, 100000)), 2),
            "transaction_type": rng.choice(transaction_types),
            "payment_method": rng.choice(payment_methods),
            "transaction_status": status
        })

        transaction_number += 1

# Create the DataFrame and save it
transactions = pd.DataFrame(records)

transactions.to_csv("transactions.csv", index=False)

print("Transactions dataset created!")
print(transactions.shape)
print(transactions.head())

transactions.info()



# checking the basic transaction statistics
print(transactions["amount"].describe())
print(transactions["transaction_status"].value_counts())
print(transactions["transaction_type"].value_counts())

# calculate the percentages
print(transactions["transaction_status"].value_counts(normalize=True) * 100)

# understanding when the transactions are happening
print(transactions["transaction_date"].min())
print(transactions["transaction_date"].max())
print(transactions["transaction_date"].describe())


# analysing transaction activity over time
transactions["transaction_month"] = transactions["transaction_date"].dt.to_period("M")

monthly_transactions = transactions.groupby("transaction_month").agg(
    transaction_count=("transaction_id", "count"),
    total_transaction_value=("amount", "sum"),
    average_transaction_value=("amount", "mean")
)

print(monthly_transactions)



# which transaction types generate the most transaction value
transaction_type_summary = transactions.groupby("transaction_type").agg(
    transaction_count=("transaction_id", "count"),
    total_transaction_value=("amount", "sum"),
    average_transaction_value=("amount", "mean")
).sort_values(
    "total_transaction_value",
    ascending=False
)

print(transaction_type_summary)



# Payment methods
payment_method_summary = transactions.groupby("payment_method").agg(
    transaction_count=("transaction_id", "count"),
    total_transaction_value=("amount", "sum"),
    average_transaction_value=("amount", "mean")
).sort_values(
    "transaction_count",
    ascending=False
)

print(payment_method_summary)



# payment method performance
payment_method_status = pd.crosstab(
    transactions["payment_method"],
    transactions["transaction_status"],
    normalize="index"
) * 100

print(payment_method_status)



# to see whether the transaction type has different success/failure patterns
transaction_type_status = pd.crosstab(
    transactions["transaction_type"],
    transactions["transaction_status"],
    normalize="index"
) * 100

print(transaction_type_status)





# To find out many how many transactions each customer makes
customer_transactions = transactions.groupby("customer_id").agg(
    transaction_count=("transaction_id", "count"),
    total_transaction_value=("amount", "sum"),
    average_transaction_value=("amount", "mean")
)

print(customer_transactions.describe())




# categorizing customers based on how frequently they transact. This will help us distinguish lower activity customers from more active ones.
customer_transactions["activity_level"] = pd.cut(
    customer_transactions["transaction_count"],
    bins=[0, 4, 8, float("inf")],
    labels=["Low", "Medium", "High"]
)

activity_summary = customer_transactions.groupby(
    "activity_level", observed=False
).agg(
    customer_count=("transaction_count", "count"),
    average_transactions=("transaction_count", "mean"),
    average_total_value=("total_transaction_value", "mean")
)

activity_summary["customer_percentage"] = (
    activity_summary["customer_count"]
    / activity_summary["customer_count"].sum()
) * 100

print(activity_summary)







# merging the customer and transaction datasets to see how customer characteristics relate to their transaction activity
customer_analysis = df.merge(
    customer_transactions,
    on="customer_id",
    how="left"
)

print(customer_analysis.shape)
print(customer_analysis.head())




# identify customers with no transactions
no_transaction_customers = customer_analysis[
    customer_analysis["transaction_count"].isna()
]

print("Customers with no transactions:", len(no_transaction_customers))


# analyze the no-transaction customers i.e. among the customers who have no transactions, how many are active vs inactive
no_transaction_status = (
    no_transaction_customers["status"]
    .value_counts()
)

print(no_transaction_status)




# comparing transaction vs no transaction customers
customer_analysis["transaction_participation"] = (
    customer_analysis["transaction_count"]
    .notna()
    .map({
        True: "Transacted",
        False: "No Transaction"
    })
)

participation_summary =(
    customer_analysis["transaction_participation"]
    .value_counts()
)

print(participation_summary)



# Which types of customers are more or less likely to transact
participation_by_type = (
    customer_analysis
    .groupby("customer_type")["transaction_participation"]
    .value_counts(normalize=True)
    .unstack()
    .fillna(0) * 100
)

print(participation_by_type)



# to see whether the customer's plan is associated with transaction participation
participation_by_plan = (
    customer_analysis
    .groupby("plan")["transaction_participation"]
    .value_counts(normalize=True)
    .unstack()
    .fillna(0) * 100
)

print(participation_by_plan)



# compareing transaction activity by plan
activity_by_plan = (
    customer_analysis[
        customer_analysis["transaction_participation"] == "Transacted"
    ]
    .groupby("plan")
    .agg(
        customer_count=("customer_id", "count"),
        average_transactions=("transaction_count", "mean"),
        average_total_value=("total_transaction_value", "mean"),
        average_transaction_value=("average_transaction_value", "mean")
    )
)

print(activity_by_plan)




# to know which acquisition channels produced customers who are more likely to transact
participation_by_channel = (
    customer_analysis
    .groupby("acquisition_channel_id")["transaction_participation"]
    .value_counts(normalize=True)
    .unstack()
    .fillna(0) * 100
)

print(participation_by_channel)




# to see which acquisition channels bring the most active and financially valuable customers
activity_by_channel = (
    customer_analysis[
        customer_analysis["transaction_participation"] == "Transacted"
    ]
    .groupby("acquisition_channel_id")
    .agg(
        customer_count=("customer_id", "count"),
        average_transactions=("transaction_count", "mean"),
        average_total_value=("total_transaction_value", "mean"),
        average_transaction_value=("average_transaction_value", "mean")
    )
)

print(activity_by_channel)

print(activity_by_channel.to_string())





# investigating whether business and individual customers behave differently once they start transacting
activity_by_customer_type = (
    customer_analysis[
        customer_analysis["transaction_participation"] == "Transacted"
    ]
    .groupby("customer_type")
    .agg(
        customer_count=("customer_id", "count"),
        average_transactions=("transaction_count", "mean"),
        average_total_value=("total_transaction_value", "mean"),
        average_transaction_value=("average_transaction_value", "mean")
    )
)

print(activity_by_customer_type)





# checking whether male and female customers differ in transaction behaviour
activity_by_gender = (
    customer_analysis[
        customer_analysis["transaction_participation"] == "Transacted"
    ]
    .groupby("gender")
    .agg(
        customer_count=("customer_id", "count"),
        average_transactions=("transaction_count", "mean"),
        average_total_value=("total_transaction_value", "mean"),
        average_transaction_value=("average_transaction_value", "mean")
    )
)

print(activity_by_gender.to_string())




# to check age groups
customer_analysis["age_group"] = pd.cut(
    customer_analysis["age"],
    bins=[17, 24, 34, 44, 54, 64, 70],
    labels=["18-24", "25-34", "35-44", "45-54", "55-64", "65-70"]
)

activity_by_age_group = (
    customer_analysis[
        customer_analysis["transaction_participation"] == "Transacted"
    ]
    .groupby("age_group", observed=False)
    .agg(
        customer_count=("customer_id", "count"),
        average_transactions=("transaction_count", "mean"),
        average_total_value=("total_transaction_value", "mean"),
        average_transaction_value=("average_transaction_value", "mean")
    )
)

print(activity_by_age_group)





# seeing whether customers from different states behave diffrently
activity_by_state = (
    customer_analysis[
        customer_analysis["transaction_participation"] == "Transacted"
    ]
    .groupby("state")
    .agg(
        customer_count=("customer_id", "count"),
        average_transactions=("transaction_count", "mean"),
        average_total_value=("total_transaction_value", "mean"),
        average_transaction_value=("average_transaction_value", "mean")
    )
    .sort_values("average_total_value", ascending=False)
)

print(activity_by_state)



# to know the behaviour of customers who joined earlier versus later cohorts
activity_by_signup_month = (
    customer_analysis[
        customer_analysis["transaction_participation"] == "Transacted"
    ]
    .groupby(customer_analysis["signup_date"].dt.to_period("M"))
    .agg(
        customer_count=("customer_id", "count"),
        average_transactions=("transaction_count", "mean"),
        average_total_value=("total_transaction_value", "mean"),
        average_transaction_value=("average_transaction_value", "mean")
    )
)

print(activity_by_signup_month)






# creating customer level transaction success rates
customer_success_rate = (
    transactions
    .groupby("customer_id")
    .agg(
        total_transactions=("transaction_id", "count"),
        successful_transactions=("transaction_status", lambda x: (x == "Successful").sum())
    )
)

customer_success_rate["success_rate"] = (
    customer_success_rate["successful_transactions"]
    / customer_success_rate["total_transactions"]
) * 100

print(customer_success_rate.head())




# adding activity level to the success-rate data
customer_success_rate["activity_level"] = (
    customer_transactions["activity_level"]
)

print(customer_success_rate.head())




# comparing success rates by activity level
success_rate_by_activity = (
    customer_success_rate
    .groupby("activity_level", observed=False)
    .agg(
        customer_count=("success_rate", "count"),
        average_success_rate=("success_rate", "mean")
    )
)

print(success_rate_by_activity)




# to know which transaction types have the highest failure rates
failure_by_type = (
    transactions
    .groupby("transaction_type")
    .agg(
        total_transactions=("transaction_id", "count"),
        failed_transactions=(
            "transaction_status",
            lambda x: (x == "failed").sum()
        )
    )
)

failure_by_type["failure_rate"] = (
    failure_by_type["failed_transactions"]
    / failure_by_type["total_transactions"]
) * 100

failure_by_type = failure_by_type.sort_values(
    "failure_rate",
    ascending=False
)

print(failure_by_type)




# investigating where the 7885 failed transactions are actually coming from
failure_by_method = (
    transactions
    .groupby("payment_method")
    .agg(
        total_transactions=("transaction_id", "count"),
        failed_transactions=(
            "transaction_status",
            lambda x: (x == "failed").sum()
        )
    )
)

failure_by_method["failure_rate"] =(
    failure_by_method["failed_transactions"]
    / failure_by_method["total_transactions"]
) * 100

failure_by_method = failure_by_method.sort_values(
    "failure_rate",
    ascending=False
)

print(failure_by_method.to_string())


# checking the actual failed transaction records
failed_transactions = transactions[
    transactions["transaction_status"] == "Failed"
]

print(failed_transactions.head(10).to_string())
print("\nFailed transactions:", len(failed_transactions))



# checking the actual status values
print(transactions["transaction_status"].value_counts())

print(
    transactions[
        transactions["transaction_status"] == "Failed"
    ]["transaction_type"].value_counts()
)




# redoing the transaction type failure analysis
failure_by_type = (
    transactions[transactions["transaction_status"] == "Failed"]
    .groupby("transaction_type")
    .size()
    .reset_index(name="failed_transactions")
)

total_by_type = (
    transactions
    .groupby("transaction_type")
    .size()
    .reset_index(name="total_transactions")
)

failure_by_type = failure_by_type.merge(
    total_by_type,
    on="transaction_type"
)

failure_by_type["failure_rate"] = (
    failure_by_type["failed_transactions"]
    / failure_by_type["total_transactions"]
) * 100

failure_by_type = failure_by_type.sort_values(
    "failure_rate",
    ascending=False
)

print(failure_by_type.to_string(index=False))




# payment method failure analysis
failure_by_method = (
    transactions[transactions["transaction_status"] == "Failed"]
    .groupby("payment_method")
    .size()
    .reset_index(name="failed_transactions")
)

total_by_method = (
    transactions
    .groupby("payment_method")
    .size()
    .reset_index(name="total_transactions")
)

failure_by_method = failure_by_method.merge(
    total_by_method,
    on="payment_method"
)

failure_by_method["failure_rate"] = (
    failure_by_method["failed_transactions"]
    / failure_by_method["total_transactions"]
) * 100

failure_by_method = failure_by_method.sort_values(
    "failure_rate",
    ascending=False
)

print(failure_by_method.to_string(index=False))




# let's connect customer activity level with transaction value and reliability
activity_performance = (
    customer_success_rate
    .groupby("activity_level", observed=False)
    .agg(
        customer_count=("success_rate", "count"),
        average_success_rate=("success_rate", "mean")
    )
)

activity_performance = activity_performance.join(
    activity_summary[
        ["average_transactions", "average_total_value"]
    ]
)

print(activity_performance)