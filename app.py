import streamlit as st
import pickle
import re
import base64
import numpy as np

# --- Model Selection ---
model_options = {
    'SVC': ('phishing_detector_model_svc.pkl', 'tfidf_vectorizer_svc.pkl'),
    'Naive Bayes': ('phishing_detector_model_naive.pkl', 'tfidf_vectorizer_naive.pkl')
}
selected_model = st.sidebar.selectbox('Select Model', list(model_options.keys()), index=0)
model_path, vectorizer_path = model_options[selected_model]
try:
    with open(model_path, 'rb') as model_file:
        loaded_model = pickle.load(model_file)
    with open(vectorizer_path, 'rb') as vectorizer_file:
        loaded_vectorizer = pickle.load(vectorizer_file)
except FileNotFoundError:
    st.error(f"Model or vectorizer file not found. Please run the training script first to create '{model_path}' and '{vectorizer_path}'.")
    st.stop()

# --- Prediction Function ---
def predict_email(email_text):
    email_tfidf = loaded_vectorizer.transform([email_text])
    prediction = loaded_model.predict(email_tfidf)
    # Try to get probability/confidence score if available
    if hasattr(loaded_model, 'predict_proba'):
        proba = loaded_model.predict_proba(email_tfidf)
        confidence = proba.max()
    elif hasattr(loaded_model, 'decision_function'):
        decision = loaded_model.decision_function(email_tfidf)
        confidence = 1 / (1 + np.exp(-abs(decision[0])))
    else:
        confidence = None
    return prediction[0], confidence

# --- Streamlit App Interface ---
st.title("Phishing Email Detector 🎣")
st.write(
    "Enter the full text of an email below to check if it's a potential phishing attempt. "
    "The model was trained on a dataset of real phishing and safe emails."
)

# --- File Attachment Analysis (Basic) ---
uploaded_file = st.file_uploader("Or upload a .txt file to analyze the email content:", type=["txt"])
if uploaded_file is not None:
    email_text = uploaded_file.read().decode("utf-8")
    st.info("Loaded email text from uploaded file.")
else:
    email_text = ""

# Text area for user input
email_text = st.text_area("Paste Email Text Here:", value=email_text, height=250)

# Predict button
if st.button("Analyze Email"):
    if email_text:
        # --- Make Prediction ---
        with st.spinner("Analyzing..."):
            prediction, confidence = predict_email(email_text)

        # --- Highlight Suspicious Words ---
        suspicious_keywords = [
            'urgent', 'verify', 'account', 'password', 'credit', 'card', 'winner',
            'congratulations', 'claim', 'prize', 'suspend', 'confirm', 'login', 'bank'
        ]
        def highlight_words(text, keywords):
            pattern = r'(' + '|'.join(re.escape(word) for word in keywords) + r')'
            return re.sub(pattern, r'<mark>\\1</mark>', text, flags=re.IGNORECASE)
        highlighted_text = highlight_words(email_text, suspicious_keywords)

        # --- Display Result ---
        st.subheader("Analysis Result")
        st.markdown(f"**Email Text (suspicious words highlighted):**<br>{highlighted_text}", unsafe_allow_html=True)
        if confidence is not None:
            st.write(f"**Model Confidence:** {confidence:.2%}")
        if prediction == "Phishing Email":
            st.error("🚨 This looks like a Phishing Email!")
            st.warning("Be cautious with any links or attachments. Do not provide personal information.")
            st.info("**Reason:** The email contains suspicious keywords and/or patterns often found in phishing attempts.")
        else:
            st.success("✅ This appears to be a Safe Email.")
            st.info("However, always remain vigilant when reading emails.")
            st.info("**Reason:** The email does not contain strong phishing indicators based on the model's training.")

        # --- Downloadable Report ---
        report = f"Email Text:\\n{email_text}\\n\\nPrediction: {prediction}\\nConfidence: {confidence if confidence is not None else 'N/A'}\\n"
        b64 = base64.b64encode(report.encode()).decode()
        href = f'<a href=\"data:file/txt;base64,{b64}\" download=\"phishing_report.txt\">Download Analysis Report</a>'
        st.markdown(href, unsafe_allow_html=True)

        # --- User Feedback ---
        st.markdown("---")
        st.write("**Was this prediction correct?**")
        feedback = st.radio("Feedback", ("Yes", "No"), horizontal=True)
        if st.button("Submit Feedback"):
            st.success("Thank you for your feedback!")
    else:
        st.warning("Please paste some email text to analyze.")
