from customtkinter import *
from PIL import Image
from commands import Actions
from locales.language_manager import LanguageManager
from settings import SettingsManager
from CTkMessagebox import CTkMessagebox

settings = SettingsManager()
lm = LanguageManager()
set_appearance_mode("dark")
logo_img = Image.open('assets/logo.png').resize((300, 300))
loading_img = Image.open('assets/loading.png').resize((300, 300))

app = CTk()
app.title("Ergut AI Voice Assistant")

window_width = 500
window_height = 800

screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

app.geometry(f"{window_width}x{window_height}+{x}+{y}")
app.resizable(height=False, width=False)


def on_language_selected(event=None):
    Actions.on_language_changed(language_combobox.get())
    msg = CTkMessagebox(title=lm.get_text("languageChangedTitle"),
                        message=lm.get_text("languageChangedDescription"),
                        icon="warning", option_1=lm.get_text("close"))
    response = msg.get()
    if response == lm.get_text("close"):
        app.destroy()


language_combobox = CTkComboBox(
    master=app,
    values=["English", "Türkçe"],
    state='readonly',
    command=on_language_selected
)
language_combobox.set(settings.get("language"))
language_combobox.place(x=10, y=10)

title = CTkLabel(
    master=app,
    text=lm.get_text("welcome"),
    font=("Arial", 28, "bold"),
    text_color="white",
)
title.pack(pady=(80, 0))

ergutLogo = CTkImage(
    light_image=logo_img,
    dark_image=logo_img,
    size=(300, 300)
)

ergutLogoFrame = CTkLabel(
    master=app,
    text="",
    image=ergutLogo
)
ergutLogoFrame.pack()

transcript_box = CTkTextbox(master=app, width=400, height=300, font=("Arial", 14))
transcript_box.pack(pady=(10, 20))
transcript_box.configure(state="disabled")
startButton = CTkButton(
    master=app,
    text=lm.get_text("start"),
    width=220,
    height=45,
    corner_radius=10,
    font=("Arial", 14, "bold"),
    fg_color=("#1E90FF", "#1F538D"),
    command=lambda: Actions.start_ergut(app, transcript_box, ergutLogoFrame, ergutLogo, startButton),
    border_width=1,
)
startButton.pack(pady=(10, 10))


settingsButton = CTkButton(
    master=app,
    text=lm.get_text("settings"),
    width=220,
    height=45,
    corner_radius=10,
    font=("Arial", 14, "bold"),
    border_width=1,
    fg_color="transparent"
)
settingsButton.pack(pady=(0, 10))

helpButton = CTkButton(
    master=app,
    text=lm.get_text("help"),
    width=100,
    height=35,
    corner_radius=10,
    font=("Arial", 12),
    fg_color="transparent",
    border_width=0,
    text_color=("gray50", "gray70"),
    command=Actions.help_button
)
helpButton.pack(pady=(10, 30))

app.mainloop()
