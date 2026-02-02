import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import random

st.set_page_config(page_title="Truth or Dare Private", page_icon="🎲")

# --- KẾT NỐI DỮ LIỆU ---
conn = st.connection("gsheets", type=GSheetsConnection)

def get_data():
    try:
        # ttl=0 để lấy dữ liệu mới nhất
        df = conn.read(ttl=0)
        # Làm sạch tên cột: bỏ khoảng trắng và viết thường
        df.columns = [str(c).strip().lower() for c in df.columns]
        return df
    except:
        return pd.DataFrame()

df = get_data()

# --- XỬ LÝ SỐ LIỆU ---
# Lấy tổng số lượng từ cột 'all' (dòng cuối cùng có chứa số)
if not df.empty and 'all' in df.columns:
    # Lấy giá trị lớn nhất trong cột 'all' hoặc đếm số dòng
    total_cards = len(df)
else:
    total_cards = 0

st.title("🎲 Sự Thật hay Thử Thách")

# Hiển thị tổng số lá bài bằng widget metric cho đẹp
st.metric(label="Tổng số lá bài trong kho", value=f"{total_cards} thẻ")

# --- PHẦN 1: XOAY THẺ (BỊ KHÓA BỞI MÃ) ---
st.subheader("🔓 Khu vực xoay thẻ")
code_input = st.text_input("Nhập mã để mở chức năng xoay:", type="password", placeholder="Nhập mã...")

if code_input == "hihihi":
    if st.button("🎁 MỞ THẺ BÀI NGẪU NHIÊN", use_container_width=True):
        if not df.empty and 'content' in df.columns:
            row = df.sample(n=1).iloc[0]
            q_text = row['content']
            # Kiểm tra cột type để hiển thị màu sắc
            q_type = str(row['type']).lower() if 'type' in df.columns else ""
            
            if 'sự thật' in q_type:
                st.info(f"✨ **SỰ THẬT:** \n\n {q_text}")
            elif 'thử thách' in q_type:
                st.error(f"🔥 **THỬ THÁCH:** \n\n {q_text}")
            else:
                st.success(f"🃏 **NỘI DUNG:** \n\n {q_text}")
        else:
            st.warning("Kho bài đang trống!")
else:
    st.button("🎁 Mở thẻ bài (Đang bị khóa)", disabled=True, use_container_width=True)

st.divider()

# --- PHẦN 2: THÊM CÂU HỎI ---
st.subheader("➕ Đóng góp câu hỏi mới")

with st.form("add_question_form", clear_on_submit=True):
    new_c = st.text_input("Nội dung câu hỏi:")
    new_t = st.selectbox("Loại thẻ:", ["Sự thật", "Thử thách"])
    submit = st.form_submit_button("Lưu vĩnh viễn vào kho bài")

    if submit:
        if new_c:
            # Tự động tính số thứ tự mới cho cột 'all'
            new_all_value = total_cards + 1
            
            new_row = pd.DataFrame([{
                "content": new_c, 
                "type": new_t, 
                "all": new_all_value
            }])
            
            updated_df = pd.concat([df, new_row], ignore_index=True)
            
            try:
                conn.update(data=updated_df)
                st.success(f"Đã thêm thành công lá bài số {new_all_value}!")
                st.balloons()
                st.rerun() # Refresh để cập nhật con số hiển thị ngay lập tức
            except Exception as e:
                st.error(f"Lỗi: {e}")
        else:
            st.warning("Vui lòng nhập nội dung.")
