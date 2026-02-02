import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import random

st.set_page_config(page_title="Random True or Dare", page_icon="🎲")

# Kết nối tự động lấy thông tin từ Secrets
conn = st.connection("gsheets", type=GSheetsConnection)

df = conn.read(ttl=0)

st.title("🎲 TRUE or DARE")

if st.button("🎁 Mở thẻ bài may mắn", use_container_width=True):
    if not df.empty:
        random_row = df.sample(n=1).iloc[0]
        if str(random_row['type']).lower() == 'sự thật':
            st.info(f"**SỰ THẬT:** \n\n {random_row['content']}")
        else:
            st.error(f"**THỬ THÁCH:** \n\n {random_row['content']}")

st.divider()

with st.form("add_form", clear_on_submit=True):
    new_content = st.text_input("Nội dung:")
    new_type = st.selectbox("Loại:", ["Sự thật", "Thử thách"])
    if st.form_submit_button("Lưu vĩnh viễn"):
        if new_content:
            new_data = pd.DataFrame([{"content": new_content, "type": new_type}])
            updated_df = pd.concat([df, new_data], ignore_index=True)
            # Hàm update lúc này sẽ chạy mượt vì đã có chìa khóa trong Secrets
            conn.update(data=updated_df)
            st.success("Đã lưu! Hãy F5 để cập nhật.")
