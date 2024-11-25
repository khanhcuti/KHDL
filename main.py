# main.py

from src.data_preprocessing import load_data, preprocess_data
from src.model_training import train_model
from src.visualization import plot_confusion_matrix, plot_training_history
import joblib
import os

def main():
    if not os.path.exists('model'):
        os.makedirs('model')
    
    file_path = 'data/plant_health_data.csv'
    data = load_data(file_path)
    
    X, y, scaler = preprocess_data(data)
    
    # Huấn luyện mô hình CNN
    model, y_test, y_pred, label_encoder, history = train_model(X, y)
    
    # Trực quan hóa kết quả
    plot_confusion_matrix(y_test, y_pred)
    plot_training_history(history)
    
    # Lưu scaler và label encoder
    joblib.dump(scaler, 'model/scaler.pkl')
    joblib.dump(label_encoder, 'model/label_encoder.pkl')

if __name__ == "__main__":
    main()