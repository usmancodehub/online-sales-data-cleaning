import pandas as pd

# ---------- STEP 1: Load ----------
df = pd.read_csv("data/online_sales_raw.csv")
print("Shape:", df.shape)
print(df.head())

# # ---------- STEP 2: Inspect ----------
# df.info()
# print(df.describe())

# ---------- STEP 3: Find missing values (BEFORE) ----------
print("Missing values per column (BEFORE):")
print(df.isnull().sum())
print("Missing % :")
print((df.isnull().mean()*100).round(2))

# # ---------- STEP 4: Fix inconsistent text (so hidden duplicates become visible) ----------
# for col in ["Product_Category","Payment_Method","Region"]:
#     df[col] = df[col].str.strip().str.title()
# df["Payment_Method"] = df["Payment_Method"].replace({"Paypal":"PayPal"})

# ---------- STEP 5: Duplicates ----------
print("Exact duplicate rows:", df.duplicated().sum())
print("Duplicate Order_IDs :", df.duplicated(subset="Order_ID").sum())
df["_nulls"] = df.isnull().sum(axis=1)                       # keep the most complete copy
df = (df.sort_values(["Order_ID","_nulls"]).drop_duplicates(subset="Order_ID", keep="first")
        .drop(columns="_nulls").reset_index(drop=True))
print("Shape after removing duplicates:", df.shape)

# ---------- STEP 6: Fix data types ----------
df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")

# ---------- STEP 7: Handle missing values ----------
df["Order_Date"] = df["Order_Date"].fillna(df["Order_Date"].median())          # date -> median date
df["Customer_ID"] = df["Customer_ID"].fillna("Unknown")                        # ID -> 'Unknown'
for col in ["Product_Category","Payment_Method","Region"]:                     # categorical -> mode
    df[col] = df[col].fillna(df[col].mode()[0])
df["Quantity"] = df["Quantity"].fillna(df["Quantity"].median())                # numeric -> median
df["Unit_Price"] = df["Unit_Price"].fillna(df.groupby("Product_Name")["Unit_Price"].transform("median"))
df["Discount_Pct"] = df["Discount_Pct"].fillna(0)                              # no discount recorded -> 0
df["Total_Revenue"] = df["Total_Revenue"].fillna(df["Quantity"]*df["Unit_Price"]).round(2)  # recompute

# ---------- STEP 8: Outlier check ----------
q1,q3 = df["Total_Revenue"].quantile([.25,.75]); iqr=q3-q1
print("Outliers in Total_Revenue:", ((df["Total_Revenue"]<q1-1.5*iqr)|(df["Total_Revenue"]>q3+1.5*iqr)).sum())

# ---------- STEP 9: Verify (AFTER) ----------
print("Missing values per column (AFTER):")
print(df.isnull().sum())
print("Duplicate rows (AFTER):", df.duplicated().sum())
df["Quantity"] = df["Quantity"].astype(int)
df.info()

# ---------- STEP 10: Save ----------
df.to_csv("data/online_sales_clean.csv", index=False)
print("Saved cleaned file:", df.shape)
