import streamlit as st
import pandas as pd
from gestionale import formatta, aggiorna_file_github

st.title("📂 Registro Movimenti")
st.divider()

finanze = st.session_state.get("finanze", {})
movimenti = finanze.get("movimenti", [])

if movimenti:
    df = pd.DataFrame(movimenti)
    df = df.iloc[::-1].reset_index(drop=True)

    st.dataframe(df, use_container_width=True)

    st.divider()

    if st.button("🗑️ Reset Registro"):
        st.session_state.finanze["movimenti"] = []
        aggiorna_file_github(
            "data/finanze.json",
            st.session_state.finanze,
            "Reset registro movimenti"
        )
        st.success("Registro resettato correttamente.")
        st.rerun()
else:
    st.info("Nessun movimento registrato.")
