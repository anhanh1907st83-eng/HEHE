import streamlit as st
from streamlit_gsheets import GSheetsConnection
import random
import pandas as pd

st.set_page_config(page_title="True or Dare Pro", page_icon="🔥")

# 1. Khởi tạo kết nối
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. Đọc dữ liệu (Thêm ttl=0 để luôn làm mới dữ liệu khi load trang)
url = "LINK_GOOGLE_SHEET_CỦA_BẠN"

try:
    df = conn.read(spreadsheet=url, ttl=0)
    
    # Ép kiểu tên cột về chữ thường để tránh lỗi viết hoa/thường
    df.columns = [str(c).strip().lower() for c in df.columns]
    
    # Lấy danh sách dựa trên cột 'content' và 'type'
    # Lưu ý: Sửa tên 'sự thật' và 'thử thách' cho khớp với Sheet của bạn
    truths = df[df['type'].str.lower() == 'sự thật']['content'].tolist() if 'type' in df.columns else []
    dares = df[df['type'].str.lower() == 'thử thách']['content'].tolist() if 'type' in df.columns else []

except Exception as e:
    st.error(f"Lỗi kết nối dữ liệu: {e}")
    truths, dares = [], []

st.title("🃏 True or Dare")

col1, col2 = st.columns(2)

with col1:
    if st.button("✨ Sự Thật"):
        if truths: # Kiểm tra nếu danh sách không rỗng
            st.info(random.choice(truths))
        else:
            st.warning("Kho 'Sự thật' đang trống! Hãy kiểm tra Google Sheet.")

with col2:
    if st.button("🔥 Thử Thách"):
        if dares: # Kiểm tra nếu danh sách không rỗng
            st.error(random.choice(dares))
        else:
            st.warning("Kho 'Thử thách' đang trống! Hãy thêm dữ liệu.")

# Hiển thị bảng dữ liệu bên dưới để debug (Chỉ bạn mới thấy)
with st.expander("🔍 Kiểm tra dữ liệu nguồn"):
    st.write(df)
