# GRAD-5900-Project-1
# 🎮 Fighting Game Combo Assistant

A Streamlit application that generates **combos, strategy tips, and practice drills for fighting game characters** using a local LLM powered by **Ollama**.
The assistant improves accuracy by scraping trusted fighting game wikis such as **SuperCombo**, **Dustloop**, and **Mizuumi** and injecting that information into the model prompt.

---

# 🚀 Features

* Generate **character-specific combos**
* Provides **execution tips and matchup advice**
* Supports **Beginner / Intermediate / Advanced** skill levels
* Uses **Ollama + Llama3 locally** (no paid APIs)
* Pulls data from popular **FGC wiki resources**
* Simple **Streamlit UI**

---

# 🧠 Architecture

The application follows a lightweight **Retrieval-Augmented Generation (RAG)** pipeline.

```
User Input (Game, Character, Skill Level)
              │
              ▼
        Streamlit UI
              │
              ▼
        Combo Chain
              │
              ▼
        Wiki Scraper
   (SuperCombo / Dustloop / Mizuumi)
              │
              ▼
      Extract Relevant Text
 (Combos / Strategy / Frame Data)
              │
              ▼
        Prompt Builder
              │
              ▼
          Ollama LLM
           (Llama3)
              │
              ▼
      Structured Combo Guide
              │
              ▼
        Streamlit Output
```

### Key Components

| Component           | Description                                                  |
| ------------------- | ------------------------------------------------------------ |
| **Streamlit UI**    | User interface for entering game, character, and skill level |
| **Combo Chain**     | Connects the prompt and LLM                                  |
| **Wiki Scraper**    | Collects relevant information from fighting game wikis       |
| **Prompt Template** | Structures the request sent to the LLM                       |
| **LLM Factory**     | Initializes the Ollama LLM instance                          |

---

# 📁 Project Structure

```
project/
│
├── app.py
│
├── chains/
│   └── combo_chain.py
│
├── prompts/
│   └── combo_prompt.py
│
├── services/
│   ├── llm_factory.py
│   └── wiki_scraper.py
│
├── requirements.txt
│
└── README.md
```

---

# ⚙️ Requirements

* Python **3.9 – 3.12**
* Ollama installed locally
* Llama3 model pulled locally

---

# 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/fighting-game-assistant.git
cd fighting-game-assistant
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it:

**Mac/Linux**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🤖 Install Ollama

Download and install:

https://ollama.com

Then pull the Llama3 model:

```bash
ollama pull llama3
```

Verify it works:

```bash
ollama run llama3
```

---

# ▶️ Running the App

Start the Streamlit server:

```bash
streamlit run app.py
```

Your browser will open at:

```
http://localhost:8501
```

---

# 🎮 How to Use

1. Enter a **Fighting Game**
2. Enter a **Character**
3. Choose a **Skill Level**
4. Click **Generate Combos & Tips**

The assistant will generate:

* Combo routes
* Execution advice
* Matchup tips
* Practice drills
* Notation explanations

---

# 🌐 Data Sources

The assistant gathers information from:

* SuperCombo Wiki
* Dustloop Wiki
* Mizuumi Wiki

These are widely used resources within the **Fighting Game Community (FGC)**.

---

# ⚠️ Limitations

* Wiki pages may differ in formatting
* Some games/characters may not exist on all wikis
* Results depend on the accuracy of scraped data
* LLM responses may still occasionally hallucinate

---

# 🔮 Future Improvements

Planned improvements include:

* Vector database retrieval (FAISS)
* Embedding-based semantic search
* Frame data extraction
* Character matchup database
* Combo difficulty filtering
* Video example integration
* Character move notation standardization

---

# 🛠 Tech Stack

* **Python**
* **Streamlit**
* **LangChain**
* **Ollama**
* **Llama3**
* **BeautifulSoup**
* **Requests**

---

# 📜 License

MIT License

---

# 🙏 Acknowledgements

Special thanks to the **Fighting Game Community** and the maintainers of:

* SuperCombo Wiki
* Dustloop Wiki
* Mizuumi Wiki

Their documentation makes projects like this possible.
