import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import random
import time
import streamlit.components.v1 as components

# --- 1. CẤU HÌNH TRANG & CSS LIGHT MODE ---
st.set_page_config(
    page_title="Sự Thật hay Thử Thách",
    page_icon="🔥",
    layout="centered"
)

# CSS Tùy chỉnh: Nền Trắng + Thẻ bài Tiếng Việt
st.markdown("""
<style>
    .stApp { background-color: #ffffff; color: #31333F; }
    
    /* Card Style */
    .game-card {
        padding: 40px; border-radius: 20px; text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 20px; color: white;
        animation: zoomIn 0.5s;
    }
    .card-truth { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); } /* Xanh dương */
    .card-dare { background: linear-gradient(120deg, #ff9a9e 0%, #fecfef 100%); background-color: #FA8BFF; background-image: linear-gradient(45deg, #FA8BFF 0%, #2BD2FF 52%, #2BFF88 90%); } /* Màu cầu vồng/đỏ */
    .card-dare { background: linear-gradient(135deg, #FF512F 0%, #DD2476 100%); } /* Đỏ hồng mạnh mẽ */

    .card-type { font-size: 1.5rem; font-weight: 800; text-transform: uppercase; margin-bottom: 15px; opacity: 0.9; letter-spacing: 2px; }
    .card-content { font-size: 1.8rem; font-weight: bold; line-height: 1.5; text-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    
    @keyframes zoomIn { from { transform: scale(0.8); opacity: 0; } to { transform: scale(1); opacity: 1; } }
    .stButton > button { border-radius: 30px; height: 50px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- 2. QUẢN LÝ TRẠNG THÁI (SESSION STATE) ---
if 'drawn_indices' not in st.session_state:
    st.session_state.drawn_indices = []
if 'current_card' not in st.session_state:
    st.session_state.current_card = None
if 'show_dialog' not in st.session_state:
    st.session_state.show_dialog = False
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False # Kiểm soát việc hiển thị ô mật khẩu

# --- 3. DỮ LIỆU ---
def get_data():
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(ttl="1m")
        df.columns = [str(c).strip().lower() for c in df.columns]
        if 'content' not in df.columns: return pd.DataFrame(columns=['content', 'type'])
        return df
    except:
        # Mock Data (Tiếng Việt)
        return pd.DataFrame({
            'content': ["Khai thật số dư tài khoản hiện tại.", "Hít đất 10 cái ngay lập tức.", "Kể về mối tình đầu của bạn.", "Gọi điện cho người yêu cũ hỏi thăm."],
            'type': ['Sự thật', 'Thử thách', 'Sự thật', 'Thử thách']
        })

df = get_data()



# --- 5. POPUP HIỂN THỊ (DIALOG) ---
@st.dialog("✨ LÁ BÀI ĐỊNH MỆNH ✨")
def show_card_popup():
    card = st.session_state.current_card
    
    if card is not None:
        c_content = card['content']
        raw_type = str(card['type']).lower()
        
        # Chuyển đổi hiển thị sang Tiếng Việt chuẩn
        if raw_type in ['truth', 'sự thật']:
            display_type = "SỰ THẬT"
            css_class = "card-truth"
            icon = "😇"
        else:
            display_type = "THỬ THÁCH"
            css_class = "card-dare"
            icon = "😈"
        
        
        # 2. Hiển thị Card
        st.markdown(f"""
        <div class="game-card {css_class}">
            <div class="card-type">{icon} {display_type}</div>
            <div class="card-content">{c_content}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # 3. Nút bấm
        col1, col2 = st.columns(2)
        with col1:
            if st.button("❌ Đóng", use_container_width=True):
                st.session_state.show_dialog = False
                st.rerun()
        with col2:
            remain = len(df) - len(st.session_state.drawn_indices)
            if remain > 0:
                if st.button("🔄 Xoay tiếp", type="primary", use_container_width=True):
                    st.rerun()
            else:
                st.button("Hết bài", disabled=True, use_container_width=True)

# --- 6. GIAO DIỆN CHÍNH ---
st.title("🎲 Sự Thật hay Thử Thách")

total = len(df)
drawn = len(st.session_state.drawn_indices)
st.progress(drawn / total if total > 0 else 0)
st.caption(f"Đã chơi: {drawn}/{total} thẻ")

st.divider()

# --- KHU VỰC ĐIỀU KHIỂN (LOGIC ẨN MẬT KHẨU) ---
st.subheader("🔥 Khu vực xoay bài")

# Kiểm tra trạng thái Admin
if not st.session_state.is_admin:
    # --- TRẠNG THÁI 1: CHƯA NHẬP PASS (HIỆN Ô NHẬP) ---
    c1, c2 = st.columns([2,1])
    with c1:
        pwd = st.text_input("Mật khẩu mở khóa:", type="password", placeholder="Nhập mật khẩu...")
    with c2:
        st.write("")
        st.write("")
        if st.button("Mở khóa 🔓", use_container_width=True):
            if pwd == "hihihi":
                st.session_state.is_admin = True # Lưu trạng thái đã mở
                st.rerun() # Load lại trang để ẩn ô mật khẩu đi
            else:
                st.error("Sai mật khẩu!")
else:
    # --- TRẠNG THÁI 2: ĐÃ MỞ KHÓA (CHỈ HIỆN NÚT CHƠI) ---
    # Ô mật khẩu đã biến mất hoàn toàn
    col_play, col_lock = st.columns([3, 1])
    
    with col_play:
        if (total - drawn) > 0:
            if st.button("🚀 BẮT ĐẦU QUAY NGAY", use_container_width=True, type="primary"):
                with st.spinner("Đang chọn ngẫu nhiên..."):
                    time.sleep(0.5)
                pick_card()
                st.rerun()
        else:
            if st.button("🔄 Trộn lại bộ bài", use_container_width=True):
                st.session_state.drawn_indices = []
                st.rerun()
                
    with col_lock:
        # Nút để khóa lại nếu cần
        if st.button("🔒 Khóa", use_container_width=True):
            st.session_state.is_admin = False
            st.rerun()

# --- KÍCH HOẠT POPUP ---
if st.session_state.show_dialog:
    show_card_popup()

st.divider()

# --- KHU VỰC THÊM CÂU HỎI (CÔNG KHAI) ---
st.subheader("➕ Thêm câu hỏi mới")

with st.expander("📝 Nhấn để mở form đóng góp", expanded=True):
    with st.form("add_new_card_form", clear_on_submit=True):
        c1, c2 = st.columns([3, 1])
        with c1:
            new_content = st.text_input("Nội dung:", placeholder="Ví dụ: Kể tên 3 người yêu cũ...")
        with c2:
            # Selectbox giờ là Tiếng Việt
            new_type = st.selectbox("Loại thẻ:", ["Sự thật", "Thử thách"])
            
        if st.form_submit_button("Lưu ngay 💾", use_container_width=True):
            if new_content:
                try:
                    conn = st.connection("gsheets", type=GSheetsConnection)
                    new_row = pd.DataFrame([{"content": new_content, "type": new_type}])
                    updated_df = pd.concat([df, new_row], ignore_index=True)
                    conn.update(data=updated_df)
                    st.success("Đã thêm thành công!")
                    time.sleep(1)
                    st.cache_data.clear()
                    st.rerun()
                except:
                    st.error("Lỗi kết nối!")
            else:
                st.warning("Nhập nội dung đi bạn!")

st.caption("Âm thanh được tạo bởi trình duyệt của bạn (Chị Google).")
