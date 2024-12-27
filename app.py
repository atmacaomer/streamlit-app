import streamlit as st
from transformers import pipeline


# ------------------------------
# Load Whisper Model
# ------------------------------
def load_whisper_model():
    """
    Load the Whisper model for audio transcription.
    """
    # TODO
    model = "openai/whisper-tiny"
    pipe = pipeline(task="automatic-speech-recognition",model=model,return_timestamps=True)
    return pipe
    # add logic to load the whisper model


# ------------------------------
# Load NER Model
# ------------------------------
def load_ner_model():
    """
    Load the Named Entity Recognition (NER) model pipeline.
    """
    # TODO
    model = "dslim/bert-base-NER"
    pipe = pipeline(task="ner",model=model)
    return pipe
    # add logic to load the NER model


# ------------------------------
# Transcription Logic
# ------------------------------
def transcribe_audio(uploaded_file):
    """
    Transcribe audio into text using the Whisper model.
    Args:
        uploaded_file: Audio file uploaded by the user.
    Returns:
        str: Transcribed text from the audio file.
    """
    # TODO
    model = load_whisper_model()
    result = model(uploaded_file)
    return result["text"]
    # implement transcription logic here


# ------------------------------
# Entity Extraction
# ------------------------------
def extract_entities(text, ner_pipeline):
    """
    Extract entities from transcribed text using the NER model.
    Args:
        text (str): Transcribed text.
        ner_pipeline: NER pipeline loaded from Hugging Face.
    Returns:
        dict: Grouped entities (ORGs, LOCs, PERs).
    """
    #TODO
    results = ner_pipeline(text)
    print(results)
    dct = {"PER":[],"ORG":[],"LOC":[]}
    for result in results:
        start_indicator , kind_indicator = result["entity"].split("-")
        name = result["word"].replace("#","")
        if kind_indicator in dct.keys():
            if start_indicator == "B":
                dct[kind_indicator].append(name)
            elif start_indicator == "I":
                if name[0].isupper() and len(name) != 1:
                    name = " " + name
                dct[kind_indicator][-1] += name
    for key , value in dct.items():
        dct[key] = list(set(value))
    return dct
    # implement entity extraction logic here

    


# ------------------------------
# Main Streamlit Application
# ------------------------------
def main():
    if "text" not in st.session_state:
        st.session_state.text = None
    
    st.title("Meeting Transcription and Entity Extraction")
    # You must replace below
    STUDENT_NAME = "Ömer Atmaca"
    STUDENT_ID = "150220335"
    st.write(f"**{STUDENT_ID} - {STUDENT_NAME}**")

    # TODO
    uploaded_file = st.file_uploader("Upload your audio file",type=["wav"])
    if(st.button("Transcribe audio") and uploaded_file != None):
        st.session_state.text = transcribe_audio(uploaded_file.read())
    if(st.session_state.text != None):
         st.write(st.session_state.text)
    if(st.button("Extract Entities") and st.session_state.text != None):
        ner_model = load_ner_model()
        extracted_dct = extract_entities(st.session_state.text,ner_model)
        writing_lst = ["Persons","Organizations","Locations"]
        s = 0
        for key , value in extracted_dct.items():    
            st.write(f"{writing_lst[s]} ({key}s): \n")
            s += 1
            for i in value:
                st.write(f"   -{i}\n")
    # Fill here to create the streamlit application by using the functions you filled

    
    
if __name__ == "__main__":
    main()
