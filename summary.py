import streamlit as st

def show_summary():
    st.title("🧾 Order Summary")

    if not st.session_state.cart:
        st.warning("Cart is empty")
        if st.button("⬅ Back to Shop"):
            st.session_state.page = "shop"
            st.rerun()
        return

    total = 0

    for item in st.session_state.cart:
        subtotal = item["Price"] * item["qty"]
        total += subtotal

        col1, col2 = st.columns([3,1])
        with col1:
            st.write(f"{item['Name']} (x{item['qty']})")
        with col2:
            st.write(f"₹{subtotal}")

    st.markdown("---")

    discount = total * 0.1 if total > 5000 else 0
    delivery = 0 if total > 1000 else 50
    final_total = total - discount + delivery

    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(f"Subtotal:")
        st.write(f"Discount(10% if Sub total more then 5000):")
        st.write(f"Delivery(free above 1000):")
        st.markdown(f"### 💰 Final Total:")
    with col2:
        st.write(f"₹{total}")
        st.write(f"-₹{discount}")
        st.write(f"₹{delivery}")
        st.markdown(f"### ₹{final_total}")

    # Navigation buttons
    col1, col2 = st.columns([3,1])

    with col1:
        if st.button("⬅ Back"):
            st.session_state.page = "shop"
            st.rerun()

    with col2:
        if st.button("✅ Proceed to Checkout"):
            st.session_state.final_total = final_total
            st.session_state.page = "checkout"
            st.rerun()