import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import random

st.set_page_config(page_title="Truth or Dare Private", page_icon="🎲")

# --- KẾT NỐI DỮ LIỆU ---
conn = st.connection("gsheets", type=GSheetsConnection)

def get_data():
    try:
        # ttl=0 để lấy dữ liệu mới nhất ngay lập tức
        df = conn.read(ttl=0)
        df.columns = [str(c).strip().lower() for c in df.columns]
        return df
    except:
        return pd.DataFrame()

df = get_data()

st.title("🎲 Sự Thật hay Thử Thách")

# --- PHẦN 1: XOAY THẺ (BỊ KHÓA BỞI MÃ) ---
st.subheader("🔓 Khu vực xoay thẻ")
# Ô nhập mã nằm ngay trên nút xoay để dễ thấy
code_input = st.text_input("Nhập mã để mở chức năng xoay:", type="password", placeholder="Nhập mã tại đây...")

if code_input == "hihihi":
    if st.button("🎁 MỞ THẺ BÀI NGẪU NHIÊN", use_container_width=True):
        if not df.empty and 'content' in df.columns:
            row = df.sample(n=1).iloc[0]
            q_text = row['content']
            q_type = str(row['type']).lower()
            
            if q_type == 'sự thật':
                st.info(f"✨ **SỰ THẬT:** \n\n {q_text}")
            else:
                st.error(f"🔥 **THỬ THÁCH:** \n\n {q_text}")
        else:
            st.warning("Sheet hiện đang trống, hãy đóng góp câu hỏi ở phía dưới!")
else:
    # Trạng thái khi chưa nhập mã hoặc nhập sai
    st.lock_button = st.button("🎁 Mở thẻ bài (Đang bị khóa)", disabled=True, use_container_width=True)
    if code_input != "":
        st.toast("Sai mã rồi bạn ơi! 🤫", icon="❌")

st.divider()

# --- PHẦN 2: THÊM CÂU HỎI (LUÔN MỞ) ---
st.subheader("➕ Đóng góp câu hỏi mới")
st.write("Mọi người đều có thể thêm câu hỏi mà không cần mã!")

with st.form("add_question_form", clear_on_submit=True):
    new_c = st.text_input("Nội dung câu hỏi:")
    new_t = st.selectbox("Loại thẻ:", ["Sự thật", "Thử thách"])
    submit = st.form_submit_button("Lưu vĩnh viễn vào kho bài")

    if submit:
        if new_c:
            new_row = pd.DataFrame([{"content": new_c, "type": new_t}])
            # Gộp dữ liệu mới vào dữ liệu hiện tại
            updated_df = pd.concat([df, new_row], ignore_index=True)
            try:
                conn.update(data=updated_df)
                st.success("Đã lưu thành công! Cảm ơn bạn đã đóng góp.")
                st.balloons()
            except Exception as e:
                st.error(f"Lỗi ghi dữ liệu: {e}")
        else:
            st.warning("Vui lòng không để trống nội dung.")
