import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import random
import time

# --- 1. CẤU HÌNH TRANG & CSS LIGHT MODE ---
st.set_page_config(
    page_title="Truth or Dare - Private",
    page_icon="🎲",
    layout="centered"
)

# CSS Tùy chỉnh: Nền Trắng + Thẻ bài đẹp
st.markdown("""
<style>
    /* Ép nền trắng và chữ đen */
    .stApp {
        background-color: #ffffff;
        color: #31333F;
    }
    
    /* Style cho thẻ bài (Card) */
    .game-card {
        padding: 40px; 
        border-radius: 20px; 
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1); /* Bóng nhẹ nhàng */
        margin-bottom: 20px; 
        color: white; /* Chữ trên thẻ màu trắng */
        animation: zoomIn 0.5s;
    }
    
    /* Màu nền cho thẻ Truth (Xanh) và Dare (Đỏ/Cam) */
    .card-truth { 
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
        border: none;
    }
    .card-dare { 
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 99%, #fecfef 100%); 
        background: linear-gradient(120deg, #f6d365 0%, #fda085 100%); /* Màu cam tươi sáng hơn */
        border: none;
    }
    
    .card-type { 
        font-size: 1.2rem; 
        font-weight: 600; 
        text-transform: uppercase; 
        margin-bottom: 15px; 
        opacity: 0.9; 
        letter-spacing: 2px;
    }
    .card-content { 
        font-size: 1.8rem; 
        font-weight: bold; 
        line-height: 1.5; 
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    @keyframes zoomIn { from { transform: scale(0.8); opacity: 0; } to { transform: scale(1); opacity: 1; } }
    
    /* Nút bấm bo tròn */
    .stButton > button { border-radius: 30px; height: 50px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- 2. QUẢN LÝ TRẠNG THÁI (STATE) ---
if 'drawn_indices' not in st.session_state:
    st.session_state.drawn_indices = []
if 'current_card' not in st.session_state:
    st.session_state.current_card = None

# --- 3. DỮ LIỆU ---
def get_data():
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(ttl="1m")
        df.columns = [str(c).strip().lower() for c in df.columns]
        if 'content' not in df.columns: return pd.DataFrame(columns=['content', 'type'])
        return df
    except:
        # Mock Data (Dữ liệu mẫu)
        return pd.DataFrame({
            'content': ["Khai thật số dư tài khoản.", "Hít đất 10 cái.", "Kể về tình đầu.", "Gọi cho người yêu cũ."],
            'type': ['Sự thật', 'Thử thách', 'Sự thật', 'Thử thách']
        })

df = get_data()

# --- 4. HÀM LOGIC ---
def pick_card():
    available = [i for i in df.index if i not in st.session_state.drawn_indices]
    if available:
        idx = random.choice(available)
        st.session_state.drawn_indices.append(idx)
        st.session_state.current_card = df.loc[idx]
        return True
    return False

# --- 5. POPUP HIỂN THỊ KẾT QUẢ ---
@st.dialog("✨ KẾT QUẢ BỐC THĂM ✨")
def show_card_popup():
    card = st.session_state.current_card
    if card is not None:
        c_type = str(card['type']).capitalize()
        # Kiểm tra loại thẻ để tô màu
        is_truth = c_type.lower() in ['sự thật', 'sự thật']
        css_class = "card-truth" if is_truth else "card-dare"
        icon = "😇" if is_truth else "😈"
        
        # Hiển thị thẻ bài
        st.markdown(f"""
        <div class="game-card {css_class}">
            <div class="card-type">{icon} {c_type}</div>
            <div class="card-content">{card['content']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Nút điều khiển trong popup
        col1, col2 = st.columns(2)
        with col1:
            if st.button("❌ Đóng", use_container_width=True): st.rerun()
        with col2:
            remain = len(df) - len(st.session_state.drawn_indices)
            if remain > 0:
                if st.button("🔄 Xoay tiếp", type="primary", use_container_width=True):
                    pick_card()
                    st.rerun()
            else:
                st.button("Hết bài", disabled=True, use_container_width=True)

# --- 6. GIAO DIỆN CHÍNH ---
st.title("🎲 Truth or Dare - Phiên bản nội bộ")

# Thống kê
total = len(df)
drawn = len(st.session_state.drawn_indices)
st.caption(f"Tiến độ: {drawn}/{total} thẻ")
st.progress(drawn / total if total > 0 else 0)

st.divider()

# --- KHU VỰC 1: TRÒ CHƠI (CẦN MẬT KHẨU) ---
st.subheader("🔥 Khu vực xoay bài")
col_pwd, col_btn = st.columns([1, 2])

with col_pwd:
    code_input = st.text_input("Mật khẩu Admin:", type="password", placeholder="")

with col_btn:
    st.write("") # Spacer cho thẳng hàng
    st.write("") 
    if code_input == "matkhau":
        # Mật khẩu đúng -> Hiện nút chơi
        if (total - drawn) > 0:
            if st.button("🚀 BẮT ĐẦU QUAY", use_container_width=True, type="primary"):
                with st.spinner("Đang chọn ngẫu nhiên..."):
                    time.sleep(0.5)
                pick_card()
                show_card_popup()
        else:
            if st.button("🔄 Reset Game", use_container_width=True):
                st.session_state.drawn_indices = []
                st.rerun()
    else:
        # Mật khẩu sai/trống -> Nút bị khóa
        st.button("🔒 Nhập đúng mã để mở", disabled=True, use_container_width=True)

st.divider()

# --- KHU VỰC 2: THÊM CÂU HỎI MỚI (CÔNG KHAI Ở DƯỚI) ---
st.subheader("➕ Thêm thử thách mới")
st.info("Bất kỳ ai cũng có thể đóng góp câu hỏi tại đây!")

with st.expander("📝 Nhấn để mở form thêm câu hỏi", expanded=True):
    with st.form("add_new_card_form", clear_on_submit=True):
        c1, c2 = st.columns([3, 1])
        with c1:
            new_content = st.text_input("Nội dung câu hỏi/thử thách:", placeholder="Ví dụ: Hát một bài...")
        with c2:
            new_type = st.selectbox("Loại thẻ:", ["Sự thật", "Thử thách"])
            
        submit_btn = st.form_submit_button("Lưu vào bộ bài 💾", use_container_width=True)
        
        if submit_btn:
            if new_content:
                try:
                    conn = st.connection("gsheets", type=GSheetsConnection)
                    new_row = pd.DataFrame([{"content": new_content, "type": new_type}])
                    updated_df = pd.concat([df, new_row], ignore_index=True)
                    conn.update(data=updated_df)
                    st.success("Đã thêm câu hỏi mới thành công!")
                    time.sleep(1)
                    st.cache_data.clear()
                    st.rerun()
                except:
                    st.error("Không thể lưu (Lỗi kết nối hoặc đang chạy chế độ Offline).")
            else:
                st.warning("Vui lòng nhập nội dung câu hỏi!")

# Footer
st.markdown("---")
st.caption("Game được thiết kế cho nhóm bạn vui vẻ! 🎉")
