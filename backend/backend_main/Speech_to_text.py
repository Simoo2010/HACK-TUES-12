import os
import shutil
import time
import whisper
import gradio as gr

# ПЪРВА СТЪПКА: Добавяме текущата папка в системния PATH на Python
# Увери се, че ffmpeg.exe е в същата папка като този файл!
current_dir = os.path.dirname(os.path.abspath(__file__))
os.environ["PATH"] += os.pathsep + current_dir

print("⏳ Зареждане на Whisper (английски модел)...")
try:
    # "tiny" е супер бърз, ако искаш по-добро качество, смени на "base"
    model = whisper.load_model("tiny", device="cpu")
    print("✅ Whisper е готов за английска реч!")
except Exception as e:
    print(f"❌ Грешка при зареждане: {e}")

def transcribe_audio(audio_path):
    if audio_path is None:
        return ""

    # Локално копие за Windows стабилност
    local_filename = os.path.join(current_dir, "temp_english_audio.wav")
    
    try:
        time.sleep(0.5)
        shutil.copyfile(audio_path, local_filename)
        
        print(f"🎙️ AI обработва английска реч...")
        
        # МАГИЯТА: Добавяме language="en" за максимална точност
        result = model.transcribe(local_filename, fp16=False, language="en")
        
        return result.get("text", "").strip()

    except Exception as e:
        print(f"🚨 Грешка: {e}")
        return "Грешка: Проверете дали ffmpeg.exe е в папката!"
    
    finally:
        if os.path.exists(local_filename):
            try: os.remove(local_filename)
            except: pass

# 3. Интерфейс на Gradio
with gr.Blocks(title="English AI Voice") as demo:
    gr.Markdown("# 🎤 English Voice-to-Text")
    gr.Markdown("Speak in English and the AI will transcribe it instantly.")
    
    with gr.Row():
        audio_input = gr.Audio(sources=["microphone"], type="filepath", label="Record your voice")
        output_text = gr.Textbox(label="AI Transcription:")

    # Автоматично стартиране
    audio_input.change(fn=transcribe_audio, inputs=audio_input, outputs=output_text)

if __name__ == "__main__":
    # share=True е критично за микрофона
    demo.launch(share=True)