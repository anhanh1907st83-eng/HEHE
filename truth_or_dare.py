import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import random
import time
import streamlit.components.v1 as components

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="Sự Thật hay Thử Thách", page_icon="🎲", layout="centered")

# CSS Light Mode & Giao diện thẻ bài
st.markdown("""
<style>
    .stApp { background-color: #ffffff; color: #31333F; }
    .game-card {
        padding: 40px; border-radius: 20px; text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 20px; color: white;
        animation: zoomIn 0.5s;
    }
    .card-truth { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }
    .card-dare { background: linear-gradient(135deg, #FF512F 0%, #DD2476 100%); }
    .card-type { font-size: 1.5rem; font-weight: 800; text-transform: uppercase; margin-bottom: 15px; opacity: 0.9; }
    .card-content { font-size: 1.8rem; font-weight: bold; line-height: 1.5; }
    @keyframes zoomIn { from { transform: scale(0.8); opacity: 0; } to { transform: scale(1); opacity: 1; } }
    .stButton > button { border-radius: 30px; height: 50px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- 2. KHỞI TẠO SESSION STATE ---
if 'drawn_indices' not in st.session_state: st.session_state.drawn_indices = []
if 'current_card' not in st.session_state: st.session_state.current_card = None
if 'show_dialog' not in st.session_state: st.session_state.show_dialog = False
if 'is_admin' not in st.session_state: st.session_state.is_admin = False

# --- 3. KẾT NỐI DỮ LIỆU ---
def get_data():
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(ttl="1m")
        df.columns = [str(c).strip().lower() for c in df.columns]
        return df
    except:
        return pd.DataFrame({
            'content': ["Khai thật số dư tài khoản.", "Hít đất 10 cái.", "Kể về tình đầu."],
            'type': ['Sự thật', 'Thử thách', 'Sự thật']
        })

df = get_data()

# --- 4. HÀM ĐỌC GIỌNG TIẾNG VIỆT (NÂNG CẤP) ---
def auto_read_vietnamese(text):
    safe_text = text.replace("'", "").replace('"', "")
    js_code = f"""
    <script>
        function speak() {{
            window.speechSynthesis.cancel();
            const msg = new SpeechSynthesisUtterance('{safe_text}');
            msg.lang = 'vi-VN';
            
            // Tìm giọng Việt trong hệ thống
            const voices = window.speechSynthesis.getVoices();
            const viVoice = voices.find(v => v.lang.includes('vi-VN') || v.lang.includes('vi_VN'));
            if (viVoice) msg.voice = viVoice;
            
            msg.rate = 1.0; 
            window.speechSynthesis.speak(msg);
        }}
        // Chạy ngay và chạy khi danh sách giọng nói thay đổi
        speak();
        if (speechSynthesis.onvoiceschanged !== undefined) {{
            speechSynthesis.onvoiceschanged = speak;
        }}
    </script>
    """
    components.html(js_code, height=0, width=0)

# --- 5. LOGIC GAME ---
def pick_card():
    available = [i for i in df.index if i not in st.session_state.drawn_indices]
    if available:
        idx = random.choice(available)
        st.session_state.drawn_indices.append(idx)
        st.session_state.current_card = df.loc[idx]
        st.session_state.show_dialog = True
        return True
    return False

@st.dialog("✨ LÁ BÀI ĐỊNH MỆNH ✨")
def show_card_popup():
    # FIX LỖI: Sử dụng 'is not None' thay vì kiểm tra trực tiếp card
    card = st.session_state.current_card
    if card is not None:
        raw_type = str(card['type']).lower()
        is_truth = raw_type in ['truth', 'sự thật']
        display_type = "SỰ THẬT" if is_truth else "THỬ THÁCH"
        css_class = "card-truth" if is_truth else "card-dare"
        
        # Đọc nội dung
        auto_read_vietnamese(f"{display_type}. {card['content']}")
        
        st.markdown(f"""
        <div class="game-card {css_class}">
            <div class="card-type">{'😇' if is_truth else '😈'} {display_type}</div>
            <div class="card-content">{card['content']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("❌ Đóng", use_container_width=True):
                st.session_state.show_dialog = False
                st.rerun()
        with col2:
            if (len(df) - len(st.session_state.drawn_indices)) > 0:
                if st.button("🔄 Xoay tiếp", type="primary", use_container_width=True):
                    pick_card()
                    st.rerun()
            else:
                st.button("Hết bài", disabled=True, use_container_width=True)

# --- 6. GIAO DIỆN CHÍNH ---
st.title("🎲 Sự Thật hay Thử Thách")
drawn_n = len(st.session_state.drawn_indices)
st.progress(drawn_n / len(df) if len(df) > 0 else 0)
st.caption(f"Tiến độ: {drawn_n}/{len(df)}")

st.divider()

# Khu vực xoay bài
st.subheader("🔥 Khu vực xoay bài")
if not st.session_state.is_admin:
    # Ô mật khẩu sẽ ẩn sau khi nhập đúng
    c1, c2 = st.columns([2,1])
    with c1:
        pwd = st.text_input("Nhập mật khẩu Admin:", type="password", placeholder="Mật khẩu là hihihi")
    with c2:
        st.write(" ")
        st.write(" ")
        if st.button("Mở khóa 🔓", use_container_width=True):
            if pwd == "hihihi":
                st.session_state.is_admin = True
                st.rerun()
            else: st.error("Sai mã!")
else:
    # Khi đã là admin, chỉ hiện nút quay
    col_play, col_lock = st.columns([3, 1])
    with col_play:
        if (len(df) - drawn_n) > 0:
            if st.button("🚀 BẮT ĐẦU QUAY NGAY", use_container_width=True, type="primary"):
                pick_card()
                st.rerun()
        else:
            if st.button("🔄 Trộn lại bộ bài", use_container_width=True):
                st.session_state.drawn_indices = []
                st.session_state.current_card = None
                st.rerun()
    with col_lock:
        if st.button("🔒 Khóa", use_container_width=True):
            st.session_state.is_admin = False
            st.rerun()

# Kích hoạt Popup
if st.session_state.show_dialog:
    show_card_popup()

st.divider()

# Khu vực thêm câu hỏi (Công khai ngay trang chính)
st.subheader("➕ Thêm câu hỏi mới")
with st.expander("📝 Nhấn để mở form đóng góp câu hỏi", expanded=True):
    with st.form("add_form", clear_on_submit=True):
        c1, c2 = st.columns([3, 1])
        with c1:
            new_c = st.text_input("Nội dung câu hỏi/thử thách:")
        with c2:
            new_t = st.selectbox("Loại bài:", ["Sự thật", "Thử thách"])
            
        if st.form_submit_button("Lưu ngay 💾", use_container_width=True):
            if new_c:
                try:
                    conn = st.connection("gsheets", type=GSheetsConnection)
                    new_row = pd.DataFrame([{"content": new_c, "type": new_t}])
                    updated_df = pd.concat([df, new_row], ignore_index=True)
                    conn.update(data=updated_df)
                    st.success("Đã thêm thành công!")
                    st.cache_data.clear()
                    time.sleep(1)
                    st.rerun()
                except: st.error("Lỗi kết nối Google Sheets!")
            else: st.warning("Vui lòng điền nội dung!")
