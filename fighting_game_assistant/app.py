import streamlit as st
from chains.combo_chain import get_combo_chain

st.set_page_config(page_title="Fighting Game Assistant")

st.title("🎮 Fighting Game Combo Assistant")

game = st.text_input("Enter the Fighting Game")
character = st.text_input("Enter the Character")

skill_level = st.selectbox(
    "Select Skill Level",
    ["Beginner", "Intermediate", "Advanced"]
)

if st.button("Generate Combos & Tips"):
    if not game or not character:
        st.warning("Please enter both game and character.")
    else:
        with st.spinner("Training mode loading..."):
            chain = get_combo_chain()
            response = chain.invoke({
                "game": game,
                "character": character,
                "skill_level": skill_level
            })

        st.markdown("## 🥋 Results")
        st.markdown(response.content)
