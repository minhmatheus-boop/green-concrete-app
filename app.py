import streamlit as st
import pandas as pd
import joblib

# 1. Cấu hình trang Web
st.set_page_config(
    page_title="Hệ thống Bê tông Xanh AI",
    page_icon="🌿",
    layout="wide"
)

# 2. Load các mô hình AI đã lưu
@st.cache_resource
def load_models():
    model_str = joblib.load('model_strength_extratrees.pkl')
    model_co2 = joblib.load('model_co2_extratrees.pkl')
    return model_str, model_co2

try:
    model_strength, model_co2 = load_models()
except Exception as e:
    st.error("⚠️ Không tìm thấy file mô hình '.pkl'. Vui lòng đảm bảo 'model_strength_extratrees.pkl' và 'model_co2_extratrees.pkl' nằm cùng thư mục!")

# Giao diện chính
st.title("🌿 HỆ THỐNG DỰ ĐOÁN & ĐÁNH GIÁ CẤP PHỐI BÊ TÔNG XANH (AI)")
st.markdown("---")

# Chia 2 cột: Cột trái nhập liệu - Cột phải hiển thị kết quả
col_input, col_result = st.columns([1, 1])

with col_input:
    st.subheader("📋 Nhập thông số Cấp phối Bê tông (kg/m³)")

    cement = st.number_input("Xi măng (kg/m³)", min_value=0.0, max_value=800.0, value=210.0, step=5.0)
    slag = st.number_input("Xỉ lò cao GGBFS (kg/m³)", min_value=0.0, max_value=500.0, value=147.0, step=5.0)
    flyash = st.number_input("Tro bay Fly Ash (kg/m³)", min_value=0.0, max_value=500.0, value=84.0, step=5.0)
    water = st.number_input("Nước (kg/m³)", min_value=0.0, max_value=300.0, value=171.0, step=2.0)
    superplasticizer = st.number_input("Phụ gia siêu dẻo (l/m³)", min_value=0.0, max_value=50.0, value=4.3, step=0.1)
    coarse_agg = st.number_input("Đá dăm / Coarse Agg (kg/m³)", min_value=0.0, max_value=1500.0, value=1106.0, step=10.0)
    fine_agg = st.number_input("Cát sông / Fine Agg (kg/m³)", min_value=0.0, max_value=1200.0, value=738.0, step=10.0)
    age = st.number_input("Tuổi bảo dưỡng bê tông (Ngày)", min_value=1, max_value=365, value=28, step=1)

    btn_predict = st.button("🚀 CHẠY DỰ ĐOÁN AI", use_container_width=True)

with col_result:
    st.subheader("📊 Kết quả Dự đoán & Đánh giá Bê tông Xanh")

    if btn_predict:
        feature_columns = ['Xi măng (kg/m³)', 'Xỉ lò cao GGBFS (kg/m³)', 'Tro bay Fly Ash (kg/m³)',
                           'Nước (kg/m³)', 'Phụ gia siêu dẻo (l/m³)', 'Đá / Coarse Agg (kg/m³)',
                           'Cát / Fine Agg (kg/m³)', 'Tuổi bê tông (Ngày)']

        input_data = pd.DataFrame([[cement, slag, flyash, water, superplasticizer, coarse_agg, fine_agg, age]],
                                  columns=feature_columns)

        # Chạy AI dự đoán
        pred_strength = model_strength.predict(input_data)[0]
        pred_co2_red = model_co2.predict(input_data)[0]

        # Tính chỉ số W/B
        total_binder = cement + slag + flyash
        wb_ratio = water / (total_binder + 1e-5)

        st.metric("💪 Cường độ nén dự đoán (28 ngày/tuổi nhập)", f"{pred_strength:.2f} MPa")
        st.metric("🌱 Tỷ lệ cắt giảm phát thải CO₂", f"{pred_co2_red:.2f} %")
        st.metric("💧 Tỷ lệ Nước / Chất kết dính (W/B Ratio)", f"{wb_ratio:.2f}")

        st.markdown("---")
        st.subheader("🏷️ Đánh giá & Xếp hạng Bê tông Xanh:")
        if pred_co2_red >= 35:
            st.success("🟢 **BÊ TÔNG XANH NHÃN A (HẠNG CAO)**\n\nCấp phối giảm hơn 35% phát thải CO₂ so với bê tông chuẩn. Rất thân thiện với môi trường!")
        elif pred_co2_red >= 15:
            st.warning("🟡 **BÊ TÔNG XANH NHÃN B (HẠNG TRUNG BÌNH)**\n\nCấp phối giảm từ 15% - 35% phát thải CO₂. Tận dụng phụ gia khoáng tốt.")
        else:
            st.error("🔴 **BÊ TÔNG TRUYỀN THỐNG (HẠNG THẤP)**\n\nCấp phối ít sử dụng phụ gia khoáng tái chế, hàm lượng xi măng còn cao.")
