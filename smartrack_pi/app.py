import json
import os
from ipaddress import IPv4Network
from time import sleep
import streamlit as st
from ip.set_adaptor import Adaptor
from netaddr import IPAddress


def get_mask(mask_bit):
    return IPv4Network(f"0.0.0.0/{mask_bit}").netmask

dir_path = os.path.dirname(os.path.realpath(__file__))
st.set_page_config(initial_sidebar_state="collapsed")

adaptor = Adaptor()
current_cidr = adaptor.config.get("static_ip")
current_ip = current_cidr.split("/")[0]
current_mask_bit = int(current_cidr.split("/")[1])



st.image(
    f"{dir_path}/static/1. Super Landscape - Without Box - Colour With Black Text - PNG.png"
)
link = f"http://{current_ip}:8000"
st.markdown("""
<style>
.big-font {
    font-size:30px !important;
}
</style>
""", unsafe_allow_html=True)
st.markdown(f'<a class="big-font" href="http://{current_ip}:8000" target="_self">Go To Companion</a>', unsafe_allow_html=True)

st.divider()
st.header("Smartrack Static IP", divider="grey")


mask_bit = st.sidebar.slider("Subnet Calculator", 0, 32, value=current_mask_bit)
mask = get_mask(mask_bit)
st.sidebar.write(f"The subnet mask is {mask}")

with st.form(key="my-form"):
    ip = st.text_input("Enter the static ip address", value=current_ip)
    mask = st.text_input("Enter subnet mask", value=mask)
    gateway = st.text_input("Enter the gateway", value=adaptor.config.get("gateway", "192.168.1.1"))
    submit = st.form_submit_button("Submit")

if submit:
    mask_bit = IPAddress(mask).netmask_bits()
    st.write("Changing IP!! Please use the following links... (Takes 5-10 Seconds)")
    st.page_link(f"http://{ip}:8000",  label="Click to Open Companion at New Address")
    st.page_link(f"http://{ip}",  label="Click to Open This page at New Address")
    sleep(5)
    adaptor.set_adaptor_static(f"{ip}/{mask_bit}", gateway)
