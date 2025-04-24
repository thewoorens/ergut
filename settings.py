import json
import os


class SettingsManager:
    def __init__(self, file_path="settings.json", defaults=None):
        self.file_path = file_path
        self.defaults = defaults or {
            "theme": "dark",
            "language": "English",
            "languageCode": "en"
        }
        self.settings = self.load()

    def load(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r") as file:
                    return json.load(file)
            except json.JSONDecodeError:
                print("[!] Settings file is corrupted. Resetting to defaults.")
                return self.defaults.copy()
        else:
            return self.defaults.copy()

    def save(self):
        with open(self.file_path, "w") as file:
            json.dump(self.settings, file, indent=4)

    def get(self, key):
        return self.settings.get(key, self.defaults.get(key))

    def set(self, key, value):
        self.settings[key] = value
        self.save()

    def reset(self):
        self.settings = self.defaults.copy()
        self.save()

    def all(self):
        return self.settings
