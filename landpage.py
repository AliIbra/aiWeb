import streamlit as st
import textwrap

if "game_started" not in st.session_state:
    st.session_state.game_started = False

if not st.session_state.game_started:
    st.title("How culturly base are you")

# Explanation

st.markdown(textwrap.dedent("""\
    ### Game Rules
    Welcome to the game!

    **Game Objectives:**
    Guess the name of the country from the map  
    Survive 5 rounds without running out of guesses.

    **Game Rules:**  
    Good day and welcome! Here we will play the Guess the Country game:
    * Each game consists of 5 rounds. During each round, you are asked to guess the name of a country (**Secret Word**).
    * Each **Secret Word** comes with 5 progressive **Hints**.
    * Users have 4 attempts in each round.
    * The score is calculated based on the number of attempts used and hints consumed until the right answer.
    * If a user consumes all 4 allowed attempts in a round, it is **Game Over**.
    * Users cannot skip any round. If you get stuck, you can rerun the game, and the previous game will count as a loss.

    **How to calculate your score:**  
    **
"""))


st.divider()

if st.button("Start Game", type="primary", use_container_width=True):
    st.switch_page("pages/round.py")

if st.button("Stats", type= "primary", use_container_width= True):
    st.switch_page("pages/statistics.py")
