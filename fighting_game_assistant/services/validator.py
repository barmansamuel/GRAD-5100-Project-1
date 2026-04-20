# services/validator.py

from rapidfuzz import process, fuzz

# Allowlist of supported games and their characters.
# Keys are canonical names; values are character rosters.
GAME_REGISTRY: dict[str, list[str]] = {
    "Street Fighter 6": [
        "Ryu", "Ken", "Chun-Li", "Guile", "Zangief", "Dhalsim",
        "E. Honda", "Blanka", "Cammy", "Dee Jay", "Manon", "Marisa",
        "JP", "Juri", "Kimberly", "Lily", "Luke", "Jamie",
        "Rashid", "A.K.I.", "Ed", "Akuma", "M. Bison", "Terry",
        "Mai", "Elena",
    ],
    "Tekken 8": [
        "Jin", "Kazuya", "Paul", "Law", "King", "Yoshimitsu",
        "Nina", "Jack-8", "Lars", "Alisa", "Asuka", "Hwoarang",
        "Lili", "Steve", "Bryan", "Lee", "Xiaoyu", "Claudio",
        "Shaheen", "Dragunov", "Feng", "Leroy", "Zafina", "Devil Jin",
        "Reina", "Victor", "Raven", "Azucena", "Leo", "Kuma",
        "Panda", "Jun", "Eddy", "Lidia", "Heihachi",
    ],
    "Mortal Kombat 1": [
        "Liu Kang", "Scorpion", "Sub-Zero", "Kitana", "Mileena",
        "Kung Lao", "Raiden", "Johnny Cage", "Kenshi", "Smoke",
        "Rain", "Li Mei", "Tanya", "Baraka", "Geras", "Nitara",
        "Ashrah", "Havik", "Sindel", "General Shao", "Reiko",
        "Reptile", "Shang Tsung", "Ermac", "Quan Chi", "Takeda",
        "Cyrax", "Sektor", "Noob Saibot", "Ghostface", "Homelander",
        "Omni-Man", "Peacemaker", "Conan", "T-800",
    ],
    "Guilty Gear Strive": [
        "Sol Badguy", "Ky Kiske", "May", "Axl Low", "Chipp Zanuff",
        "Potemkin", "Faust", "Millia Rage", "Zato-1", "Ramlethal Valentine",
        "Leo Whitefang", "Nagoriyuki", "Giovanna", "Anji Mito", "I-No",
        "Goldlewis Dickinson", "Jack-O", "Happy Chaos", "Baiken",
        "Testament", "Bridget", "Sin Kiske", "Bedman?", "Asuka R#",
        "Johnny", "Elphelt Valentine", "A.B.A", "Slayer",
    ],
    "Dragon Ball FighterZ": [
        "Goku", "Vegeta", "Gohan", "Piccolo", "Frieza", "Cell",
        "Beerus", "Hit", "Android 16", "Android 18", "Android 17",
        "Nappa", "Trunks", "Gotenks", "Yamcha", "Tien", "Krillin",
        "Kid Buu", "Majin Buu", "Janemba", "Gogeta", "Vegito",
        "Broly", "Bardock", "Goku Black", "Zamasu", "Cooler",
        "Android 21", "Master Roshi", "Videl", "Jiren", "Goku GT",
        "Vegeta GT", "Super Baby 2", "SSJ4 Gogeta",
    ],
    "Granblue Fantasy Versus: Rising": [
        "Gran", "Katalina", "Charlotta", "Lancelot", "Percival",
        "Lowain", "Ferry", "Metera", "Zeta", "Vaseraga", "Narmaya",
        "Soriz", "Djeeta", "Beelzebub", "Belial", "Avatar Belial",
        "Cagliostro", "Yuel", "Anre", "Eustace", "Seox",
        "Vira", "Nier", "Grimnir", "Id", "Sandalphon",
        "Siegfried", "Ghandagoza", "Vikala", "Tweyen", "Lucilius",
    ],
    "Blazblue Centralfiction": [
        "Ragna the Bloodedge", "Jin Kisaragi", "Noel Vermillion",
        "Rachel Alucard", "Taokaka", "Iron Tager", "Litchi Faye-Ling",
        "Arakune", "Bang Shishigami", "Carl Clover", "Hakumen",
        "Nu-13", "Tsubaki Yayoi", "Hazama", "Mu-12", "Makoto Nanaya",
        "Valkenhayn R. Hellsing", "Platinum the Trinity", "Relius Clover",
        "Izayoi", "Amane Nishiki", "Bullet", "Azrael", "Kagura Mutsuki",
        "Kokonoe", "Yuuki Terumi", "Celica A. Mercury", "Lambda-11",
        "Hibiki Kohaku", "Naoto Kurogane", "Nine the Phantom",
        "Izanami", "Es", "Mai Natsume", "Susanoo",
    ],
    "Skullgirls 2nd Encore": [
        "Filia", "Cerebella", "Peacock", "Parasoul", "Ms. Fortune",
        "Painwheel", "Valentine", "Double", "Squigly", "Big Band",
        "Fukua", "Eliza", "Beowulf", "Robo-Fortune", "Annie",
        "Umbrella", "Black Dahlia", "Marie",
    ],
}

SIMILARITY_THRESHOLD = 75  # percent, for fuzzy matching


def get_all_games() -> list[str]:
    return sorted(GAME_REGISTRY.keys())


def get_characters(game: str) -> list[str]:
    return sorted(GAME_REGISTRY.get(game, []))


def fuzzy_find(query: str, candidates: list[str]) -> tuple[str | None, int]:
    """Return the best match and its score (0-100), or (None, 0) if below threshold."""
    if not candidates:
        return None, 0
    result = process.extractOne(query, candidates, scorer=fuzz.WRatio)
    if result is None:
        return None, 0
    match, score, _ = result
    if score >= SIMILARITY_THRESHOLD:
        return match, score
    return None, score


def validate_game(game: str) -> tuple[str | None, str]:
    """
    Validate a game name.
    Returns (canonical_name, error_message).
    canonical_name is None if invalid.
    """
    all_games = get_all_games()

    # Exact match first
    for g in all_games:
        if g.lower() == game.strip().lower():
            return g, ""

    # Fuzzy match
    match, score = fuzzy_find(game, all_games)
    if match:
        return match, f"Did you mean **{match}**? Showing results for that game."

    return None, (
        f'**"{game}"** was not found in the supported game list. '
        f"Please select a game from the dropdown."
    )


def validate_character(game: str, character: str) -> tuple[str | None, str]:
    """
    Validate a character name for a given (already-validated) game.
    Returns (canonical_name, error_message).
    canonical_name is None if invalid.
    """
    roster = get_characters(game)

    # Exact match first
    for c in roster:
        if c.lower() == character.strip().lower():
            return c, ""

    # Fuzzy match
    match, score = fuzzy_find(character, roster)
    if match:
        return match, f"Did you mean **{match}**? Showing results for that character."

    return None, (
        f'**"{character}"** is not a recognised character in {game}. '
        f"Please select a character from the dropdown."
    )