import streamlit as st
import cv2
from pyzbar.pyzbar import decode
import numpy as np
import pymongo
from pymongo import MongoClient

class Product:
    def __init__(self, name, product_id, details, expiry_date):
        self.name = name
        self.product_id = product_id
        self.details = details
        self.expiry_date = expiry_date

def main():
    st.title("QR Code Scanner App")

    st.write("Click the button to start scanning...")

    # Set up MongoDB Atlas connection
    username = "Swadhesh"
    password = "swadplac472"
    cluster_name = "QRCluster"
    client = MongoClient(f"mongodb+srv://Swadhesh:swadplac472@qrcluster.i7rwc2i.mongodb.net/?retryWrites=true&w=majority")
    db = client["AddToCart"]
    collection = db["Products"]

    # Create a button to start the scanner
    start_button = st.button("Start Scanner")

    if start_button:
        cap = cv2.VideoCapture(0)
        stop_button = st.button("Stop Scanner")

        while not stop_button:
            ret, frame = cap.read()

            if not ret:
                break

            decoded_objects = decode(frame)
            for obj in decoded_objects:
                qr_data = obj.data.decode('utf-8')
                stop_button = True  # Stop the scanner after detecting QR code

                # Split the QR data into components
                components = qr_data.split('\n')
                if len(components) == 4:
                    product = Product(
                        name=components[0].split(': ')[1],
                        product_id=components[1].split(': ')[1],
                        details=components[2].split(': ')[1],
                        expiry_date=components[3].split(': ')[1]
                    )
                    # Insert product data into MongoDB collection
                    product_data = {
                        "name": product.name,
                        "product_id": product.product_id,
                        "details": product.details,
                        "expiry_date": product.expiry_date
                    }
                    collection.insert_one(product_data)

            # Convert the OpenCV frame to RGB format for Streamlit
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            st.image(frame_rgb, channels="RGB", use_column_width=True)

        cap.release()
        cv2.destroyAllWindows()

    st.subheader("Cart")
    show_cart = st.button("Show Cart")
    delete_specific = st.button("Skip product and continue")
    empty_cart = st.button("Empty Cart")
    
    if show_cart:
        # Fetch items from MongoDB and display in the cart
        cart_items = collection.find()
        if cart_items:
            st.write("Items in Cart:")
            for idx, item in enumerate(cart_items, start=1):
                st.write(f"Item {idx}:")
                st.write(f"Product Name: {item['name']}")
                st.write(f"Product ID: {item['product_id']}")
                st.write(f"Product Details: {item['details']}")
                st.write(f"Expiry Date: {item['expiry_date']}")
        else:
            st.write("Cart is empty.")
    if empty_cart:
        collection.delete_many({})
        st.success("Cart has been emptied.")
    if delete_specific:
        last_product = collection.find().sort('_id', -1).limit(1)
        if last_product:
            collection.delete_one(last_product[0])
            st.success("Product not added")
        else:
            st.warning("Cart is empty")


if __name__ == "__main__":
    main()
