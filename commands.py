import webbrowser

from settings import SettingsManager


class Actions:
    settings = SettingsManager()

    CLICK_PREFIX = "[LOG] [Click] => "

    @staticmethod
    def help_button(event=None):
        print(f"\n{Actions.CLICK_PREFIX} Opening help page...")
        url = "https://github.com/thewoorens/ergut"
        webbrowser.open(url)

    @staticmethod
    def on_language_changed(selected_language):
        print(f"\n{Actions.CLICK_PREFIX} Language changed. New language is '{selected_language}'")

        language_map = {
            "English": "en",
            "Türkçe": "tr"
        }
        print(language_map.get(selected_language, "en"))
        Actions.settings.set("language", selected_language)
        language_code = language_map.get(selected_language, "en")
        Actions.settings.set("languageCode", language_code)
