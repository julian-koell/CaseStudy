import streamlit as st

if "sb_current_device" not in st.session_state:
    st.session_state.sb_current_device = ""

# Eine Überschrift der ersten Ebene
st.write("# Wartungsmanagement")

# Eine Überschrift der zweiten Ebene
st.write("## Geräteauswahl")

# Eine Auswahlbox mit hard-gecoded Optionen, das Ergebnis

st.session_state.sb_current_device = st.selectbox(label='Gerät auswählen',
        options = ["Gerät_A", "Gerät_B"])

st.write(f"Das ausgewählte Gerät ist {st.session_state.sb_current_device}")

#UI ELEMENTE BEISPIEL
st.write("## Wartungskosten")

# Callbacks for the number inputs
def update_price_from_euro():
    st.session_state.price_dollar = st.session_state.price_euro * 1.1

def update_price_from_dollar():
    st.session_state.price_euro = st.session_state.price_dollar * 0.9

# Number inputs for the maintenance costs
st.number_input(label="Wartungskosten in Euro", 
                            key = "price_euro",
                            on_change=update_price_from_euro)

st.number_input(label="Wartungskosten in Dollar", 
                            key = "price_dollar",
                            on_change=update_price_from_dollar)