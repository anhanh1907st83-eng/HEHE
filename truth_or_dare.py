import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import random
from PIL import Image
import os
import time

# 1. Cấu hình trang
st.set_page_config(page_title="Truth or Dare - Team", page_icon="🎲", layout="centered")

# Khởi tạo trạng thái phiên (Session State) để lưu lịch sử bài đã bốc
if 'drawn_indices' not in st.session_state:
    st.session_state.drawn_indices = []

# --- HÀM POP-UP HIỂN THỊ THẺ BÀI ---
@st.dialog("✨ LÁ BÀI ĐỊNH MỆNH ✨")
def show_card_popup(card_type, content):
    # CSS tùy chỉnh để làm chữ to và đẹp hơn trong popup
    st.markdown("""
    <style>
        .big-font { font-size: 24px !important; font-weight: bold; }
        .card-container { padding: 20px; border-radius: 10px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

    if str(card_type).lower() in ['sự thật', 'truth']:
        st.info("🟦 BẠN ĐÃ BỐC TRÚNG: **SỰ THẬT**")
        st.markdown(f"<div class='card-container'><h3>🎤 {content}</h3></div>", unsafe_allow_html=True)
    else:
        st.error("🟥 BẠN ĐÃ BỐC TRÚNG: **THỬ THÁCH**")
        st.markdown(f"<div class='card-container'><h3>🔥 {content}</h3></div>", unsafe_allow_html=True)
    
    st.divider()
    st.write("👉 Hãy thực hiện ngay, không được trốn!")
    
    # Nút đóng popup
    if st.button("Đã hiểu / Đóng thẻ", use_container_width=True):
        st.rerun()

# Hàm tạo hiệu ứng ngẫu nhiên
def random_effect():
    eff_type = random.choice(["balloons", "snow", "toast"])
    if eff_type == "balloons":
        st.balloons()
    elif eff_type == "snow":
        st.snow()
    else:
        st.toast("🔥 Quá cháy luôn!", icon="🎉")

# --- 2. THANH BÊN (SIDEBAR) ---
with st.sidebar:
    st.header("📸 NHÓM CHÚNG MÌNH")
    if os.path.exists("background.jpg"):
        st.image("background.jpg")
    else:
        st.info("Hãy tải 'background.jpg' lên cùng thư mục code!")
    st.divider()
    
    # Thêm nút Reset thủ công
    st.write("🎮 **Công cụ Game Master**")
    if st.button("🔄 Xào lại bộ bài (Reset)", use_container_width=True):
        st.session_state.drawn_indices = []
        st.rerun()
        
    st.divider()
    st.write("📝 **Luật chơi:** Đã chọn là phải làm, không được bỏ!")

# --- 3. BANNER CHÍNH ---
try:
    img = Image.open("background.jpg")
    st.image(img, use_container_width=True)
except:
    st.info("💡 Mẹo: Thêm ảnh background.jpg để app đẹp hơn.")

# --- 4. KẾT NỐI DỮ LIỆU ---
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

# --- Xử lý Logic lọc bài trùng ---
if not df.empty:
    available_indices = [i for i in df.index if i not in st.session_state.drawn_indices]
else:
    available_indices = []

st.title("🎲 Truth or Dare Private")
st.caption(f"Kho bài: {len(df)} | Đã bốc: {len(st.session_state.drawn_indices)} | Còn lại: {len(available_indices)}")
st.divider()

# --- 5. KHU VỰC CHƠI ---
st.subheader("🔓 Khu vực xoay thẻ")
code_input = st.text_input("🔑 Nhập mã để mở khóa:", type="password")

if code_input == "hihihi":
    # Kiểm tra xem còn bài không
    if len(available_indices) > 0:
        if st.button("🎁 BỐC BÀI NGẪU NHIÊN", use_container_width=True):
            with st.spinner("Đang xào bài..."):
                time.sleep(1.5) 
            
            # Chọn bài ngẫu nhiên từ danh sách CHƯA BỐC
            chosen_index = random.choice(available_indices)
            row = df.loc[chosen_index]
            
            # Lưu index vào session_state
            st.session_state.drawn_indices.append(chosen_index)
            
            # 1. Chạy hiệu ứng trước
            random_effect()
            
            # 2. Gọi hàm Pop-up hiển thị kết quả
            show_card_popup(row['type'], row['content'])
            
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
