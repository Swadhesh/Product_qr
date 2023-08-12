import streamlit as st
import qrcode
from PIL import Image
import io

def generate_qr_code(product_name, product_id, product_details, expiry_date):
    data = f"Product Name: {product_name}\nProduct ID: {product_id}\nProduct Details: {product_details}\nExpiry Date: {expiry_date}"
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img

def main():
    st.title("Product QR Code Generator")
    st.write("Enter Product Details:")
    product_name = st.text_input("Product Name")
    product_id = st.text_input("Product ID")
    product_details = st.text_area("Product Details")
    expiry_date = st.date_input("Expiry Date")

    if st.button("Generate QR Code"):
        qr_img = generate_qr_code(product_name, product_id, product_details, expiry_date)

        # Convert PIL image to BytesIO object
        img_stream = io.BytesIO()
        qr_img.save(img_stream, format="PNG")

        # Display the QR code image
        st.image(img_stream, caption="Generated QR Code", use_column_width=True)

    st.write("---")
    st.write("Scan the QR code to view product details")

if __name__ == "__main__":
    main()
