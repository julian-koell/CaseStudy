import streamlit as st
import sqlite3
from typing import List, Optional

DB_PATH = "app.db"

def init_db() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id   TEXT PRIMARY KEY,   -- E-Mail
                name TEXT NOT NULL
            )
        """)
        conn.commit()



class User:
    def __init__(self, id: str, name: str) -> None:
        """Create a new user based on the given name and id (id = E-Mail)"""
        self.id = (id or "").strip().lower()
        self.name = (name or "").strip()

    def store_data(self) -> None:
        """Save the user to the database"""
        if not self.id or "@" not in self.id:
            raise ValueError("Bitte eine gültige E-Mail-Adresse eingeben (id).")
        if not self.name:
            raise ValueError("Bitte einen Namen eingeben.")

        # Vorbedingung: Nutzer darf noch nicht existieren
        if User.find_by_attribute("id", self.id) is not None:
            raise ValueError("Nutzer existiert bereits (E-Mail ist schon vergeben).")

        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("INSERT INTO users (id, name) VALUES (?, ?)", (self.id, self.name))
            conn.commit()

    def delete(self) -> None:
        """Delete the user from the database"""
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("DELETE FROM users WHERE id = ?", (self.id,))
            conn.commit()

    def __str__(self):
        return f"User {self.id} - {self.name}"

    def __repr__(self):
        return self.__str__()

    @classmethod
    def find_all(cls) -> List["User"]:
        """Find all users in the database"""
        with sqlite3.connect(DB_PATH) as conn:
            rows = conn.execute(
                "SELECT id, name FROM users ORDER BY name COLLATE NOCASE"
            ).fetchall()
        return [cls(id=r[0], name=r[1]) for r in rows]

    @classmethod
    def find_by_attribute(cls, by_attribute: str, attribute_value: str) -> Optional["User"]:
        """From the matches in the database, select the user with the given attribute value"""
        if by_attribute not in ("id", "name"):
            raise ValueError("by_attribute muss 'id' oder 'name' sein.")

        value = (attribute_value or "").strip()
        if by_attribute == "id":
            value = value.lower()

        with sqlite3.connect(DB_PATH) as conn:
            row = conn.execute(
                f"SELECT id, name FROM users WHERE {by_attribute} = ? LIMIT 1",
                (value,),
            ).fetchone()

        return cls(id=row[0], name=row[1]) if row else None





st.set_page_config(page_title="Nutzer-Verwaltung", layout="wide")
init_db()

st.title("Nutzer-Verwaltung")
st.caption("Administrator: Nutzer anlegen, anzeigen und löschen (id = E-Mail, name = Nutzername)")

tab_list, tab_create = st.tabs(["Nutzer anzeigen / löschen", "Neuen Nutzer anlegen"])

# --- Tab 1: Anzeigen / Löschen
with tab_list:
    st.subheader("Nutzer anzeigen / löschen")

    users = User.find_all()
    if not users:
        st.info("Noch keine Nutzer vorhanden. Lege zuerst einen Nutzer im zweiten Tab an.")
    else:
        # Auswahlbox
        label_to_id = {f"{u.name} ({u.id})": u.id for u in users}
        selected_label = st.selectbox("Nutzer auswählen", list(label_to_id.keys()))
        selected_id = label_to_id[selected_label]

        user = User.find_by_attribute("id", selected_id)

        if user is None:
            st.warning("Nutzer wurde nicht gefunden (evtl. gerade gelöscht).")
        else:
            col1, col2 = st.columns(2)
            with col1:
                st.text_input("E-Mail (id)", value=user.id, disabled=True)
            with col2:
                st.text_input("Name (name)", value=user.name, disabled=True)

            st.divider()
            if st.button("Nutzer löschen", type="primary"):
                user.delete()
                st.success("Nutzer wurde gelöscht.")
                st.rerun()

# --- Tab 2: Anlegen
with tab_create:
    st.subheader("Neuen Nutzer anlegen")

  
    with st.form("nutzer_anlegen_form"):
        col1, col2 = st.columns(2)
        with col1:
            email = st.text_input("E-Mail-Adresse (id)", placeholder="max.mustermann@example.com")
        with col2:
            name = st.text_input("Name (name)", placeholder="Max Mustermann")

        submitted = st.form_submit_button("Nutzer anlegen")

        if submitted:
            try:
                u = User(email, name)
                u.store_data()
                st.success("Nutzer wurde angelegt.")
                st.rerun()
            except ValueError as e:
                st.error(str(e))
