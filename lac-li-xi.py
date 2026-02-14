import streamlit as st
import random
import time

# --- Cấu hình trang ---
st.set_page_config(
    page_title="Lắc Lì Xì Nghịch Thủy Hàn",
    page_icon="🧧",
    layout="centered"
)

# --- Danh sách phần thưởng (Giả lập database) ---
REWARDS = [
    "🧧 Giftcode: VIP-TET-2025",
    "🍀 Lời chúc: Tấn Tài Tấn Lộc",
    "💰 Lì xì: 50.000 VNĐ",
    "👘 Trang phục: Áo Dài Tết (7 ngày)",
    "🌸 Vật phẩm: Cành Đào Tiên",
    "✨ Chúc bạn may mắn lần sau!"
]

# --- CSS tùy chỉnh giao diện (Theme Tết) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #8B0000;
        background-image: linear-gradient(180deg, #8B0000 0%, #B22222 100%);
        color: #FFD700;
    }
    h1 {
        color: #FFD700 !important;
        text-align: center;
        font-family: 'Arial', sans-serif;
        text-shadow: 2px 2px 4px #000000;
    }
    .stButton>button {
        display: block;
        margin: 0 auto;
        background-color: #FFD700;
        color: #8B0000;
        font-size: 24px;
        font-weight: bold;
        border-radius: 50px;
        padding: 15px 30px;
        border: 2px solid #FF4500;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.3);
        transition: transform 0.1s;
    }
    .stButton>button:active {
        transform: scale(0.95);
        background-color: #FFC125;
    }
    .reward-box {
        background-color: rgba(0, 0, 0, 0.5);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-top: 20px;
        border: 2px solid #FFD700;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Header ---
st.title("🐯 LẮC LÌ XÌ - NGHỊCH THỦY HÀN 🐯")
st.markdown("<p style='text-align: center; color: #FFF;'>Chào mừng Đại Hiệp! Hãy lắc quẻ cầu may đầu năm.</p>", unsafe_allow_html=True)

# --- Hình ảnh minh họa (Placeholder) ---
# Bạn có thể thay link này bằng hình ảnh cái cây hoặc bao lì xì
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMjR4Zmx4Zmx4Zmx4Zmx4Zmx4Zmx4Zmx4Zmx4Zmx4ZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/LpDmM2wSt6kCM/giphy.gif", width=300)

# --- Logic Lắc Lì Xì ---
# Sử dụng session_state để lưu trạng thái đã lắc hay chưa
if 'shaken' not in st.session_state:
    st.session_state.shaken = False
if 'reward' not in st.session_state:
    st.session_state.reward = ""

# Khoảng trống để căn giữa nút
st.write("")
st.write("")

# Nút Lắc
col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
with col_btn2:
    if st.button("🧧 LẮC NGAY 🧧"):
        with st.spinner('Đang lắc...'):
            time.sleep(1.5) # Giả lập thời gian lắc
            st.session_state.reward = random.choice(REWARDS)
            st.session_state.shaken = True

# Hiển thị kết quả
if st.session_state.shaken:
    st.balloons() # Hiệu ứng bóng bay/pháo hoa
    st.markdown(f"""
        <div class="reward-box">
            <h2 style="color: #FFD700;">CHÚC MỪNG!</h2>
            <h3 style="color: #FFF;">{st.session_state.reward}</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Nút Reset
    if st.button("Lắc tiếp"):
        st.session_state.shaken = False
        st.rerun()

# --- Footer ---
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 12px; color: #EEE;'>© 2026 Clone Event by Tuấn Anh</p>", unsafe_allow_html=True)
