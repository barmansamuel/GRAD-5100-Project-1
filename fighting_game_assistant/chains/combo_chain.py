from services.llm_factory import get_llm
from prompts.combo_prompt import combo_prompt

def get_combo_chain():
    llm = get_llm()
    chain = combo_prompt | llm
    return chain
