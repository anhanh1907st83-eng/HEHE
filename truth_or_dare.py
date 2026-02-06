# --- HIỂN THỊ HÌNH ẢNH Ở THANH BÊN ---
with st.sidebar:
    st.header("GƯƠNG MẶT THÂN QUEN")
    try:
        # Kiểm tra nếu có file ảnh thì mới hiển thị
        st.image("background.jpg")
    except Exception as e:
        # Nếu lỗi (không tìm thấy file), chỉ hiển thị dòng nhắc nhở nhẹ nhàng
        st.info("Thêm ảnh 'background.jpg' để làm đẹp thanh bên nhé!")
        
    st.write("App này dành riêng cho hội bạn thân. Chơi vui vẻ nhé!")
