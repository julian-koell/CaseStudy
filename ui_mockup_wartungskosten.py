import streamlit as st
from user import User, init_db

st.set_page_config(page_title="Verwaltungssystem", layout="wide")
init_db()

st.title("Verwaltungssystem")
st.caption("Administrator-Oberfläche")


# Geräte

if "current_device" not in st.session_state:
    st.session_state.current_device = {
        "name": "Demo-Gerät",
        "responsible_person": "Admin",
        "id": "NR-0001",
        "end_of_life": "20.10.2027"
    }


# HAUPT-TABS

tab_devices, tab_users = st.tabs(["Geräte-Verwaltung", "Nutzer-Verwaltung"])


# GERÄTE-VERWALTUNG

with tab_devices:
    st.header("Geräte-Verwaltung")
    st.caption("Geräte ändern oder neu anlegen")

    tab1, tab2 = st.tabs(["Gerät ändern", "Neues Gerät"])

    with tab1:
        st.subheader("Gerät ändern")

        st.selectbox(
            label="Gerät auswählen",
            options=["Gerät_A", "Gerät_B"],
            key="sb_current_device"
        )

        aktuelles_geraet = st.session_state.current_device

        with st.form("geraet_aendern_form"):
            col1, col2 = st.columns(2)

            with col1:
                id = st.text_input("ID-Nummer", value=aktuelles_geraet["id"])
                responsible_person = st.text_input(
                    "Verantwortlicher",
                    value=aktuelles_geraet["responsible_person"]
                )

            with col2:
                name = st.text_input("Gerätename", value=aktuelles_geraet["name"])
                end_of_life = st.text_input(
                    "Ende Lebenszyklus",
                    value=aktuelles_geraet["end_of_life"]
                )

            if st.form_submit_button("Änderungen speichern"):
                st.session_state.current_device.update({
                    "name": name,
                    "id": id,
                    "responsible_person": responsible_person,
                    "end_of_life": end_of_life
                })
                st.success("Gerät wurde aktualisiert.")

    with tab2:
        st.subheader("Neues Gerät anlegen")

        with st.form("geraet_anlegen_form"):
            col1, col2 = st.columns(2)

            with col1:
                id = st.text_input("ID-Nummer")
                responsible_person = st.text_input("Verantwortlicher")

            with col2:
                name = st.text_input("Gerätename")
                end_of_life = st.text_input("Ende Lebenszyklus")

            if st.form_submit_button("Gerät anlegen"):
                st.session_state.current_device = {
                    "name": name,
                    "id": id,
                    "responsible_person": responsible_person,
                    "end_of_life": end_of_life
                }
                st.success("Gerät wurde angelegt.")


