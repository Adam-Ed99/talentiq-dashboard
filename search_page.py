import streamlit as st
import pandas as pd

def render_search(df: pd.DataFrame):
    st.subheader("🔎 Advanced Search")

    with st.sidebar:
        st.markdown("### Filters")

        roles = st.multiselect(
            "Role",
            sorted(df["role"].dropna().unique()) if "role" in df.columns else []
        )

        locations = st.multiselect(
            "Location",
            sorted(df["location"].dropna().unique()) if "location" in df.columns else []
        )

        seniorities = st.multiselect(
            "Seniority",
            sorted(df["seniority"].dropna().unique()) if "seniority" in df.columns else []
        )

        remote_mode = st.selectbox(
            "Remote mode",
            ["All", "Remote", "Onsite", "Hybrid"]
        ) if "remote" in df.columns else None

        exp_min, exp_max = st.slider(
            "Years of experience",
            0, 30, (0, 10)
        ) if "experience_years" in df.columns else (None, None)

        skill_query = st.text_input(
            "Skill contains… (e.g. Python, AWS)"
        ) if "skills" in df.columns else ""

    df_f = df.copy()

    # Appliquer les filtres
    if "role" in df.columns and roles:
        df_f = df_f[df_f["role"].isin(roles)]

    if "location" in df.columns and locations:
        df_f = df_f[df_f["location"].isin(locations)]

    if "seniority" in df.columns and seniorities:
        df_f = df_f[df_f["seniority"].isin(seniorities)]

    if remote_mode and remote_mode != "All" and "remote" in df.columns:
        df_f = df_f[df_f["remote"] == remote_mode]

    if exp_min is not None and exp_max is not None and "experience_years" in df.columns:
        df_f = df_f[
            (df_f["experience_years"] >= exp_min) &
            (df_f["experience_years"] <= exp_max)
        ]

    if skill_query and "skills" in df.columns:
        df_f = df_f[
            df_f["skills"].fillna("").str.contains(skill_query, case=False)
        ]

    st.write(f"Profiles found: **{len(df_f)}**")

    st.dataframe(df_f.head(200))

    # Sauvegarder le df filtré pour l'export
    st.session_state["last_filtered_df"] = df_f
