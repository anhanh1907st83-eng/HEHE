import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import random

st.set_page_config(page_title="True or Dare", page_icon="🎲")

# Kết nối (sẽ tự lấy cấu hình từ Secrets)
conn = st.connection("gsheets", type=GSheetsConnection)

def get_data():
    return conn.read(ttl=0)

try:
    df = get_data()
    # Kiểm tra cột để tránh lỗi logic
    df.columns = [str(c).strip().lower() for c in df.columns]
except Exception as e:
    st.error(f"Lỗi kết nối: {e}")
    st.stop()

st.title("🎲 Random True or Dare")

if st.button("🎁 Mở thẻ bài may mắn", use_container_width=True):
    if not df.empty and 'content' in df.columns:
        row = df.sample(n=1).iloc[0]
        color = "info" if str(row['type']).lower() == 'sự thật' else "error"
        label = str(row['type']).upper()
        
        if color == "info":
            st.info(f"**{label}:** \n\n {row['content']}")
        else:
            st.error(f"**{label}:** \n\n {row['content']}")

st.divider()

with st.form("add_form", clear_on_submit=True):
    st.subheader("➕ Thêm câu hỏi")
    c1 = st.text_input("Nội dung:")
    t1 = st.selectbox("Loại:", ["Sự thật", "Thử thách"])
    if st.form_submit_button("Lưu vĩnh viễn"):
        if c1:
            new_row = pd.DataFrame([{"content": c1, "type": t1}])
            updated_df = pd.concat([df, new_row], ignore_index=True)
            conn.update(data=updated_df)
            st.success("Đã lưu thành công! F5 để cập nhật.")
