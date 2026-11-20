import pandas as pd
import plotly.express as px
import streamlit as st
from state import init_session_state

st.set_page_config(page_title="Game Statistics", layout="centered")

# Makes sure st.session_state["game_history"] exists even if this page is opened first.
init_session_state()

# Won / Lost colors: blue + orange, checked to stay distinguishable for colorblind readers.
RESULT_COLORS = {"Won": "#2a78d6", "Lost": "#eb6834"}

st.title("Player Statistics")

# ── 1. Read the saved history ─────────────────────────────────────────────────
# game_history is a list of finished games. Each game looks like:
#   {"game_id": "Game 1", "round_id": 5,
#    "rounds": [{"game_id": ..., "round_id": 1, "num_attempts": 2, "quality": 71.7}, ...]}
# Only the fields that round.py's end_round() actually saves are used below.
history = st.session_state["game_history"]


rows = []
for g in history:
    for r in g["rounds"]:
        rows.append({
            "Game": g["game_id"],
            "Round": r["round_id"],
            "Attempts": r["num_attempts"],
            "Quality": r["quality"],
        })

# ── 2. No finished games yet ──────────────────────────────────────────────────
if not rows:
    st.info("Haven't finished any games yet. Go to the start page and play one!")
    if st.button("Go to start page", type="primary"):
        st.switch_page("landpage.py")
    st.stop()

# ── 3. Build the table the page works from ───────────────────────────────────
df = pd.DataFrame(rows)

# A (Game, Round) pair is unique by design, so this only removes accidental repeats
# (for example if the same game was appended to game_history twice).
df = df.drop_duplicates(subset=["Game", "Round"]).reset_index(drop=True)

df["Quality"] = df["Quality"].round(1)

# round.py gives a lost round quality 0, and any won round at least
# 65 / MAX_ATTEMPTS points, so "quality above 0" means the round was won.
df["Result"] = df["Quality"].gt(0).map({True: "Won", False: "Lost"})

# Short label for the x-axis (the "Round" column stays a plain number).
df["Label"] = df["Game"] + " · R" + df["Round"].astype(str)

# ── 4. Headline numbers ──────────────────────────────────────────────────────
won = df["Result"] == "Won"

total_games = df["Game"].nunique()
win_rate = won.mean() * 100
avg_quality = df["Quality"].mean()
# Attempts for a lost round are always the maximum, so averaging only the won
# rounds gives a meaningful "how fast do you find it" number.
avg_attempts_won = f"{df.loc[won, 'Attempts'].mean():.1f}" if won.any() else "–"

m1, m2, m3, m4 = st.columns(4)
m1.metric("Games", total_games)
m2.metric("Win rate", f"{win_rate:.0f}%")
m3.metric("Avg quality", f"{avg_quality:.1f}")
m4.metric("Attempts / win", avg_attempts_won)

st.divider()

# ── 5. Quality per round ─────────────────────────────────────────────────────
st.subheader("Quality across rounds")

fig = px.bar(
    df,
    x="Label",
    y="Quality",
    color="Result",
    color_discrete_map=RESULT_COLORS,
    # keep rounds in play order (otherwise all "Won" bars would be grouped first)
    category_orders={"Label": df["Label"].tolist(), "Result": ["Won", "Lost"]},
    range_y=[0, 110],
)
if len(df) <= 15:  # value labels only while there is room for them
    fig.update_traces(texttemplate="%{y:.0f}", textposition="outside")
fig.update_layout(
    xaxis_title="Game & round",
    yaxis_title="Quality score (max 100)",
    legend_title_text="Result",
    bargap=0.35,
    height=400,
)

st.plotly_chart(fig)

st.divider()

# ── 6. Breakdown of one game ─────────────────────────────────────────────────
st.subheader("Game breakdown")

games = df["Game"].unique().tolist()
selected_game = st.selectbox(
    "Select a game:",
    games,
    index=len(games) - 1,  # newest game first
)

game_df = df[df["Game"] == selected_game][["Round", "Result", "Attempts", "Quality"]]
st.dataframe(game_df, hide_index=True)

st.divider()

# New games (and the region choice) are set up on the start page.
if st.button("Play another game", type="primary"):
    st.switch_page("landpage.py")
