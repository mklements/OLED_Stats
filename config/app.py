import time
from ipaddress import IPv4Network

import streamlit as st
from netaddr import IPAddress

st.image("config/static/tempsnip.png")
st.header("Smartrack Static IP", divider="grey")


mask_bit = st.slider("Select a mask", 0, 32, value=24)
mask = IPv4Network(f"0.0.0.0/{mask_bit}").netmask

st.write(f"The subnet mask is {mask}")

# Add a selectbox to the sidebar:
with st.form(key="my-form"):
    ip = st.text_input("Enter the static ip address", value="192.168.1.241")
    # mask = st.text_input("Enter subnet mask")
    submit = st.form_submit_button("Submit")

if submit:
    # st.write(f"You entered {ip} and {mask_bit}")
    # mask_bits = IPAddress(mask).netmask_bits()
    st.write(f"{ip}/{mask_bit}")
# "Starting a long computation..."

# # Add a placeholder
# latest_iteration = st.empty()
# bar = st.progress(0)

# for i in range(100):
#     # Update the progress bar with each iteration.
#     latest_iteration.text(f"Iteration {i+1}")
#     bar.progress(i + 1)
#     time.sleep(0.1)

# "...and now we're done!"
