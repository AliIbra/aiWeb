import streamlit as st
import pandas as pd
import plotly.express as px
from state import init_session_state


# if "game_history" not in st.session_state:
#    st.session_state.game_history = [
#        {
#            "game_id": "Game 1",
#            "rounds": [
#                {"round_num": 1, "guesses": 2, "hints": 1, "s_hints": 0, "quality": 88},
#                {"round_num": 2, "guesses": 3, "hints": 0, "s_hints": 1, "quality": 75},
#                {"round_num": 3, "guesses": 1, "hints": 0, "s_hints": 0, "quality": 95},
#                {"round_num": 4, "guesses": 4, "hints": 2, "s_hints": 0, "quality": 68},
#                {"round_num": 5, "guesses": 2, "hints": 1, "s_hints": 0, "quality": 88}
#            ]
#        },
#        {
#            "game_id": "Game 2",
#            "rounds": [
#                {"round_num": 1, "guesses": 4, "hints": 1, "s_hints": 0, "quality": 82},
#                {"round_num": 2, "guesses": 2, "hints": 0, "s_hints": 0, "quality": 90},
#                {"round_num": 3, "guesses": 4, "hints": 1, "s_hints": 1, "quality": 63},
#                {"round_num": 4, "guesses": 1, "hints": 0, "s_hints": 0, "quality": 95},
#                {"round_num": 5, "guesses": 3, "hints": 2, "s_hints": 0, "quality": 71}
#            ]
#        }
#    ] """


#if "game_history" not in st.session_state:
    #st.session_state.game_history = []

st.set_page_config(page_title= "Game Statistics", layout= "centered")


init_session_state()

st.title("Player Statistics")
# read the saved history
history = st.session_state["game_history"]

# no history case
if not history:
    st.info("Haven't finished any games yet. Go to the Game round page and try it out!")
    if st.button("Go to Game", type="primary"):
        st.switch_page("pages/round.py")
    st.stop()

# convert json (stats) to pandas df
rows = []
for g in history:
    for r in g["rounds"]:
        rows.append({
            "Game": g["game_id"],
            "Round": r["round_id"],
            "Guesses": r["guesses"],
            "Hints": r["hints"],
            "Special Hints": r["s_hints"],
            "Quality score": r["quality"],
            "won": r["quality"] > 0,
        })

df = pd.DataFrame(rows)

# extract variables
total_games = len(history)
total_rounds = len(df)
win_avg = (df["won"].sum() / total_rounds) * 100
avg_quality = df["Quality score"].mean()
avg_guesses= df["Guesses"].mean()

# the graph 4 sections:
bar1, bar2, bar3, bar4 = st.columns(4)
bar1.metric("Game Played", total_games)
bar2.metric("Win Rate", f"{win_avg:.0f}%")
bar3.metric("Avg Quality", f"{avg_quality:.1f}/ 100")
bar4.metric("Avg Guesses", f"{avg_guesses:.1f}")

st.divider()

# scores according to the round
st.subheader("Quality across rounds")
df["Round"] = df["Game"] + " - R" + df["Round"].astype(str)


# creating the bar chart
fig = px.bar(
    df,
    x = "Round",
    y= "Quality score",
    color= "Game",
    text= "Quality score",
    range_y = [0,100],
)
# positioning
fig.update_traces(textposition="outside")

# chart display config
fig.update_layout(
    xaxis_title= "Game & Round",
    yaxis_title = "Quality Score",
    showlegend= True,
    height = 400,
)

# Streamlit's render
st.plotly_chart(fig, use_container_width= True)

st.divider()

# deatialed statistics for each game played
# individual game breakdown
st.subheader("Game Breakdown")
# select the game that you want to see
selected_game= st.selectbox("Please select a game to breakdown: ", [g["game_id"] for g in history])

# create a dataframe for the selected game
game_df = df[df["Game"] == selected_game][["Round", "Guesses", "Hints", "Special Hints", "Quality score"]]
st.dataframe(game_df, use_container_width= True, hide_index=True)

st.divider()

nav1, nav2 = st.columns(2)
with nav1:
    if st.button("Back to Home", use_container_width=True):
        st.switch_page("landpage.py")
with nav2:
    if st.button("Play Another Game", type="primary", use_container_width=True):
        st.switch_page("pages/round.py")



        
#    st.subheader("Number of guesses per round")
#    chart_data = df.pivot(index="round_num", columns="game_id", values="guesses")
#    st.bar_chart(chart_data)

#    expander = st.expander("See quality score formula explanation")
#    expander.write("""
#    #The quality score for each round is calculated based on the following formula:
        
#    #$$\\text{Quality} = 100 - (5 \\times \\text{guesses}) - (2 \\times \\text{hints}) - (10 \\times \\text{s\\_hints})$$
        
#    #* **Guesses**: Each attempt deducts 5 points.
#    #* **Hints**: Each regular hint consumed deducts 2 points.
#    #* **Special Hints**: Each special hint consumed deducts 10 points.
#    """)
# if st.button("Go back to start"):
 #   st.switch_page("landpage.py") """