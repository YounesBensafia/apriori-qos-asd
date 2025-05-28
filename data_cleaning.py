import pandas as pd
import numpy as np
import os

def load_data():
    """Load the Autism dataset from CSV file"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, 'Autism_Data.csv')
    return pd.read_csv(data_path)

def clean_data(df):
    """
    Clean and preprocess the Autism dataset
    """
    # Create a copy to avoid modifying the original dataframe
    df_clean = df.copy()
    
    # 1. Handle missing values
    # Replace '?' with NaN
    df_clean = df_clean.replace('?', np.nan)
    
    # 2. Convert categorical columns to proper format
    categorical_columns = df_clean.select_dtypes(include=['object']).columns
    for col in categorical_columns:
        if col not in ['age', 'result', 'Class']:
            df_clean[col] = df_clean[col].str.strip().str.lower()
    
    # 3. Convert age to numeric, handling any non-numeric values
    df_clean['age'] = pd.to_numeric(df_clean['age'], errors='coerce')
    
    # 4. Convert result to numeric (0 or 1)
    df_clean['result'] = pd.to_numeric(df_clean['result'], errors='coerce')
    
    # 5. Clean Class column and convert to 1/0
    df_clean['Class'] = df_clean['Class'].str.strip().str.lower()
    df_clean['Class'] = (df_clean['Class'] == 'yes').astype(int)
    
    # 6. Convert yes/no columns to 1/0
    binary_columns = ['jundice', 'austim', 'used_app_before']
    for col in binary_columns:
        df_clean[col] = (df_clean[col].str.lower() == 'yes').astype(int)
    
    # 7. Remove duplicates
    df_clean = df_clean.drop_duplicates()
    
    # 8. Remove rows with all missing values
    df_clean = df_clean.dropna(how='all')
    
    return df_clean

def get_data_summary(df):
    """Generate a summary of the dataset"""
    summary = {
        'shape': df.shape,
        'columns': df.columns.tolist(),
        'missing_values': df.isnull().sum().to_dict(),
        'unique_values': {col: df[col].nunique() for col in df.columns},
        'data_types': df.dtypes.to_dict()
    }
    return summary

def main():
    # Load the data
    df = load_data()
    
    # Clean the data
    df_clean = clean_data(df)
    
    # Get summary of cleaned data
    summary = get_data_summary(df_clean)
    
    # Print summary
    print("\nDataset Summary:")
    print(f"Shape: {summary['shape']}")
    print("\nColumns:", summary['columns'])
    print("\nMissing Values:")
    for col, count in summary['missing_values'].items():
        if count > 0:
            print(f"{col}: {count}")
    print("\nUnique Values per Column:")
    for col, count in summary['unique_values'].items():
        print(f"{col}: {count}")
    
    # Save cleaned data
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Autism_Data_Cleaned.csv')
    df_clean.to_csv(output_path, index=False)
    print(f"\nCleaned data saved to: {output_path}")
    
    return df_clean
if __name__ == "__main__":
    df_clean = main()
    df_clean = df_clean.dropna()
    print(f"\nRemoved all rows with missing values. New shape: {df_clean.shape}")
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Autism_Data_Final.csv')
    df_clean.to_csv(output_path, index=False)
    print(f"\nFinal cleaned data saved to: {output_path}")
    empty_values = df_clean.isna().sum().sum()
    print(f"\nNumber of empty values in final dataset: {empty_values}")