from io import BytesIO
import pydub
import speech_recognition as sr
import ffmpy


def extract_from_audio_mp3(file_bytes):
    wav_io = convert_mp3_to_wav(file_bytes)
    text = extract_from_audio_wav(wav_io)
    return text

def convert_mp3_to_wav(file_bytes):
    # Usa o BytesIO para tratar o conteúdo do arquivo como um arquivo
    file = BytesIO(file_bytes)
    
    # Carrega o áudio MP3 em um AudioSegment
    sound = pydub.AudioSegment.from_file(file)
    
    # Converte o áudio para WAV e salva em um BytesIO
    wav_io = BytesIO()
    sound.export(wav_io, format="wav")
    wav_io.seek(0)  # Reseta o ponteiro para o início do buffer
    return wav_io

def extract_from_audio_wav(wav_io):
    
    doc = {
        'extractor': 'speech_recognition',
        'pages': [],
    }
    
    # Usa o BytesIO como fonte de áudio para o reconhecedor de fala
    with sr.AudioFile(wav_io) as source:
        r = sr.Recognizer()
        audio = r.record(source)
    
    # Reconhece o texto do áudio
    text = r.recognize_google(audio, language='pt-BR').strip()
    doc['pages'].append(text)

    if not text:
        raise Exception('Não foi possível extrair texto do audio')
    
    return doc