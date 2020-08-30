import streamlit as st
from chalice import Chalice
from chalicelib import storage_service
from chalicelib import transcription_service
import base64
import json
import os
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk
nltk.download('punkt')
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


#####
# chalice app configuration
#####

#####
# services initialization
#####
storage_location = 'aws-bucket-fun'
storage_service = storage_service.StorageService(storage_location)
transcription_service = transcription_service.TranscriptionService(storage_service)


"""
#  Welcome to Reflect :) 
"""


filename = st.text_input('Enter a file path:')
if filename:
    file_info = storage_service.upload_file(filename)
    st.write(file_info)
    recording_id = file_info["fileId"]
    
if recording_id:
    transcription_text = transcription_service.transcribe_audio(recording_id)
    st.write(transcription_text)
       
if transcription_text:
    wordcloud = WordCloud().generate(transcription_text)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    st.pyplot()

if transcription_text:
    text = word_tokenize(transcription_text)
    stopWords = set(stopwords.words('english'))
    text = [w for w in text if w not in stopWords]
    #ps = PorterStemmer()
    
    analyser = SentimentIntensityAnalyzer()
    score = analyser.polarity_scores(text)
    st.write("{:-<40} {}".format(text, str(score)))
    
    
    
text = st.text_input("for wordcloud")
if text:
    wordcloud = WordCloud().generate(text)

    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    st.pyplot()
    
    
sentence = st.text_input('Write here:') 
if sentence:
    file_bytes = bytes(sentence, 'utf-8')
    file_info = storage_service.upload_file(file_bytes, sentence)
   
text = st.text_input("for wordcloud")
if text:
    wordcloud = WordCloud().generate(text)

    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    st.pyplot()


