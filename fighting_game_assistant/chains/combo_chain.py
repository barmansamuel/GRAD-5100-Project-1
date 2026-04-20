# chains/combo_chain.py

from services.llm_factory import get_llm
from prompts.combo_prompt import combo_prompt
from services.wiki_scraper import scrape
from services.vector_store import build_vector_store
from services.retriever import get_relevant_chunks
from services.validator import validate_game, validate_character


class ValidationError(Exception):
    """Raised when game or character input fails validation."""
    pass


class NoDataError(Exception):
    """Raised when scraping returns no usable content."""
    pass


def get_combo_chain():
    llm = get_llm()

    def invoke(inputs: dict) -> object:
        raw_game = inputs["game"]
        raw_character = inputs["character"]
        skill_level = inputs["skill_level"]

        # ── Step 1: Validate game ─────────────────────────────────────────
        canonical_game, game_msg = validate_game(raw_game)
        if canonical_game is None:
            raise ValidationError(game_msg)

        # ── Step 2: Validate character ────────────────────────────────────
        canonical_character, char_msg = validate_character(canonical_game, raw_character)
        if canonical_character is None:
            raise ValidationError(char_msg)

        # ── Step 3: Scrape wikis ──────────────────────────────────────────
        texts = scrape(canonical_game, canonical_character)

        if not texts:
            raise NoDataError(
                f"No wiki data was found for **{canonical_character}** in "
                f"**{canonical_game}**. The character may not have a page on "
                f"SuperCombo, Dustloop, or Mizuumi yet. "
                f"Try checking the wikis directly."
            )

        # ── Step 4: Build vector store & retrieve relevant chunks ─────────
        vector_db = build_vector_store(texts)
        query = f"{canonical_game} {canonical_character} combos frame data strategy"
        context, found_relevant = get_relevant_chunks(vector_db, query)

        if not found_relevant:
            raise NoDataError(
                f"Wiki pages were found for **{canonical_character}**, but none of "
                f"the retrieved sections scored above the relevance threshold. "
                f"The page may lack combo or strategy content."
            )

        # ── Step 5: Build prompt & call LLM ──────────────────────────────
        prompt = combo_prompt.format(
            game=canonical_game,
            character=canonical_character,
            skill_level=skill_level,
            context=context,
        )

        # Attach correction notices to the LLM response if fuzzy-matching fired
        notices = []
        if game_msg:
            notices.append(game_msg)
        if char_msg:
            notices.append(char_msg)

        response = llm.invoke(prompt)

        # Prepend any fuzzy-match notices so the user sees them
        if notices:
            notice_text = "\n\n".join(f"> ℹ️ {n}" for n in notices)
            response.content = f"{notice_text}\n\n---\n\n{response.content}"

        return response

    class Chain:
        def invoke(self, inputs: dict) -> object:
            return invoke(inputs)

    return Chain()