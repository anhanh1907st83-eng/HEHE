import streamlit as st
import random

# Dữ liệu từ file Excel của bạn
data = {
    "Hearts (Món Nước)": [
        "Phở", "Bún bò Huế", "Bún riêu", "Hủ tiếu", "Miến gà", 
        "Cháo sườn", "Bánh canh", "Bún mọc", "Bún thang", 
        "Mì Quảng", "Bún cá", "Bún chả cá", "Bún mắm"
    ],
    "Diamonds (Món Cơm)": [
        "Cơm tấm", "Cơm gà", "Cơm sườn", "Cơm chiên", "Cơm bò lúc lắc",
        "Cơm niêu", "Cơm cá kho", "Cơm gà xối mỡ", "Cơm trộn",
        "Cơm chay", "Cơm cà ri", "Cơm vịt", "Cơm thịt kho"
    ],
    "Clubs (Món Ăn Nhẹ/Bánh)": [
        "Bánh mì", "Bánh xèo", "Bánh cuốn", "Bánh khọt", "Bánh căn",
        "Bánh ướt", "Bánh bèo", "Bánh đúc", "Bánh hỏi",
        "Bánh tráng nướng", "Bánh tráng trộn", "Bánh bột lọc", "Bánh bao"
    ],
    "Spades (Món Khác/Lẩu/Nướng)": [
        "Bún đậu mắm tôm", "Bún chả", "Nem nướng", "Gỏi cuốn", "Chả giò",
        "Ốc các loại", "Lẩu Thái", "Lẩu bò", "Lẩu hải sản",
        "BBQ nướng", "Gà nướng", "Vịt quay", "Hải sản"
    ]
}

# Giao diện ứng dụng
st.set_page_config(page_title="Hôm nay ăn gì?", page_icon="🍲")

st.title("🍲 App: Hôm nay ăn gì?")
st.write("Dựa trên thực đơn của bạn!")

# Lựa chọn thể loại
category = st.selectbox("Bạn đang thèm kiểu gì?", ["Tất cả"] + list(data.keys()))

if st.button("Chọn món giúp tôi!"):
    if category == "Tất cả":
        # Gom tất cả các món lại
        all_foods = [item for sublist in data.values() for item in sublist]
        pick = random.choice(all_foods)
    else:
        pick = random.choice(data[category])
    
    # Hiển thị kết quả rực rỡ
    st.balloons()
    st.success(f"Chốt luôn: **{pick}** nhé!")
    st.info("Chúc bạn ngon miệng! 😋")

# Hiển thị thực đơn để tham khảo
with st.expander("Xem toàn bộ thực đơn"):
    st.table(data)
