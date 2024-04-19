import json
import os
from ipaddress import IPv4Network
from time import sleep

import streamlit as st
from net.adaptor import Address
from netaddr import IPAddress
from settings import software
from streamlit_js_eval import get_page_location


def get_mask(mask_bit):
    return IPv4Network(f"0.0.0.0/{mask_bit}").netmask


dir_path = os.path.dirname(os.path.realpath(__file__))


def get_companion_configs():
    folder = "/home/smartrack/smartrack-pi/companion"
    return [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

def main():
    st.set_page_config(
        initial_sidebar_state="collapsed",
        page_title="Smartrack Settings",
        page_icon=f"{dir_path}/assets/app/static/4. CT Mark - Colour PNG.png",
    )
    with open(f"{dir_path}/assets/app/style.css", encoding="utf-8") as css:
        st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

    adaptor = Address()
    current_cidr = adaptor.config.get("static_ip")
    current_ip = current_cidr.split("/")[0]
    current_mask_bit = int(current_cidr.split("/")[1])

    st.image(
        f"{dir_path}/assets/app/static/1. Super Landscape - Without Box - Colour With Black Text - PNG.png"
    )

    page_loc = get_page_location() or {"origin": "localhost"}
    link = f"{page_loc.get('origin')}:8000"
    st.markdown(
        """
    <style>
    .big-font {
        font-size:30px !important;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<a class="big-font" href="{link}" target="_self">Go To Companion</a>',
        unsafe_allow_html=True,
    )

    st.divider()
    tab1, tab2, tab3 = st.tabs(["Companion", "Network", "System"])

    with tab1:
        file_tab_1,file_tab_2,file_tab_3 = st.tabs(["Backup", "Restore", "Delete"])
        with file_tab_1:
            st.write("Backup to file")
            with st.form(key="backup-file"):
                name = st.text_input("File Name", value="")
                def_form_submit = st.form_submit_button("Backup Config")
            if def_form_submit:
                st.write(software.backup_companion_file(name))
                
        with file_tab_2:
            st.write("Load from file")
            with st.form(key="store-file"):
                select = st.selectbox("File Name", get_companion_configs())
                def_form_submit = st.form_submit_button("Overwrite config and restart")
            if def_form_submit:
                st.write(f"{software.restore_companion_file(select)} \nRestarting!")
                

        with file_tab_3:
            st.write("Delete file")
            with st.form(key="delete-file"):
                configs = get_companion_configs()
                configs.remove('default') if 'default' in configs else ""
                select = st.selectbox("File Name", configs)
                def_form_submit = st.form_submit_button("Delete File")
            if def_form_submit:
                st.write(software.delete_companion_file(select))
                st.rerun()
            

    with tab2:
        st.write("Set Static Ip")
        with st.expander("Bit Mask Calculator", expanded=False):
            mask_bit = st.slider("Subnet Calculator", 0, 32, value=current_mask_bit)
            mask = get_mask(mask_bit)
            st.write(f"The subnet mask is {mask}")    
        with st.form(key="my-form"):
            ip = st.text_input("Enter the static ip address", value=current_ip)
            mask = st.text_input(
                "Enter the subnet mask (Click the Arrow in the Top Left for Bit Mask Calculator)",
                value=mask,
            )
            gateway = st.text_input(
                "Enter the gateway", value=adaptor.config.get("gateway", "192.168.1.1")
            )
            submit = st.form_submit_button("Set to Static IP")

        if submit:
            mask_bit = IPAddress(mask).netmask_bits()
            st.write("Changing IP!! Please use the following links... (Takes 5-10 Seconds)")
            st.page_link(
                f"http://{ip}:8000", label="Click to Open Companion at New Address"
            )
            st.page_link(f"http://{ip}", label="Click to Open This page at New Address")
            sleep(5)
            adaptor.set_adaptor_static(f"{ip}/{mask_bit}", gateway)

    with tab3:
        system_tab_1,system_tab_2 = st.tabs(["Software Update", "Factory Reset"])
        with system_tab_1:
            st.write("Software for device, no changes to companion")
            with st.form(key="update"):
                update_submit = st.form_submit_button("Update")
            if update_submit:
                st.write("Updating!")
                software.update()
        with system_tab_2:
            st.write("Overwrites companion, deletes user configs, and reset to DHCP")
            with st.form(key="reset"):
                reset_submit = st.form_submit_button("Reset")
            if reset_submit:
                st.write("Resetting!")
                software.factory_reset()
main()
