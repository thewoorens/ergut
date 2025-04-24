import json
import os
from settings import SettingsManager

settings = SettingsManager()

class LanguageManager:
    def __init__(self):
        self.languages = {}
        print("Helloooo"+ settings.get('languageCode'))
        self.current_lang = settings.get('languageCode')
        self.load_languages()

    def load_languages(self):
        locales_dir = os.path.join(os.path.dirname(__file__))
        for filename in os.listdir(locales_dir):
            if filename.endswith(".json"):
                lang_code = filename.split(".")[0]
                with open(os.path.join(locales_dir, filename), "r", encoding="utf-8") as f:
                    self.languages[lang_code] = json.load(f)

    def set_language(self, lang_code):
        if lang_code in self.languages:
            self.current_lang = lang_code
            return True
        return False

    def get_text(self, key):
        return self.languages[self.current_lang].get(key, key)

    def get_available_languages(self):
        return list(self.languages.keys())
