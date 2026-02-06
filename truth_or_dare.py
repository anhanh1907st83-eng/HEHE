import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import random
from PIL import Image
import os
import time

# 1. Cấu hình trang
st.set_page_config(page_title="Truth or Dare - Team", page_icon="🎲", layout="centered")

# Hàm tạo hiệu ứng ngẫu nhiên
def random_effect():
    effect = random.choice(["balloons", "snow", "toast"])
    if effect == "balloons":
        st.balloons()
    elif effect == "snow":
        st.snow()
    else:
        st.toast("🔥 Tới công chuyện luôn!", icon="🎯")

# --- 2. THANH BÊN (SIDEBAR) ---
with st.sidebar:
    st.header("👥 THÀNH VIÊN")
    # Bạn có thể sửa danh sách tên ở đây
    team_members = st.text_area("Nhập tên các thành viên (cách nhau bằng dấu phẩy):", 
                                "An, Bình, Chi, Dũng, Hoa, Tuấn").split(",")
    team_members = [name.strip() for name in team_members if name.strip()]
    
    st.divider()
    if os.path.exists("background.jpg"):
        st.image("background.jpg")
    st.write("Chúc nhóm mình chơi vui vẻ! ❤️")

# --- 3. KẾT NỐI DỮ LIỆU ---
conn = st.connection("gsheets", type=GSheetsConnection)
def get_data():
    try:
        df = conn.read(ttl="1m")
        df.columns = [str(c).strip().lower() for c in df.columns]
        return df
    except:
        return pd.DataFrame(columns=['content', 'type'])

df = get_data()

# --- 4. GIAO DIỆN CHÍNH ---
st.title("🎲 Truth or Dare & Lucky Spin")

# Tab để phân chia giữa bốc bài và vòng quay
tab1, tab2 = st.tabs(["🎁 Bốc Bài", "🎡 Vòng Quay May Mắn"])

# --- TAB 1: BỐC BÀI ---
with tab1:
    st.subheader("🔓 Khu vực xoay thẻ")
    code_input = st.text_input("Nhập mã bí mật:", type="password", key="code_card")
    
    if code_input == "hihihi":
        if st.button("🚀 BỐC BÀI NGẪU NHIÊN", use_container_width=True):
            if not df.empty:
                with st.spinner("Đang tìm thử thách..."):
                    time.sleep(0.8)
                random_effect()
                row = df.sample(n=1).iloc[0]
                if str(row['type']).lower() in ['sự thật', 'truth']:
                    st.info(f"✨ **TRUTH:** \n\n ### {row['content']}")
                else:
                    st.error(f"🔥 **DARE:** \n\n ### {row['content']}")
    else:
        st.button("🎁 Mở bài (Cần mã)", disabled=True, use_container_width=True)

# --- TAB 2: VÒNG QUAY MAY MẮN ---
with tab2:
    st.subheader("🎡 Ai sẽ là người tiếp theo?")
    if st.button("🎯 XOAY NGƯỜI MAY MẮN", use_container_width=True):
        if len(team_members) > 0:
            # Hiệu ứng chạy tên giả lập vòng quay
            placeholder = st.empty()
            for _ in range(15):  # Chạy 15 lần để tạo hiệu ứng
                random_name = random.choice(team_members)
                placeholder.markdown(f"<h1 style='text-align: center; color: #FF4B4B;'>{random_name}</h1>", unsafe_allow_html=True)
                time.sleep(0.1)
            
            # Kết quả cuối cùng
            winner = random.choice(team_members)
            placeholder.markdown(f"<h1 style='text-align: center; color: #00FF00; border: 2px solid #00FF00; border-radius: 10px; padding: 10px;'>🏆 {winner}</h1>", unsafe_allow_html=True)
            st.balloons()
            st.success(f"Người được chọn là: **{winner}**! Chúc may mắn nha!")
        else:
            st.warning("Hãy nhập tên thành viên ở thanh bên (Sidebar) trước!")

st.divider()

# --- 5. THÊM CÂU HỎI ---
st.subheader("➕ Đóng góp nội dung")
with st.expander("Thêm câu hỏi mới vào kho"):
    with st.form("add_form", clear_on_submit=True):
        c = st.text_input("Nội dung:")
        t = st.selectbox("Loại:", ["Sự thật", "Thử thách"])
        if st.form_submit_button("Lưu vĩnh viễn"):
            if c:
                new_row = pd.DataFrame
