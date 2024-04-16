import json
import os
from ipaddress import IPv4Network

import streamlit as st
from ip.set_adaptor import Adaptor
from netaddr import IPAddress


def get_mask(mask_bit):
    return IPv4Network(f"0.0.0.0/{mask_bit}").netmask

dir_path = os.path.dirname(os.path.realpath(__file__))

adaptor = Adaptor()
current_cidr = adaptor.config.get("static_ip")
current_ip = current_cidr.split("/")[0]
current_mask_bit = int(current_cidr.split("/")[1])

st.set_page_config(initial_sidebar_state="collapsed")
st.image(
    f"{dir_path}/static/1. Super Landscape - Without Box - Colour With Black Text - PNG.png"
)
st.header("Smartrack Static IP", divider="grey")

mask_bit = st.sidebar.slider("Subnet Calculator", 0, 32, value=current_mask_bit)
mask = get_mask(mask_bit)
st.sidebar.write(f"The subnet mask is {mask}")

with st.form(key="my-form"):
    ip = st.text_input("Enter the static ip address", value=current_ip)
    mask = st.text_input("Enter subnet mask", value=mask)
    gateway = st.text_input("Enter the gateway", value=adaptor.config.get("gateway"))
    submit = st.form_submit_button("Submit")

if submit:
    mask_bit = IPAddress(mask).netmask_bits()
    st.write(f"{ip}/{mask_bit}")
    adaptor.set_adaptor_static(f"{ip}/{mask_bit}", "192.168.1.1")
