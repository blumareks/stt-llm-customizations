# created by Marek Sadowski 20241120
# github: https://github.com/blumareks/stt-llm-customizations
# Apache 2 Licence
from string import punctuation
import streamlit as st
from dotenv import load_dotenv
import os

#STT
import json
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

#gen ai
import http.client
import requests

# Load environment variables from the .env file
load_dotenv()

# getting config for Watsonx
apikey=os.getenv("STT_APIKEY")
url=os.getenv("STT_URL")
corpora=os.getenv("STT_CORPORA")
print(apikey)
print(url)
print(corpora)

# getting config env for wx.ai
# get the IAM API Key from the environment variable    
iam_api_key = os.getenv("WATSONX_IAM_API_KEY")

# get the IAM API URL from the environment variable    
iam_api_url = os.getenv("WATSONX_IAM_API_URL")

wx_project_id = os.getenv("PROJECT_ID")

# setting Watsonx
authenticator = IAMAuthenticator(apikey)
speech_to_text = SpeechToTextV1(
    authenticator=authenticator
)


# Retrieve the database configuration from the environment
AUDIO_FILE = os.getenv("AUDIO_FILE")
AUDIO_FILE2 = os.getenv("AUDIO_FILE2")
AUDIO_FILE3 = os.getenv("AUDIO_FILE3")
AUDIO_FILE4 = os.getenv("AUDIO_FILE4")
#audioFiles = [AUDIO_FILE, AUDIO_FILE2, AUDIO_FILE3, AUDIO_FILE4]
audioFiles = [AUDIO_FILE4]

corporaFiles = [corpora]

# Page title
st.title('Analyzing audio file for transcript with Watsonx STT, and GenAI based on watsonx.ai')


audioFile = st.radio("Select AUDIO FILE", audioFiles)
corporaFile = st.radio("Select corpora", corporaFiles)

st.write(f"Selected apikey: {apikey} ")
st.write(f"Selected url: {url} ")
st.write(f"Selected audio file: {audioFile} ")
st.write(f"Selected corpora file: {corporaFile} ")

def main():

    if st.button("Analyze file", type="primary"):
        st.write("starting processing STT")
        speech_to_text.set_service_url(url)

        
        with open(audioFile,'rb') as audio_file:

            speech_recognition_results = speech_to_text.recognize(
                audio=audio_file,
                #content_type='audio/mp3', #check the file extension and adapt to it
                content_type='audio/wav',
                model = 'en-US'#,
                #language_customization_id=corporaFile
            ).get_result()
        
        #st.write(json.dumps(speech_recognition_results, indent=2))
        st.write("------STT------")
        transcript_txt = ""
        for transcript in speech_recognition_results['results']:
            t = transcript['alternatives'][0]['transcript']  # will produce "Hello world!"

            st.write(t)
            # Extract the transcription from the response
            #transcript = response['results'][0]['alternatives'][0]['transcript']
            print(t)
            transcript_txt = transcript_txt+t.rstrip() + " "

        # Save the transcription to a file
        with open(f"{audioFile}transcriptionSTT.txt", "w") as text_file:
            text_file.write(transcript_txt)


        st.write("starting processing LLM based improvements")

        #get token
        # code that reads the token from the .env or OS
        def get_token():
            # create a token using the IAM API Key
            token = create_token(iam_api_key, iam_api_url)
            return token

        # code that creates a token to connect to watsonx.ai based on the IAM API Key
        def create_token(iam_api_key, iam_api_url):
            conn_ibm_cloud_iam = http.client.HTTPSConnection(iam_api_url)
            payload = "grant_type=urn%3Aibm%3Aparams%3Aoauth%3Agrant-type%3Aapikey&apikey="+iam_api_key
            headers = { 'Content-Type': "application/x-www-form-urlencoded" }
            conn_ibm_cloud_iam.request("POST", "/identity/token", payload, headers)
            res = conn_ibm_cloud_iam.getresponse()
            data = res.read()
            decoded_json=json.loads(data.decode("utf-8"))
            access_token=decoded_json["access_token"]
            return access_token


        #prepare prompt


        genai_url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"

        ## summary use case
        body = {
            "input": f"""Instructions: 
            You are a level 1 technical support that receives audio voicemails
             to address technical issues and provide solutions
             to the problem described in the voice message. 
             Reference the transcript input and recommend step-by-step process on resolving the issue. 
             Structure your step-by-step process according to this context
        {transcript_txt}
        \n\n
        Provide the step by step process here:\n\n""",
            "parameters": {#                "decoding_method": "sample","temperature":0,"max_new_tokens": 8000, "top_k": 50, "top_p": 1,     "repetition_penalty": 1
                "decoding_method": "greedy",
                "max_new_tokens": 2000,
                "stop_sequences": ["\\n\\n"],
                "repetition_penalty": 1
           },
            "model_id": "meta-llama/llama-3-1-70b-instruct",
            "project_id": wx_project_id
        }


        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {get_token()}"
        }
        #call GenAi

        response = requests.post(
            genai_url,
            headers=headers,
            json=body
        )
        #get response

        if response.status_code != 200:
            raise Exception("Non-200 response: " + str(response.text))

        data = response.json()


        #write results
        st.write("------LLM------")
        st.write(data["results"][0]["generated_text"])
        print("------LLM------")
        print(data["results"][0]["generated_text"])
        with open(f"{audioFile}transcriptionLLM.txt", "w") as text_file:
            text_file.write(data["results"][0]["generated_text"])
        st.write("that is all. thank you for using watsonx")

if __name__ == "__main__":
    main()
  