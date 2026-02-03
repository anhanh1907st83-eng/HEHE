import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import random
from PIL import Image

st.set_page_config(page_title="Truth or Dare - Team", page_icon="🎲", layout="centered")

# --- HIỂN THỊ HÌNH ẢNH NHÓM ---
# Cách 1: Hiển thị ở đầu trang như một Banner kỷ niệm
try:
    img = Image.open("background.jpg")
    st.image(img, use_container_width=True, caption="Kỷ niệm chúng mình ❤️")
except:
    st.warning("Hãy tải file ảnh lên GitHub với tên 'background.jpg' để hiển thị banner!")

# --- KẾT NỐI DỮ LIỆU ---
conn = st.connection("gsheets", type=GSheetsConnection)

def get_data():
    try:
        df = conn.read(ttl=0)
        df.columns = [str(c).strip().lower() for c in df.columns]
        return df
    except:
        return pd.DataFrame(columns=['content', 'type'])

df = get_data()

# Thống kê
total_q = len(df)

st.title("🎲 Truth or Dare Private")
st.write(f"🔥 Hiện đang có **{total_q}** thử thách trong kho bài!")

st.divider()

# --- PHẦN 1: XOAY THẺ (BỊ KHÓA) ---
st.subheader("🔓 Khu vực xoay thẻ")
code_input = st.text_input("Nhập mã bí mật:", type="password")

if code_input == "hihihi":
    if st.button("🎁 BỐC BÀI NGẪU NHIÊN", use_container_width=True):
        if not df.empty:
            row = df.sample(n=1).iloc[0]
            if str(row['type']).lower() == 'sự thật':
                st.info(f"✨ **TRUTH:** \n\n {row['content']}")
            else:
                st.error(f"🔥 **DARE:** \n\n {row['content']}")
else:
    st.button("🎁 Mở thẻ bài (Cần nhập mã)", disabled=True, use_container_width=True)

st.divider()

# --- PHẦN 2: THÊM CÂU HỎI ---
st.subheader("➕ Đóng góp nội dung")
st.write("Nhập theo cấu trúc nếu không làm được hoặc nói sai sự thật thì kèm theo hình phạt")
with st.form("add_form", clear_on_submit=True):
    c = st.text_input("Nội dung:")
    t = st.selectbox("Loại:", ["Sự thật", "Thử thách"])
    if st.form_submit_button("Lưu vĩnh viễn"):
        if c:
            new_row = pd.DataFrame([{"content": c, "type": t}])
            updated_df = pd.concat([df, new_row], ignore_index=True)
            conn.update(data=updated_df)
            st.success("Đã thêm! Hệ thống đang cập nhật...")
            st.rerun()

# --- HIỂN THỊ HÌNH ẢNH Ở THANH BÊN (TÙY CHỌN) ---
with st.sidebar:
    st.header("GƯƠNG MẶT THÂN QUEN")
    try:
        st.image("background.jpg")
    except:
        pass
    st.write("App này dành riêng cho hội bạn thân. Chơi vui vẻ nhé!")
