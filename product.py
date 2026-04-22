import streamlit as st
from streamlit import columns

from Shop import load_image
from Shop import add_to_cart

def show_product_page():
    product = st.session_state.get("selected_product")

    if not product:
        st.write("No product selected")
        return



    st.title(product["Name"])

    # 🔥 Load multiple images
    import os

    image_folder = os.path.join("Data/Image/", str(product["Index"]))
    images = []

    if os.path.exists(image_folder):
        for file in os.listdir(image_folder):
            if file.endswith((".jpg", ".png", ".jpeg")):
                images.append(load_image(os.path.join(image_folder, file)))

    # ---------------- LAYOUT ----------------
    left, right = st.columns([1, 1])

    # 🖼️ LEFT → Images
    with left:
        if images:
            selected_key = f"selected_img_{product['Index']}"

            if selected_key not in st.session_state:
                st.session_state[selected_key] = 0

            selected_idx = st.session_state[selected_key]

            # Main image
            st.image(images[selected_idx], use_container_width=True, width=100)

            # Thumbnails
            cols = st.columns(len(images))
            for idx, col in enumerate(cols):
                with col:
                    if st.button("🔘", key=f"thumb_{product['Index']}_{idx}", type="tertiary"):
                        st.session_state[selected_key] = idx
                        st.rerun()

                    #st.image(images[idx], width=80)
        else:
            st.image(load_image("Data/Image/default.jpg"))

    # 📄 RIGHT → Info
    with right:
        st.subheader("Product Details")
        st.write(f"📦 Category: {product['Category']}")

        # Add more fields if available
        if "Description" in product:
            st.write(product["Description"])
        st.write(f"💰 Price: ₹{product['Price']}")

        col1, col2 = columns([1,1])
        with col1:
            # Add to cart
            if st.button("➕ Add to Cart"):
                add_to_cart(product)
                st.success("Added to cart!")
        with col2:
            # 🔙 Back button
            if st.button("⬅ Back"):
                st.session_state.page = "shop"
                st.rerun()