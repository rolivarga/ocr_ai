from openai import OpenAI
from langdetect import detect_langs

def text_summarize(text, lang):
    API_KEY = open("API_KEY", "r").read()
    client = OpenAI(
        api_key=API_KEY
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Summarize this text: {}".format(text)}
        ]
    )
    
    return response.choices[0].message.content.strip()

def remove_empty_lines(text):
    "\n".join([s for s in text.split("\n") if s])
    text = "".join([s for s in text.splitlines(True) if s.strip("\r\n")])
    return text

def detect_language(text): 
    try: 
        langs = detect_langs(text)
        for item in langs: 
            # The first one returned is usually the one that has the highest probability
            return item.lang, item.prob 
    except: return "err", 0.0 

def convert_lang_prefix(lang):
    match lang:
        case "en":
            return "eng"
        case "hu":
            return "hun"