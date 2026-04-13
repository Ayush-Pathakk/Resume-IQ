# ResumeIQ

AI-powered resume screener using TF-IDF + cosine similarity.

## Setup

```bash
pip install -r requirements.txt
```

## Run CLI

```bash
python main.py resumes/
```

## Run UI

```bash
streamlit run app.py
```

## Structure

```
resumeiq/
├── core.py         # parsing, cleaning, scoring logic
├── config.py       # skills list, thresholds
├── main.py         # CLI runner
├── app.py          # Streamlit UI
├── requirements.txt
└── resumes/        # drop PDFs here
```
