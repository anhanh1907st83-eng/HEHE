import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import random
from PIL import Image
import os

# 1. Cấu hình trang (Phải là lệnh Streamlit đầu tiên)
st.set_page_config(page_title="Truth or Dare - Team", page_icon="🎲", layout="centered")

# Hàm tạo hiệu ứng ngẫu nhiên
def random_effect():
    effect = random.choice(["balloons", "snow"])
    if effect == "balloons":
        st.balloons()
    else:
        st.snow()

# --- 2. THANH BÊN (SIDEBAR) ---
# Đưa lên đây cũng được, nhưng phải sau khi import st
with st.sidebar:
    st.header("GƯƠNG MẶT THÂN QUEN")
    if os.path.exists("background.jpg"):
        st.image("background.jpg")
    else:
        st.info("Chưa có ảnh background.jpg")
    st.write("Chúc hội bạn chơi vui vẻ!")

# --- 3. HIỂN THỊ BANNER CHÍNH ---
try:
    img = Image.open("background.jpg")
    st.image(img, use_container_width=True, caption="Kỷ niệm chúng mình ❤️")
except:
    st.warning("Thiếu file 'background.jpg'!")

# --- 4. KẾT NỐI DỮ LIỆU ---
conn = st.connection("gsheets", type=GSheetsConnection)

def get_data():
    try:
        df = conn.read(ttl=0)
        df.columns = [str(c).strip().lower() for c in df.columns]
        return df
    except:
        return pd.DataFrame(columns=['content', 'type'])

df = get_data()

st.title("🎲 Truth or Dare Private")
st.write(f"🔥 Hiện đang có **{len(df)}** thử thách!")
st.divider()

# --- 5. KHU VỰC CHƠI ---
st.subheader("🔓 Khu vực xoay thẻ")
code_input = st.text_input("Nhập mã bí mật:", type="password")

if code_input == "hihihi":
    if st.button("🎁 BỐC BÀI NGẪU NHIÊN", use_container_width=True):
        if not df.empty:
            random_effect() # Hiệu ứng ngẫu nhiên ở đây
            row = df.sample(n=1).iloc[0]
            if str(row['type']).lower() == 'sự thật':
                st.info(f"✨ **TRUTH:** \n\n {row['content']}")
            else:
                st.error(f"🔥 **DARE:** \n\n {row['content']}")
else:
    st.button("🎁 Mở thẻ bài (Cần mã)", disabled=True, use_container_width=True)

st.divider()

# --- 6. THÊM CÂU HỎI ---
st.subheader("➕ Đóng góp nội dung")
with st.form("add_form", clear_on_submit=True):
    c = st.text_input("Nội dung:")
    t = st.selectbox("Loại:", ["Sự thật", "Thử thách"])
    if st.form_submit_button("Lưu vĩnh viễn"):
        if c:
            new_row = pd.DataFrame([{"content": c, "type": t}])
            updated_df = pd.concat([df, new_row], ignore_index=True)
            conn.update(data=updated_df)
            random_effect() # Hiệu ứng ngẫu nhiên khi lưu
            st.success("Đã thêm thành công!")
