from ipaddress import IPv4Network

import streamlit as st
from netaddr import IPAddress

st.image("static/tempsnip.png")
st.header("Smartrack Static IP", divider="grey")


mask_bit = st.sidebar.slider("Subnet Calculator", 0, 32, value=24)
mask = IPv4Network(f"0.0.0.0/{mask_bit}").netmask
st.sidebar.write(f"The subnet mask is {mask}")

with st.form(key="my-form"):
    ip = st.text_input("Enter the static ip address", value="192.168.1.241")
    mask = st.text_input("Enter subnet mask", value=mask)
    submit = st.form_submit_button("Submit")

if submit:
    mask_bit = IPAddress(mask).netmask_bits()
    st.write(f"{ip}/{mask_bit}")
