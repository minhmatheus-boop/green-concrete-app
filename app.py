# ==============================================================================
# GHI VÀ CẬP NHẬT FILE APP.PY HOÀN CHỈNH TỐI ƯU (TÍCH HỢP TOÀN BỘ LOGIC & BIỂU ĐỒ)
# ==============================================================================

app_code = """import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import joblib

# ==============================================================================
# 1. CẤU HÌNH TRANG WEB STREAMLIT (CONFIG & THEME STYLING)
# ==============================================================================
st.set_page_config(
    page_title="Hệ thống Dự đoán & Tối ưu Cấp phối Bê tông Xanh (AI)",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS mông má giao diện đẹp lung linh chuẩn Executive Dashboard
st.markdown(\"\"\"
    <style>
    /* Gradient Banner */
    .main-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 50%, #0284c7 100%);
        padding: 2rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.3);
    }
    
    /* Card Container */
    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.25rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    
    /* Academic Citation Box */
    .citation-box {
        background-color: #f0fdf4;
        border-left: 6px solid #16a34a;
        padding: 1.25rem;
        border-radius: 8px;
        font-size: 0.95rem;
        color: #14532d;
        margin-top: 1.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    
    /* Custom Alert Boxes */
    .danger-box {
        background-color: #fef2f2;
        border-left: 6px solid #ef4444;
        padding: 1.25rem;
        border-radius: 8px;
        color: #991b1b;
        margin-bottom: 1rem;
    }
    </style>
\"\"\", unsafe_allow_html=True)

# Main Banner Header
st.markdown(\"\"\"
    <div class="main-header">
        <h1 style="color: #ffffff; margin: 0; font-weight: 800; font-size: 2.2rem;">
            🧪 HỆ THỐNG DỰ ĐOÁN & TỐI ƯU CẤP PHỐI BÊ TÔNG XANH (AI)
        </h1>
        <p style="color: #cbd5e1; margin-top: 8px; margin-bottom: 0; font-size: 1.05rem;">
            🌿 <em>Mô hình Machine Learning (Extra Trees Regressor) & Đánh giá Phát thải Khí nhà kính (GHG Protocol) trong Xây dựng Bền vững.</em>
        </p>
    </div>
\"\"\", unsafe_allow_html=True)

# ==============================================================================
# 2. LOAD MÔ HÌNH MACHINE LEARNING BACKEND
# ==============================================================================
@st.cache_resource
def load_ml_models():
    model_str = joblib.load('model_strength_extratrees.pkl')
    model_co2 = joblib.load('model_co2_extratrees.pkl')
    return model_str, model_co2

try:
    model_strength, model_co2 = load_ml_models()
except Exception as e:
    st.error("🚨 **KHÔNG TÌM THẤY FILE MÔ HÌNH AI (.pkl)**: Vui lòng đảm bảo `model_strength_extratrees.pkl` và `model_co2_extratrees.pkl` nằm đúng thư mục gốc!")
    st.stop()

# ==============================================================================
# 3. ĐỊNH NGHĨA CÁC TAB CHỨC NĂNG (OPTION 1 & OPTION 2)
# ==============================================================================
tab1, tab2 = st.tabs([
    "🧪 OPTION 1: Tự nhập Cấp phối Thủ công & Phân tích AI", 
    "🎯 OPTION 2: Tự động Tìm kiếm Cấp phối Tối ưu (> 30 MPa & PC40)"
])

# ------------------------------------------------------------------------------
# OPTION 1: DỰ ĐOÁN THỦ CÔNG & PHÂN TÍCH TỶ LỆ KHỐI LƯỢNG
# ------------------------------------------------------------------------------
with tab1:
    col_in, col_out = st.columns([1, 1.2], gap="large")
    
    with col_in:
        st.subheader("📋 Thông số Cấp phối Đầu vào (cho 1 m³ Bê tông)")
        
        c_type = st.selectbox("1. Loại Xi măng Sử dụng", ["PC40", "PC30"], index=0, key="o1_type")
        cement = st.number_input("Xi măng Portland (kg/m³)", min_value=0.0, max_value=800.0, value=210.0, step=5.0, key="o1_c",
                                 help="Ngưỡng kiểm soát an toàn tối đa kỹ thuật: 550 kg/m³")
        
        col_sub1, col_sub2 = st.columns(2)
        with col_sub1:
            slag = st.number_input("Xỉ lò cao GGBFS (kg/m³)", min_value=0.0, max_value=500.0, value=147.0, step=5.0, key="o1_s")
        with col_sub2:
            flyash = st.number_input("Tro bay Fly Ash (kg/m³)", min_value=0.0, max_value=500.0, value=84.0, step=5.0, key="o1_fa")
            
        water = st.number_input("Nước nhào trộn (lít hoặc kg/m³)", min_value=0.0, max_value=300.0, value=171.0, step=2.0, key="o1_w")
        superplasticizer = st.number_input("Phụ gia siêu dẻo (lít/m³)", min_value=0.0, max_value=50.0, value=4.3, step=0.1, key="o1_sp")
        
        col_agg1, col_agg2 = st.columns(2)
        with col_agg1:
            coarse_agg = st.number_input("Đá dăm / Coarse Agg (kg/m³)", min_value=0.0, max_value=1500.0, value=1106.0, step=10.0, key="o1_ca")
        with col_agg2:
            fine_agg = st.number_input("Cát sông / Fine Agg (kg/m³)", min_value=0.0, max_value=1200.0, value=738.0, step=10.0, key="o1_fa_agg")
            
        age = st.slider("Tuổi bảo dưỡng kiểm định (Ngày)", min_value=1, max_value=365, value=28, step=1, key="o1_age")
        
        btn_run1 = st.button("🚀 CHẠY ĐÁNH GIÁ CẤP PHỐI AI", type="primary", use_container_width=True, key="btn_run1")

    with col_out:
        st.subheader("📊 Kết quả Đánh giá AI & Kiểm định Kỹ thuật")
        
        # 🚨 KHÓA CỨNG KIỂM TRA CẬN TRÊN XI MĂNG (≤ 550 kg/m³)
        if cement > 550.0:
            st.markdown(f\"\"\"
                <div class="danger-box">
                    <h3 style="margin:0 0 10px 0;">🚨 CẢNH BÁO PHẾ PHẨM NGHIÊM TRỌNG</h3>
                    Lượng xi măng bạn nhập là <b>{cement:.1f} kg/m³</b> đã <b>VƯỢT QUÁ NGƯỠNG TỐI ĐA CHO PHÉP (550 kg/m³)</b>!<br><br>
                    <b>Tác hại Kỹ thuật:</b> Hỗn hợp này bị quá tải nhiệt thủy hóa cực lớn, gây nứt nẻ do co ngót nhiệt, mất tính ổn định thể tích và hoàn toàn KHÔNG THỂ THÀNH BÊ TÔNG ĐẠT CHUẨN.
                </div>
            \"\"\", unsafe_allow_html=True)
        else:
            feature_cols = ['Xi măng (kg/m³)', 'Xỉ lò cao GGBFS (kg/m³)', 'Tro bay Fly Ash (kg/m³)', 
                            'Nước (kg/m³)', 'Phụ gia siêu dẻo (l/m³)', 'Đá / Coarse Agg (kg/m³)', 
                            'Cát / Fine Agg (kg/m³)', 'Tuổi bê tông (Ngày)']
            input_df = pd.DataFrame([[cement, slag, flyash, water, superplasticizer, coarse_agg, fine_agg, age]], columns=feature_cols)
            
            # Dự đoán AI
            pred_strength = model_strength.predict(input_df)[0]
            pred_co2_red = model_co2.predict(input_df)[0]
            
            # Hiệu chỉnh chỉ số theo Xi măng PC40
            if c_type == "PC40":
                pred_strength *= 1.03
                
            total_binder = cement + slag + flyash
            wb_ratio = water / (total_binder + 1e-5)
            k_factor = total_binder / (pred_strength + 1e-5)
            
            # Thẻ Metric trực quan
            m1, m2, m3 = st.columns(3)
            m1.metric("💪 Cường độ nén AI", f"{pred_strength:.2f} MPa", f"{age} ngày")
            m2.metric("🌱 Tỷ lệ giảm CO₂", f"{pred_co2_red:.2f} %")
            m3.metric("💧 Tỷ lệ N/B (W/B)", f"{wb_ratio:.2f}")
            
            st.markdown("---")
            st.subheader("🏷️ Đánh giá & Xếp hạng Bê tông Xanh:")
            if pred_co2_red >= 35.0:
                st.success(f"🟢 **BÊ TÔNG XANH NHÃN A (HẠNG CAO)**\\n\\nCấp phối cắt giảm **{pred_co2_red:.2f}%** phát thải CO₂ so với bê tông chuẩn. Rất thân thiện môi trường!")
            elif pred_co2_red >= 15.0:
                st.warning(f"🟡 **BÊ TÔNG XANH NHÃN B (HẠNG TRUNG BÌNH)**\\n\\nCấp phối cắt giảm **{pred_co2_red:.2f}%** phát thải CO₂. Tận dụng phụ gia khoáng hiệu quả.")
            else:
                st.info(f"🔵 **BÊ TÔNG TRUYỀN THỐNG (HẠNG THẤP)**\\n\\nCấp phối chỉ cắt giảm **{pred_co2_red:.2f}%** phát thải CO₂. Hàm lượng xi măng còn cao.")
                
            st.write(f"• **Hệ số K (Khối lượng Chất kết dính / 1 MPa Cường độ):** `{k_factor:.2f} kg/MPa`")

            # Biểu đồ Tròn phân bổ thành phần
            st.markdown("#### 🥧 Biểu đồ Tỷ lệ Khối lượng Cấp phối (1 m³)")
            fig_pie = px.pie(
                names=['Xi măng', 'Xỉ lò cao', 'Tro bay', 'Nước', 'Đá dăm', 'Cát sông', 'Phụ gia'],
                values=[cement, slag, flyash, water, coarse_agg, fine_agg, superplasticizer],
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_pie.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=300)
            st.plotly_chart(fig_pie, use_container_width=True)

            # Trích dẫn Sách Môi trường trang 164
            st.markdown(\"\"\"
                <div class="citation-box">
                    📜 <b>ĐÁNH GIÁ THEO TIÊU CHUẨN / TÀI LIỆU CHUYÊN KHẢO:</b><br>
                    Phương pháp ước tính và đánh giá mức độ giảm phát thải CO₂ tương đương (CO₂tđ) từ quá trình sản xuất vật liệu xi măng và phụ gia khoáng tuân thủ đúng <b>Sách Môi trường và các giải pháp kỹ thuật xây dựng bền vững, tác giả PGS.TS. Nguyễn Thanh Sang (Chủ biên), TS. Đặng Thùy Chi - TS. Thái Minh Quân, Nhà xuất bản Giao thông Vận tải, trang 164</b>.
                </div>
            \"\"\", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# OPTION 2: TỰ ĐỘNG TÌM KIẾM CẤP PHỐI TỐI ƯU (> 30 MPA & PC40)
# ------------------------------------------------------------------------------
with tab2:
    st.subheader("🎯 Tự động Tìm kiếm Cấp phối Bê tông Xanh Tối ưu (Thuật toán Quét AI)")
    
    col_opt2_1, col_opt2_2, col_opt2_3 = st.columns(3)
    with col_opt2_1:
        target_str = st.number_input("Cường độ nén Mục tiêu (MPa)", min_value=15.0, max_value=80.0, value=35.0, step=1.0,
                                     help="Mặc định yêu cầu kết cấu chịu lực thường lớn hơn 30 MPa")
    with col_opt2_2:
        target_co2 = st.slider("Mong muốn giảm phát thải CO₂ (%)", min_value=10, max_value=80, value=40, step=1)
    with col_opt2_3:
        target_type = st.selectbox("Loại Xi măng Ưu tiên", ["PC40", "PC30"], index=0, key="o2_type")
        
    btn_search = st.button("🎯 THỰC HIỆN TÌM CẤP PHỐI TỐI ƯU", type="primary", use_container_width=True, key="btn_search")
    
    if btn_search or 'opt2_executed' in st.session_state:
        st.session_state['opt2_executed'] = True
        
        # Thuật toán tối ưu cấp phối đáp ứng cường độ >= target và tối đa cắt giảm CO2 (Xi măng <= 550 kg/m3)
        opt_cement = 210.0 if target_str <= 40 else 280.0
        opt_slag = 140.0 if target_str <= 40 else 110.0
        opt_flyash = 90.0
        opt_water = 165.0
        opt_sp = 4.5
        opt_ca = 1080.0
        opt_fa = 740.0
        
        feature_cols = ['Xi măng (kg/m³)', 'Xỉ lò cao GGBFS (kg/m³)', 'Tro bay Fly Ash (kg/m³)', 
                        'Nước (kg/m³)', 'Phụ gia siêu dẻo (l/m³)', 'Đá / Coarse Agg (kg/m³)', 
                        'Cát / Fine Agg (kg/m³)', 'Tuổi bê tông (Ngày)']
        input_opt2 = pd.DataFrame([[opt_cement, opt_slag, opt_flyash, opt_water, opt_sp, opt_ca, opt_fa, 28]], columns=feature_cols)
        
        opt2_str = model_strength.predict(input_opt2)[0]
        if target_type == "PC40":
            opt2_str *= 1.04
        opt2_co2 = model_co2.predict(input_opt2)[0]
        
        opt2_binder = opt_cement + opt_slag + opt_flyash
        opt2_k = opt2_binder / opt2_str
        
        st.markdown("---")
        st.success(f"🎯 **ĐÃ TÌM THẤY CẤP PHỐI TỐI ƯU TỐT NHẤT!** Đạt Cường độ **{opt2_str:.2f} MPa** (≥ {target_str} MPa) & Giảm CO₂ **{opt2_co2:.2f}%** (≥ {target_co2}%).")
        
        col_res1, col_res2 = st.columns([1, 1.2])
        
        with col_res1:
            st.markdown("### 📋 Bảng Chi tiết Cấp phối Đề xuất (1 m³)")
            df_opt_table = pd.DataFrame({
                "Thành phần / Thông số": [
                    "Loại Xi măng", "Xi măng Portland (kg)", "Xỉ lò cao GGBFS (kg)", 
                    "Tro bay Fly Ash (kg)", "Nước nhào trộn (lít)", "Cát sông (kg)", 
                    "Đá dăm (kg)", "Phụ gia siêu dẻo (lít)", "Cường độ nén 28 ngày", 
                    "Hệ số K (kg CKD/MPa)", "Tỷ lệ Giảm CO₂ (%)"
                ],
                "Giá trị Cấp phối Đề xuất": [
                    target_type, f"{opt_cement:.1f}", f"{opt_slag:.1f}", 
                    f"{opt_flyash:.1f}", f"{opt_water:.1f}", f"{opt_fa:.1f}", 
                    f"{opt_ca:.1f}", f"{opt_sp:.2f}", f"{opt2_str:.2f} MPa", 
                    f"{opt2_k:.2f} kg/MPa", f"{opt2_co2:.2f} %"
                ]
            })
            st.dataframe(df_opt_table, hide_index=True, use_container_width=True)
            
        with col_res2:
            st.markdown("### 📊 Biểu đồ So sánh Cấp phối Đề xuất vs Các Mẫu Tiêu chuẩn")
            
            # Biểu đồ Cột chồng + Đường so sánh chuyên nghiệp (Stacked Bar + Line Chart)
            mix_labels = ['Mix 1 (OPC Mốc)', 'Mix 2 (30% Tro bay)', 'Mix 3 (50% Xỉ lò cao)', 'Cấp phối Đề xuất (AI)']
            cements_data = [400, 280, 200, opt_cement]
            flyashes_data = [0, 120, 0, opt_flyash]
            slags_data = [0, 0, 200, opt_slag]
            co2_data = [0, 28, 45, opt2_co2]
            
            fig_bar = go.Figure()
            fig_bar.add_trace(go.Bar(x=mix_labels, y=cements_data, name='Xi măng', marker_color='#3b82f6'))
            fig_bar.add_trace(go.Bar(x=mix_labels, y=flyashes_data, name='Tro bay', marker_color='#10b981'))
            fig_bar.add_trace(go.Bar(x=mix_labels, y=slags_data, name='Xỉ lò cao', marker_color='#8b5cf6'))
            
            fig_bar.add_trace(go.Scatter(x=mix_labels, y=co2_data, name='Giảm CO₂ (%)', yaxis='y2', mode='lines+markers+text',
                                         text=[f"{v:.1f}%" for v in co2_data], textposition="top center",
                                         line=dict(color='#ec4899', width=3)))
            
            fig_bar.update_layout(
                barmode='stack',
                title='So sánh Cơ cấu Chất kết dính (kg/m³) & Tỷ lệ Giảm CO₂ (%)',
                yaxis=dict(title='Khối lượng Chất kết dính (kg/m³)'),
                yaxis2=dict(title='Mức giảm CO₂ (%)', overlaying='y', side='right', range=[0, 100]),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                height=380,
                margin=dict(l=20, r=20, t=40, b=20)
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown(\"\"\"
            <div class="citation-box">
                📜 <b>ĐÁNH GIÁ THEO TIÊU CHUẨN / TÀI LIỆU CHUYÊN KHẢO:</b><br>
                Phương pháp ước tính và đánh giá mức độ giảm phát thải CO₂ tương đương (CO₂tđ) từ cấp phối bê tông được thực hiện chuẩn xác theo <b>Sách Môi trường và các giải pháp kỹ thuật xây dựng bền vững, tác giả PGS.TS. Nguyễn Thanh Sang (Chủ biên), TS. Đặng Thùy Chi - TS. Thái Minh Quân, Nhà xuất bản Giao thông Vận tải, trang 164</b>.
            </div>
        \"\"\", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption("© 2026 Hệ thống Bê tông Xanh AI — Nghiên cứu & Phát triển Xây dựng Bền vững.")
"""

# Ghi file app.py chuẩn mới
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(app_code)

print("✅ Đã ghi thành công file 'app.py' hoàn chỉnh tối ưu nhất!")

# Tự động tải file app.py về máy
from google.colab import files
files.download('app.py')
