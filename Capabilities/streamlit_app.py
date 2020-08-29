import streamlit as st
from chalice import Chalice
from chalicelib import storage_service
from chalicelib import transcription_service
import base64
import json
import os

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
try:
    with open(filename) as input:
        st.text(input.read())
except FileNotFoundError:
    st.error('File not found.')  
if filename:
    file_bytes = base64.b64decode(filename)
    file_info = storage_service.upload_file(file_bytes, filename)
    
  
sentence = st.text_input('Write here:') 
if sentence:
    file_bytes = bytes(sentence, 'utf-8')
    file_info = storage_service.upload_file(file_bytes, sentence)
    


#def translate_recording(recording_id):
#    #request_data = json.loads(app.current_request.raw_body)
#    from_lang = "eng-US"
#    transcription_text = transcription_service.transcribe_audio(recording_id, from_lang)
#
#    return {
#        'text': transcription_text,
#    }