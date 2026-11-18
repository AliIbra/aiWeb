import streamlit as st
import pandas as pd

st.header(" Game Statistics ")

if "game_history" not in st.session_state:
    st.session_state.game_history = [
        {
            "game_id": "Game 1",
            "rounds": [
                {"round_num": 1, "guesses": 2, "hints": 1, "s_hints": 0, "quality": 88},
                {"round_num": 2, "guesses": 3, "hints": 0, "s_hints": 1, "quality": 75},
                {"round_num": 3, "guesses": 1, "hints": 0, "s_hints": 0, "quality": 95},
                {"round_num": 4, "guesses": 4, "hints": 2, "s_hints": 0, "quality": 68},
                {"round_num": 5, "guesses": 2, "hints": 1, "s_hints": 0, "quality": 88}
            ]
        },
        {
            "game_id": "Game 2",
            "rounds": [
                {"round_num": 1, "guesses": 4, "hints": 1, "s_hints": 0, "quality": 82},
                {"round_num": 2, "guesses": 2, "hints": 0, "s_hints": 0, "quality": 90},
                {"round_num": 3, "guesses": 4, "hints": 1, "s_hints": 1, "quality": 63},
                {"round_num": 4, "guesses": 1, "hints": 0, "s_hints": 0, "quality": 95},
                {"round_num": 5, "guesses": 3, "hints": 2, "s_hints": 0, "quality": 71}
            ]
        }
    ]


#if "game_history" not in st.session_state:
    #st.session_state.game_history = []

history = st.session_state.game_history

if not history:
    st.info("Haven't finished any games yet. Go to the Game round page and try it out!")
else:
    all_rounds_data = []
    for game in history:
        for r in game["rounds"]:
            all_rounds_data.append({
                "game_id": game["game_id"],
                "round_num": r.get("round_num"),
                "guesses": r.get("guesses"),
                "hints": r.get("hints"),
                "s_hints": r.get("s_hints"),
                "quality": r.get("quality")
            })
               

if not all_rounds_data:
    st.warning("Haven't finished any games yet. Go to the Game round page and try it out!")
else:
    df = pd.DataFrame(all_rounds_data)

    total_games_played = len(history)
    total_rounds_played = len(df)
    avg_guesses = df["guesses"].mean()
    avg_quality = df["quality"].mean()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric(label="Total Games", value=total_games_played)
    col2.metric(label="Total Rounds", value=total_rounds_played)
    col3.metric(label="Avg. Guesses / Round", value=round(avg_guesses, 1))
    col4.metric(label="Avg. Quality Score", value=f"{round(avg_quality, 1)}%")

    st.divider()

    st.subheader("Number of guesses per round")
    chart_data = df.pivot(index="round_num", columns="game_id", values="guesses")
    st.bar_chart(chart_data)

    expander = st.expander("See quality score formula explanation")
    expander.write("""
    The quality score for each round is calculated based on the following formula:
        
    $$\\text{Quality} = 100 - (5 \\times \\text{guesses}) - (2 \\times \\text{hints}) - (10 \\times \\text{s\\_hints})$$
        
    * **Guesses**: Each attempt deducts 5 points.
    * **Hints**: Each regular hint consumed deducts 2 points.
    * **Special Hints**: Each special hint consumed deducts 10 points.
    """)
