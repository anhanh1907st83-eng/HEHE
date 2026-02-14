import streamlit as st
import pandas as pd
import time
import random
from datetime import datetime
from streamlit_gsheets import GSheetsConnection
from streamlit.web.server.websocket_headers import _get_websocket_headers

# --- CẤU HÌNH ---
st.set_page_config(page_title="Lắc Lì Xì - Tết 2026", page_icon="🧧", layout="centered")

REWARDS = [
    "🧧 Giftcode: VIP-TET-2026", 
    "🍀 Lời chúc: Tấn Tài Tấn Lộc",
    "💰 Lì xì: 50.000 VNĐ", 
    "👘 Áo Dài Tết (7 ngày)",
    "🌸 Cành Đào Tiên", 
    "✨ Chúc bạn may mắn lần sau!"
]

# --- HÀM LẤY IP ---
def get_remote_ip():
    try:
        headers = _get_websocket_headers()
        if headers:
            x_forwarded = headers.get("X-Forwarded-For")
            if x_forwarded:
                return x_forwarded.split(",")[0].strip()
            return headers.get("Remote-Addr")
    except Exception:
        pass
    return "unknown_ip"

# --- HÀM XỬ LÝ GOOGLE SHEETS ---
def get_data():
    # Tạo kết nối
    conn = st.connection("gsheets", type=GSheetsConnection)
    # Đọc dữ liệu, ttl=0 nghĩa là không cache, luôn lấy mới nhất
    try:
        df = conn.read(worksheet="Logs", ttl=0)
        return df
    except Exception:
        # Nếu sheet trắng chưa có header, tạo dataframe rỗng
        return pd.DataFrame(columns=["ip_address", "reward", "time"])

def check_ip_played(ip, df):
    # Kiểm tra xem IP đã tồn tại trong cột ip_address chưa
    if ip in df['ip_address'].values:
        user_row = df[df['ip_address'] == ip].iloc[0]
        return user_row['reward'], user_row['time']
    return None

def save_play_history(ip, reward):
    conn = st.connection("gsheets", type=GSheetsConnection)
    try:
        # 1. Lấy dữ liệu hiện tại
        df = conn.read(worksheet="Logs", ttl=0)
        
        # 2. Tạo dòng mới
        new_row = pd.DataFrame([{
            "ip_address": ip,
            "reward": reward,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }])
        
        # 3. Gộp và Ghi đè lại vào Sheet
        # Lưu ý: Với lượng truy cập lớn cùng lúc, cách này có thể bị race condition nhẹ
        # nhưng với quy mô nhỏ thì ổn.
        updated_df = pd.concat([df, new_row], ignore_index=True)
        conn.update(worksheet="Logs", data=updated_df)
        return True
    except Exception as e:
        st.error(f"Lỗi lưu dữ liệu: {e}")
        return False

# --- CSS GIAO DIỆN ---
st.markdown("""
    <style>
    .stApp {
        background-color: #8B0000;
        background-image: linear-gradient(180deg, #8B0000 0%, #B22222 100%);
        color: #FFD700;
    }
    h1, h2, h3 { color: #FFD700 !important; text-align: center; }
    .stButton>button {
        display: block; margin: 0 auto; background-color: #FFD700; color: #8B0000;
        font-size: 24px; font-weight: bold; border-radius: 50px; padding: 15px 30px;
        border: 2px solid #FF4500;
    }
    .status-box {
        background-color: rgba(0,0,0,0.6); padding: 15px; border-radius: 10px;
        text-align: center; border: 1px solid #FFD700; margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- LOGIC CHÍNH ---
st.title("🐯 LẮC LÌ XÌ ONLINE 🐯")

user_ip = get_remote_ip()

# Load dữ liệu từ Google Sheet
with st.spinner("Đang tải dữ liệu..."):
    df_history = get_data()

# Kiểm tra lịch sử
history = check_ip_played(user_ip, df_history)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMjR4Zmx4Zmx4Zmx4Zmx4Zmx4Zmx4Zmx4Zmx4Zmx4ZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/LpDmM2wSt6kCM/giphy.gif", width=300)

st.write("")

if history:
    # --- ĐÃ CHƠI ---
    reward_received, time_played = history
    st.warning("⛔ THIẾT BỊ NÀY ĐÃ NHẬN QUÀ!")
    st.markdown(f"""
        <div class="status-box">
            <h3>Phần quà của bạn:</h3>
            <h2 style="color: #00FF00;">{reward_received}</h2>
            <p style="color: #DDD; font-size: 12px;">Đã nhận: {time_played}</p>
        </div>
    """, unsafe_allow_html=True)

else:
    # --- CHƯA CHƠI ---
    if st.button("🧧 LẮC NGAY 🧧"):
        if user_ip == "unknown_ip":
            st.error("Vui lòng tắt VPN/Proxy để tham gia.")
        else:
            with st.spinner('Đang kết nối thần tài...'):
                time.sleep(2) # Hiệu ứng hồi hộp
                
                final_reward = random.choice(REWARDS)
                
                # Lưu vào Google Sheet
                if save_play_history(user_ip, final_reward):
                    st.balloons()
                    st.success("Chúc mừng!")
                    st.markdown(f"""
                        <div class="status-box">
                            <h2 style="color: #FFD700;">{final_reward}</h2>
                        </div>
                    """, unsafe_allow_html=True)
                    time.sleep(2)
                    st.rerun()
