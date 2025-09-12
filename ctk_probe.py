try:
    import tkinter as tk
    print("tkinter OK")
except Exception as e:
    raise SystemExit(f"tkinter fehlt/kaputt: {e}")

try:
    import customtkinter as ctk
    print("customtkinter OK, Version:", ctk.__version__)
except Exception as e:
    raise SystemExit(f"customtkinter fehlt/kaputt: {e}")

import customtkinter as ctk
ctk.set_appearance_mode("dark"); ctk.set_default_color_theme("dark-blue")
app = ctk.CTk(); app.title("CTk Probe"); app.geometry("320x150")
ctk.CTkLabel(app, text="✔ CTk läuft").pack(pady=20)
app.mainloop()
