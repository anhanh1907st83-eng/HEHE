import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import random

st.set_page_config(page_title="Random Card", page_icon="🎲")

# --- KẾT NỐI ---
conn = st.connection("gsheets", type=GSheetsConnection)

@st.cache_data(ttl=2)
def get_data():
    try:
        df = conn.read(ttl=0)
        df.columns = [str(c).strip().lower() for c in df.columns]
        return df
    except:
        return pd.DataFrame()

df = get_data()

st.title("🎲 Sự Thật hay Thử Thách")

# --- CHỨC NĂNG KHÓA MÃ ---
st.sidebar.header("🔐 Chế độ quản trị")
access_code = st.sidebar.text_input("Nhập mã để chơi:", type="password")

if access_code == "hihihi":
    st.sidebar.success("Đã mở khóa chức năng Random!")
    
    # Chỉ khi nhập đúng mã mới hiện nút này
    if st.button("🎁 Mở thẻ bài ngẫu nhiên", use_container_width=True):
        if not df.empty and 'content' in df.columns:
            row = df.sample(n=1).iloc[0]
            q_text = row['content']
            q_type = str(row['type']).lower()
            
            if q_type == 'sự thật':
                st.info(f"✨ **SỰ THẬT:** \n\n {q_text}")
            else:
                st.error(f"🔥 **THỬ THÁCH:** \n\n {q_text}")
        else:
            st.warning("Chưa có dữ liệu trong Sheet.")
else:
    if access_code == "":
        st.warning("Vui lòng nhập mã ở thanh bên trái để bắt đầu chơi.")
    else:
        st.error("Mã sai rồi bạn ơi! 🤫")

st.divider()

# --- PHẦN THÊM DỮ LIỆU (V
