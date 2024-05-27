import streamlit as st
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

def has_vowel(word):
    vowels = 'aeiouAEIOU'
    return any(char in vowels for char in word)

@st.cache_resource()
def get_model():
    tokenizer = AutoTokenizer.from_pretrained('flax-community/indonesian-roberta-base')
    model1 = AutoModelForSequenceClassification.from_pretrained("yogie27/IndoRoBERTa-Sentiment-Classifier-for-Twitter", token="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")
    model2 = AutoModelForSequenceClassification.from_pretrained("yogie27/IndoRoBERTa-Emotion-Classifier-for-Twitter", token="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")
    return tokenizer,model1,model2

tokenizer,model1,model2 = get_model()

header = st.header("Prediksi Sentimen & Emosi Pada Kalimat Berbahasa Indonesia Dengan Metode Transformers")
note1 = st.caption("**AUTHOR: YOGIE OKTAVIANUS SIHOMBING**")
note2 = st.caption("SENTIMEN adalah sikap, perasaan, atau pandangan yang lebih stabil dan cenderung bertahan lebih lama terhadap seseorang, situasi, atau fenomena tertentu. Sentimen merupakan cerminan dari emosi yang lebih menetap dan terinternalisasi. EMOSI adalah respons psikologis yang intens, sering kali singkat, terhadap suatu peristiwa atau situasi. Emosi biasanya bersifat sementara dan bisa berubah dengan cepat. ***-Ivanov, D. (2023)-.***")
st.info("*Info: Masukkan kalimat Anda di kolom bawah dan tekan 'Lakukan Analisis' untuk memulai.")
user_input = st.text_area('Inputkan Kalimat:')
note3 = st.caption("****Harap memasukkan kalimat yang mempunyai konteks, minimal 7 kata dalam 1 kalimat.***")
note4 = st.caption("****Rekomendasi media sosial berbasis teks: Twitter.***")
note5 = st.caption("****Dimungkinkan analisis dari media sosial lainnya.***")
note6 = st.caption("****Analisis selain menggunakan bahasa Indonesia tidak dibenarkan.***")
button = st.button("Lakukan Analisis")

# Variabel untuk menyimpan status konfirmasi
confirm = False

sentimen = {
  2:'Positif',  
  1:'Netral',
  0:'Negatif'
}

emosi = {
  4:'Sedih - Kecewa',
  3:'Sayang',
  2:'Senang - Bahagia',  
  1:'Takut - Khawatir',
  0:'Marah - Jijik'
}

# Jika tombol ditekan, lakukan analisis awal
if user_input and button:
    # Cek apakah input memiliki lebih dari 7 kata
    if len(user_input.split()) > 7:
        # Variabel untuk melacak kata-kata yang memenuhi kriteria
        problematic_words = []
        # Cek apakah setiap kata dalam input memiliki huruf vokal
        for word in user_input.split():
            # Inisialisasi variabel untuk melacak karakter dan jumlah kemunculannya dalam kata
            char_count = {}
            # Hitung kemunculan setiap karakter dalam kata
            for char in word:
                char_count[char] = char_count.get(char, 0) + 1
            # Periksa apakah ada karakter dengan kemunculan lebih dari 2
            if any(count > 2 for count in char_count.values()):
                problematic_words.append(word)
                st.warning(f"Kata '{word}' memiliki lebih dari 2 huruf yang sama/dobel, dapat mempengaruhi konteks dan prediksi.")
            # Periksa apakah kata tidak memiliki huruf vokal
            if not has_vowel(word):
                problematic_words.append(word)
                st.warning(f"Kata '{word}' tidak memiliki huruf vokal, dapat mempengaruhi konteks dan prediksi.")
                
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
        st.write("Sentimen:", f"**{sentimen[max_sentiment_index]}**", "; Persentase Prediksi:", f"**{max_sentiment_prob:.2%}**")
        st.write("Emosi:", f"**{emosi[max_emotion_index]}**", "; Persentase Prediksi:", f"**{max_emotion_prob:.2%}**")
    else:
        st.error("Panjang 1 kalimat disarankan lebih dari 7 kata untuk memahami konteks dalam kalimat, input kembali pada kolom teks.")
    
