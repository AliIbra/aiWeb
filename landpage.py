import streamlit as st
import textwrap
from state import init_session_state

st.set_page_config(
    page_title= "Europe Country Guesser",
    page_icon= "Q",
    layout= "centered"
)

# initialize state upon each render of the landing page
init_session_state()

st.title("How Geograpgically Based Are You")

# game explanation
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

    **How the score is calculated:**
    * The total score is 100.  
    * Guesses: each failed attempt deducts 5 points.
    * Rregular hints: each regular hint consumed deducts 2 points.
    * Special hints: each special hint consumed deducts 10 points.
"""))


st.divider() 

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Start", type="primary", use_container_width=True):
        # refreash the content of the game
        st.session_state.game_active= False
        st.switch_page("pages/round.py")

with col2:
    if st.button("Start Animal Guessing Game", use_container_width= True):
        st.session_state.game_active = False
        st.switch_page("pages/animal_round.py")

with col3:
    if st.button("view statistics", use_container_width=True):
        st.switch_page("pages/statistics.py")

