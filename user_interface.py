import streamlit as st
from tinydb import TinyDB, Query
from users import User
from devices import Device
from queries import find_devices

if "state" not in st.session_state:
    st.session_state["state"] = "Geräte"

def goto_users():
    st.session_state["state"] = "Nutzer"

def goto_devices():
    st.session_state["state"] = "Geräte"

# Using "with" notation
with st.sidebar:
    st.write("Funktion Auswählen:")
    device_switch = st.button("Geräte-Verwaltung", type="primary", on_click= goto_devices)
    user_switch = st.button("Nutzer-Verwaltung", type="primary", on_click=goto_users)

if st.session_state["state"] == "Geräte":
    st.set_page_config(page_title="Geräte-Verwaltung", layout="wide")

    st.title("Geräte-Verwaltung")
    st.caption("Hier können Geräte geändert werden oder neue Geräte hinzugefügt werden.")


    # Gerät ändern
    tab1, tab2 = st.tabs(["Gerät ändern","Neues Gerät"])
    with tab1:
        st.header("Gerät ändern")

        devices_in_db = find_devices()

        current_device_name = st.selectbox(
            'Gerät auswählen',
            options=devices_in_db, key="sbDevice")

        loaded_device = Device.find_by_attribute("device_name", current_device_name)
        if loaded_device:
            st.write(f"Loaded Device: {loaded_device}")
        else:
            st.error("Device not found in the database.")

        with st.form("Edit_Device"):
                st.write(loaded_device.device_name)

                col1, col2 = st.columns(2)

                with col1:
                    id = st.text_input("ID-Nummer", value=loaded_device.device_id)
                    responsible_person = st.text_input("Geräte-Verantwortlicher", value=loaded_device.managed_by_user_id)
                    loaded_device.set_managed_by_user_id(responsible_person)
                
                with col2:
                    end_of_life = st.text_input("Ende des Lebenszyklus", value=loaded_device.end_of_life)

                # Every form must have a submit button.
                submitted = st.form_submit_button("Speichern")
                if submitted:
                    loaded_device.store_data()
                    st.write("Änderungen gespeichert!")
                    st.rerun()
        
        deleted = st.button("Gerät löschen")
        if deleted:
            loaded_device.delete()
            st.write("Gerät gelöscht!")
            st.rerun()
        
    # Gerät anlegen
    with tab2:
        st.header("Neues Gerät anlegen")

        with st.form("New_Device"):
                st.write("Neues Gerät erstellen:")

                name = st.text_input("Gerätename", value = None)

                col1, col2 = st.columns(2)

                with col1:
                    id = st.text_input("ID-Nummer", value = None)
                    responsible_person = st.text_input("Geräte-Verantwortlicher", value = None)
                
                with col2:
                    end_of_life = st.text_input("Ende des Lebenszyklus", value = None)

                # Every form must have a submit button.
                submitted = st.form_submit_button("Erstellen")
                if submitted:
                    new_device = Device(name,id,responsible_person,end_of_life)
                    new_device.store_data()
                    st.write("Neues Gerät erstellt!")
                    name = None
                    responsible_person = None
                    id = None
                    end_of_life = None
                    st.rerun()

elif st.session_state["state"] == "Nutzer":
    st.set_page_config(page_title="Nutzer-Verwaltung", layout="wide")

    st.title("Nutzer-Verwaltung")
    st.caption("Administrator: Nutzer anlegen, anzeigen und löschen (id = E-Mail, name = Nutzername)")

    tab_list, tab_create = st.tabs(["Nutzer anzeigen", "Neuen Nutzer anlegen"])

    #Tab 1: Anzeigen / Löschen
    with tab_list:
        st.subheader("Nutzer anzeigen / löschen")

        users = User.find_all()
        if not users:
            st.info("Noch keine Nutzer vorhanden. Lege zuerst einen Nutzer an.")
        else:
            # Auswahlbox
            label_to_id = {f"{u.name} ({u.id})": u.id for u in users}
            selected_label = st.selectbox("Nutzer auswählen", list(label_to_id.keys()))
            selected_id = label_to_id[selected_label]

            user = User.find_by_attribute("id", selected_id)

            if user is None:
                st.warning("Nutzer wurde nicht gefunden.")
            else:
                col1, col2 = st.columns(2)
                with col1:
                    st.text_input("E-Mail ", value=user.id, disabled=True)
                with col2:
                    st.text_input("Name ", value=user.name, disabled=True)

                st.divider()
                if st.button("Nutzer löschen", type="primary"):
                    user.delete()
                    st.success("Nutzer wurde gelöscht.")
                    st.rerun()

    #Tab 2: Anlegen
    with tab_create:
        st.subheader("Neuen Nutzer anlegen")

        with st.form("nutzer_anlegen_form"):
            col1, col2 = st.columns(2)
            with col1:
                email = st.text_input("E-Mail-Adresse")
            with col2:
                name = st.text_input("Name")

            submitted = st.form_submit_button("Nutzer anlegen")

            if submitted:
                try:
                    u = User(email, name)
                    u.store_data()
                    st.success("Nutzer wurde angelegt.")
                    st.rerun()
                except ValueError as e:
                    st.error(str(e))
