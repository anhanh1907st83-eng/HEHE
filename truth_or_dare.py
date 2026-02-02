import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import random

st.set_page_config(page_title="Random True or Dare", page_icon="🎲")

# --- KẾT NỐI GOOGLE SHEET ---
conn = st.connection("gsheets", type=GSheetsConnection)

# Hàm đọc dữ liệu
def get_data():
    # ttl=0 để luôn lấy dữ liệu mới nhất từ Sheet khi load lại
    return conn.read(ttl=0)

df = get_data()

st.title("🎲 Thử Thách Ngẫu Nhiên")

# --- PHẦN CHƠI GAME (RANDOM CẢ TYPE) ---
if st.button("🎁 Mở thẻ bài may mắn", use_container_width=True):
    if not df.empty:
        # Lấy ngẫu nhiên 1 dòng từ toàn bộ bảng
        random_row = df.sample(n=1).iloc[0]
        content = random_row['content']
        q_type = random_row['type']
        
        # Hiển thị màu sắc dựa trên loại câu hỏi nhưng gộp chung 1 nút
        if q_type.lower() == 'sự thật':
            st.info(f"**SỰ THẬT:** \n\n {content}")
        else:
            st.error(f"**THỬ THÁCH:** \n\n {content}")
    else:
        st.warning("Dữ liệu trống, hãy thêm câu hỏi bên dưới!")

st.divider()

# --- PHẦN THÊM DỮ LIỆU VĨNH VIỄN ---
st.subheader("➕ Đóng góp câu hỏi mới")
with st.form("add_question_form"):
    new_content = st.text_input("Nội dung câu hỏi:")
    new_type = st.selectbox("Phân loại:", ["Sự thật", "Thử thách"])
    submit_button = st.form_submit_button("Lưu vĩnh viễn vào Sheet")

    if submit_button:
        if new_content:
            # Tạo DataFrame mới từ câu hỏi vừa nhập
            new_data = pd.DataFrame([{"content": new_content, "type": new_type}])
            
            # Cập nhật (Append) vào Sheet hiện tại
            updated_df = pd.concat([df, new_data], ignore_index=True)
            conn.update(data=updated_df)
            
            st.success("Đã lưu thành công! Hãy nhấn nút 'Mở thẻ bài' để chơi.")
            st.balloons()
        else:
            st.warning("Vui lòng nhập nội dung trước khi lưu.")

# Danh sách dữ liệu nguồn đã bị ẩn (không dùng st.write(df) hay st.expander nữa)
