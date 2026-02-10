# 📊 Vietnam IT Job Market Analysis

Dự án phân tích xu hướng tuyển dụng và dự đoán mức lương ngành IT tại Việt Nam.

## 🚀 Cách chạy dự án

### 1. Cài đặt thư viện
```bash
pip install -r requirements.txt
```

### 2. Tạo dữ liệu (nếu chưa có)
```bash
python src/generate_data.py
python src/clean_data.py
```

### 3. Huấn luyện Model (Tùy chọn - cho tính năng Dự đoán)
```bash
python src/train_model.py
```

### 4. Chạy Web Dashboard
```bash
streamlit run app.py
```

## 📁 Cấu trúc dự án

```
data-project-sample/
├── data/                          # Dữ liệu
│   ├── vietnam_it_jobs.csv       # Dữ liệu gốc
│   └── vietnam_it_jobs_cleaned.csv  # Dữ liệu đã làm sạch
├── src/                           # Mã nguồn
│   ├── generate_data.py          # Tạo dữ liệu
│   ├── clean_data.py             # Làm sạch dữ liệu
│   ├── eda_analysis.py           # Phân tích EDA (tạo biểu đồ PNG)
│   └── train_model.py            # Huấn luyện mô hình
├── models/                        # Mô hình đã train
│   └── salary_model.pkl
├── app.py                         # Web Dashboard (Streamlit)
├── requirements.txt               # Thư viện cần thiết
└── README.md                      # Tệp này
```

## 🎨 Tính năng

### 📊 Dashboard (Trang chủ)
- **Metrics tổng quan**: Tổng số việc làm, lương trung bình, thị trường lớn nhất
- **Biểu đồ phân tích**:
  - Phân phối mức lương
  - Lương theo kinh nghiệm (Fresher → Manager)
  - Top 10 kỹ năng được yêu cầu
  - Lương theo địa điểm (HCM, Hà Nội, Đà Nẵng...)
  - Phân bố chức danh công việc

### 🔮 Salary Predictor (Dự đoán)
- Nhập thông tin: Kinh nghiệm, Địa điểm, Chức danh
- Nhận mức lương dự đoán chính xác
- So sánh với thị trường (Lương TB, Min, Max)

