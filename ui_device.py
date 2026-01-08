import streamlit as st
from devices import Device
from queries import find_devices

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
