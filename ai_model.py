import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Load your dataset
def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

# Step 2: Preprocess the data
def preprocess_data(data, target_column, time_column=None):
    # Fill missing values (forward fill)
    data = data.fillna(method='ffill').fillna(method='bfill')
    
    # Remove commas from numeric columns and convert them to float
    for column in data.select_dtypes(include=['object']).columns:
        if column != target_column:
            data[column] = data[column].replace({',': ''}, regex=True)
            data[column] = pd.to_numeric(data[column], errors='coerce')  # Convert to numeric, invalid parsing will be NaN

    # Ensure target column is numeric, removing commas and converting to float
    data[target_column] = data[target_column].replace({',': ''}, regex=True)
    data[target_column] = pd.to_numeric(data[target_column], errors='coerce')

    # Handle categorical columns by encoding them (if necessary)
    label_encoder = LabelEncoder()
    for column in data.select_dtypes(include=['object']).columns:
        if column != target_column:
            data[column] = label_encoder.fit_transform(data[column])

    # If there is a time column, extract useful features (year, month, etc.)
    if time_column:
        data[time_column] = pd.to_datetime(data[time_column], errors='coerce')
        data['Year'] = data[time_column].dt.year
    
    # Separate features (X) and target (y)
    X = data.drop(columns=[target_column])
    y = data[target_column]
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    return X_scaled, y

# Step 3: Train the model
def train_model(X, y):
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Use Random Forest Regressor for this task
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Predict and evaluate the model
    y_pred = model.predict(X_test)
    print("Mean Squared Error:", mean_squared_error(y_test, y_pred))
    
    return model, X_test, y_test, y_pred

# Step 4: Visualize the trends
def visualize_trends(data, time_column, target_column):
    # Group by year or another time period
    trend_data = data.groupby([data[time_column]])[target_column].agg('sum').reset_index()
    
    # Plot trends
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=trend_data, x=time_column, y=target_column)
    plt.title(f'{target_column} Trends Over Time')
    plt.xlabel('Year')
    plt.ylabel(target_column)
    plt.show()
    
# Function to determine if an outbreak will occur
def analyze_outbreak(predictions, threshold):
    outbreak = predictions > threshold
    if np.any(outbreak):
        return "Alert: Potential outbreak detected!"
    else:
        return "No outbreak predicted."

# Main Program
if __name__ == "__main__":
    # File path to your dataset (adjust to your file's location)
    file_path = r"C:\Users\rohit\OneDrive\Desktop\health_guard\dataset\Dengue.csv"  # Change to your actual file path
    
    # Load and preprocess the data
    data = load_data(file_path)
    target_column = "Total_Deaths"  # Change this to the actual column you're predicting
    time_column = "Year"  # Assuming you have a time-related column in the data
    
    # Preprocess the data
    X, y = preprocess_data(data, target_column, time_column)
    
    # Train the model
    model, X_test, y_test, y_pred = train_model(X, y)
    
    # Visualize the trends (e.g., death_rate trends by year)
    visualize_trends(data, time_column, target_column)
    
    # Predict on new data (if available)
    new_data = pd.read_csv(r"C:\Users\rohit\OneDrive\Desktop\health_guard\recent.csv")
    X_new, _ = preprocess_data(new_data, target_column, time_column)
    predictions = model.predict(X_new)
    print("Predictions:", predictions)
    threshold = 100  # Adjust based on your dataset
    result = analyze_outbreak(predictions, threshold)
    print(result)