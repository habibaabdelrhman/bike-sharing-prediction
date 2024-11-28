import os
import pandas as pd
from sklearn.model_selection import train_test_split

def load_data(file_paths):
    """
    Load and combine multiple CSV datasets.
    Returns a combined DataFrame and handles missing data.
    """
    data_frames = []
    
    # Iterate over each file path and load the data
    for file_path in file_paths:
        if os.path.exists(file_path):
            try:
                data = pd.read_csv(file_path, encoding='ISO-8859-1')  # Adjust encoding as necessary
                data_frames.append(data)
                print(f"Loaded dataset: {file_path}")
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
        else:
            print(f"Dataset not found at: {file_path}")
            raise FileNotFoundError(f"Dataset not found at: {file_path}")

    # Combine all dataframes along rows (axis=0)
    combined_data = pd.concat(data_frames, axis=0, ignore_index=True)
    print(f"Combined data shape: {combined_data.shape}")
    
    # Ensure the necessary columns exist for model preparation
    if 'discount' not in combined_data.columns or 'quantity' not in combined_data.columns or 'list_price' not in combined_data.columns:
        raise ValueError("One or more required columns are missing from the dataset: 'discount', 'quantity', or 'list_price'")
    
    return combined_data

def prepare_data(data):
    """
    Prepare the data for model training by creating a binary target variable (high_discount)
    and splitting the data into training and testing sets.
    """
    # Create a binary target variable for high discount (1 if discount > 0.1, else 0)
    data['high_discount'] = (data['discount'].astype(float) > 0.1).astype(int)
    
    # Select features (quantity, list_price) and target (high_discount)
    X = data[['quantity', 'list_price']]  # Features
    y = data['high_discount']  # Target variable
    
    # Split the dataset into training and testing sets (70% train, 30% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, stratify=y, random_state=2022)
    
    return X_train, X_test, y_train, y_test

# Example usage:
def load_and_prepare_data():
    try:
        # List of file paths
        file_paths = [
            "C:\\Users\\walee\\Downloads\\Depi\\Depi\\app\\DateDim.csv",
            "C:\\Users\\walee\\Downloads\\Depi\\Depi\\app\\CustomerDim.csv",
            "C:\\Users\\walee\\Downloads\\Depi\\Depi\\app\\OrderDim.csv",
            "C:\\Users\\walee\\Downloads\\Depi\\Depi\\app\\predicted_sentiments.csv",
            "C:\\Users\\walee\\Downloads\\Depi\\Depi\\app\\ProductDim.csv",
            "C:\\Users\\walee\\Downloads\\Depi\\Depi\\app\\CategoryDim.csv"
        ]

        # Load the data
        combined_data = load_data(file_paths)

        # Prepare the data for model training
        X_train, X_test, y_train, y_test = prepare_data(combined_data)

        print(f"Data prepared: {X_train.shape[0]} training samples, {X_test.shape[0]} testing samples")
        
        return X_train, X_test, y_train, y_test

    except Exception as e:
        print("An error occurred during data loading and preparation:", e)
        return None, None, None, None
