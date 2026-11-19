# To be used as a global (central) variables' manger
import streamlit as st

# a function for a safe var setup acroos pages
def init_session_state():
    # completed games history 
    if "game_history" not in st.session_state:
        st.session_state["game_history"] = []

    # active multi-round game tracker
    if "game_active" not in st.session_state:
        st.session_state["game_active"] = False

    if "current_game" not in st.session_state:
        start_new_game()

# helper function to generate consequential games_id(s)
def start_new_game():
    next_game_id = len(st.session_state["game_history"]) + 1
    st.session_state["current_game"] = {
        "game_id": f"Game {next_game_id}",
        "rounds": [],
    }
    st.session_state["game_active"] = True


def end_current_game_early():
    current = st.session_state["current_game"]
    if len(current["rounds"]) > 0:
        st.session_state["game_history"].append(current)
    start_new_game()
    st.session_state["game_active"] =False