import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import random
from PIL import Image

st.set_page_config(page_title="Truth or Dare - Team", page_icon="🎲", layout="centered")

# Hàm tạo hiệu ứng ngẫu nhiên
def random_effect():
    effect = random.choice(["balloons", "snow"])
    if effect == "balloons":
        st.balloons()
    else:
        st.snow()

# --- HIỂN THỊ HÌNH ẢNH NHÓM ---
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
total_q = len(df)

st.title("🎲 Truth or Dare Private")
st.write(f"🔥 Hiện đang có **{total_q}** thử thách trong kho bài!")
st.divider()

# --- PHẦN 1: XOAY THẺ ---
st.subheader("🔓 Khu vực xoay thẻ")
code_input = st.text_input("Nhập mã bí mật:", type="password")

if code_input == "hihihi":
    if st.button("🎁 BỐC BÀI NGẪU NHIÊN", use_container_width=True):
        if not df.empty:
            # Gọi hiệu ứng ngẫu nhiên khi bốc bài
            random_effect()
            
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
with st.form("add_form", clear_on_submit=True):
    c = st.text_input("Nội dung:")
    t = st.selectbox("Loại:", ["Sự thật", "Thử thách"])
    if st.form_submit_button("Lưu vĩnh viễn"):
        if c:
            new_row = pd.DataFrame([{"content": c, "type": t}])
            updated_df = pd.concat([df, new_row], ignore_index=True)
            conn.update(data=updated_df)
            
            # Hiệu ứng khi thêm thành công
            random_effect()
            st.success("Đã thêm thành công!")
            # Không dùng st.rerun() ngay để hiệu ứng kịp chạy

# --- THANH BÊN ---
with st.sidebar:
    st.header("GƯƠNG MẶT THÂN QUEN")
    try:
        st.image
