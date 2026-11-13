import streamlit as st

if "game_started" not in st.session_state:
    st.session_state.game_started = False

if not st.session_state.game_started:
    st.title("How culturly base are you")

    # Explanation
    st.markdown("""
        ### Game Rules:
        Welcom to the game ...

        **Game Objectives:** survive 5 rounds without running out of guesses
        **Game Rules:** 
        **How to calculate your score:** 
    """)

    st.divider()

    if st.button("Start Game", type="primary", use_container_width=True):
        st.switch_page("pages/round.py")
