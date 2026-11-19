import pandas as pd
import streamlit as st

import re
import plotly.express as px
from openai import OpenAI

st.set_page_config(page_title="Game Rounds")

DEFAULT_API_KEY = "sk-oaYuig_9CsU85oLW3AIv9A"

# ── ask for API Key, stop if not yet provided  ────────────────────────────────────────────
with st.sidebar:
    api_key = st.text_input(
        "UOS AI API-Key",
        value=DEFAULT_API_KEY,
        type="password",
        key="uos_api_key",
        placeholder="sk-...",
    ).strip()
    
if not api_key:
    st.info("Please enter your Uni Osnabrück API key. If you don't have one, you can obtain it from https://ai-keys.uni-osnabrueck.de.")
    st.stop()
    
# pass the entered key
client = OpenAI(
    base_url="https://litellm.uni-osnabrueck.de/v1",
    api_key=api_key
)

MODEL = "google/gemma-4-E4B-it"   # same model as in your sample

DEFAULT_HINT_TEMPLATE = """\
two famous people (comma separated and give specific names):
two famous food (comma separated):
sentence-long greeting in the national language including stereotypical name of a citizen of that country, their job and a hobby (include a romanized transliteration beside the original language text if the language does not use the Latin script):
flag colors:"""


def generate_default_hints(country):
    prompt = (
        "You are the hint giver in a country guessing game. "
        f"The secret country is {country}. "
        "Fill in the template below with short, factual hints about this country. "
        "Never write the country's name, its capital, or its demonym (e.g. 'German'). "
        "Reply with only the filled-in template, with the fields separated by the | character, "
	"in the form: label: value | label: value | label: value\n\n"
        f"{DEFAULT_HINT_TEMPLATE}"
    )
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return response.choices[0].message.content

def generate_random_hint(country, old_hints, hint_count):
    prompt = (
        "You are the hint giver in a country guessing game. "
        f"The secret country is {country}. "
        "Provide a short sentence containing a notable factual hint about this country. You have been provided with a dictionary {old_hints} containing old hints so take care to generate something without any overlap with the old hints. "
        "Never write the country's name, its capital, or its demonym (e.g. 'German'). "
        "Reply with only the filled-in template in the form: hint_{hint_count}: \"hint string\""
    )
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return response.choices[0].message.content


def parse_hints(raw):
    hint_list = []
    for part in re.split(r"[|\n]", raw.replace("**", "")):
        part = part.strip().lstrip("-*• ").strip()
        label, sep, value = part.partition(":")
        if sep and value.strip():
            hint_list.append(value.strip())
    KEYS = ["people", "food", "greeting", "flag_colors"]

    if len(hint_list) == len(KEYS):
        hints_dict = dict(zip(KEYS, hint_list))
    else:
        st.error("The model's reply didn't have all four hints. Please try again.")
    return hints_dict

#Regional list of countries
EUROPE = {
    "United Kingdom": "GBR",
    "France": "FRA",
    "Germany": "DEU",
    "Italy": "ITA",
    "Spain": "ESP",
    "Portugal": "PRT",
    "Poland": "POL",
    "Sweden": "SWE",
    "Norway": "NOR",
    "Finland": "FIN",
    "Greece": "GRC",
    "Ireland": "IRL",
    "Austria": "AUT",
    "Switzerland": "CHE",
    "Romania": "ROU",
    "Ukraine": "UKR",
}

st.title("Guess the Country")

df = pd.DataFrame({"country": list(EUROPE), "iso": list(EUROPE.values())})

fig = px.choropleth(
    df,
    locations="iso",
    locationmode="ISO-3",
    color="country",
    color_discrete_sequence=px.colors.qualitative.Alphabet,
    hover_name="country",
    hover_data={"iso": False},
    scope="europe",
)
fig.update_geos(showcountries=True)
fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
fig.update_traces(hovertemplate="%{hovertext}<extra></extra>")

st.plotly_chart(fig)

st.session_state.random_hint_count = 0
TARGET = "Russia"   # hard-coded for now

if st.button("Generate default hints"):
    try:
        with st.spinner("Generating hints …"):
            raw_hints = generate_default_hints(TARGET)
            st.session_state.hints_dict = parse_hints(raw_hints)
        st.write(st.session_state.hints_dict)
    except AuthenticationError:
        st.error("API key was not accepted. Please check it.")
    except OpenAIError:
        st.error("AI request failed. Please try again.")

if st.button("Generate Random Hint", disabled="hints_dict" not in st.session_state):
    try:
        with st.spinner("Generating random hint …"):
            rand_hint = generate_random_hint(TARGET, st.session_state.hints_dict, st.session_state.random_hint_count)
            # add rand_hint into st.session_state.hints_dict #####
            st.session_state.random_hint_count += 1
            st.write(rand_hint)
    except AuthenticationError:
        st.error("API key was not accepted. Please check it.")
    except OpenAIError:
        st.error("AI request failed. Please try again.")
