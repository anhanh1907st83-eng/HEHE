import streamlit as st
import random

# Dữ liệu 52 món Eat Clean "Chuẩn Chợ Việt"
data = {
    "🥗 Nhóm Rau Củ": [
        "Nộm đu đủ tai heo", "Gỏi cuốn tôm thịt", "Salad dưa leo - cà chua", 
        "Rau muống luộc", "Bông cải xanh luộc", "Giá xào lòng gà", 
        "Đậu cô deeee xào thịt bò", "Bắp cải luộc chấm trứng dầm", "Gỏi gà bắp cải", 
        "Khổ qua xào trứng"
    ],
    "🥩 Nhóm Đạm": [
        "Ức gà luộc xé phay", "Cá rô phi áp chảo", "Đậu hủ luộc", 
        "Trứng hấp nấm mèo", "Thăn thịt lợn luộc", "Cá nục kho trà xanh/cà chua", 
        "Tép rang cháy cạnh", "Đậu phụ sốt cà chua", "Cá lóc hấp hành gừng", 
        "Chả gà lá lốt", "Hến xào xúc bánh đa", "Lòng trắng trứng chiên hành"
    ],
    "🍚 Nhóm Tinh Bột": [
        "Cơm gạo lứt muối vừng", "Khoai lang mật luộc", "Bắp ngô luộc", 
        "Bún gạo lứt trộn", "Cháo đậu xanh", "Sắn hấp nước cốt dừa", 
        "Cơm trắng trộn hạt sen", "Miến dong trộn tôm nõn", "Bánh đúc nóng Healthy", 
        "Xôi xéo gạo lứt"
    ],
    "🍲 Nhóm Canh": [
        "Canh rau ngót thịt băm", "Canh bầu nấu tôm đồng", "Canh bí đỏ nấu lạc", 
        "Canh khổ qua rừng", "Canh cua mồng tơi", "Canh cà chua trứng", 
        "Canh hẹ đậu phụ non", "Canh khoai mỡ nấu tôm"
    ],
    "🍎 Ăn Vặt & Đồ Uống": [
        "Chuối sứ luộc/nướng", "Lạc rang muối", "Nước đậu đen xanh lòng", 
        "Chè đỗ đen ít đường", "Sữa đậu nành tự làm", "Ổi xanh chấm muối tôm", 
        "Đu đủ chín", "Dưa hấu tươi", "Chùm ruột/Sơ ri", "Hạt sen tươi", 
        "Sữa chua không đường", "Nước vối/Chè xanh"
    ]
}

# Cấu hình giao diện
st.set_page_config(page_title="Eat Clean Chợ Việt", page_icon="🥒")

# Tùy chỉnh CSS để app trông "sạch" và "xanh"
st.markdown("""
    <style>
    .stApp { background-color: #FCFDFB; }
    h1 { color: #2D5A27; font-family: 'Segoe UI', sans-serif; }
    .stButton>button { 
        width: 100%; 
        background-color: #4E944F; 
        color: white; 
        border-radius: 8px;
        height: 3em;
        font-weight: bold;
    }
    .result-box {
        padding: 25px;
        background-color: #F0F7EF;
        border-radius: 12px;
        border: 2px dashed #4E944F;
        text-align: center;
        margin: 20px 0;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🥒 App Eat Clean: Đi Chợ Thôi!")
st.write("Dinh dưỡng từ những nguyên liệu gần gũi nhất.")

# Lựa chọn nhóm món
category = st.selectbox("Hôm nay bạn muốn chọn món từ nhóm nào?", ["🎲 Ngẫu nhiên tất cả"] + list(data.keys()))

if st.button("XOAY MÓN NGAY"):
    if category == "🎲 Ngẫu nhiên tất cả":
        all_foods = [item for sublist in data.values() for item in sublist]
        pick = random.choice(all_foods)
        group = "Tất cả"
    else:
        pick = random.choice(data[category])
        group = category
    
    st.balloons()
    st.markdown(f"""
        <div class="result-box">
            <p style="color: #4E944F; margin-bottom: 5px;">Hôm nay ăn món này nhé:</p>
            <h2 style="color: #1E3F1C; margin: 0;">{pick}</h2>
            <small style="color: #666;">(Nhóm: {group})</small>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# Hiển thị thực đơn chi tiết theo cột để tối ưu không gian
st.subheader("📋 Thực đơn 52 món của bạn")
cols = st.columns(2)
for i, (group_name, items) in enumerate(data.items()):
    with cols[i % 2]:
        with st.expander(f"{group_name} ({len(items)})"):
            for item in items:
                st.write(f"• {item}")

st.info("💡 **Mẹo:** Ăn Eat Clean Việt Nam là ưu tiên thực phẩm tươi sống tại chợ địa phương và hạn chế gia vị tổng hợp!")
