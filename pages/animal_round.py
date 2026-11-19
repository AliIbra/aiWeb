import streamlit as st
import random
from state import init_session_state, start_new_game, end_current_game_early
import json
from pathlib import Path
import os 

# ______ session initiation and helper function _________ #
init_session_state()

# data loading
@st.cache_data # instead of reading each time
def load_data():
    #base_dir = os.path.dirname(os.path.abspath(__file__))
    #file_path = os.path.join(base_dir, "..", "data", "animals.json")
    path = Path(__file__).resolve().parent.parent / "data" / "animals.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

animals_list = load_data()

# global variables
total_rounds= 5
max_guesses = 5

# a helper function for round initiation
def init_round():
    used_animals = st.session_state.get("used_animals", [])
    avialable = [a for a in animals_list if a["name"] not in used_animals]
    target = random.choice(avialable if avialable else animals_list)

    st.session_state["round_data"] = {
        "target": target,
        "guesses": [],
        "hints_used": 0,
        "s_hints_used": 0,
        "round_over": False,
        "won": False,
    }

# a helper function to calculate the quality of the quesses based on the following:      
# guesses: each failed attempt deducts 5 points.
# hints: each regular hint consumed deducts 2 points.
# special hints: each special hint consumed deducts 10 points.
def calculate_quality(guesses_count, hints_used, s_hints_used, won):
    if not won:
        return 0

    failed_attempts= guesses_count -1
    score = 100 - (failed_attempts * 5) - (hints_used * 2) - (s_hints_used * 10)
    return max(0, score) # to execlude negative values, in case a player has a very bad luck  

# fresh round initialization
if "round_data" not in st.session_state:
    st.session_state["used_animals"] = []
    init_round()

# variables initiation
current_game = st.session_state["current_game"]
round_id = len(current_game["rounds"]) + 1
round_data = st.session_state["round_data"]
target = round_data["target"]


# ____ layout start here __________#
st.title(f"{current_game['game_id']} — Round {min(round_id, total_rounds)} of {total_rounds}")
st.progress(len(current_game["rounds"]) / total_rounds)

# end of a single game case (5 rounds)
if len(current_game["rounds"]) >= total_rounds:
    st.success(f"{current_game["game_id"]} complete")
    st.json(current_game)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Next Game", type="primary", use_container_width=True):
            st.session_state["used_animals"] = []
            start_new_game()
            init_round()
            st.rerun()
    with col2:
        if st.button("View Statistics", use_container_width= True):
            st.switch_page("pages/statistics.py")
    
    st.stop()

# hints section
st.subheader("Hints")
h_col1, h_col2 = st.columns(2)

# regular hint
with h_col1:
    if round_data["hints_used"] == 0:
        if st.button("Primary Hints", disabled=round_data["round_over"], use_container_width= True):
            round_data["hints_used"]= 1
            st.rerun()
    else:
        st.info(f"**Hints** {target["hint"]}")

# special hint
with h_col2:
    if round_data["s_hints_used"] == 0:
        if st.button("Special Hint", disabled=round_data["round_over"], use_container_width= True):
            round_data["s_hints_used"] =1
            st.rerun()
    else:
        st.warning(f"**special hint** {target['s_hint']}")

# guessing Form
if not round_data["round_over"]:
    animals_names = [a["name"] for a in animals_list if a["name"] not in round_data["guesses"]]
    left_attempts = max_guesses - len(round_data["guesses"])
    st.write(f"**Number of remaining attempts** {left_attempts}")


    with st.form("gussing_form"):
        guess = st.selectbox("Pick the animal:", animals_names)
        submitted= st.form_submit_button("Submit a Guess", type="primary")

        if submitted:
            round_data["guesses"].append(guess)
            if guess== target["name"]:
                round_data["won"]= True
                round_data["round_over"]= True
            elif len(round_data["guesses"]) >= max_guesses:
                round_data["round_over"]= True
            st.rerun()
if round_data["guesses"] and not round_data["round_over"]:
    last_guess = round_data["guesses"][-1]
    st.error(f"**{last_guess}** is not the secret word! Try again.")

# display the previous guesses
if round_data["guesses"]:
    st.write("**previous guesses**" + ", ".join(round_data["guesses"]))

# end a round and start a new one
if round_data["round_over"]:
    guesses_count = len(round_data["guesses"])
    # calculate the quality of the guesses
    quality = calculate_quality(
        guesses_count,
        round_data["hints_used"],
        round_data["s_hints_used"],
        round_data["won"],
    )
    # display the result
    if round_data["won"]:
        st.success(f"You answer is right **{target['name']}**")
    else:
        st.error(f"Sorry you are out of attempts, the right answer was **{target['name']}**")

    # end of rounds case
    btn_fin =  "Next Round" if round_id < total_rounds else "Finish Game"
    if st.button(btn_fin, type="primary"):
        current_game["rounds"].append({
            "round_id": round_id,
            "guesses": guesses_count,
            "hints": round_data["hints_used"],
            "s_hints": round_data["s_hints_used"],
            "quality": quality,
        })

        st.session_state["used_animals"].append(target["name"])
        if len(current_game["rounds"]) >= total_rounds:
            st.session_state["game_history"].append(current_game)
        init_round()
        st.rerun()


# in case a player wants out
st.divider()
if st.button("End Game Early"):
    end_current_game_early()
    st.switch_page("landpage.py")

# back to start page
if st.button("Go back to start"):
    st.switch_page("landpage.py")