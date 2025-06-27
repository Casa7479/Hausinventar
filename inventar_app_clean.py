
import streamlit as st
import pandas as pd
import uuid

st.set_page_config(page_title="Hausinventar", layout="wide")
st.title("📦 Hausinventar – Räume, Schränke, Boxen & Artikel")

# Initialize session state
if "inventory" not in st.session_state:
    st.session_state.inventory = []

# Eingabeformular
with st.form("add_item"):
    st.subheader("➕ Artikel hinzufügen")
    col1, col2, col3 = st.columns(3)

    with col1:
        room = st.text_input("🏠 Raum", placeholder="z. B. Keller")
    with col2:
        cabinet = st.text_input("🗄️ Schrank / Regal", placeholder="z. B. Regal A4")
    with col3:
        box = st.text_input("📦 Box (Nummer)", placeholder="z. B. Box001")

    item_name = st.text_input("🔖 Artikelname", placeholder="z. B. Schlafsack")
    item_description = st.text_area("Beschreibung", placeholder="Kurze Notiz...")
    uploaded_image = st.file_uploader("📷 Foto hinzufügen", type=["png", "jpg", "jpeg"])

    submitted = st.form_submit_button("✅ Speichern")

    if submitted and item_name and room and box:
        item_id = str(uuid.uuid4())
        st.session_state.inventory.append({
            "ID": item_id,
            "Raum": room,
            "Schrank": cabinet,
            "Box": box,
            "Artikel": item_name,
            "Beschreibung": item_description,
            "Bild": uploaded_image,
        })
        st.success(f"✅ Artikel **{item_name}** wurde gespeichert!")

# Suchfunktion
st.divider()
st.subheader("🔍 Suche & Übersicht")

search_term = st.text_input("Suche nach Artikel, Box oder Raum")

# Ergebnisse anzeigen
if st.session_state.inventory:
    filtered_items = [
        item for item in st.session_state.inventory
        if search_term.lower() in item["Artikel"].lower()
        or search_term.lower() in item["Box"].lower()
        or search_term.lower() in item["Raum"].lower()
    ]

    for item in filtered_items:
        with st.expander(f"📦 {item['Artikel']} ({item['Raum']} > {item['Schrank']} > {item['Box']})"):
            st.write(f"**Beschreibung:** {item['Beschreibung']}")
            st.write(f"**Raum:** {item['Raum']}")
            st.write(f"**Schrank:** {item['Schrank']}")
            st.write(f"**Box:** {item['Box']}")
            if item["Bild"] is not None:
                st.image(item["Bild"], width=200)
else:
    st.info("Noch keine Artikel hinzugefügt.")

# CSV Export
st.divider()
if st.session_state.inventory:
    if st.button("📤 CSV-Export"):
        df = pd.DataFrame(st.session_state.inventory)
        st.download_button("📥 Download CSV", data=df.to_csv(index=False), file_name="hausinventar.csv", mime="text/csv")
