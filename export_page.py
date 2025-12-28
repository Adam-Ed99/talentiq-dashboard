import streamlit as st
import pandas as pd
import io

def render_export(df: pd.DataFrame):
    st.subheader("📥 Export Profiles")

    if "last_filtered_df" in st.session_state:
        df_export = st.session_state["last_filtered_df"]
        st.write(f"Exporting filtered selection: **{len(df_export)}** profiles.")
    else:
        st.info("No filters applied yet. Exporting full dataset.")
        df_export = df

    st.dataframe(df_export.head(100))

    buffer = io.StringIO()
    df_export.to_csv(buffer, index=False)
    csv_data = buffer.getvalue()

    st.download_button(
        label="Download as CSV",
        data=csv_data,
        file_name="talentiq_export.csv",
        mime="text/csv"
    )
