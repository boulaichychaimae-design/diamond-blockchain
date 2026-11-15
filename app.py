import streamlit as st
from blockchain_core import Blockchain

st.title("Registre Blockchain - Diamonds")

bc = Blockchain.load_from_file("blockchain.json")

if st.button("Vérifier la chaîne"):
    if bc.is_valid():
        st.success("Chaîne VALIDE ✅")
    else:
        st.error("Chaîne INVALIDE ❌ - Triche détectée !")

st.subheader(f"Total blocs : {len(bc.chain)}")
for b in bc.chain:
    st.write(f"--- Block {b.index} ---")
    st.write(f"Date : {b.timestamp}")
    st.write(f"Data : {b.data}")
    st.write(f"Hash : {b.hash}")
    st.write(f"Previous : {b.previous_hash}")
