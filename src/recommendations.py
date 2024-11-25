def get_recommendations(inputs):
    recommendations = []
    
    # Định nghĩa các ngưỡng giá trị lý tưởng
    ideal_ranges = {
        "Soil Moisture": (32, 40),           # % - Dựa trên các mẫu Healthy (30-40%)
        "Ambient Temperature": (18, 29),      # °C - Phạm vi tối ưu từ dữ liệu
        "Soil Temperature": (15, 24),         # °C - Nhiệt độ đất phù hợp
        "Humidity": (45, 65),                 # % - Độ ẩm không khí tối ưu
        "Light Intensity": (350, 850),        # LUX - Dựa trên phân tích mẫu khỏe mạnh
        "Soil pH": (5.5, 7.3),               # pH - Khoảng pH phù hợp nhất
        "Nitrogen": (30, 45),                 # Mg/kg - Hàm lượng N tối ưu
        "Phosphorus": (25, 45),               # Mg/kg - Hàm lượng P tối ưu
        "Potassium": (30, 50),                # Mg/kg - Hàm lượng K tối ưu
        "Chlorophyll": (25, 45),              # mg/m² - Hàm lượng diệp lục tối ưu
        "Electrochemical": (0.7, 1.8)         # mV - Tín hiệu điện hóa khỏe mạnh
    }
    
    current_values = {
        "Soil Moisture": inputs[0],
        "Ambient Temperature": inputs[1],
        "Soil Temperature": inputs[2],
        "Humidity": inputs[3],
        "Light Intensity": inputs[4],
        "Soil pH": inputs[5],
        "Nitrogen": inputs[6],
        "Phosphorus": inputs[7],
        "Potassium": inputs[8],
        "Chlorophyll": inputs[9],
        "Electrochemical": inputs[10]
    }

    # Phân tích từng chỉ số và đưa ra khuyến nghị cụ thể
    for param, value in current_values.items():
        min_val, max_val = ideal_ranges[param]
        if value < min_val:
            recommendations.append(
                f"{param}: {value:.2f} → {min_val:.2f} - {max_val:.2f}\n"
                f"Cần tăng {(min_val - value):.2f} đơn vị"
            )
        elif value > max_val:
            recommendations.append(
                f"{param}: {value:.2f} → {min_val:.2f} - {max_val:.2f}\n"
                f"Cần giảm {(value - max_val):.2f} đơn vị"
            )

    # Dựa vào dữ liệu của bạn
    specific_recommendations = []
    
    # Soil Moisture (33.30% → 40-60%)
    if inputs[0] < 40:
        specific_recommendations.append(
            "Tăng độ ẩm đất lên 40-60% bằng cách:\n"
            "- Tăng tần suất tưới nước\n"
            "- Sử dụng hệ thống tưới nhỏ giọt"
        )
    
    # Light Intensity (455.69 LUX → 1000-2000 LUX)
    if inputs[4] < 1000:
        specific_recommendations.append(
            "Tăng cường ánh sáng bằng cách:\n"
            "- Di chuyển cây đến nơi có nhiều ánh sáng\n"
            "- Bổ sung đèn grow light"
        )
    
    # NPK Levels
    if inputs[6] < 20 or inputs[7] < 15 or inputs[8] < 30:
        specific_recommendations.append(
            "Cải thiện dinh dưỡng NPK bằng cách:\n"
            "- Bổ sung phân NPK cân bằng\n"
            "- Sử dụng phân hữu cơ"
        )

    # Kết hợp các khuyến nghị
    final_message = "Khuyến nghị để đạt trạng thái Healthy:\n\n"
    final_message += "Các chỉ số cần điều chỉnh:\n"
    final_message += "\n".join(recommendations)
    final_message += "\n\nCách thực hiện:\n"
    final_message += "\n\n".join(specific_recommendations)
    
    return final_message 