import pandas as pd
import os

# Read the autism dataset
current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_dir, 'Autism_Data.csv')

# Read CSV file
df = pd.read_csv(data_path)

# Convert dataframe to list of transactions
transactions = []
for _, row in df.iterrows():
    transaction = set()
    for column in df.columns:
        if column not in ['age', 'result', 'Class/ASD']:  # Exclude non-categorical columns
            value = row[column]
            if pd.notna(value):  # Only add non-null values
                transaction.add(f"{column}_{value}")
    transactions.append(transaction)
