import streamlit as st
from typing import List, Optional
from tinydb import TinyDB, Query

DB_PATH = "app_db.json"


def get_db() -> TinyDB:
    return TinyDB(DB_PATH)


def init_db() -> None:
   
    db = get_db()
    db.close()


class User:
    def __init__(self, id: str, name: str) -> None:
       
        self.id = (id or "").strip().lower()
        self.name = (name or "").strip()

    def store_data(self) -> None:
        
        if not self.id or "@" not in self.id:
            raise ValueError("Ungültige E-Mail.")
        if not self.name:
            raise ValueError("Bitte einen Namen eingeben.")

        # Nutzer darf noch nicht existieren
        if User.find_by_attribute("id", self.id) is not None:
            raise ValueError("Nutzer existiert bereits.")

        db = get_db()
        users_table = db.table("users")
        users_table.insert({"id": self.id, "name": self.name})
        db.close()

    def delete(self) -> None:
   
        db = get_db()
        users_table = db.table("users")
        UserQ = Query()
        users_table.remove(UserQ.id == self.id)
        db.close()

    def __str__(self):
        return f"User {self.id} - {self.name}"

    def __repr__(self):
        return self.__str__()

    @classmethod
    def find_all(cls) -> List["User"]:
    
        db = get_db()
        users_table = db.table("users")
        rows = users_table.all()
        db.close()

        # Sortierung
        rows.sort(key=lambda r: (r.get("name") or "").lower())
        return [cls(id=r["id"], name=r["name"]) for r in rows]

    @classmethod
    def find_by_attribute(cls, by_attribute: str, attribute_value: str) -> Optional["User"]:
        
        if by_attribute not in ("id", "name"):
            raise ValueError("by_attribute muss 'id' oder 'name' sein.")

        value = (attribute_value or "").strip()
        if by_attribute == "id":
            value = value.lower()

        db = get_db()
        users_table = db.table("users")
        UserQ = Query()

        if by_attribute == "id":
            row = users_table.get(UserQ.id == value)
        else:
            row = users_table.get(UserQ.name == value)

        db.close()

        return cls(id=row["id"], name=row["name"]) if row else None


st.set_page_config(page_title="Nutzer-Verwaltung", layout="wide")
init_db()

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
            email = st.text_input("E-Mail-Adresse", placeholder="T.Schranzhofer@gmx.at")
        with col2:
            name = st.text_input("Name", placeholder="Tobias Schranzhofer")

        submitted = st.form_submit_button("Nutzer anlegen")

        if submitted:
            try:
                u = User(email, name)
                u.store_data()
                st.success("Nutzer wurde angelegt.")
                st.rerun()
            except ValueError as e:
                st.error(str(e))
