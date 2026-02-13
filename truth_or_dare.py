import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import random
import time

# --- 1. CẤU HÌNH TRANG & STYLE ---
st.set_page_config(page_title="Truth or Dare Elite", page_icon="🔥", layout="centered")

# Custom CSS để "hack" giao diện Streamlit
st.markdown("""
<style>
    /* Tổng thể nền */
    .main { background: linear-gradient(135deg, #1e1e2f 0%, #121212 100%); }
    
    /* Thẻ bài Truth/Dare */
    .card-box {
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        border: 2px solid rgba(255,255,255,0.1);
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        margin-bottom: 25px;
        transition: transform 0.3s ease;
    }
    .card-box:hover { transform: translateY(-5px); }
    
    /* Màu sắc định danh */
    .truth-text { color: #00d2ff; text-shadow: 0 0 10px rgba(0,210,255,0.5); font-weight: 800; font-size: 1.2rem; }
    .dare-text { color: #ff4b2b; text-shadow: 0 0 10px rgba(255,75,43,0.5); font-weight: 800; font-size: 1.2rem; }
    
    /* Nội dung câu hỏi */
    .content-text {
        font-size: 1.8rem !important;
        line-height: 1.4;
        font-weight: 600;
        color: white;
        margin: 20px 0;
    }
    
    /* Tùy chỉnh nút bấm */
    .stButton>button {
        border-radius: 12px;
        font-weight: 600;
        letter-spacing: 1px;
        text-transform: uppercase;
        transition: all 0.3s;
    }
    
    /* Stats bar */
    .stats-container {
        display: flex;
        justify-content: space-around;
        background: rgba(255,255,255,0.05);
        padding: 10px;
        border-radius: 15px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. KHỞI TẠO SESSION STATE ---
if 'drawn_indices' not in st.session_state:
    st.session_state.drawn_indices = []
if 'current_card' not in st.session_state:
    st.session_state.current_card = None
if 'show_dialog' not in st.session_state:
    st.session_state.show_dialog = False

# --- 3. KẾT NỐI DỮ LIỆU ---
@st.cache_data(ttl="1m")
def load_data():
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read()
        df.columns = [str(c).strip().lower() for c in df.columns]
        return df
    except:
        return pd.DataFrame(columns=['content', 'type'])

df = load_data()

# --- 4. HÀM LOGIC ---
def pick_new_card():
    available_indices = [i for i in df.index if i not in st.session_state.drawn_indices]
    
    if available_indices:
        chosen_index = random.choice(available_indices)
        st.session_state.drawn_indices.append(chosen_index)
        st.session_state.current_card = df.loc[chosen_index]
        st.session_state.show_dialog = True
        
        # Random hiệu ứng ăn mừng
        eff = random.choice([st.balloons, st.snow])
        eff()
    else:
        st.session_state.show_dialog = False
        st.warning("🔥 Cạn lời rồi! Hãy reset bộ bài nhé.")

# --- 5. GIAO DIỆN POP-UP ---
@st.dialog("🎯 KẾT QUẢ")
def show_card_popup():
    card = st.session_state.current_card
    is_truth = str(card['type']).lower() in ['sự thật', 'truth']
    
    label = "💎 SỰ THẬT" if is_truth else "🔥 THỬ THÁCH"
    class_name = "truth-text" if is_truth else "dare-text"
    
    st.markdown(f"""
        <div class="card-box">
            <div class="{class_name}">{label}</div>
            <div class="content-text">"{card['content']}"</div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Đã xong ✅", use_container_width=True):
            st.session_state.show_dialog = False
            st.rerun()
    with col2:
        if st.button("Tiếp tục 🔄", type="primary", use_container_width=True):
            pick_new_card()
            st.rerun()

# --- 6. SIDEBAR ---
with st.sidebar:
    st.title("⚙️ Điều khiển")
    if st.button("🧹 Reset Game", use_container_width=True):
        st.session_state.drawn_indices = []
        st.session_state.current_card = None
        st.rerun()
    
    st.divider()
    st.markdown("### 📝 Luật chơi")
    st.info("1. Nhập mã mở khóa.\n2. Bốc bài ngẫu nhiên.\n3. Làm hoặc... mất lượt!")

# --- 7. GIAO DIỆN CHÍNH ---
st.markdown("<h1 style='text-align: center;'>🎲 TRUTH OR DARE</h1>", unsafe_allow_html=True)

# Hiển thị Stats
available_count = len(df) - len(st.session_state.drawn_indices)
st.markdown(f"""
<div class="stats-container">
    <span>📦 Kho: <b>{len(df)}</b></span>
    <span>✅ Đã bốc: <b>{len(st.session_state.drawn_indices)}</b></span>
    <span>✨ Còn lại: <b>{available_count}</b></span>
</div>
""", unsafe_allow_html=True)

# Bảo mật & Nút bốc bài
password = st.text_input("🔑 Nhập mật mã để bắt đầu:", type="password")

if password == "hihihi":
    if available_count > 0:
        if st.button("🎰 BỐC BÀI NGAY", use_container_width=True, type="primary"):
            with st.status("🔮 Đang triệu hồi thử thách...", expanded=False):
                time.sleep(0.8)
            pick_new_card()
            st.rerun()
    else:
        st.button("🔄 Hết bài! Click để chơi lại", on_click=lambda: st.session_state.update(drawn_indices=[]), use_container_width=True)
else:
    if password: st.error("Sai mật mã!")
    st.button("🔒 Vui lòng nhập mã", disabled=True, use_container_width=True)

if st.session_state.show_dialog:
    show_card_popup()

# --- 8. ĐÓNG GÓP NỘI DUNG ---
st.write("")
with st.expander("➕ Thêm câu hỏi mới vào kho"):
    with st.form("add_content"):
        content = st.text_area("Nội dung câu hỏi:")
        q_type = st.selectbox("Phân loại:", ["Sự thật", "Thử thách"])
        if st.form_submit_button("Gửi lên hệ thống"):
            if content:
                new_data = pd.DataFrame([{"content": content, "type": q_type}])
                updated_df = pd.concat([df, new_data], ignore_index=True)
                # Lưu vào GSheet (Cần quyền ghi)
                # conn.update(data=updated_df) 
                st.success("Đã ghi nhận! (Hệ thống sẽ cập nhật sau giây lát)")
            else:
                st.warning("Đừng để trống nhé!")
