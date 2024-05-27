import streamlit as st
import numpy as np
from transformers import RobertaTokenizerFast, AutoModelForSequenceClassification
import torch

@st.cache_resource()
def get_model():
    tokenizer = RobertaTokenizerFast.from_pretrained('flax-community/indonesian-roberta-base')
    model1 = AutoModelForSequenceClassification.from_pretrained("yogie27/IndoRoBERTa-Sentiment-Classifier-for-Twitter", token="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")
    model2 = AutoModelForSequenceClassification.from_pretrained("yogie27/IndoRoBERTa-Emotion-Classifier-for-Twitter", token="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")
    return tokenizer,model1,model2

tokenizer,model1,model2 = get_model()

header = st.header("Klasifikasi Sentimen & Emosi Pada Teks Media Sosial Berbahasa Indonesia Dengan Metode Deep Learning")
note1 = st.caption("Author: Yogie Oktavianus Sihombing")
note2 = st.caption("Sentimen adalah sikap, perasaan, atau pandangan yang lebih stabil dan cenderung bertahan lebih lama terhadap seseorang, situasi, atau fenomena tertentu. Sentimen merupakan cerminan dari emosi yang lebih menetap dan terinternalisasi. Sedangkan emosi adalah respons psikologis yang intens, sering kali singkat, terhadap suatu peristiwa atau situasi. Emosi biasanya bersifat sementara dan bisa berubah dengan cepat. -Ivanov, D. (2023)-")
user_input = st.text_area('Masukkan postingan/komentar dalam bahasa Indonesia untuk dianalisis:')
note3 = st.caption("*Untuk masukan kalimat, direkomendasikan lebih dari 7 kata, agar model dapat merepresentasi konteks kalimat keseluruhan.")
note4 = st.caption("*Rekomendasi media sosial: Twitter.")
note5 = st.caption("*Dimungkinkan analisis dari media sosial lainnya.")
note5 = st.caption("*Analisis selain menggunakan bahasa Indonesia tidak dibenarkan, dikarenakan model dilatih menggunakan dataset Twitter berbahasa Indonesia.")
button = st.button("Lakukan Analisis")

sentimen = {
  2:'Positif',  
  1:'Netral',
  0:'Negatif'
}

emosi = {
  4:'Sedih / Kecewa',
  3:'Cinta / Sayang',
  2:'Senang / Bahagia',  
  1:'Takut / Khawatir',
  0:'Marah / Jijik'
}

# Jika tombol ditekan, lakukan analisis
if user_input and button:
    inputs = tokenizer([user_input], padding=True, truncation=True, max_length=512, return_tensors='pt')

    # Forward pass through classification layers for model1 and model2
    output1 = model1(**inputs)
    output2 = model2(**inputs)

    logits1 = output1.logits
    logits2 = output2.logits

    # Get the index and probability of the highest predicted sentiment and emotion
    max_sentiment_index = torch.argmax(logits1, dim=1).item()
    max_sentiment_prob = torch.softmax(logits1, dim=1).squeeze()[max_sentiment_index].item()

    max_emotion_index = torch.argmax(logits2, dim=1).item()
    max_emotion_prob = torch.softmax(logits2, dim=1).squeeze()[max_emotion_index].item()

    # Display the highest predicted sentiment and emotion along with their scores
    st.write("Prediksi Sentimen:", d[max_sentiment_index], "- Skor:", f"{max_sentiment_prob:.2%}")
    st.write("Prediksi Emosi:", e[max_emotion_index], "- Skor:", f"{max_emotion_prob:.2%}")
