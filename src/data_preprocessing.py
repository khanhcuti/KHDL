# src/data_preprocessing.py

import pandas as pd
from sklearn.preprocessing import StandardScaler

def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

def preprocess_data(data):
    # Bỏ các cột không cần thiết
    X = data.drop(columns=['Plant_Health_Status', 'Timestamp', 'Plant_ID'])
    y = data['Plant_Health_Status']
    
    # Chuẩn hóa dữ liệu
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_scaled = pd.DataFrame(X_scaled, columns=X.columns)
    
    return X_scaled, y, scaler