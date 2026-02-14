import streamlit as st
import random
import time
import sqlite3
import socket
from datetime import datetime
from streamlit.web.server.websocket_headers import _get_websocket_headers

# --- CẤU HÌNH DATABASE (SQLite) ---
# Lưu ý: Trên Streamlit Cloud miễn phí, file này sẽ bị reset khi App reboot/deploy lại.
# Để chạy sự kiện thật, Tuấn Anh nên đổi sang kết nối Google Sheets hoặc Supabase.
DB_FILE = "lucky_shaker.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS history
                 (ip_address TEXT PRIMARY KEY, 
                  reward TEXT, 
                  time TIMESTAMP)''')
    conn.commit()
    conn.close()

def check_ip_played(ip):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT reward, time FROM history WHERE ip_address = ?", (ip,))
    result = c.fetchone()
    conn.close()
    return result

def save_play_history(ip, reward):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO history (ip_address, reward, time) VALUES (?, ?, ?)", 
                  (ip, reward, datetime.now()))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False # Đã tồn tại
    finally:
        conn.close()

# --- HÀM LẤY IP (Hỗ trợ Streamlit Cloud) ---
def get_remote_ip():
    try:
        headers = _get_websocket_headers()
        if headers:
            # Ưu tiên lấy X-Forwarded-For (dùng cho Proxy/Cloud)
            x_forwarded = headers.get("X-Forwarded-For")
            if x_forwarded:
                return x_forwarded.split(",")[0].strip()
            return headers.get("Remote-Addr")
    except Exception:
        pass
    return "unknown_ip"

# --- KHỞI TẠO APP ---
st.set_page_config(page_title="🐎 TẾT BÍNG NGỌ - LẮC DÌ DỌ 🐎", page_icon="🧧", layout="centered")
init_db()

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
st.title("🐎 TẾT BÍNG NGỌ - LẮC DÌ DỌ 🐎")

# 1. Lấy IP người dùng
user_ip = get_remote_ip()

# Debug: Hiển thị IP (Tắt dòng này khi chạy thật để bảo mật)
# st.caption(f"Debug IP: {user_ip}") 

# 2. Kiểm tra lịch sử
played_data = check_ip_played(user_ip)

REWARDS = [
    "🧧 Phong bao lì xì thật: Ngẫu nhiên",
    "🍀 Lời chúc: Tấn Tài Tấn Lộc",
    "💰 Lì xì +bank: 50.000 VNĐ",
    "💰 Lì xì +bank: 100.000 VNĐ",
    "💰 Lì xì +bank: 10.000 VNĐ",
    "💰 Lì xì +bank: 20.000 VNĐ",
    "💰 Lì xì +bank: 200.000 VNĐ",
    "🌸 Vật phẩm: Linh vật Ngựa trị giá 69k",
    "✨ Chúc bạn may mắn lần sau!"
]

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMjR4Zmx4Zmx4Zmx4Zmx4Zmx4Zmx4Zmx4Zmx4Zmx4ZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/LpDmM2wSt6kCM/giphy.gif", width=300)

st.write("")

# 3. Điều hướng hiển thị
if played_data:
    # --- TRƯỜNG HỢP ĐÃ CHƠI ---
    reward_received, time_played = played_data
    st.warning("⛔ BẠN ĐÃ NHẬN QUÀ RỒI!")
    st.markdown(f"""
        <div class="status-box">
            <h3>Phần quà của bạn:</h3>
            <h2 style="color: #00FF00;">{reward_received}</h2>
            <p style="color: #DDD; font-size: 12px;">Đã nhận lúc: {time_played}</p>
            <p>Chỉ được nhận 1 lần.</p>
        </div>
    """, unsafe_allow_html=True)

else:
    # --- TRƯỜNG HỢP CHƯA CHƠI ---
    if st.button("🧧 LẮC NGAY 🧧"):
        if user_ip == "unknown_ip":
            st.error("Không xác định được danh tính. Vui lòng tắt VPN/Proxy.")
        else:
            with st.spinner('Đang lắc lì xì...'):
                time.sleep(1.5)
                # Random quà
                final_reward = random.choice(REWARDS)
                
                # Lưu vào DB
                saved = save_play_history(user_ip, final_reward)
                
                if saved:
                    st.balloons()
                    st.success("Chúc mừng!")
                    st.markdown(f"""
                        <div class="status-box">
                            <h2 style="color: #FFD700;">{final_reward}</h2>
                        </div>
                    """, unsafe_allow_html=True)
                    time.sleep(1)
                    st.rerun() # Load lại trang để khóa nút
                else:
                    st.error("Có lỗi xảy ra hoặc bạn đã chơi rồi!")
