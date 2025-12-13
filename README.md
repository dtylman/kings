# Kings Study Assistant 📚

> **An AI-powered study companion for preparing for biblical exams in the LLM era**

This project demonstrates how students can leverage Large Language Models (LLMs) to prepare for comprehensive exams. Using the Book of Kings as a case study, it shows how AI can help create structured study materials, character indices, and location references—all automatically generated from biblical texts.

## 🎯 Project Purpose

This is a proof-of-concept (PoC) project that explores how modern AI technology can assist students in preparing for traditional exams, particularly those requiring extensive memorization and comprehension of large texts. The project specifically targets Hebrew Bible proficiency exams by:

- Automatically generating chapter summaries
- Extracting and indexing characters with descriptions
- Cataloging important locations
- Creating a comprehensive study document in Hebrew

## ✨ Features

- **Automatic Text Retrieval**: Downloads biblical chapters from Sefaria API
- **AI-Powered Summarization**: Uses Google's Gemini AI to create concise chapter summaries
- **Character Extraction**: Identifies and describes all characters mentioned in each chapter
- **Location Mapping**: Lists and describes important places
- **Hebrew Support**: Full right-to-left (RTL) Hebrew text support
- **Document Generation**: Creates a formatted Word document (.docx) with:
  - Chapter-by-chapter plot summaries with Hebrew numerals
  - Alphabetically sorted character index with descriptions and chapter references
  - Alphabetically sorted location index with descriptions and chapter references

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- A Google Gemini API key ([Get one here](https://aistudio.google.com/api-keys))

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd kings
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set your Gemini API key:
```bash
export GEMINI_API_KEY='your-api-key-here'
```

### Usage

Run the main script to process both books of Kings:

```bash
./kings.py
```

Or with Python:

```bash
python3 kings.py
```

The script will:
1. Download chapter texts from Sefaria (if not already cached)
2. Generate AI summaries for each chapter (if not already generated)
3. Compile a comprehensive study document: `kings_summary.docx`

## 📂 Project Structure

```
kings/
├── kings.py              # Main entry point
├── kings_text.py         # Handles downloading and caching biblical texts
├── analyzer.py           # AI-powered chapter analysis using Gemini
├── summarizer.py         # Compiles summaries into a Word document
├── prompt.tmpl           # Template for AI prompts (in Hebrew)
├── system_instructions.tmpl  # AI system instructions
├── response.tmpl         # JSON response format template
├── requirements.txt      # Python dependencies
└── data/                 # Cached texts and summaries
    ├── I_Kings_*.text.txt
    ├── I_Kings_*.summary.json
    ├── II_Kings_*.text.txt
    └── II_Kings_*.summary.json
```

## 🔧 How It Works

### 1. Text Retrieval (`kings_text.py`)
- Fetches chapter texts from the Sefaria API
- Caches downloaded texts locally to avoid redundant API calls
- Handles HTML entity conversion for clean text

### 2. AI Analysis (`analyzer.py`)
- Uses Pydantic models to define structured output schema
- Sends chapter text to Google Gemini 2.5 Flash model
- Requests JSON-formatted responses with:
  - 100-word Hebrew synopsis
  - List of all characters with descriptions
  - List of all locations with descriptions
- Caches results to avoid re-processing

### 3. Document Compilation (`summarizer.py`)
- Aggregates character and location information across all chapters
- Creates a Word document with RTL Hebrew support
- Organizes content into three sections:
  - **Plot** (עלילה): Sequential chapter summaries
  - **Characters** (דמויות): Alphabetical character index
  - **Places** (מקומות): Alphabetical location index

### 4. Orchestration (`kings.py`)
- Processes all 21 chapters of I Kings
- Processes all 25 chapters of II Kings
- Coordinates the workflow from download to document generation

## 📚 Example Output

The generated document includes entries like:

**Plot Section:**
> (א) המלך דוד זקן ותשוש, ואבישג השונמית משרתת אותו. בנו אדוניהו מנצל את המצב ומנסה לתפוס את המלוכה...

**Character Index:**
> **דוד המלך:** מלך ישראל המזדקן והתשוש, שבסוף ימיו מורה למשוח את שלמה למלך. מלכים א פרק א, מלכים א פרק ב

## 🎓 Educational Implications

This project demonstrates several important concepts for modern learners:

1. **Automated Study Material Creation**: Transform large texts into manageable study guides
2. **Structured Knowledge Extraction**: Convert narrative text into organized reference materials
3. **AI-Assisted Learning**: Leverage AI as a study companion, not a replacement for learning
4. **Smart Caching**: Efficient processing by avoiding redundant API calls and computations

## 🛠️ Technologies Used

- **Python 3**: Core programming language
- **Google Gemini AI**: For intelligent text analysis and summarization
- **Pydantic**: For structured data validation and schema definition
- **python-docx**: For Word document generation with Hebrew/RTL support
- **hebrew-numbers**: For converting chapter numbers to Hebrew numerals (gematria)
- **Sefaria API**: For accessing biblical texts

