import  streamlit as st
import re
import random
from success import send_email

def show_checkout():
    if "order" not in st.session_state:
        st.session_state.order = {}
    if "payment_status" not in st.session_state:
        st.session_state.payment_status = "pending"
    if "show_payment" not in st.session_state:
        st.session_state.show_payment = False
    if "otp_verified" not in st.session_state:
        st.session_state.otp_verified = False
    if "payment_done" not in st.session_state:
        st.session_state.payment_done = False
    if "otp_sent" not in st.session_state:
        st.session_state.otp_sent = False

    st.title("💳 Checkout")

    st.write(f"Amount to Pay: ₹{st.session_state.get('final_total', 0)}")

    # Example form
    name = st.text_input("Name*")
    if not name:
        st.caption("⚠️ Name is required")
    address = st.text_area("Address*")
    if not address:
        st.caption("⚠️ Address is required")
    phone = st.text_input("Phone Number *", help="Enter 10-digit mobile number")
    if not phone:
        st.caption("⚠️ Phone is required")
    if not phone.isdigit() or len(phone) != 10:
        st.caption("Phone must be 10 digits")
    email = st.text_input("Email *")
    if not email:
        st.caption("⚠️ Email is required")
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(email_pattern, email):
        st.caption("Invalid email format")
    pincode = st.text_input("Pincode *", help="6-digit area code")
    payment = st.selectbox("Payment Method", ["COD", "UPI", "Card"])

    col1, col2,col4, col3 = st.columns([6,1,1,1])

    with col1:
        is_disable_back = (st.session_state.payment_done == True)
        if st.button("⬅ Back", disabled= is_disable_back):
            st.session_state.page = "summary"
            st.session_state.otp_verified = False
            st.session_state.show_payment = False
            st.rerun()
    with col2:
        is_valid = (
                name.strip() and
                phone.isdigit() and len(phone) == 10 and
                re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email) and
                address.strip() and
                pincode.isdigit() and len(pincode) == 6
        )

        # ---------------- SEND OTP ----------------


        if st.button("📩 Send OTP", disabled= not is_valid):
            if is_valid:
                otp = random.randint(100000, 999999)
                st.session_state.generated_otp = otp
                st.session_state.otp_sent = True
                st.success(f"OTP sent to {phone} (for demo: {otp})")  # In real app, send via SMS API

        # ---------------- ENTER OTP ----------------
        if st.session_state.otp_sent:
            entered_otp = st.text_input("Enter OTP")
            if str(entered_otp) == str(st.session_state.generated_otp):
                #st.success("🎉 OTP Verified! Order placed successfully!")
                # Save order
                st.session_state.order = {
                    "name": name,
                    "phone": phone,
                    "email": email,
                    "address": address,
                    "pincode": pincode,
                    "payment": payment
                }

                # Clear cart & reset OTP
                # st.session_state.cart.clear()
                st.session_state.otp_sent = False
                st.session_state.generated_otp = None
                st.session_state.otp_verified = True
                st.success("🎉 OTP Verified! You can now place the order.")
            else:
                st.error("❌ Invalid OTP. Try again.")
    with col4:
        #st.write(st.session_state.otp_verified)
        is_disabled = (not is_valid) or (st.session_state.otp_verified == False)
        if st.button("Proceed to Pay", disabled= is_disabled):
            st.session_state.show_payment = True
        if st.session_state.show_payment:

            st.subheader("💳 Payment")

            if payment == "COD":
                st.info("Pay cash at delivery")
                if st.button("Confirm Order"):
                    st.session_state.payment_status = "Cash_Pending"
                    st.session_state.payment_done = True

            elif payment == "UPI":
                st.image("https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=upi://pay")
                st.info("Scan QR and pay")

                if st.button("I have paid"):
                    st.session_state.payment_status = "Paid"
                    st.session_state.payment_done = True

            elif payment == "Card":
                st.text_input("Card Number")
                st.text_input("Expiry")
                st.text_input("CVV", type="password")

                if st.button("Pay Now"):
                    st.session_state.payment_status = "Paid"
                    st.session_state.payment_done = True
        st.write("Payment Status:", st.session_state.payment_status)


    with col3:
        is_disabled = (
                (not is_valid) or
                (not st.session_state.otp_verified) or
                (st.session_state.payment_status != "Paid" and
                st.session_state.payment_status != "Cash_Pending")

        )

        if st.button("💰 Place Order", disabled= is_disabled):
            if not is_valid:
                st.error("Please fill all required fields")
            else:
                st.success("🎉 Order placed successfully!")

                # Save order
                st.session_state.order.update( {
                    "items": st.session_state.cart.copy(),
                    "total": st.session_state.final_total,
                    "payment_status": st.session_state.payment_status
                })


                st.session_state.page = "success"
                st.rerun()

