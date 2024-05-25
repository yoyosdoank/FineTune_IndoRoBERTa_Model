import streamlit as st
import numpy as np
from transformers import RobertaTokenizerFast, AutoModelForSequenceClassification
import torch

@st.cache_resource()
def get_model():
    tokenizer = RobertaTokenizerFast.from_pretrained('flax-community/indonesian-roberta-base')
    model1 = AutoModelForSequenceClassification.from_pretrained("yogie27/IndoRoBERTa-Sentiment-Classifier-for-Twitter")
    model2 = AutoModelForSequenceClassification.from_pretrained("yogie27/IndoRoBERTa-Emotion-Classifier-for-Twitter")
    return tokenizer,model1,model2

tokenizer,model1,model2 = get_model()

user_input = st.text_area('Masukkan kalimat yang akan dianalisis:')
button = st.button("Lakukan Analisis")

d = {
  2:'Positif',  
  1:'Netral',
  0:'Negatif'
}

e = {
  4:'Sedih',
  3:'Sayang',
  2:'Senang',  
  1:'Takut',
  0:'Marah'
}

if user_input and button :
    test_sample = tokenizer([user_input], padding=True, truncation=True, max_length=512,return_tensors='pt')
    # test_sample
    
    output1 = model1(**test_sample)
    output2 = model2(**test_sample)
    probs1 = output1[0].softmax(1)
    probs2 = output2[0].softmax(1)
    pred_label_idx1 = probs1.argmax()
    pred_label_idx2 = probs2.argmax()
    st.write("Label Sentimen: ",pred_label_idx1)
    st.write("Label Emosi: ",pred_label_idx2)
    y_pred1 = np.argmax(output1.logits.detach().numpy(),axis=1)
    y_pred2 = np.argmax(output2.logits.detach().numpy(),axis=1)
    st.write("Klasifikasi Sentimen: ",d[y_pred1[0]])
    st.write("Klasifikasi Emosi: ",e[y_pred2[0]])
