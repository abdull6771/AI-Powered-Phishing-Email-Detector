# Phishing Email Detector

A lightweight Streamlit web app that detects phishing emails using pre-trained ML models (SVC and Naive Bayes) with TF-IDF vectorizers. The app lets users paste or upload email text, highlights suspicious words, shows model confidence, allows model selection, and produces a downloadable PDF analysis report.

## Features

- Detects whether an email is a phishing attempt or safe.
- Select between available models (SVC, Naive Bayes) if present.
- Upload a `.txt` email file or paste email text into the UI.
- Highlights suspicious keywords in the displayed email.
- Shows a model confidence score (when supported by the model).
- Generates a downloadable PDF report containing the email and the analysis.
- Collects simple user feedback for each prediction.

---

## Quick Start

These quick steps assume you're on macOS (zsh) and have Python 3.8+ installed.

1. Clone or copy the project to your machine and change into the directory:

```bash
cd /path/to/Spam_Email
```

2. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies (create `requirements.txt` or install directly):

```bash
pip install streamlit scikit-learn pandas numpy fpdf
```

(Optionally create `requirements.txt` with the exact pinned versions you used.)

4. Ensure the required model and vectorizer files are present in this folder:

- `phishing_detector_model_svc.pkl`
- `tfidf_vectorizer_svc.pkl`
- `phishing_detector_model_naive.pkl` (optional)
- `tfidf_vectorizer_naive.pkl` (optional)

If these files are missing, run your training script or copy the files into this directory.

5. Run the Streamlit app:

```bash
streamlit run app.py
```

Open the URL shown in the terminal (usually `http://localhost:8501`).

---

## Usage

- Paste an email into the "Paste Email Text Here" box or upload a `.txt` file.
- Choose the model from the sidebar (SVC or Naive Bayes) if both vectorizer/model pairs are present.
- Click **Analyze Email**.
- The app will show:
  - Highlighted suspicious words in the email.
  - Prediction ("Phishing Email" or "Safe Email").
  - Model confidence (if available).
  - A link to download a PDF report containing the email and the analysis.
- Optionally submit feedback (Yes/No) to indicate whether the prediction was correct.

Example output (in-app):

- "🚨 This looks like a Phishing Email!"
- "✅ This appears to be a Safe Email."

---

## Project Structure

```
Spam_Email/
├─ app.py                         # Streamlit app
├─ phishing_detector_model_svc.pkl
├─ tfidf_vectorizer_svc.pkl
├─ phishing_detector_model_naive.pkl (optional)
├─ tfidf_vectorizer_naive.pkl (optional)
└─ README.md
```

Key files:

- `app.py` — Main Streamlit application.
- `phishing_detector_model_*.pkl` — Serialized ML model(s).
- `tfidf_vectorizer_*.pkl` — Serialized TF-IDF vectorizer(s) used to transform input text.

---

## Configuration

- No extra environment variables are required by default.
- The app expects the model and vectorizer `.pkl` files to be present in the same directory as `app.py`.
- If you have different filenames or locations, update `model_options` in `app.py` or modify the code to load from a configurable path.

---

## Contributing

Contributions are welcome. Suggested workflow:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feat/your-feature`.
3. Make changes and add tests where appropriate.
4. Commit and push: `git push origin feat/your-feature`.
5. Open a pull request describing your changes and rationale.

When opening issues or PRs, include:

- Steps to reproduce (if a bug).
- The expected vs actual behavior.
- Any logs or error traces.

---

## Roadmap (optional ideas)

- Add a lightweight API endpoint (FastAPI) so the model can be consumed by other services.
- Add more feature explanations (why the model made a decision) using LIME/SHAP.
- Add automated feedback collection and a small admin UI to review feedback and retrain the model.
- Add tests and CI (GitHub Actions) to run linting and tests on PRs.
- Improve file-attachment scanning (PDF/DOCX) with safe sandboxing.

---

## License

This project is provided under the MIT License. See LICENSE file for details.

---

## Acknowledgments

- Built with Streamlit and scikit-learn.
- PDF report generation uses `fpdf`.

If you'd like, I can also:

- Create a `requirements.txt` with pinned versions.
- Add a minimal `LICENSE` file (MIT) to the repo.
- Add a small CONTRIBUTING.md and ISSUE_TEMPLATE for smoother collaboration.

Would you like me to add any of those next?
