import streamlit as st

st.set_page_config(page_title="Geräte-Verwaltung", layout="wide")

# ---------- Session State Platzhalter ----------
if "current_device" not in st.session_state:
    st.session_state.current_device = {
        "name": "Der Gerät",
        "typ": "3D-Drucker",
        "standort": "Labor 1",
        "status": "verfügbar",
        "inventarnummer": "DEV-0001"
    }

# ---------- Sidebar Navigation ----------
##st.sidebar.title("Geräte-Verwaltung")
##action = st.sidebar.radio(
##    "Aktion wählen:",
##    ("Gerät anlegen", "Gerät ändern")
##)






# ---------- Header ----------
st.title("🏭 Geräte-Verwaltung")
st.caption("Mock-Up für den Administrator-Zweig „Geräte-Verwaltung“")

# ---------- Gerät anlegen ----------
tab1, tab2 = st.tabs(["Gerät anlegen","Gerät ändern"])
with tab1: 
    st.header("➕ Neues Gerät anlegen")
    st.write("Hier kann der Administrator ein neues Gerät in das System aufnehmen.")

    with st.form("geraet_anlegen_form"):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Gerätename", placeholder="z. B. Lasercutter")
            typ = st.text_input("Gerätetyp", placeholder="z. B. Schneidgerät")
            inventarnummer = st.text_input("Inventarnummer", placeholder="z. B. DEV-0010")

        with col2:
            standort = st.text_input("Standort", placeholder="z. B. Werkstatt 2")
            status = st.selectbox("Status", ["verfügbar", "in Wartung", "defekt", "reserviert"])
            bemerkung = st.text_area("Bemerkungen", placeholder="Optionale Beschreibung")

        submitted = st.form_submit_button("Gerät anlegen")

        if submitted:
            # Nur Mock: wir überschreiben einfach den Platzhalter im Session State
            st.session_state.current_device = {
                "name": name or "Platzhalter-Gerät",
                "typ": typ or "Platzhalter-Typ",
                "standort": standort or "Platzhalter-Standort",
                "status": status,
                "inventarnummer": inventarnummer or "DEV-XXXX",
            }
            st.success("Gerät wurde (im Mock-Up) angelegt und als aktuelles Gerät gespeichert.")

# ---------- Gerät ändern ----------
with tab2:
    st.header("✏️ Gerät ändern")
    st.write("Im Mock-Up wird das aktuell ausgewählte Gerät aus dem Session State geladen.")

    aktuelles_geraet = st.session_state.current_device

    st.info(
        f"Aktuelles Gerät aus Session State: **{aktuelles_geraet['name']}** "
        f"({aktuelles_geraet['inventarnummer']})"
    )

    with st.form("geraet_aendern_form"):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Gerätename", value=aktuelles_geraet["name"])
            typ = st.text_input("Gerätetyp", value=aktuelles_geraet["typ"])
            inventarnummer = st.text_input("Inventarnummer", value=aktuelles_geraet["inventarnummer"])

        with col2:
            standort = st.text_input("Standort", value=aktuelles_geraet["standort"])
            status = st.selectbox(
                "Status",
                ["verfügbar", "in Wartung", "defekt", "reserviert"],
                index=["verfügbar", "in Wartung", "defekt", "reserviert"].index(aktuelles_geraet["status"])
            )
            bemerkung = st.text_area("Bemerkungen", placeholder="Optionale Beschreibung")

        saved = st.form_submit_button("Änderungen speichern")

        if saved:
            # Wieder nur Mock: Session State überschreiben
            st.session_state.current_device.update({
                "name": name,
                "typ": typ,
                "standort": standort,
                "status": status,
                "inventarnummer": inventarnummer,
            })
            st.success("Änderungen wurden im Session State aktualisiert (Mock-Up).")

# ---------- Debug / Anzeige Session State ----------
with st.expander("Debug: Session State anzeigen"):
    st.write(st.session_state.current_device)