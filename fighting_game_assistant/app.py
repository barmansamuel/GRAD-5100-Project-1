# app.py

import streamlit as st
from chains.combo_chain import get_combo_chain, ValidationError, NoDataError
from services.validator import get_all_games, get_characters

st.set_page_config(page_title="Fighting Game Assistant", page_icon="🎮")

st.title("🎮 Fighting Game Combo Assistant")

# ── Game selector (dropdown, driven from allowlist) ───────────────────────────
games = get_all_games()
game = st.selectbox("Select a Fighting Game", options=["— choose a game —"] + games)

# ── Character selector (dropdown, updates when game changes) ──────────────────
if game and game != "— choose a game —":
    characters = get_characters(game)
    character = st.selectbox(
        "Select a Character",
        options=["— choose a character —"] + characters,
    )
else:
    character = st.selectbox(
        "Select a Character",
        options=["— choose a game first —"],
        disabled=True,
    )

# ── Skill level ───────────────────────────────────────────────────────────────
skill_level = st.selectbox(
    "Select Skill Level",
    ["Beginner", "Intermediate", "Advanced"],
)

# ── Generate ──────────────────────────────────────────────────────────────────
if st.button("Generate Combos & Tips", type="primary"):
    # Guard: both selections must be real choices
    if game == "— choose a game —":
        st.warning("Please select a game.")
    elif not character or character in ("— choose a character —", "— choose a game first —"):
        st.warning("Please select a character.")
    else:
        with st.spinner("Scraping wikis and building context…"):
            try:
                chain = get_combo_chain()
                response = chain.invoke({
                    "game": game,
                    "character": character,
                    "skill_level": skill_level,
                })
                st.markdown("## 🥋 Results")
                st.markdown(response.content)

            except ValidationError as e:
                # Game or character not in allowlist
                st.error(f"❌ Invalid selection: {e}")

            except NoDataError as e:
                # Scraping succeeded but no usable data came back
                st.warning(f"⚠️ {e}")

            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")