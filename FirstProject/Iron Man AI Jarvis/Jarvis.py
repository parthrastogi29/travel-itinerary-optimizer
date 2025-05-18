import pyttsx3


engine = pyttsx3.init('sepi5')
voices = engine.getProperty('voices')
print(voices[0].id)
engine.setProperty('voice', voices[0].id)


def speak(audio):
    pass