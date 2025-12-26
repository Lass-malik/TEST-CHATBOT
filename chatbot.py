# Importation des bibliothèques nécessaires
import nltk
import string
import streamlit as st

from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')

# Chargement et prétraitement des données (adapté au fichier fag.txt)
# Chargement du fichier texte
def load_faq(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    faq = []
    for i in range(0, len(lines) - 1, 2):
        question = lines[i]
        answer = lines[i + 1]
        faq.append((question, answer))

    return faq

# Prétraitement NLP
stop_words = set(stopwords.words("french"))

def preprocess(text):
    tokens = word_tokenize(text.lower())
    tokens = [
        word for word in tokens
        if word not in stop_words and word not in string.punctuation
    ]
    return set(tokens)



# Fonction de similarité
def get_best_answer(user_question, faq):
    user_tokens = preprocess(user_question)

    best_score = 0
    best_answer = "Désolé, je n’ai pas trouvé de réponse."

    for question, answer in faq:
        question_tokens = preprocess(question)

        if not question_tokens:
            continue

        similarity = len(user_tokens & question_tokens) / len(user_tokens | question_tokens)

        if similarity > best_score:
            best_score = similarity
            best_answer = answer

    return best_answer



# Fonction chatbot
faq_data = load_faq("fag.txt")

def chatbot(user_input):
    return get_best_answer(user_input, faq_data)

# Interface utilisateur avec Streamlit
def main():
    st.title("🤖 Chatbot – Seconde Guerre mondiale")
    st.write("Posez une question sur la Seconde Guerre mondiale.")

    question = st.text_input("Votre question :")

    if st.button("Envoyer"):
        if question.strip():
            response = chatbot(question)
            st.success(response)
        else:
            st.warning("Veuillez entrer une question.")

if __name__ == "__main__":
    main()

