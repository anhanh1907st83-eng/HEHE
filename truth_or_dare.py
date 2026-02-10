import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import random
from PIL import Image
import os
import time

# 1. Cấu hình trang
st.set_page_config(page_title="Truth or Dare - Team", page_icon="🎲", layout="centered")

# --- KHỞI TẠO SESSION STATE ---
if 'drawn_indices' not in st.session_state:
    st.session_state.drawn_indices = []
if 'current_card' not in st.session_state:
    st.session_state.current_card = None # Lưu nội dung lá bài hiện tại
if 'show_dialog' not in st.session_state:
    st.session_state.show_dialog = False # Kiểm soát việc hiển thị popup

# --- KẾT NỐI DỮ LIỆU ---
conn = st.connection("gsheets", type=GSheetsConnection)

def get_data():
    try:
        df = conn.read(ttl="1m")
        df.columns = [str(c).strip().lower() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"Lỗi kết nối: {e}")
        return pd.DataFrame(columns=['content', 'type'])

df = get_data()

# --- HÀM LOGIC: BỐC BÀI MỚI ---
def pick_new_card():
    """Hàm này dùng để chọn bài, dùng được cho cả nút bên ngoài và nút trong popup"""
    # Tính toán các thẻ còn lại
    if not df.empty:
        available_indices = [i for i in df.index if i not in st.session_state.drawn_indices]
    else:
        available_indices = []
        
    if len(available_indices) > 0:
        # Chọn ngẫu nhiên
        chosen_index = random.choice(available_indices)
        row = df.loc[chosen_index]
        
        # Cập nhật Session State
        st.session_state.drawn_indices.append(chosen_index)
        st.session_state.current_card = row
        st.session_state.show_dialog = True # Bật cờ hiển thị popup
        
        # Hiệu ứng (chạy mỗi khi bốc bài mới)
        eff_type = random.choice(["balloons", "snow", "toast"])
        if eff_type == "balloons":
            st.balloons()
        elif eff_type == "snow":
            st.snow()
        else:
            st.toast("🔥 Quá cháy luôn!", icon="🎉")
    else:
        st.session_state.show_dialog = False # Tắt popup nếu hết bài
        st.warning("😱 Đã hết thẻ bài rồi!")

# --- GIAO DIỆN POP-UP (DIALOG) ---
@st.dialog("✨ LÁ BÀI ĐỊNH MỆNH ✨")
def show_card_popup():
    row = st.session_state.current_card
    
    # CSS tùy chỉnh
    st.markdown("""
    <style>
        .big-font { font-size: 24px !important; font-weight: bold; }
        .card-container { padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

    if row is not None:
        if str(row['type']).lower() in ['sự thật', 'truth']:
            st.info("🟦 BẠN ĐÃ BỐC TRÚNG: **SỰ THẬT**")
            st.markdown(f"<div class='card-container'><h3>🎤 {row['content']}</h3></div>", unsafe_allow_html=True)
        else:
            st.error("🟥 BẠN ĐÃ BỐC TRÚNG: **THỬ THÁCH**")
            st.markdown(f"<div class='card-container'><h3>🔥 {row['content']}</h3></div>", unsafe_allow_html=True)
    
    st.divider()
    
    # 2 Nút điều khiển trong Popup
    col1, col2 = st.columns(2)
    
    with col1:
        # Nút đóng
        if st.button("❌ Đóng", use_container_width=True):
            st.session_state.show_dialog = False
            st.rerun()
            
    with col2:
        # Nút xoay tiếp
        # Kiểm tra xem còn bài để xoay tiếp không
        available_check = [i for i in df.index if i not in st.session_state.drawn_indices]
        if len(available_check) > 0:
            if st.button("🔄 Xoay tiếp", type="primary", use_container_width=True):
                pick_new_card() # Gọi hàm bốc bài
                st.rerun() # Load lại trang để cập nhật nội dung popup
        else:
            st.button("Hết bài", disabled=True, use_container_width=True)

# --- 2. THANH BÊN (SIDEBAR) ---
with st.sidebar:
    st.header("📸 NHÓM CHÚNG MÌNH")
    if os.path.exists("background.jpg"):
        st.image("background.jpg")
    else:
        st.info("Upload 'background.jpg' để có ảnh bìa!")
    st.divider()
    
    st.write("🎮 **Công cụ Game Master**")
    if st.button("🔄 Reset Bộ Bài", use_container_width=True):
        st.session_state.drawn_indices = []
        st.session_state.current_card = None
        st.session_state.show_dialog = False
        st.rerun()
        
    st.divider()
    st.write("📝 **Luật chơi:** Đã chọn là phải làm!")

# --- 3. BANNER CHÍNH ---
try:
    img = Image.open("background.jpg")
    st.image(img, use_container_width=True)
except:
    st.info("💡 Mẹo: Thêm ảnh background.jpg để app đẹp hơn.")

# --- Xử lý hiển thị thông tin ---
available_indices = [i for i in df.index if i not in st.session_state.drawn_indices] if not df.empty else []

st.title("🎲 Truth or Dare Private")
st.caption(f"Kho bài: {len(df)} | Đã bốc: {len(st.session_state.drawn_indices)} | Còn lại: {len(available_indices)}")
st.divider()

# --- 5. KHU VỰC CHƠI ---
st.subheader("🔓 Khu vực xoay thẻ")
code_input = st.text_input("🔑 Nhập mã để mở khóa:", type="password")

if code_input == "hihihi":
    # Kiểm tra xem còn bài không
    if len(available_indices) > 0:
        # Nút bấm chính ở ngoài
        if st.button("🎁 BẮT ĐẦU BỐC BÀI", use_container_width=True):
            with st.spinner("Đang xào bài..."):
                time.sleep(1)
            pick_new_card() # Gọi hàm bốc bài lần đầu
            st.rerun()      # Rerun để kích hoạt dialog
            
    else:
        st.warning("😱 Đã hết thẻ bài rồi!")
        if st.button("🔄 Xào lại bài để chơi tiếp", use_container_width=True):
            st.session_state.drawn_indices = []
            st.rerun()

    if df.empty:
        st.warning("Kho bài đang trống, hãy thêm câu hỏi bên dưới nhé!")

else:
    if code_input != "":
        st.error("Sai mã rồi bạn ơi! 😂")
    st.button("🎁 Mở thẻ bài (Cần mã)", disabled=True, use_container_width=True)

# --- QUAN TRỌNG: Kích hoạt hiển thị Dialog nếu cờ được bật ---
if st.session_state.show_dialog:
    show_card_popup()

st.divider()

# --- 6. THÊM CÂU HỎI ---
st.subheader("➕ Đóng góp nội dung")
with st.expander("Nhấn vào đây để thêm câu hỏi mới"):
    with st.form("add_form", clear_on_submit=True):
        c = st.text_input("Nội dung thử thách/câu hỏi:")
        t = st.selectbox("Loại:", ["Sự thật", "Thử thách"])
        submit = st.form_submit_button("Lưu vào kho bài")
        
        if submit:
            if c:
                new_row = pd.DataFrame([{"content": c, "type": t}])
                updated_df = pd.concat([df, new_row], ignore_index=True)
                conn.update(data=updated_df)
                st.toast("Đã lưu thành công!", icon="✅")
                time.sleep(1)
                st.cache_data.clear()
            else:
                st.warning("Vui lòng nhập nội dung trước khi lưu!")
