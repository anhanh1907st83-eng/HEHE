import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import random

st.set_page_config(page_title="Random True or Dare", page_icon="🎲")

conn = st.connection("gsheets", type=GSheetsConnection)

# Hàm đọc dữ liệu có cache để tăng tốc
def get_data():
    return conn.read(ttl="1s") # Làm mới sau mỗi 1 giây nếu có thay đổi

try:
    df = get_data()
except Exception as e:
    st.error("Lỗi kết nối Secrets hoặc Google API. Kiểm tra lại định dạng private_key trong Secrets.")
    st.stop()

st.title("🎲 Thử Thách Ngẫu Nhiên")

if st.button("🎁 Mở thẻ bài may mắn", use_container_width=True):
    if not df.empty:
        random_row = df.sample(n=1).iloc[0]
        content = random_row['content']
        q_type = str(random_row['type']).lower()
        
        if q_type == 'sự thật':
            st.info(f"**SỰ THẬT:** \n\n {content}")
        else:
            st.error(f"**THỬ THÁCH:** \n\n {content}")

st.divider()

with st.form("add_form", clear_on_submit=True):
    new_content = st.text_input("Nội dung câu hỏi mới:")
    new_type = st.selectbox("Loại:", ["Sự thật", "Thử thách"])
    if st.form_submit_button("Lưu vĩnh viễn vào Sheet"):
        if new_content:
            new_row = pd.DataFrame([{"content": new_content, "type": new_type}])
            updated_df = pd.concat([df, new_row], ignore_index=True)
            conn.update(data=updated_df)
            st.success("Đã gửi dữ liệu! Hãy chờ 1-2 giây rồi bấm Mở thẻ để cập nhật.")
            st.balloons()
