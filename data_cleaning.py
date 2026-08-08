import pandas as pd
import os

# Excel file path
file = input("Enter file path: ")

# Check if file exists
if not os.path.exists(file):
    print("File not found!")
    print("Please enter the correct file path.")
    exit()

# Read Excel file
df = pd.read_excel(file)

print("\nOriginal Dataset:")
print(df)

# --------------------------------
# 1. Check Missing Values
# --------------------------------

print("\nChecking missing values...")

missing = df.isnull().sum()

for col in df.columns:
    if missing[col] > 0:
        print(f"Missing data found in {col}: {missing[col]} value(s)")

# --------------------------------
# 2. Remove Duplicate Records
# --------------------------------

duplicates = df.duplicated().sum()

if duplicates > 0:
    print(f"\nDuplicate records found: {duplicates}")
    df = df.drop_duplicates()
    print("Duplicate records removed.")
else:
    print("\nNo duplicate records found.")

# --------------------------------
# 3. Remove Completely Empty Rows
# --------------------------------

df = df.dropna(how="all")

# --------------------------------
# 4. Clean Text Columns
# --------------------------------

for col in df.select_dtypes(include="object"):
    df[col] = df[col].str.strip()

# --------------------------------
# 5. Convert Age to Numeric
# --------------------------------

if "Age" in df.columns:

    df["Age"] = pd.to_numeric(
        df["Age"],
        errors="coerce"
    )

    # Fill missing Age with median
    if df["Age"].isnull().sum() > 0:

        median_age = df["Age"].median()

        df["Age"] = df["Age"].fillna(median_age)

        print(
            f"\nMissing Age filled with median age: {median_age}"
        )

# --------------------------------
# 6. Convert Date Columns
# --------------------------------

for col in df.columns:

    if "date" in col.lower():

        df[col] = pd.to_datetime(
            df[col],
            errors="coerce"
        )

        print(f"Date format corrected for column: {col}")

# --------------------------------
# 7. Fill Missing Text Values
# --------------------------------

for col in df.select_dtypes(include="object"):

    if df[col].isnull().sum() > 0:

        df[col] = df[col].fillna("Unknown")

        print(
            f"Missing values filled in {col}"
        )

# --------------------------------
# 8. Save Cleaned Dataset
# --------------------------------

output_file = "clean_dataset.xlsx"

df.to_excel(
    output_file,
    index=False
)

# --------------------------------
# Final Output
# --------------------------------

print("\n--------------------------------")
print("Cleaned Dataset:")
print(df)

print("\nDataset cleaned successfully!")
print(f"Clean file saved as: {output_file}")
