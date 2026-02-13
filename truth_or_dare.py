import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import random
import time

# --- 1. CẤU HÌNH TRANG & CSS (GIỮ NGUYÊN GIAO DIỆN ĐẸP) ---
st.set_page_config(
    page_title="Truth or Dare - Private",
    page_icon="🔥",
    layout="centered"
)

# CSS Tùy chỉnh: Dark Mode + Thẻ bài hiệu ứng 3D
st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: white; }
    
    /* Style cho thẻ bài */
    .game-card {
        padding: 30px; border-radius: 20px; text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5); margin-bottom: 20px; color: white;
        animation: fadeIn 0.5s;
    }
    .card-truth { background: linear-gradient(135deg, #00C6FF 0%, #0072FF 100%); border: 2px solid #89f7fe; }
    .card-dare { background: linear-gradient(135deg, #FF416C 0%, #FF4B2B 100%); border: 2px solid #ff9a9e; }
    .card-type { font-size: 1.5rem; font-weight: 800; text-transform: uppercase; margin-bottom: 10px; opacity: 0.8; }
    .card-content { font-size: 2rem; font-weight: bold; line-height: 1.4; }
    
    /* Animation */
    @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
    
    /* Button */
    .stButton > button { border-radius: 50px; font-weight: bold; height: 50px; }
</style>
""", unsafe_allow_html=True)

# --- 2. QUẢN LÝ STATE ---
if 'drawn_indices' not in st.session_state:
    st.session_state.drawn_indices = []
if 'current_card' not in st.session_state:
    st.session_state.current_card = None

# --- 3. DỮ LIỆU ---
def get_data():
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(ttl="1m")
        df.columns = [str(c).strip().lower() for c in df.columns]
        if 'content' not in df.columns: return pd.DataFrame(columns=['content', 'type'])
        return df
    except:
        # Dữ liệu mẫu phòng khi lỗi kết nối
        return pd.DataFrame({
            'content': ["Khai thật số dư tài khoản.", "Hít đất 10 cái.", "Kể về tình đầu.", "Gọi cho người yêu cũ."],
            'type': ['Truth', 'Dare', 'Truth', 'Dare']
        })

df = get_data()

# --- 4. HÀM XỬ LÝ (LOGIC CŨ) ---
def pick_card():
    available = [i for i in df.index if i not in st.session_state.drawn_indices]
    if available:
        idx = random.choice(available)
        st.session_state.drawn_indices.append(idx)
        st.session_state.current_card = df.loc[idx]
        return True
    return False

# --- 5. POPUP HIỂN THỊ (DIALOG) ---
@st.dialog("🔥 LÁ BÀI ĐỊNH MỆNH 🔥")
def show_card_popup():
    card = st.session_state.current_card
    if card is not None:
        # Giao diện thẻ bài đẹp
        c_type = str(card['type']).capitalize()
        is_truth = c_type.lower() in ['truth', 'sự thật']
        css_class = "card-truth" if is_truth else "card-dare"
        icon = "🟦" if is_truth else "🟥"
        
        st.markdown(f"""
        <div class="game-card {css_class}">
            <div class="card-type">{icon} {c_type}</div>
            <div class="card-content">{card['content']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("❌ Đóng", use_container_width=True): st.rerun()
        with col2:
            # Logic nút "Bốc tiếp" ngay trong popup
            remain = len(df) - len(st.session_state.drawn_indices)
            if remain > 0:
                if st.button("🎲 Bốc tiếp", type="primary", use_container_width=True):
                    pick_card()
                    st.rerun()
            else:
                st.button("Hết bài", disabled=True, use_container_width=True)

# --- 6. GIAO DIỆN CHÍNH (MAIN LAYOUT) ---
st.title("🎲 Truth or Dare")

# Thanh tiến trình
total = len(df)
drawn = len(st.session_state.drawn_indices)
st.progress(drawn / total if total > 0 else 0, text=f"Đã bốc: {drawn}/{total}")

st.divider()

# --- KHÔI PHỤC LOGIC QUYỀN XOAY BÀI NHƯ CŨ ---
st.subheader("🔓 Khu vực Game Master")
code_input = st.text_input("🔑 Nhập mã để mở khóa nút xoay:", type="password")

if code_input == "matkhau":
    # MÃ ĐÚNG -> HIỆN NÚT BẤM
    remain_cards = total - drawn
    if remain_cards > 0:
        if st.button("🚀 BỐC BÀI NGAY", use_container_width=True, type="primary"):
            with st.spinner("Đang xào bài..."):
                time.sleep(0.5)
            
            # Hiệu ứng
            eff = random.choice(["balloons", "snow", "toast"])
            if eff == "balloons": st.balloons()
            elif eff == "snow": st.snow()
            else: st.toast("🔥 Cháy quá!", icon="🎉")
            
            pick_card()
            show_card_popup() # Gọi popup ngay sau khi bốc
    else:
        st.warning("😱 Hết bài rồi!")
        if st.button("🔄 Reset Bộ Bài", use_container_width=True):
            st.session_state.drawn_indices = []
            st.rerun()
else:
    # MÃ SAI HOẶC TRỐNG -> HIỆN NÚT VÔ HIỆU HÓA
    if code_input != "":
        st.error("Sai mã rồi bạn ơi! 😂")
    st.button("🔒 Nút xoay bị khóa", disabled=True, use_container_width=True)

st.divider()

# --- 7. SIDEBAR (CÔNG KHAI CHO MỌI NGƯỜI THÊM BÀI) ---
with st.sidebar:
    st.header("📝 Thêm câu hỏi mới")
    
    with st.form("add_card_form", clear_on_submit=True):
        new_c = st.text_area("Nội dung:")
        new_t = st.selectbox("Loại:", ["Sự thật", "Thử thách"])
        submitted = st.form_submit_button("Lưu vào kho")
        
        if submitted:
            if new_c:
                try:
                    conn = st.connection("gsheets", type=GSheetsConnection)
                    new_row = pd.DataFrame([{"content": new_c, "type": new_t}])
                    updated_df = pd.concat([df, new_row], ignore_index=True)
                    conn.update(data=updated_df)
                    st.toast("Đã thêm thành công!", icon="✅")
                    time.sleep(1)
                    st.cache_data.clear()
                    st.rerun()
                except:
                    st.error("Lỗi kết nối Gsheets (hoặc đang chạy local).")
            else:
                st.warning("Nhập nội dung đi bạn ơi!")
