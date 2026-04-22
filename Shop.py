import streamlit as st
import pandas as pd
import os
from PIL import Image


#def add_to_cart(product):
#    st.session_state.cart.append(product)
def add_to_cart(product):


    for item in st.session_state.cart:
        if item["Index"] == product["Index"]:
            item["qty"] += 1
            return

    new_product = product.copy()
    new_product["qty"] = 1
    st.session_state.cart.append(new_product)


@st.cache_data
def load_image(path):
    img = Image.open(path)
    #st.write(st.session_state.is_mobile)
    if st.session_state.is_mobile:
        img = img.resize((50, 50), Image.LANCZOS)
    else:
        img = img.resize((50, 50), Image.LANCZOS)
    return img

def show_shop():
    data = pd.read_csv("Data/products-100.csv")

    search_query = st.text_input("Search product")

    categories = ["All"] + list(data["Category"].unique())
    category = st.selectbox("Category", categories)

    filtered = data.copy()

    if search_query:
        filtered = filtered[filtered["Name"].str.contains(search_query, case=False)]

    if category != "All":
        filtered = filtered[filtered["Category"] == category]

    # 🔥 Main layout (LEFT: products, RIGHT: cart)
    if st.session_state.is_mobile:
        left = st.container()
        right = st.container()
    else:
        left, right = st.columns([4, 2])

    # ---------------- LEFT SIDE (PRODUCTS) ----------------

    with left:
        st.markdown("""
        <style>
        /* Force grid to stay horizontal */
        div[data-testid="stHorizontalBlock"] {
            display: flex !important;
            flex-wrap: wrap !important;
        }

        /* Force each column to take 50% width */
        @media (max-width: 768px) {
            div[data-testid="column"] {
                flex: 0 0 50% !important;
                max-width: 50% !important;
            }
        }
        </style>
        """, unsafe_allow_html=True)
        st.title("🛍️ Marketplace")
        # Display in grid (3 columns)
        num_cols = 2 if st.session_state.is_mobile else 5
        rows = [filtered.iloc[i:i + num_cols] for i in range(0, len(filtered), num_cols)]

        for row_group in rows:
            cols = st.columns(num_cols)
            for col, (_, row) in zip(cols, row_group.iterrows()):
                with col:
                    with st.container():
                        st.markdown('<div class="card">', unsafe_allow_html=True)
                        image_folder = os.path.join("Data/Image/", str(row['Index']))

                        images = []
                        if os.path.exists(image_folder):
                            for file in os.listdir(image_folder):
                                if file.endswith((".jpg", ".png", ".jpeg")):
                                    img_path = os.path.join(image_folder, file)
                                    images.append(load_image(img_path))
                        # Image inside card
                        if images:
                            #st.image(images[0])  # main image
                            selected_key = f"selected_img_{row['Index']}"

                            # Default selected image
                            if selected_key not in st.session_state:
                                st.session_state[selected_key] = 0

                            selected_idx = st.session_state[selected_key]

                            # 👉 Show ONLY selected image (top)
                            if images:
                                st.image(images[selected_idx], use_container_width=True)
                            # 👉 Thumbnails at bottom
                            cols_img = st.columns(len(images))

                            #for idx, col in enumerate(cols_img):
                            #    with col:
                            #        if st.button("🔘", key=f"thumb_{row['Index']}_{idx}", type="tertiary"):
                            #            st.session_state[selected_key] = idx
                            #            st.rerun()

                        else:
                            img = load_image("Data/Image/default.jpg")
                            st.image(img)

                    # Product Name
                    st.markdown(f'<div class="product-name">{row["Name"]}</div>', unsafe_allow_html=True)

                    # Bottom row: price + button
                    col1, col2, col3 = st.columns([1,1, 1])
                    with col1:
                        st.markdown(f'<div class="price">₹{row["Price"]}</div>', unsafe_allow_html=True)
                    with col2:
                        if st.button("ℹ️️", key=f"view_{row['Index']}",type="tertiary"):
                            st.session_state.selected_product = row.to_dict()
                            st.session_state.page = "product"
                            st.rerun()
                    with col3:
                        if st.button("➕", key=f"add_{row['Index']}",type="tertiary"):
                            add_to_cart(row.to_dict())

                    st.markdown('</div>', unsafe_allow_html=True)


    # Cart preview


    with right:
        st.markdown("## 🛒 Cart")

        if st.session_state.cart:

            total = 0

            for i, item in enumerate(st.session_state.cart):

                st.markdown("""
                <div style="
                    padding:1px;
                    border-radius:10px;
                    background-color:#f9f9f9;
                    margin-bottom:10px;
                    box-shadow:0 2px 3px rgba(0,0,0,0.05);
                ">
                """, unsafe_allow_html=True)

                if st.session_state.is_mobile:
                    col1, col2 = st.columns([2, 1])
                else:
                    col1, col2 = st.columns([3, 2])

                # Product Info
                with col1:
                    st.markdown(f"**{item['Name']}**")
                    st.markdown(f"₹{item['Price']}")

                # Quantity Controls
                with col2:
                    c1, c2, c3, c4 = st.columns([1,1,1,1])

                    with c1:
                        if st.button("➖", key=f"dec_{i}",type="tertiary"):
                            item["qty"] -= 1
                            if item["qty"] <= 0:
                                st.session_state.cart.pop(i)
                            st.rerun()
                    with c2:
                        st.markdown(f"**{item['qty']}**",text_alignment="center")

                    with c3:
                        use_width = st.session_state.is_mobile
                        if st.button("➕", key=f"inc_{i}",type="tertiary", use_container_width=use_width):
                            item["qty"] += 1
                            st.rerun()
                    with c4:
                        # Remove button
                        if st.button("🗑", key=f"remove_{i}",type="tertiary"):
                            st.session_state.cart.pop(i)
                            st.rerun()

                ##st.markdown("</div>", unsafe_allow_html=True)

                total += item["Price"] * item["qty"]

            # 🔥 Summary Section
            st.markdown("---")
            c1, c2 = st.columns([2, 1])
            with c1:
                st.markdown(f"### 💰 Total: ₹{total}")

            with c2:
                if st.button("Go to Summary"):
                    st.session_state.page = "summary"
                    st.rerun()
        else:
            st.write("Cart is empty")
