import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import random

st.set_page_config(page_title="Random True or Dare", page_icon="🎲")

# --- LINK GOOGLE SHEET CỦA BẠN ---
# Dán link sheet của bạn vào đây
SHEET_URL = "https://docs.google.com/spreadsheets/d/1lknKFA9Ekg3OAfTjQ60ckgYVZwKLPLvJW-cpaxBPq2w/edit"

# --- KẾT NỐI GOOGLE SHEET ---
conn = st.connection("gsheets", type=GSheetsConnection)

# Hàm đọc dữ liệu
def get_data():
    # Truyền trực tiếp spreadsheet URL vào đây
    return conn.read(spreadsheet=SHEET_URL, ttl=0)

try:
    df = get_data()
except Exception as e:
    st.error("Chưa kết nối được với Sheet. Hãy đảm bảo Sheet đã được Share ở chế độ 'Anyone with link can Edit'.")
    st.stop()

st.title("🎲 Thử Thách Ngẫu Nhiên")

# --- PHẦN CHƠI GAME ---
if st.button("🎁 Mở thẻ bài may mắn", use_container_width=True):
    if not df.empty:
        random_row = df.sample(n=1).iloc[0]
        content = random_row['content']
        q_type = random_row['type']
        
        if str(q_type).lower() == 'sự thật':
            st.info(f"**SỰ THẬT:** \n\n {content}")
        else:
            st.error(f"**THỬ THÁCH:** \n\n {content}")
    else:
        st.warning("Dữ liệu trống, hãy thêm câu hỏi bên dưới!")

st.divider()

# --- PHẦN THÊM DỮ LIỆU VĨNH VIỄN ---
st.subheader("➕ Đóng góp câu hỏi mới")
with st.form("add_question_form", clear_on_submit=True):
    new_content = st.text_input("Nội dung câu hỏi:")
    new_type = st.selectbox("Phân loại:", ["Sự thật", "Thử thách"])
    submit_button = st.form_submit_button("Lưu vĩnh viễn vào Sheet")

    if submit_button:
        if new_content:
            # Tạo DataFrame mới
            new_data = pd.DataFrame([{"content": new_content, "type": new_type}])
            
            # Gộp dữ liệu cũ và mới
            updated_df = pd.concat([df, new_data], ignore_index=True)
            
            # Cập nhật ngược lại Sheet (Truyền spreadsheet URL vào đây)
            conn.update(spreadsheet=SHEET_URL, data=updated_df)
            
            st.success("Đã lưu thành công! Hãy Refresh (F5) trang hoặc đợi giây lát để cập nhật kho bài.")
            st.balloons()
        else:
            st.warning("Vui lòng nhập nội dung trước khi lưu.")
