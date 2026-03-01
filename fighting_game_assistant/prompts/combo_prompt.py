from langchain_core.prompts import PromptTemplate

combo_prompt = PromptTemplate(
    input_variables=["game", "character", "skill_level"],
    template="""
You are a professional fighting game coach.

Game: {game}
Character: {character}
Skill Level: {skill_level}

Provide:

0. Explanation of the notation
1. 5 optimal combos appropriate for the skill level
2. Execution tips
3. Common mistakes (if beginner/intermediate)
4. 3 matchup tips
5. Practice drills

Be structured and clear.
"""
)
