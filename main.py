from fastapi import FastAPI,Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from gtts import gTTS
import speech_recognition as sr
from pydub import AudioSegment
from textblob import TextBlob

templates = Jinja2Templates(directory="templates")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

def trans(text):
	langu = 'ta'
	output =gTTS(text=text, lang=langu, slow=False)
	output.save("output.mp3")
	sound = AudioSegment.from_mp3("output.mp3")
	sound.export("transcript.wav",format="wav")
	audio_file = "transcript.wav" 
	r = sr.Recognizer()
	with sr.AudioFile(audio_file) as source:
			audio = r.record(source)
			lang_text = r.recognize_google(audio,language='ta-IN')
			word = TextBlob(lang_text)
			translate_text = word.translate(from_lang='ta',to='en')
	return translate_text

@app.get("/", response_class=HTMLResponse)
def home(request : Request):
    return templates.TemplateResponse("input.html",{"request": request})

@app.post("/" )
def res_text(request:Request,name:str = Form(...)):
    trans_text = trans(name)
    ans = trans_text
    return templates.TemplateResponse("input.html",context = {"request": request,"text": ans})
