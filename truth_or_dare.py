import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import random
from PIL import Image
import os
import time

# 1. Cấu hình trang
st.set_page_config(page_title="Truth or Dare - Team", page_icon="🎲", layout="centered")

# Hàm tạo hiệu ứng ngẫu nhiên (Thêm nhiều lựa chọn hơn)
def random_effect():
    # Chọn ngẫu nhiên giữa bong bóng, tuyết, và các hiệu ứng toast
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
    st.write("🎮 **Luật chơi:** Đã chọn là phải làm, không được huỷ!")

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
        # Đọc dữ liệu từ Google Sheets
        df = conn.read(ttl="1m") # Cache trong 1 phút để tránh load lại quá nhiều
        df.columns = [str(c).strip().lower() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"Lỗi kết nối: {e}")
        return pd.DataFrame(columns=['content', 'type'])

df = get_data()

st.title("🎲 Truth or Dare Private")
st.caption(f"Kho bài hiện tại: {len(df)} câu hỏi")
st.divider()

# --- 5. KHU VỰC CHƠI ---
st.subheader("🔓 Khu vực xoay thẻ")
code_input = st.text_input("🔑 Nhập mã bí mật để mở khóa:", type="password")

if code_input == "hihihi":
    if st.button("🎁 BỐC BÀI NGẪU NHIÊN", use_container_width=True):
        if not df.empty:
            with st.spinner("Đang xào bài..."):
                time.sleep(1) # Tạo hiệu ứng chờ đợi cho hồi hộp
                
            random_effect()
            row = df.sample(n=1).iloc[0]
            
            # Hiển thị kết quả trong một khung (Box) đẹp hơn
            st.markdown("### Kết quả dành cho bạn:")
            if str(row['type']).lower() in ['sự thật', 'truth']:
                st.info(f"✨ **TRUTH (SỰ THẬT):** \n\n ### {row['content']}")
            else:
                st.error(f"🔥 **DARE (THỬ THÁCH):** \n\n ### {row['content']}")
        else:
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
                st.balloons()
                st.success("Đã lưu! Hãy bốc bài để xem nội dung mới.")
            else:
                st.warning("Vui lòng nhập nội dung trước khi lưu!")
