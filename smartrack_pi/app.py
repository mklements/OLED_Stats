from ipaddress import IPv4Network
import os
import streamlit as st
from ip.set_adaptor import Adaptor
from netaddr import IPAddress

dir_path = os.path.dirname(os.path.realpath(__file__))
st.set_page_config(initial_sidebar_state="collapsed")
st.image(f"{dir_path}/static/1. Super Landscape - Without Box - Colour With Black Text - PNG.png")
st.header("Smartrack Static IP", divider="grey")

adaptor = Adaptor()
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
    adaptor.set_adaptor_static(f"{ip}/{mask_bit}", "192.168.1.1")
