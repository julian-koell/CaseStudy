import streamlit as st
from tinydb import TinyDB, Query
from users import User

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
