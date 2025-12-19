import streamlit as st

st.set_page_config(page_title="Geräte-Verwaltung", layout="wide")

# Session State Platzhalter
if "current_device" not in st.session_state:
    st.session_state.current_device = {
        "name": "Der Gerät",
        "responsible_person" : "Admin",
        "id": "NR-0001",
        "end_of_life": "20.10.2027"
    }

st.title("Geräte-Verwaltung")
st.caption("Hier kann der Administrator Geräte ändern oder neue Geräte anlegen")

# Gerät ändern
tab1, tab2 = st.tabs(["Gerät ändern","Neues Gerät"])
with tab1:
    st.header("Gerät ändern")

    st.session_state.sb_current_device = st.selectbox(label='Gerät auswählen',
        options = ["Gerät_A", "Gerät_B"])

    aktuelles_geraet = st.session_state.current_device

    with st.form("geraet_aendern_form"):
        col1, col2 = st.columns(2)

        with col1:
            id = st.text_input("ID-Nummer", value=aktuelles_geraet["id"])
            responsible_person = st.text_input("Verantwortlicher", value=aktuelles_geraet["responsible_person"])

        with col2:
            name = st.text_input("Gerätename", value=aktuelles_geraet["name"])
            end_of_life = st.text_input("Ende Lebenszyklus", value=aktuelles_geraet["end_of_life"])

        saved = st.form_submit_button("Änderungen speichern")

        if saved:
            # Werte werden in session_state gespeichert
            st.session_state.current_device.update({
                "name": name,
                "id": id,
                "responsible_person": responsible_person,
                 "end_of_life" : end_of_life
            })
            st.success("Änderungen wurden im Session State aktualisiert (Mock-Up).")
    
# Gerät anlegen
with tab2:
    st.header("Neues Gerät anlegen")

    with st.form("geraet_anlegen_form"):
        col1, col2 = st.columns(2)

        with col1:
            id = st.text_input("ID-Nummer", value=aktuelles_geraet["id"])
            responsible_person = st.text_input("Verantwortlicher", value=aktuelles_geraet["responsible_person"])

        with col2:
            name = st.text_input("Gerätename", value=aktuelles_geraet["name"])
            end_of_life = st.text_input("Ende Lebenszyklus", value=aktuelles_geraet["end_of_life"])

        submitted = st.form_submit_button("Gerät anlegen")

        if submitted:
            # Werte werden in session_state gespeichert
            st.session_state.current_device = {
                "name": name,
                "id": id,
                "responsible_person": responsible_person,
                "end_of_life" : end_of_life
            }
            st.success("Gerät wurde (im Mock-Up) angelegt und als aktuelles Gerät gespeichert.")
