import streamlit as st
import pandas as pd
import time
import random
import uuid
import extra_streamlit_components as stx
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

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

# --- QUẢN LÝ COOKIE (ĐỊNH DANH TRÌNH DUYỆT) ---
def get_manager():
    return stx.CookieManager()

cookie_manager = get_manager()

# --- HÀM LẤY IP ---
def get_remote_ip():
    try:
        if st.context.headers:
            x_forwarded = st.context.headers.get("X-Forwarded-For")
            if x_forwarded:
                # Lấy IP đầu tiên trong chuỗi (thường là IP thật)
                return x_forwarded.split(",")[0].strip()
            return st.context.headers.get("Remote-Addr")
    except Exception:
        pass
    return "unknown_ip"

# --- HÀM DATABASE ---
def get_data():
    conn = st.connection("gsheets", type=GSheetsConnection)
    try:
        df = conn.read(worksheet="Logs", ttl=0)
        # Đảm bảo đủ cột
        expected_cols = ["ip_address", "user_uuid", "name", "reward", "time"]
        for col in expected_cols:
            if col not in df.columns:
                df[col] = ""
        return df
    except Exception:
        return pd.DataFrame(columns=["ip_address", "user_uuid", "name", "reward", "time"])

def check_user_played(ip, user_uuid, df):
    # Logic kiểm tra kép:
    # 1. Trùng IP
    # 2. HOẶC Trùng UUID (Cookie)
    # -> Nếu dính 1 trong 2 là chặn ngay
    
    # Chuyển đổi sang string để so sánh chính xác
    df['ip_address'] = df['ip_address'].astype(str)
    df['user_uuid'] = df['user_uuid'].astype(str)
    
    mask = (df['ip_address'] == str(ip)) | (df['user_uuid'] == str(user_uuid))
    user_rows = df[mask]
    
    if not user_rows.empty:
        row = user_rows.iloc[0]
        return row.get('name', 'Bạn'), row['reward'], row['time']
    return None

def save_play_history(ip, user_uuid, name, reward):
    conn = st.connection("gsheets", type=GSheetsConnection)
    try:
        df = conn.read(worksheet="Logs", ttl=0)
        new_row = pd.DataFrame([{
            "ip_address": str(ip),
            "user_uuid": str(user_uuid),
            "name": name,
            "reward": reward,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }])
        updated_df = pd.concat([df, new_row], ignore_index=True)
        conn.update(worksheet="Logs", data=updated_df)
        return True
    except Exception as e:
        st.error(f"Lỗi: {e}")
        return False

# --- CSS ---
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
        background-color: #FFF8DC; border: 2px solid #FFD700;
    }
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

# 1. Lấy Cookies (UUID)
# Streamlit Cookie Manager cần thời gian để load, nếu chưa có thì tạo mới
user_uuid = cookie_manager.get(cookie="device_id")
if not user_uuid:
    user_uuid = str(uuid.uuid4())
    # Lưu cookie 30 ngày
    cookie_manager.set("device_id", user_uuid, expires_at=datetime.now().replace(year=datetime.now().year + 1))

# 2. Lấy IP
user_ip = get_remote_ip()

# 3. Load Data & Kiểm tra
with st.spinner("Đang kiểm tra danh sách trúng thưởng..."):
    df_history = get_data()

history = check_user_played(user_ip, user_uuid, df_history)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMjR4Zmx4Zmx4Zmx4Zmx4Zmx4Zmx4Zmx4Zmx4Zmx4ZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/LpDmM2wSt6kCM/giphy.gif", width=300)

st.write("")

if history:
    # --- ĐÃ CHƠI (PHÁT HIỆN QUA IP HOẶC COOKIE) ---
    user_name_old, reward_received, time_played = history
    st.warning(f"⛔ {str(user_name_old).upper()} ĐÃ NHẬN QUÀ RỒI!")
    
    # Hiển thị lý do bị chặn (chỉ hiện khi debug, tắt đi khi chạy thật nếu muốn)
    # st.caption(f"Debug: Phát hiện trùng khớp thiết bị (ID: {user_uuid[:5]}...) hoặc IP.")
    
    st.markdown(f"""
        <div class="status-box">
            <h3>Phần quà của bạn:</h3>
            <h2 style="color: #00FF00;">{reward_received}</h2>
            <p style="color: #DDD; font-size: 12px;">Thời gian: {time_played}</p>
        </div>
    """, unsafe_allow_html=True)

else:
    # --- CHƯA CHƠI ---
    name_input = st.text_input("Nhập tên của bạn:", placeholder="Ví dụ: Tuấn Anh")
    st.write("")

    if st.button("🧧 LẮC NGAY 🧧"):
        if not name_input.strip():
            st.error("⚠️ Vui lòng nhập tên!")
        elif user_ip == "unknown_ip":
            st.error("⚠️ Không thể xác định mạng. Tắt VPN thử xem?")
        else:
            with st.spinner(f'{name_input} đang lắc...'):
                time.sleep(2) 
                final_reward = random.choice(REWARDS)
                
                # Ghi cả IP và UUID vào sheet
                if save_play_history(user_ip, user_uuid, name_input, final_reward):
                    st.balloons()
                    st.success(f"Chúc mừng {name_input}!")
                    st.markdown(f"""
                        <div class="status-box">
                            <h2 style="color: #FFD700;">{final_reward}</h2>
                        </div>
                    """, unsafe_allow_html=True)
                    time.sleep(2)
                    st.rerun()
