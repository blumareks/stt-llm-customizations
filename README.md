# stt-llm-customizations
medical transcription of audio enriched with STT (LLM based + corpora with medical terms); post-processing for patient doctor voices with LLM

## build it

 If you have a mac, then run commands :
 ```sh
  python3 -m venv .venv
  source .venv/bin/activate
  pip3 install -r requirements.txt
```

copy your `dot-env-example` to `.env` with the required apikeys and values


## running it

run the following:

```sh
streamlit run app.py
```


# setup

N/A (as we use the default `en-US` model)

## Authors

Contributors names and contact info

* Marek Sadowski
