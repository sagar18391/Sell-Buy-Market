import streamlit as st
from summary import show_summary
from checkout import show_checkout
from success import  show_success
from Shop import show_shop
from product import show_product_page
import streamlit.components.v1 as components

# Detect screen width using JS
screen_width = components.html(
    """
    <script>
    const width = window.innerWidth;
    window.parent.postMessage(width, "*");
    </script>
    """,
    height=0,
)
if "page" not in st.session_state:
    st.session_state.page = "shop"   # default page
if "cart" not in st.session_state:
    st.session_state.cart = []
if "is_mobile" not in st.session_state:
    st.session_state["is_mobile"] = False
if "show_cart" not in st.session_state:
    st.session_state.show_cart = False
# Toggle (for testing)
    #st.sidebar.toggle("Mobile View", key="is_mobile")
try:
    if screen_width and int(screen_width) < 768:
        st.session_state.is_mobile = True
    else:
        st.session_state.is_mobile = True
except:
    st.session_state.is_mobile = True
    #st.write(st.session_state.is_mobile)

st.set_page_config(layout="wide")
# CSS styling
st.markdown("""
<style>
.card_mobile {
    padding: 1px;
    border-radius: 10px;
    background-color: #ffffff;
    box-shadow: 0 1px 2px rgba(0,0,0,0.08);
    margin-bottom: 10px;
}
.card img {
    width: 100%;
    max-width: 100px;
    height: auto;
    object-fit: cover;  /* crop if needed */
    border-radius: 8px;
}
.product-name {
    height:20px;
    font-size: 16px;
    font-weight: 600;
    min-height: 55px; /* FIX text alignment */
    text-overflow: None;
    margin-bottom: 10px;
}
.price-row {
    margin-top: 10px;              /* PUSH TO BOTTOM */
    display: flex;
    justify-content: space-between;
    align-items: center;
    text-overflow: ellipsis;
    line-height: 1.2;
}
.price {
    color: green;
    font-weight: bold;
    margin-top: 10px;              /* PUSH TO BOTTOM */
    display: flex;
    justify-content: space-between;
    align-items: center;
    text-overflow: ellipsis;
    line-height: 1.2;
}
/* Remove gap between elements inside columns */
div[data-testid="column"] > div {
    gap: 2px !important;
}
/* Remove extra block spacing */
div[data-testid="stVerticalBlock"] {
    gap: 0.5rem !important;
}
/* Prevent elements from jumping to next line */
@media (max-width: 768px) {
    div[data-testid="column"] {
        flex-wrap: nowrap !important;
}
/* Reduce spacing */
div[data-testid="column"] > div {
    gap: 4px !important;
}
section[data-testid="stSidebar"] {
    display: none;
}

/* Make right column sticky */
div[data-testid="column"]:nth-child(2) {
    position: sticky;
    top: 20px;
}
</style>
""", unsafe_allow_html=True)


if st.session_state.page == "shop":
    show_shop()
elif st.session_state.page == "summary":
    show_summary()
elif st.session_state.page == "checkout":
    show_checkout()
elif st.session_state.page == "success":
    show_success()
elif st.session_state.page == "product":
    show_product_page()


