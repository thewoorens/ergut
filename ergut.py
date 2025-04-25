import webbrowser
import subprocess
import speech_recognition as sr
import json
from datetime import datetime
import os
import winreg


class Ergut:
    transcript = []

    def __init__(self, language="en-EN", log_file="transcripts.json", update_callback=None):
        self.recognizer = sr.Recognizer()
        self.language = language
        self.log_file = log_file
        self.update_callback = update_callback
        self._setup_log()
        self.mic = sr.Microphone()

    def _setup_log(self):
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w", encoding="utf-8") as f:
                json.dump([], f)

    def log_transcription(self, text, platform=None):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "text": text,
            "platform": platform if platform else "Unknown"
        }

        with open(self.log_file, "r+", encoding="utf-8") as f:
            data = json.load(f)
            data.append(entry)
            f.seek(0)
            json.dump(data, f, indent=4, ensure_ascii=False)

    def find_spotify_path(self):
        try:
            reg_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Spotify"
            reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path)
            install_path, _ = winreg.QueryValueEx(reg_key, "InstallLocation")
            return install_path + "\\Spotify.exe"
        except WindowsError:
            return None

    def open_application(self, text):
        if "youtube" in text.lower():
            webbrowser.open("https://youtube.com")
            self.log_transcription(text, platform="YouTube")
        elif "spotify" in text.lower():
            spotify_path = self.find_spotify_path()
            if spotify_path and os.path.exists(spotify_path):
                subprocess.run([spotify_path])
            else:
                webbrowser.open("https://spotify.com")
                self.log_transcription(text, platform="Spotify")
        else:
            self.log_transcription(text)

    def start_transcribing(self):
        with self.mic as source:
            print("🎙️ Sistem başlatıldı. Konuşabilirsiniz...")
            self.recognizer.adjust_for_ambient_noise(source)

            while True:
                try:
                    audio = self.recognizer.listen(source, timeout=5)
                    text = self.recognizer.recognize_google(audio, language=self.language)
                    print(f"📝 {text}")

                    if self.update_callback:
                        self.update_callback(text)

                    self.open_application(text)

                except sr.WaitTimeoutError:
                    print("⏳ Ses algılanmadı.")
                except sr.UnknownValueError:
                    print("🤔 Anlaşılamadı.")
                except sr.RequestError as e:
                    print(f"❌ API Hatası: {e}")
