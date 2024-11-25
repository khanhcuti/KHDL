# src/model_training.py

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from src.cnn_model import create_cnn_model
import numpy as np

def train_model(X, y):
    # Mã hóa nhãn
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    
    # Chia dữ liệu
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, 
        test_size=0.2, 
        random_state=42
    )
    
    # Tạo mô hình CNN
    model = create_cnn_model()
    
    # Callbacks
    callbacks = [
        EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True
        ),
        ModelCheckpoint(
            'model/best_model.h5',
            monitor='val_loss',
            save_best_only=True
        )
    ]
    
    # Huấn luyện mô hình
    history = model.fit(
        X_train, y_train,
        epochs=100,
        batch_size=32,
        validation_split=0.2,
        callbacks=callbacks,
        verbose=1
    )
    
    # Dự đoán
    y_pred_prob = model.predict(X_test)
    y_pred = np.argmax(y_pred_prob, axis=1)
    
    return model, y_test, y_pred, le, history