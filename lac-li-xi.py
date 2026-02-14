import streamlit as st
import pandas as pd
import time
import random
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# --- CẤU HÌNH ---
st.set_page_config(page_title="Lắc Lì Xì - Tết 2026", page_icon="🧧", layout="centered")

# Danh sách quà tặng
REWARDS = [
    "🧧 Giftcode: VIP-TET-2026", 
    "🍀 Lời chúc: Tấn Tài Tấn Lộc",
    "💰 Lì xì: 50.000 VNĐ", 
    "👘 Áo Dài Tết (7 ngày)",
    "🌸 Cành Đào Tiên", 
    "✨ Chúc bạn may mắn lần sau!"
]

# --- HÀM LẤY IP (CHUẨN MỚI) ---
def get_remote_ip():
    try:
        # Sử dụng st.context.headers thay vì _get_websocket_headers
        if st.context.headers:
            # Lấy X-Forwarded-For nếu chạy trên Cloud/Proxy
            x_forwarded = st.context.headers.get("X-Forwarded-For")
            if x_forwarded:
                return x_forwarded.split(",")[0].strip()
            return st.context.headers.get("Remote-Addr")
    except Exception:
        pass
    return "unknown_ip"

# --- HÀM XỬ LÝ GOOGLE SHEETS ---
def get_data():
    conn = st.connection("gsheets", type=GSheetsConnection)
    try:
        df = conn.read(worksheet="Logs", ttl=0)
        if 'name' not in df.columns:
            df['name'] = ""
        return df
    except Exception:
        return pd.DataFrame(columns=["ip_address", "name", "reward", "time"])

def check_ip_played(ip, df):
    if ip in df['ip_address'].values:
        user_row = df[df['ip_address'] == ip].iloc[0]
        return user_row.get('name', 'Bạn'), user_row['reward'], user_row['time']
    return None

def save_play_history(ip, name, reward):
    conn = st.connection("gsheets", type=GSheetsConnection)
    try:
        df = conn.read(worksheet="Logs", ttl=0)
        new_row = pd.DataFrame([{
            "ip_address": ip,
            "name": name,
            "reward": reward,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }])
        updated_df = pd.concat([df, new_row], ignore_index=True)
        conn.update(worksheet="Logs", data=updated_df)
        return True
    except Exception as e:
        st.error(f"Lỗi hệ thống: {e}")
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
    .stTextInput > div > div > input {
        text-align: center; font-size: 18px; color: #8B0000;
        background-color: #FFF8DC; border: 2px solid #FFD700; border-radius: 10px;
    }
    .stButton>button {
        display: block; margin: 0 auto; background-color: #FFD700; color: #8B0000;
        font-size: 24px; font-weight: bold; border-radius: 50px; padding: 15px 30px;
        border: 2px solid #FF4500;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.4);
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

# Load dữ liệu
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
    user_name_old, reward_received, time_played = history
    st.warning(f"⛔ {str(user_name_old).upper()} ĐÃ NHẬN QUÀ RỒI!")
    st.markdown(f"""
        <div class="status-box">
            <h3>Phần quà của bạn:</h3>
            <h2 style="color: #00FF00;">{reward_received}</h2>
            <p style="color: #DDD; font-size: 12px;">Thời gian: {time_played}</p>
        </div>
    """, unsafe_allow_html=True)

else:
    # --- CHƯA CHƠI ---
    name_input = st.text_input("Nhập tên của bạn để nhận lộc:", placeholder="Ví dụ: Tuấn Anh", max_chars=30)
    st.write("")

    if st.button("🧧 LẮC NGAY 🧧"):
        if not name_input.strip():
            st.error("⚠️ Vui lòng nhập tên trước khi lắc!")
        elif user_ip == "unknown_ip":
            st.error("⚠️ Vui lòng tắt VPN/Proxy để tham gia.")
        else:
            with st.spinner(f'{name_input} đang lắc quẻ...'):
                time.sleep(2) 
                final_reward = random.choice(REWARDS)
                
                if save_play_history(user_ip, name_input, final_reward):
                    st.balloons()
                    st.success(f"Chúc mừng {name_input}!")
                    st.markdown(f"""
                        <div class="status-box">
                            <h2 style="color: #FFD700;">{final_reward}</h2>
                        </div>
                    """, unsafe_allow_html=True)
                    time.sleep(2)
                    st.rerun()
