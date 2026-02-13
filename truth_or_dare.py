import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import random
import time

# --- 1. CẤU HÌNH TRANG & CSS ---
st.set_page_config(
    page_title="Truth or Dare - Party",
    page_icon="🔥",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS TÙY CHỈNH (GIAO DIỆN DARK MODE) ---
st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: white; }
    .game-card {
        padding: 30px; border-radius: 20px; text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5); margin-bottom: 20px; color: white;
    }
    .card-truth { background: linear-gradient(135deg, #00C6FF 0%, #0072FF 100%); border: 2px solid #89f7fe; }
    .card-dare { background: linear-gradient(135deg, #FF416C 0%, #FF4B2B 100%); border: 2px solid #ff9a9e; }
    .card-type { font-size: 1.5rem; font-weight: 800; text-transform: uppercase; margin-bottom: 10px; opacity: 0.8; }
    .card-content { font-size: 2rem; font-weight: bold; line-height: 1.4; }
    .stButton > button { border-radius: 50px; font-weight: bold; height: 50px; transition: all 0.3s; }
    .stButton > button:hover { transform: scale(1.05); }
</style>
""", unsafe_allow_html=True)

# --- 2. QUẢN LÝ STATE ---
if 'drawn_indices' not in st.session_state:
    st.session_state.drawn_indices = []
if 'current_card' not in st.session_state:
    st.session_state.current_card = None
if 'is_authenticated' not in st.session_state:
    st.session_state.is_authenticated = False # Mặc định chưa đăng nhập quyền Admin

# --- 3. DỮ LIỆU ---
def get_data():
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(ttl="1m")
        df.columns = [str(c).strip().lower() for c in df.columns]
        if 'content' not in df.columns or 'type' not in df.columns:
            return pd.DataFrame(columns=['content', 'type'])
        return df
    except:
        # Mock Data nếu chưa nối Gsheet
        return pd.DataFrame({
            'content': ["Khai thật số dư tài khoản.", "Hít đất 10 cái.", "Kể về tình đầu."],
            'type': ['Truth', 'Dare', 'Truth']
        })

df = get_data()

# --- 4. LOGIC GAME ---
def reset_game():
    st.session_state.drawn_indices = []
    st.session_state.current_card = None
    st.rerun()

def pick_card():
    available = [i for i in df.index if i not in st.session_state.drawn_indices]
    if available:
        idx = random.choice(available)
        st.session_state.drawn_indices.append(idx)
        st.session_state.current_card = df.loc[idx]
        eff = random.choice(["balloons", "snow"])
        if eff == "balloons": st.balloons()
        else: st.snow()
        return True
    return False

# --- 5. POPUP (DIALOG) ---
@st.dialog("🔥 LÁ BÀI ĐỊNH MỆNH 🔥")
def show_card_dialog():
    card = st.session_state.current_card
    if card is not None:
        c_type = str(card['type']).capitalize()
        is_truth = c_type.lower() in ['truth', 'sự thật']
        css_class = "card-truth" if is_truth else "card-dare"
        icon = "🟦" if is_truth else "🟥"
        
        st.markdown(f"""
        <div class="game-card {css_class}">
            <div class="card-type">{icon} {c_type}</div>
            <div class="card-content">{card['content']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("❌ Đóng", use_container_width=True): st.rerun()
        with col2:
            remain = len(df) - len(st.session_state.drawn_indices)
            if remain > 0:
                if st.button("🎲 Bốc tiếp", type="primary", use_container_width=True):
                    pick_card()
                    st.rerun()
            else:
                st.button("Hết bài", disabled=True, use_container_width=True)

# --- 6. GIAO DIỆN CHÍNH ---
st.markdown("<h1 style='text-align: center; color: #FF4B2B;'>🎲 TRUTH OR DARE</h1>", unsafe_allow_html=True)

# Thống kê
total_cards = len(df)
drawn_count = len(st.session_state.drawn_indices)
st.progress(drawn_count / total_cards if total_cards > 0 else 0, text=f"Tiến độ: {drawn_count}/{total_cards}")

st.divider()

# --- KHU VỰC ĐIỀU KHIỂN GAME (QUAN TRỌNG: CÓ LOGIC CHECK PASS) ---
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Nếu ĐÃ đăng nhập -> Hiện nút chơi
    if st.session_state.is_authenticated:
        st.success("🔓 Chế độ Host: Đã mở khóa", icon="✅")
        if (total_cards - drawn_count) > 0:
            if st.button("🚀 BỐC BÀI NGAY", use_container_width=True, type="primary"):
                with st.spinner("🎲 Đang xoay..."):
                    time.sleep(0.8)
                pick_card()
                show_card_dialog()
        else:
            st.warning("Hết bài rồi!")
            if st.button("🔄 Xào lại bài", use_container_width=True):
                reset_game()
    
    # Nếu CHƯA đăng nhập -> Hiện ô nhập pass
    else:
        st.info("🔒 Khu vực dành cho Host")
        pwd = st.text_input("Nhập mã để mở khóa nút xoay:", type="password", placeholder="Nhập 'hihihi'...")
        if pwd:
            if pwd == "hihihi":
                st.session_state.is_authenticated = True
                st.toast("Đã mở khóa quyền Host!", icon="🔓")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("Sai mã rồi!")

# --- 7. SIDEBAR (CÔNG KHAI CHO MỌI NGƯỜI THÊM BÀI) ---
with st.sidebar:
    st.header("📝 Đóng góp câu hỏi")
    st.caption("Mọi người đều có thể thêm câu hỏi vào kho!")
    
    with st.form("public_add_form", clear_on_submit=True):
        new_c = st.text_area("Nội dung thử thách/câu hỏi:")
        new_t = st.selectbox("Loại:", ["Truth", "Dare"])
        submitted = st.form_submit_button("Gửi lên kho bài 📤")
        
        if submitted:
            if new_c:
                try:
                    conn = st.connection("gsheets", type=GSheetsConnection)
                    new_row = pd.DataFrame([{"content": new_c, "type": new_t}])
                    updated_df = pd.concat([df, new_row], ignore_index=True)
                    conn.update(data=updated_df)
                    st.toast("Đã gửi thành công! Cảm ơn bạn.", icon="💖")
                    time.sleep(1)
                    st.cache_data.clear()
                    st.rerun() # Reload để cập nhật số lượng bài
                except:
                    st.error("Lỗi kết nối (hoặc đang dùng data mẫu).")
            else:
                st.warning("Đừng để trống nội dung nhé!")

    st.divider()
    
    # Nút thoát quyền Host (nếu đang đăng nhập)
    if st.session_state.is_authenticated:
        if st.button("Đăng xuất quyền Host"):
            st.session_state.is_authenticated = False
            st.rerun()

st.markdown("<div style='text-align: center; margin-top: 50px; color: #666; font-size: 0.8rem;'>Built with ❤️ by Gemini</div>", unsafe_allow_html=True)
