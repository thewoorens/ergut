import webbrowser
import threading
from ergut import Ergut
from settings import SettingsManager
from PIL import Image


class Actions:
    settings = SettingsManager()

    PREFIX = "[LOG]  => "

    @staticmethod
    def help_button(event=None):
        print(f"\n{Actions.PREFIX} Opening help page...")
        url = "https://github.com/thewoorens/ergut"
        webbrowser.open(url)

    @staticmethod
    def on_language_changed(selected_language):
        print(f"\n{Actions.PREFIX} Language changed. New language is '{selected_language}'")

        language_map = {
            "English": "en",
            "Türkçe": "tr"
        }
        print(language_map.get(selected_language, "en"))
        Actions.settings.set("language", selected_language)
        language_code = language_map.get(selected_language, "en")
        Actions.settings.set("languageCode", language_code)

    @staticmethod
    def start_ergut(app, transcript_box=None, ergutLogoFrame=None, ergutLogo=None, startButton=None):
        print(f"\n{Actions.PREFIX} Ergut Voice Started")

        def update_ui(text):
            try:
                if transcript_box and ergutLogoFrame and ergutLogo and startButton:
                    loading_img = Image.open('assets/loading.png').resize((300, 300))

                    app.after(0, lambda: (
                        transcript_box.configure(state="normal"),
                        transcript_box.insert("end", f"{text}\n"),
                        transcript_box.see("end"),
                        transcript_box.configure(state="disabled"),
                        startButton.configure(text="Stop Talking"),
                        ergutLogo.configure(
                            light_image=loading_img,
                            dark_image=loading_img,
                            size=(300, 300)
                        ),
                        ergutLogoFrame.configure(text="", image=ergutLogo)
                    ))
            except Exception as e:
                print(f"UI Update Error: {e}")

        myErgut = Ergut(language="tr-TR", log_file="logs.json", update_callback=update_ui)
        transcribe_thread = threading.Thread(target=myErgut.start_transcribing, daemon=True)
        transcribe_thread.start()
