import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import random
import time

# --- 1. CẤU HÌNH TRANG & CSS DARK MODE ---
st.set_page_config(
    page_title="Truth or Dare - Ultimate Party",
    page_icon="🔥",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS TÙY CHỈNH (MAGIC UI) ---
st.markdown("""
<style>
    /* Tổng quan */
    .stApp {
        background-color: #0E1117;
        color: white;
    }
    
    /* Card Container */
    .game-card {
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        animation: fadeIn 0.5s;
        margin-bottom: 20px;
        color: white;
    }
    
    /* Truth Card Style */
    .card-truth {
        background: linear-gradient(135deg, #00C6FF 0%, #0072FF 100%);
        border: 2px solid #89f7fe;
    }
    
    /* Dare Card Style */
    .card-dare {
        background: linear-gradient(135deg, #FF416C 0%, #FF4B2B 100%);
        border: 2px solid #ff9a9e;
    }
    
    /* Text Styles */
    .card-type {
        font-size: 1.5rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 10px;
        opacity: 0.8;
    }
    .card-content {
        font-size: 2rem;
        font-weight: bold;
        line-height: 1.4;
    }
    
    /* Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Custom Button */
    .stButton > button {
        border-radius: 50px;
        font-weight: bold;
        height: 50px;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        transform: scale(1.05);
    }
</style>
""", unsafe_allow_html=True)

# --- 2. QUẢN LÝ STATE ---
if 'drawn_indices' not in st.session_state:
    st.session_state.drawn_indices = []
if 'current_card' not in st.session_state:
    st.session_state.current_card = None
if 'is_authenticated' not in st.session_state:
    st.session_state.is_authenticated = False

# --- 3. DỮ LIỆU (KÈM DATA MẪU NẾU KHÔNG CÓ GSHEETS) ---
def get_data():
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(ttl="1m")
        df.columns = [str(c).strip().lower() for c in df.columns]
        # Validate columns
        if 'content' not in df.columns or 'type' not in df.columns:
            raise ValueError("Cấu trúc bảng không đúng")
        return df
    except Exception:
        # Dữ liệu giả lập để test ngay lập tức mà không cần kết nối DB
        mock_data = {
            'content': [
                "Kể về mối tình đầu của bạn?", "Gọi điện cho người yêu cũ nói nhớ họ.", 
                "Ai là người bạn ghét nhất ở đây?", "Hít đất 10 cái ngay lập tức.",
                "Khai thật số dư tài khoản ngân hàng.", "Uống hết ly nước trong 1 hơi."
            ],
            'type': ['Truth', 'Dare', 'Truth', 'Dare', 'Truth', 'Dare']
        }
        return pd.DataFrame(mock_data)

df = get_data()

# --- 4. LOGIC GAME ---
def reset_game():
    st.session_state.drawn_indices = []
    st.session_state.current_card = None
    st.rerun()

def pick_card():
    # Lấy danh sách index chưa bốc
    available = [i for i in df.index if i not in st.session_state.drawn_indices]
    
    if available:
        idx = random.choice(available)
        row = df.loc[idx]
        
        # Cập nhật state
        st.session_state.drawn_indices.append(idx)
        st.session_state.current_card = row
        
        # Hiệu ứng ngẫu nhiên
        eff = random.choice(["balloons", "snow"])
        if eff == "balloons": st.balloons()
        else: st.snow()
        
        return True # Thành công
    else:
        return False # Hết bài

# --- 5. POPUP HIỂN THỊ (DIALOG) ---
@st.dialog("🔥 LÁ BÀI ĐỊNH MỆNH 🔥")
def show_card_dialog():
    card = st.session_state.current_card
    
    if card is not None:
        c_type = str(card['type']).capitalize()
        c_content = card['content']
        
        # Xác định Style dựa trên loại thẻ
        is_truth = c_type.lower() in ['truth', 'sự thật']
        css_class = "card-truth" if is_truth else "card-dare"
        icon = "🟦" if is_truth else "🟥"
        
        # Render HTML Card
        st.markdown(f"""
        <div class="game-card {css_class}">
            <div class="card-type">{icon} {c_type}</div>
            <div class="card-content">{c_content}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("") # Spacer
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("❌ Đóng", use_container_width=True):
                st.rerun()
        with col2:
            # Kiểm tra xem còn bài không để hiện nút "Tiếp tục"
            remain = len(df) - len(st.session_state.drawn_indices)
            if remain > 0:
                if st.button("🎲 Bốc tiếp", type="primary", use_container_width=True):
                    pick_card()
                    st.rerun()
            else:
                st.button("Hết bài", disabled=True, use_container_width=True)

# --- 6. GIAO DIỆN CHÍNH ---

# Header Section
st.markdown("<h1 style='text-align: center; color: #FF4B2B;'>🎲 TRUTH OR DARE</h1>", unsafe_allow_html=True)

# --- MÀN HÌNH ĐĂNG NHẬP (BẢO MẬT NHẸ) ---
if not st.session_state.is_authenticated:
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.info("🔒 Phòng chơi riêng tư")
        pwd = st.text_input("Nhập mật khẩu phòng:", type="password")
        if st.button("Vào chơi", use_container_width=True, type="primary"):
            if pwd
