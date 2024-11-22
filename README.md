# stt-llm-customizations
medical transcription of audio enriched with STT (LLM based + corpora with medical terms); post-processing for patient doctor voices with LLM

## build it

 If you have a mac, then run commands :
 ```sh
  python3 -m venv .venv
  source .venv/bin/activate
  pip3 install -r requirements.txt
```

## running it

run the following:

```sh
streamlit run app.py
```


# setup

adding words:
```
transient ischemic attack
arteriovenous malformation
familial hemiplegic migraine
cerebral venous thrombosis
normal venous drainage
abortive therapies  
triptans
serotonin receptor agonists
topiramate
status migrainosus
subarachnoid hemorrhage
stroke
magnetic resonance imaging 
MRI
```
```
curl -X POST -u "apikey:{apikey}" --header "Content-Type: application/json" --data "{\"name\": \"neurogoly model\",   \"base_model_name\": \"en-US\",   \"description\": \"neurology custom language model\"}" "{url}/v1/customizations"
```

```
curl -X POST -u "apikey:{apikey}" --data-binary @neurology.txt "https://api.us-south.speech-to-text.watson.cloud.ibm.com/instances/id-instance/v1/customizations/customization-id/corpora/neurology"
```

The method also accepts an optional `allow_overwrite=true` query parameter that overwrites an existing corpus for a custom model. Use the parameter if you need to update a corpus file after you add it to a model

checking on status
```
curl -X GET -u "apikey:{apikey}" "https://api.us-south.speech-to-text.watson.cloud.ibm.com/instances/id-instance/v1/customizations/customization-id/corpora/neurology"
```

calling the model
```
curl -X POST -u "apikey:{apikey}" --header "Content-Type: audio/mp3" --data-binary @Script2.mp3 "https://api.us-south.speech-to-text.watson.cloud.ibm.com/instances/id-instance/v1/recognize?model=en-US&language_customization_id=customization-id"
```

## Authors

Contributors names and contact info

* Marek Sadowski
