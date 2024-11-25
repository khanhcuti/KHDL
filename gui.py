import tkinter as tk
from tkinter import ttk
from tensorflow.keras.models import load_model
import joblib
import numpy as np
from src.recommendations import get_recommendations

# Load mô hình và scaler
model = load_model('./model/best_model.h5')
scaler = joblib.load('./model/scaler.pkl')
label_encoder = joblib.load('./model/label_encoder.pkl')

def predict_health():
    try:
        # Lấy dữ liệu từ các entry
        inputs = [
            float(entry_soil_moisture.get()),
            float(entry_ambient_temp.get()),
            float(entry_soil_temp.get()),
            float(entry_humidity.get()),
            float(entry_light_intensity.get()),
            float(entry_soil_ph.get()),
            float(entry_nitrogen.get()),
            float(entry_phosphorus.get()),
            float(entry_potassium.get()),
            float(entry_chlorophyll.get()),
            float(entry_electrochemical.get())
        ]
        
        # Chuẩn hóa dữ liệu
        inputs_scaled = scaler.transform([inputs])
        
        # Dự đoán với CNN
        prediction_prob = model.predict(inputs_scaled)
        prediction = np.argmax(prediction_prob[0])
        result = label_encoder.inverse_transform([prediction])[0]
        confidence = prediction_prob[0][prediction] * 100
        
        # Hiển thị kết quả
        result_label.config(text=f"Trạng thái hiện tại: {result}")
        confidence_label.config(text=f"Độ tin cậy: {confidence:.2f}%")
        
        # Nếu không phải Healthy, hiển thị khuyến nghị
        if result != "Healthy":
            recommendations = get_recommendations(inputs)
            recommendation_text.delete(1.0, tk.END)
            recommendation_text.insert(tk.END, recommendations)
        else:
            recommendation_text.delete(1.0, tk.END)
            recommendation_text.insert(tk.END, "Cây đang trong tình trạng khỏe mạnh!")

    except Exception as e:
        recommendation_text.delete(1.0, tk.END)
        recommendation_text.insert(tk.END, f"Lỗi: {str(e)}")

# Tạo giao diện
root = tk.Tk()
root.title("Plant Health Prediction")

# Frame chính
main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Frame bên trái cho input
input_frame = ttk.LabelFrame(main_frame, text="Input Parameters", padding="5")
input_frame.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))

# Labels và Entries cho các chỉ số
fields = [
    "Soil Moisture (%)", 
    "Ambient Temperature (°C)", 
    "Soil Temperature (°C)",
    "Humidity (%)", 
    "Light Intensity (LUX)", 
    "Soil PH", 
    "Nitrogen Level (Mg/kg)",
    "Phosphorus Level (Mg/kg)", 
    "Potassium Level (Mg/kg)",
    "Chlorophyll Content (mg/m²)", 
    "Electrochemical Signal (mV)"
]

entries = []

for i, field in enumerate(fields):
    label = ttk.Label(input_frame, text=field)
    label.grid(row=i, column=0, padx=5, pady=2, sticky=tk.W)
    entry = ttk.Entry(input_frame, width=15)
    entry.grid(row=i, column=1, padx=5, pady=2)
    entries.append(entry)

# Map các entry vào biến riêng
(entry_soil_moisture, entry_ambient_temp, entry_soil_temp,
 entry_humidity, entry_light_intensity, entry_soil_ph,
 entry_nitrogen, entry_phosphorus, entry_potassium,
 entry_chlorophyll, entry_electrochemical) = entries

# Frame bên phải cho kết quả và khuyến nghị
result_frame = ttk.LabelFrame(main_frame, text="Results and Recommendations", padding="5")
result_frame.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))

# Labels cho kết quả
result_label = ttk.Label(result_frame, text="Trạng thái hiện tại: ")
result_label.grid(row=0, column=0, padx=5, pady=2, sticky=tk.W)

confidence_label = ttk.Label(result_frame, text="Độ tin cậy: ")
confidence_label.grid(row=1, column=0, padx=5, pady=2, sticky=tk.W)

# Text widget cho khuyến nghị
recommendation_text = tk.Text(result_frame, width=40, height=20)
recommendation_text.grid(row=2, column=0, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))

# Nút dự đoán
predict_button = ttk.Button(main_frame, text="Predict Health", command=predict_health)
predict_button.grid(row=1, column=0, columnspan=2, pady=10)

# Cấu hình grid
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)
main_frame.rowconfigure(0, weight=1)
result_frame.columnconfigure(0, weight=1)
result_frame.rowconfigure(2, weight=1)

root.mainloop()