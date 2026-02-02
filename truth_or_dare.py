import streamlit as st
from streamlit_gsheets import GSheetsConnection
import random

st.set_page_config(page_title="True or Dare Pro", page_icon="🔥")

# 1. Khởi tạo kết nối với Google Sheet
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. Đọc dữ liệu từ Sheet
# Thay đổi URL này bằng link Google Sheet của bạn
url = "https://docs.google.com/spreadsheets/d/1lknKFA9Ekg3OAfTjQ60ckgYVZwKLPLvJW-cpaxBPq2w/edit#gid=0"
df = conn.read(spreadsheet=url, usecols=[0, 1])

st.title("🃏 True or Dare - GSheets Edition")

# Chia dữ liệu theo loại
truths = df[df['type'] == 'Sự thật']['content'].tolist()
dares = df[df['type'] == 'Thử thách']['content'].tolist()

# 3. Giao diện nút bấm
col1, col2 = st.columns(2)
with col1:
    if st.button("✨ Sự Thật"):
        st.info(random.choice(truths))

with col2:
    if st.button("🔥 Thử Thách"):
        st.error(random.choice(dares))

st.divider()

# 4. Thêm dữ liệu (Hướng dẫn)
st.info("💡 Để thêm câu hỏi mới vĩnh viễn, bạn chỉ cần mở file Google Sheet và nhập thêm dòng mới. App sẽ tự cập nhật khi bạn Refresh trình duyệt!")
