#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nominalwert-Rechner Pro für Trading
Berechnet den Nominalwert basierend auf maximalem Verlust und Stop-Loss Prozent
Mit Hebel, Gebühren, Take-Profit und P&L Berechnungen
"""

import os, json, tkinter as tk
from tkinter import ttk, messagebox, Canvas
import webbrowser

# ---------------- Storage ----------------
def appdata_dir():
    base = os.getenv("APPDATA") or os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base, "NominalwertRechner")
    os.makedirs(path, exist_ok=True)
    return path

SETTINGS_PATH = os.path.join(appdata_dir(), "settings.json")
DEFAULT_SETTINGS = {"maker_fee": 0.0140, "taker_fee": 0.042, "number_format": "german", "language": "german"}  # %

def load_settings():
    try:
        with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        for k, v in DEFAULT_SETTINGS.items():
            data.setdefault(k, v)
        return data
    except Exception:
        return DEFAULT_SETTINGS.copy()

def save_settings(data):
    try:
        with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        messagebox.showwarning("Warning", f"Settings could not be saved:\n{e}")

# ---------------- Number formatting ----------------
def parse_num(s: str, number_format: str = "german") -> float:
    """Parse a number from string, handling different formats."""
    if not s.strip(): return 0.0
    s = s.strip()
    
    if number_format == "german":
        # German format: 115.327,2 (dot as thousands separator, comma as decimal)
        if "," in s and "." in s:
            # Both present: dot is thousands, comma is decimal
            s = s.replace(".", "").replace(",", ".")
        elif "," in s:
            # Only comma: check if it's decimal separator
            parts = s.split(",")
            if len(parts) == 2 and len(parts[1]) <= 3:
                s = s.replace(",", ".")
        # If only dots, assume thousands separator unless last part is <=3 digits
        elif "." in s:
            parts = s.split(".")
            if len(parts) > 1 and len(parts[-1]) <= 3 and len(parts[-1]) > 0:
                # Last part looks like decimals
                s = "".join(parts[:-1]) + "." + parts[-1]
            else:
                # All dots are thousands separators
                s = s.replace(".", "")
    else:
        # US format: 115,327.2 (comma as thousands separator, dot as decimal)
        s = s.replace(",", "")
    
    return float(s)

def format_num(value: float, decimals: int = 2, number_format: str = "german") -> str:
    """Format a number according to the specified format."""
    if number_format == "german":
        # German format: 115.327,2
        formatted = f"{value:,.{decimals}f}"
        # Replace comma with temp, dot with comma, temp with dot
        formatted = formatted.replace(",", "TEMP").replace(".", ",").replace("TEMP", ".")
        return formatted
    else:
        # US format: 115,327.2
        return f"{value:,.{decimals}f}"

def format_money(value: float, number_format: str = "german") -> str:
    """Format money values."""
    return format_num(value, 2, number_format)

# ---------------- Translations ----------------
TRANSLATIONS = {
    "german": {
        "title": "💹 Nominalwert-Rechner",
        "subtitle": "Professionelle Trading-Position Berechnung",
        "basic_settings": "📊 Basis-Einstellungen",
        "direction": "Richtung:",
        "long": "📈 Long",
        "short": "📉 Short",
        "entry_price": "Einstiegskurs:",
        "max_loss": "Max. Verlust (€):",
        "stop_loss": "Stop-Loss (%):",
        "leverage_settings": "⚡ Hebel-Einstellung",
        "current_leverage": "Aktueller Hebel:",
        "results": "📈 Berechnungsergebnisse",
        "nominal": "💰 Nominal",
        "units": "📊 Stückzahl",
        "sl_price": "🛑 Stop-Loss",
        "margin": "⚖️ Margin",
        "tp_targets": "🎯 Take-Profit Ziele",
        "tp1": "🥉 TP1",
        "tp2": "🥈 TP2",
        "tp3": "🥇 TP3",
        "pnl_analysis": "💹 Profit & Loss Analyse",
        "trading_fees": "💸 Handelsgebühren",
        "entry": "Entry:",
        "exit": "Exit:",
        "fee_settings": "⚙️ Gebühren-Einstellungen",
        "maker_fee": "Maker (%):",
        "taker_fee": "Taker (%):",
        "number_format": "Zahlenformat:",
        "language": "Sprache:",
        "save": "💾 Speichern",
        "tp_config": "🎯 Take-Profit Konfiguration",
        "mode": "Modus:",
        "calculate": "🚀 Berechnen",
        "saved": "Einstellungen gespeichert.",
        "error": "Fehler",
        "invalid_input": "Ungültige Eingabe:",
        "entry_price_error": "Entry price must be > 0.",
        "stop_loss_error": "Stop-Loss % must be > 0.",
        "fees_info": "Gebühren: Entry {entry_fee}% + Exit {exit_fee}% = {total_fee}%",
        "effective_risk": "Effektives Risiko: {risk}%   •   Hebel: {leverage}×",
        "sl_pnl": "SL  → Brutto: {gross}   | Netto: {net}",
        "tp1_pnl": "TP1 → Brutto: {gross}  | Netto: {net}",
        "tp2_pnl": "TP2 → Brutto: {gross}  | Netto: {net}",
        "tp3_pnl": "TP3 → Brutto: {gross}  | Netto: {net}",
        "cut": "Ausschneiden",
        "copy": "Kopieren", 
        "paste": "Einfügen",
        "select_all": "Alles auswählen"
    },
    "english": {
        "title": "💹 Nominal Value Calculator",
        "subtitle": "Professional Trading Position Calculation",
        "basic_settings": "📊 Basic Settings",
        "direction": "Direction:",
        "long": "📈 Long",
        "short": "📉 Short", 
        "entry_price": "Order Price:",
        "max_loss": "Max. Loss (€):",
        "stop_loss": "Stop-Loss (%):",
        "leverage_settings": "⚡ Leverage Settings",
        "current_leverage": "Current Leverage:",
        "results": "📈 Calculation Results",
        "nominal": "💰 Nominal Value",
        "units": "📊 Units",
        "sl_price": "🛑 Stop-Loss",
        "margin": "⚖️ Margin",
        "tp_targets": "🎯 Take-Profit Targets",
        "tp1": "🥉 TP1",
        "tp2": "🥈 TP2",
        "tp3": "🥇 TP3", 
        "pnl_analysis": "💹 Profit & Loss Analysis",
        "trading_fees": "💸 Trading Fees",
        "entry": "Entry:",
        "exit": "Exit:",
        "fee_settings": "⚙️ Fee Settings",
        "maker_fee": "Maker (%):",
        "taker_fee": "Taker (%):",
        "number_format": "Number Format:",
        "language": "Language:",
        "save": "💾 Save",
        "tp_config": "🎯 Take-Profit Configuration",
        "mode": "Mode:",
        "calculate": "🚀 Calculate",
        "saved": "Settings saved.",
        "error": "Error",
        "invalid_input": "Invalid input:",
        "entry_price_error": "Entry price must be > 0.",
        "stop_loss_error": "Stop-Loss % must be > 0.",
        "fees_info": "Fees: Entry {entry_fee}% + Exit {exit_fee}% = {total_fee}%",
        "effective_risk": "Effective Risk: {risk}%   •   Leverage: {leverage}×",
        "sl_pnl": "SL  → Gross: {gross}   | Net: {net}",
        "tp1_pnl": "TP1 → Gross: {gross}  | Net: {net}",
        "tp2_pnl": "TP2 → Gross: {gross}  | Net: {net}",
        "tp3_pnl": "TP3 → Gross: {gross}  | Net: {net}",
        "cut": "Cut",
        "copy": "Copy",
        "paste": "Paste", 
        "select_all": "Select All"
    }
}

def get_text(key: str, language: str = "german") -> str:
    """Get translated text for given key and language."""
    return TRANSLATIONS.get(language, TRANSLATIONS["german"]).get(key, key)

def fmt_num(x: float, digits: int = 4, number_format: str = "german") -> str:
    return format_num(x, digits, number_format)

def fmt_money(x: float, number_format: str = "german") -> str:
    return format_money(x, number_format)

# ---------------- UI: Collapsible section ----------------
class Collapsible(ttk.Frame):
    def __init__(self, parent, title: str, initially_open: bool = False):
        super().__init__(parent)
        self._open = initially_open
        self._title = title
        self.header = ttk.Button(self, text=self._title_text(), command=self._toggle, style="TButton")
        self.header.grid(row=0, column=0, sticky="ew")
        self.body = ttk.Frame(self, style="Card.TFrame")
        if self._open:
            self.body.grid(row=1, column=0, sticky="ew", pady=(6, 4))

    def _title_text(self):
        return f"{'▼' if self._open else '▶'}  {self._title}"

    def _toggle(self):
        self._open = not self._open
        self.header.config(text=self._title_text())
        if self._open:
            self.body.grid(row=1, column=0, sticky="ew", pady=(6, 4))
        else:
            self.body.grid_remove()

# ---------------- App ----------------
class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, command, bg_color, fg_color="black", hover_color=None, font=("Segoe UI", 10), width=100, height=30, corner_radius=15):
        super().__init__(parent, width=width, height=height, highlightthickness=0, relief="flat")
        self.command = command
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.hover_color = hover_color or bg_color
        self.font = font
        self.text = text
        self.corner_radius = corner_radius
        self.width = width
        self.height = height
        
        try:
            parent_bg = parent.cget('bg')
        except:
            parent_bg = '#2b2b2b'
        self.config(bg=parent_bg)
        
        self.draw_button()
        self.bind("<Button-1>", self.on_click)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        
    def draw_button(self, color=None):
        self.delete("all")
        color = color or self.bg_color
        
        # Draw clean rounded rectangle using ovals
        x1, y1 = 0, 0
        x2, y2 = self.width, self.height
        r = min(self.corner_radius, self.width//2, self.height//2)
        
        # Main rectangle body
        self.create_rectangle(x1 + r, y1, x2 - r, y2, fill=color, outline="")
        self.create_rectangle(x1, y1 + r, x2, y2 - r, fill=color, outline="")
        
        # Corner circles for smooth rounded corners
        self.create_oval(x1, y1, x1 + 2*r, y1 + 2*r, fill=color, outline="")  # Top-left
        self.create_oval(x2 - 2*r, y1, x2, y1 + 2*r, fill=color, outline="")  # Top-right
        self.create_oval(x1, y2 - 2*r, x1 + 2*r, y2, fill=color, outline="")  # Bottom-left
        self.create_oval(x2 - 2*r, y2 - 2*r, x2, y2, fill=color, outline="")  # Bottom-right
        
        # Add text
        self.create_text(self.width//2, self.height//2, text=self.text, fill=self.fg_color, font=self.font)
        
    def on_click(self, event):
        if self.command:
            self.command()
            
    def on_enter(self, event):
        self.draw_button(self.hover_color)
        
    def on_leave(self, event):
        self.draw_button()

class NominalwertRechner(tk.Tk):
    def __init__(self):
        super().__init__()
        self.settings = load_settings()
        self.current_language = self.settings.get("language", "german")
        self.title(get_text("title", self.current_language))
        self._last_values = {}
        
        # --------- Modern Professional Theme ----------
        # Fixed width, variable height window
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Increase width to prevent clipping
        window_width = 400  # Increased from 367 to fit all content
        window_height = min(689, int(screen_height * 0.85))  # 810 * 0.85 = 688.5 ≈ 689
        
        # Center window on screen
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.geometry("400x689")  # Wider to prevent clipping
        self.minsize(400, 383)  # 450 * 0.85 = 382.5 ≈ 383
        self.maxsize(400, 918)  # 1080 * 0.85 = 918
        self.resizable(False, True)  # Only vertical resize
        
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except Exception:
            pass
        
        # Modern Color Palette - Black & Neon Yellow
        BG = "#121212"          # Black background
        CARD = "#1E1E1E"        # Dark card background
        SURFACE = "#2A2A2A"     # Surface elements
        PRIMARY = "#C9F24A"     # Neon yellow primary
        SECONDARY = "#FF6B6B"   # Coral secondary
        SUCCESS = "#4ECDC4"     # Teal success
        WARNING = "#FFE66D"     # Yellow warning
        DANGER = "#FF4757"      # Red for SL
        PROFIT = "#2ED573"      # Green for TP
        TEXT = "#EAEAEA"        # Light text
        TEXT_MUTED = "#A0A0A0"  # Muted text
        BORDER = "#333333"      # Subtle borders

        self.configure(bg=BG)
        
        # Configure styles - all 10% smaller
        style.configure("TLabel", background=BG, foreground=TEXT, font=("Segoe UI", 9))  # was 10
        style.configure("TFrame", background=BG)
        style.configure("TButton", background=SURFACE, foreground=TEXT, borderwidth=0, focuscolor="none", font=("Segoe UI", 9))  # was 10
        style.map("TButton", background=[("active", PRIMARY), ("pressed", PRIMARY)], foreground=[("active", "black"), ("pressed", "black")])
        style.configure("TEntry", fieldbackground=SURFACE, foreground=TEXT, bordercolor=BORDER, insertcolor=TEXT, font=("Segoe UI", 8))  # was 9
        style.configure("TCombobox", fieldbackground=SURFACE, foreground=TEXT, bordercolor=BORDER, font=("Segoe UI", 8))  # was 9
        style.configure("TScale", background=BG, troughcolor=SURFACE, borderwidth=0)
        style.configure("TRadiobutton", background=BG, foreground=TEXT, focuscolor="none", font=("Segoe UI", 9))  # was 10
        style.map("TRadiobutton", background=[("active", BG)], foreground=[("active", TEXT)])
        style.configure("Surface.TFrame", background=BG, relief="flat", borderwidth=0)
        
        # Rounded button style - compact
        style.configure("Rounded.TButton", 
                       background=SURFACE, 
                       foreground=TEXT, 
                       borderwidth=1,
                       relief="solid",
                       bordercolor=BORDER,
                       focuscolor="none",
                       padding=(8, 4),
                       font=("Segoe UI", 9))
        style.map("Rounded.TButton", 
                 background=[("active", PRIMARY), ("pressed", PRIMARY)], 
                 foreground=[("active", "black"), ("pressed", "black")],
                 bordercolor=[("active", PRIMARY), ("pressed", PRIMARY)])
        
        # Rounded Primary Button (Calculate)
        style.configure("Primary.TButton", 
                       background=PRIMARY, 
                       foreground="black", 
                       borderwidth=1,
                       relief="solid",
                       bordercolor=PRIMARY,
                       focuscolor="none",
                       padding=(12, 8),
                       font=("Segoe UI", 11, "bold"),
                       compound="center")
        style.map("Primary.TButton", 
                 background=[("active", "#00E676"), ("pressed", "#00C853")],
                 bordercolor=[("active", "#00E676"), ("pressed", "#00C853")])
        
        # Rounded Copy button styles
        style.configure("Success.Copy.TButton", 
                       background=SUCCESS, 
                       foreground="black", 
                       borderwidth=1,
                       relief="solid",
                       bordercolor=SUCCESS,
                       focuscolor="none",
                       padding=(8, 6),
                       font=("Segoe UI", 10),
                       compound="center")
        style.map("Success.Copy.TButton", 
                 background=[("active", "#26D0CE"), ("pressed", "#1BA3A0")],
                 bordercolor=[("active", "#26D0CE"), ("pressed", "#1BA3A0")])
        
        style.configure("Warning.Copy.TButton", 
                       background=WARNING, 
                       foreground="black", 
                       borderwidth=1,
                       relief="solid",
                       bordercolor=WARNING,
                       focuscolor="none",
                       padding=(8, 6),
                       font=("Segoe UI", 10),
                       compound="center")
        style.map("Warning.Copy.TButton", 
                 background=[("active", "#FFE066"), ("pressed", "#e2ff00")],
                 bordercolor=[("active", "#FFE066"), ("pressed", "#e2ff00")])
        
        style.configure("Danger.Copy.TButton", 
                       background=DANGER, 
                       foreground="white", 
                       borderwidth=1,
                       relief="solid",
                       bordercolor=DANGER,
                       focuscolor="none",
                       padding=(8, 6),
                       font=("Segoe UI", 10),
                       compound="center")
        style.map("Danger.Copy.TButton", 
                 background=[("active", "#FF6B7A"), ("pressed", "#FF3742")],
                 bordercolor=[("active", "#FF6B7A"), ("pressed", "#FF3742")])
        
        style.configure("Profit.Copy.TButton", 
                       background=PROFIT, 
                       foreground="black", 
                       borderwidth=1,
                       relief="solid",
                       bordercolor=PROFIT,
                       focuscolor="none",
                       padding=(8, 6),
                       font=("Segoe UI", 10),
                       compound="center")
        style.map("Profit.Copy.TButton", 
                 background=[("active", "#4AE584"), ("pressed", "#1ED760")],
                 bordercolor=[("active", "#4AE584"), ("pressed", "#1ED760")])
        
        # Entry styles
        style.configure("TEntry", 
                       fieldbackground=SURFACE, 
                       foreground=TEXT, 
                       borderwidth=2,
                       relief="flat",
                       insertcolor=PRIMARY,
                       font=("Segoe UI", 11))
        style.map("TEntry", 
                 focuscolor=[("focus", PRIMARY)],
                 bordercolor=[("focus", PRIMARY), ("!focus", BORDER)])
        
        # Button styles
        style.configure("Modern.TButton",
                       background=SURFACE,
                       foreground=TEXT,
                       borderwidth=2,
                       relief="flat",
                       padding=(12, 8),
                       font=("Segoe UI", 10))
        style.map("Modern.TButton",
                 background=[("active", BORDER), ("pressed", PRIMARY)],
                 foreground=[("active", "#000"), ("pressed", "#000")],
                 bordercolor=[("focus", PRIMARY), ("!focus", BORDER)])
        
        style.configure("Primary.TButton",
                       background=PRIMARY,
                       foreground="#000",
                       borderwidth=0,
                       relief="flat",
                       padding=(16, 12),
                       font=("Segoe UI", 11, "bold"))
        style.map("Primary.TButton",
                 background=[("active", "#00B8E6"), ("pressed", "#0099CC")],
                 foreground=[("active", "#000"), ("pressed", "#000")])
        
        style.configure("Success.TButton",
                       background=SUCCESS,
                       foreground="#000",
                       borderwidth=0,
                       relief="flat",
                       padding=(8, 6),
                       font=("Segoe UI", 9))
        style.map("Success.TButton",
                 background=[("active", "#45B7B8")],
                 foreground=[("active", "#000")])
        
        # TP (Profit) and SL (Danger) button styles
        style.configure("Profit.TButton",
                       background=PROFIT,
                       foreground="#000",
                       borderwidth=0,
                       relief="flat",
                       padding=(8, 6),
                       font=("Segoe UI", 9))
        style.map("Profit.TButton",
                 background=[("active", "#26C653")],
                 foreground=[("active", "#000")])
        
        style.configure("Danger.TButton",
                       background=DANGER,
                       foreground="#FFF",
                       borderwidth=0,
                       relief="flat",
                       padding=(8, 6),
                       font=("Segoe UI", 9))
        style.map("Danger.TButton",
                 background=[("active", "#E73C3C")],
                 foreground=[("active", "#FFF")])
        
        # Combobox styles - Fix readability
        style.configure("TCombobox",
                       fieldbackground=SURFACE,
                       foreground=TEXT,
                       background=SURFACE,
                       selectbackground=PRIMARY,
                       selectforeground="#000",
                       borderwidth=2,
                       relief="flat",
                       font=("Segoe UI", 10))
        style.map("TCombobox",
                 focuscolor=[("focus", PRIMARY)],
                 bordercolor=[("focus", PRIMARY), ("!focus", BORDER)],
                 fieldbackground=[("readonly", SURFACE)],
                 foreground=[("readonly", TEXT)])
        
        # Scale styles
        style.configure("Modern.Horizontal.TScale",
                       background=BG,
                       troughcolor=SURFACE,
                       borderwidth=0,
                       lightcolor=PRIMARY,
                       darkcolor=PRIMARY)
        
        # Title and Heading styles - 10% smaller
        style.configure("Title.TLabel", 
                       font=("Segoe UI", 16, "bold"),  # was 18
                       background=BG, 
                       foreground=TEXT)
        
        style.configure("Heading.TLabel", 
                       font=("Segoe UI", 11, "bold"),  # was 12
                       background=BG, 
                       foreground=TEXT)
        
        # Labelframe styles
        style.configure("Modern.TLabelframe",
                       background=CARD,
                       borderwidth=2,
                       relief="flat",
                       bordercolor=BORDER)
        style.configure("Modern.TLabelframe.Label",
                       background=CARD,
                       foreground=PRIMARY,
                       font=("Segoe UI", 11, "bold"))

        # Create scrollable main container with padding
        main_canvas = tk.Canvas(self, bg=BG, highlightthickness=0)
        scrollable_frame = ttk.Frame(main_canvas, style="TFrame")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        
        main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        main_canvas.pack(fill="both", expand=True, padx=6, pady=6)  # Centered padding
        
        # Enable smooth mouse wheel scrolling
        def _on_mousewheel(event):
            # Smooth scrolling with smaller increments
            main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        # Bind scrolling to the entire window, not just canvas
        self.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Also bind to canvas for redundancy
        main_canvas.bind("<MouseWheel>", _on_mousewheel)
        
        # Set focus to canvas so it can receive scroll events immediately
        main_canvas.focus_set()
        
        # Add scroll indicator
        self.create_scroll_indicator(main_canvas)
        
        main = ttk.Frame(scrollable_frame, padding=6, style="TFrame")  # Centered padding
        main.pack(fill="both", expand=True)
        
        # Store references for scaling
        self.main_frame = main
        self.main_canvas = main_canvas
        self.scrollable_frame = scrollable_frame
        
        # No window resize handling needed for fixed width
        
        # Title Section
        title_frame = ttk.Frame(main, style="TFrame")
        title_frame.pack(fill="x", pady=(0, 8))
        
        # Main title - smaller
        ttk.Label(title_frame, text=get_text("title", self.current_language), font=("Segoe UI", 14, "bold"), foreground="#e2ff00").pack()
        
        # Colorful WUNDAGUAD credit line
        credit_frame = ttk.Frame(title_frame, style="TFrame")
        credit_frame.pack(pady=(4, 0))
        
        # Create credit line with image
        ttk.Label(credit_frame, text="Created with ", font=("Segoe UI", 8), foreground="#9598a1").pack(side="left")
        ttk.Label(credit_frame, text="♥", font=("Segoe UI", 16), foreground="#FF0000").pack(side="left")  # Red heart - bigger
        ttk.Label(credit_frame, text=" by ", font=("Segoe UI", 8), foreground="#9598a1").pack(side="left")
        
        # Load and display WUNDAGUAD image
        try:
            import os
            from PIL import Image, ImageTk
            # Try multiple possible image names and locations
            possible_paths = [
                "wundaguad_logo.png",
                "wundaguad.png", 
                "WUNDAGUAD.png",
                "logo.png",
                os.path.join(os.path.dirname(__file__), "wundaguad_logo.png"),
                os.path.join(os.path.dirname(__file__), "wundaguad.png")
            ]
            
            image_loaded = False
            for path in possible_paths:
                try:
                    wundaguad_img = Image.open(path)
                    # Resize to fit the credit line (height ~20px, even larger)
                    img_height = 20
                    img_width = int(wundaguad_img.width * (img_height / wundaguad_img.height))
                    wundaguad_img = wundaguad_img.resize((img_width, img_height), Image.Resampling.LANCZOS)
                    self.wundaguad_photo = ImageTk.PhotoImage(wundaguad_img)
                    ttk.Label(credit_frame, image=self.wundaguad_photo).pack(side="left", padx=(2, 2))
                    image_loaded = True
                    break
                except:
                    continue
            
            if not image_loaded:
                raise Exception("No image found")
                
        except Exception as e:
            # Fallback to colorful text if image not found
            print(f"WUNDAGUAD image not found: {e}")  # Debug info
            ttk.Label(credit_frame, text="W", font=("Segoe UI", 8, "bold"), foreground="#FF0000").pack(side="left")  # Red
            ttk.Label(credit_frame, text="U", font=("Segoe UI", 8, "bold"), foreground="#FF6600").pack(side="left")  # Orange
            ttk.Label(credit_frame, text="N", font=("Segoe UI", 8, "bold"), foreground="#e2ff00").pack(side="left")  # Yellow
            ttk.Label(credit_frame, text="D", font=("Segoe UI", 8, "bold"), foreground="#66FF00").pack(side="left")  # Lime Green
            ttk.Label(credit_frame, text="A", font=("Segoe UI", 8, "bold"), foreground="#00FFCC").pack(side="left")  # Cyan
            ttk.Label(credit_frame, text="G", font=("Segoe UI", 8, "bold"), foreground="#0099FF").pack(side="left")  # Blue
            ttk.Label(credit_frame, text="U", font=("Segoe UI", 8, "bold"), foreground="#6666FF").pack(side="left")  # Purple
            ttk.Label(credit_frame, text="A", font=("Segoe UI", 8, "bold"), foreground="#CC66FF").pack(side="left")  # Violet
            ttk.Label(credit_frame, text="D", font=("Segoe UI", 8, "bold"), foreground="#FF99CC").pack(side="left")  # Pink
        
        ttk.Label(credit_frame, text=" for our community", font=("Segoe UI", 8), foreground="#9598a1").pack(side="left")
        
        # Main Input Card - larger padding for bigger section
        input_card = ttk.Frame(main, style="Card.TFrame", padding=10)  # Increased from 6 to 10
        input_card.pack(fill="x", pady=(0, 6))  # Increased from 4 to 6
        
        # Header with title and reset button
        header_frame = ttk.Frame(input_card, style="Card.TFrame")
        header_frame.pack(fill="x", pady=(0, 8))
        
        ttk.Label(header_frame, text=get_text("basic_settings", self.current_language), font=("Segoe UI", 12, "bold"), foreground="#e2ff00").pack(side="left")
        
        # Reset button
        reset_btn = ttk.Button(header_frame, text="🔄 Reset", style="Action.TButton", command=self.reset_inputs)
        reset_btn.pack(side="right", padx=(10, 0))
        
        # Grid for inputs
        input_grid = ttk.Frame(input_card, style="Card.TFrame")
        input_grid.pack(fill="x")
        input_grid.columnconfigure(1, weight=1)
        
        r = 0
        ttk.Label(input_grid, text=get_text("direction", self.current_language), font=("Segoe UI", 10, "bold")).grid(row=r, column=0, sticky="w", pady=6, padx=(0, 10))  # Larger font and spacing
        
        # Radio buttons for Long/Short - larger
        direction_frame = ttk.Frame(input_grid, style="Card.TFrame")
        direction_frame.grid(row=r, column=1, sticky="ew", pady=6)  # Increased padding
        
        self.direction_var = tk.StringVar(value="Long")
        self.rb_long = ttk.Radiobutton(direction_frame, text=get_text("long", self.current_language), variable=self.direction_var, value="Long", 
                       style="TRadiobutton", command=self.update_direction_colors)
        self.rb_long.pack(side="left", padx=(0, 25))  # Even more spacing
        self.rb_short = ttk.Radiobutton(direction_frame, text=get_text("short", self.current_language), variable=self.direction_var, value="Short", 
                        style="TRadiobutton", command=self.update_direction_colors)
        self.rb_short.pack(side="left")
        
        # Initialize colors
        self.update_direction_colors()

        r += 1
        ttk.Label(input_grid, text=get_text("entry_price", self.current_language), font=("Segoe UI", 11, "bold")).grid(row=r, column=0, sticky="w", pady=6, padx=(0, 8))  # Even larger font and spacing
        self.e_price = ttk.Entry(input_grid, width=20, font=("Segoe UI", 11))  # Larger font and width
        self.e_price.grid(row=r, column=1, sticky="w", pady=6, padx=(0, 0))  
        self.e_price.bind('<Return>', lambda e: self.calculate())
        self._add_context_menu(self.e_price)

        r += 1
        ttk.Label(input_grid, text=get_text("max_loss", self.current_language), font=("Segoe UI", 11, "bold")).grid(row=r, column=0, sticky="w", pady=6, padx=(0, 8))  # Even larger font and spacing
        self.e_max_loss = ttk.Entry(input_grid, width=20, font=("Segoe UI", 11))  # Larger font and width
        self.e_max_loss.grid(row=r, column=1, sticky="w", pady=6, padx=(0, 0))
        self.e_max_loss.insert(0, "10.00")
        self.e_max_loss.bind('<Return>', lambda e: self.calculate())
        self._add_context_menu(self.e_max_loss)

        r += 1
        ttk.Label(input_grid, text=get_text("stop_loss_percent", self.current_language), font=("Segoe UI", 11, "bold")).grid(row=r, column=0, sticky="w", pady=6, padx=(0, 8))  # Even larger font and spacing
        self.e_sl_percent = ttk.Entry(input_grid, width=20, font=("Segoe UI", 11))  # Larger font and width
        self.e_sl_percent.grid(row=r, column=1, sticky="w", pady=6, padx=(0, 0))
        self.e_sl_percent.insert(0, "0.51")
        self.e_sl_percent.bind('<Return>', lambda e: self.calculate())
        self._add_context_menu(self.e_sl_percent)

        # Leverage Card - same size as Basic Settings
        leverage_card = ttk.Frame(main, style="Card.TFrame", padding=10)  # Same as input_card
        leverage_card.pack(fill="x", pady=(0, 6))  # Same as input_card
        
        # Title with green accent
        title_frame = ttk.Frame(leverage_card, style="Card.TFrame")
        title_frame.pack(fill="x", pady=(0, 8))
        
        ttk.Label(title_frame, text="Hebelwirkung anpassen", 
                 font=("Segoe UI", 12, "bold"), foreground=PRIMARY).pack(anchor="w")  # Same size as Basic Settings
        
        # Leverage value display - centered and large
        self.leverage_var = tk.IntVar(value=self.settings.get("leverage", 1))
        
        value_frame = ttk.Frame(leverage_card, style="Card.TFrame")
        value_frame.pack(fill="x", pady=(0, 8))
        
        # Large leverage display - another 15% smaller
        self.leverage_label = ttk.Label(value_frame, text=f"{self.leverage_var.get()}X", 
                                       font=("Segoe UI", 20, "bold"), foreground=TEXT)  # 23 * 0.85 = 19.55 ≈ 20
        self.leverage_label.pack()
        
        # Slider - wider and centered
        slider_frame = ttk.Frame(leverage_card, style="Card.TFrame")
        slider_frame.pack(fill="x", pady=(0, 10))
        
        self.scale = ttk.Scale(
            slider_frame, from_=1, to=125,
            orient="horizontal", length=320,  # Increased to match button width
            style="Modern.Horizontal.TScale",
            variable=self.leverage_var
        )
        self.scale.pack(anchor="center")
        self.scale.configure(command=self._on_leverage_slide)
        
        # Scale markers with proper spacing - centered to match slider
        markers_frame = ttk.Frame(leverage_card, style="Card.TFrame")
        markers_frame.pack(fill="x", pady=(3, 15))
        markers_frame.configure(height=20)
        
        # Create inner frame for centering markers
        markers_inner = ttk.Frame(markers_frame, style="Card.TFrame")
        markers_inner.pack(anchor="center")
        markers_inner.configure(width=320, height=25)  # Match slider width and ensure height
        
        tick_values = [1, 25, 50, 75, 100, 125]
        for i, v in enumerate(tick_values):
            marker_label = ttk.Label(markers_inner, text=f"{v}X", 
                                   font=("Segoe UI", 9, "bold"), foreground=TEXT_MUTED)  # Larger, bold font
            marker_label.place(relx=i/5, rely=0.5, anchor="center")
        
        # Leverage buttons - rounded style
        buttons_frame = ttk.Frame(leverage_card, style="Card.TFrame")
        buttons_frame.pack(fill="x", pady=(8, 0))
        
        # Center buttons to prevent clipping
        button_container = ttk.Frame(buttons_frame, style="Card.TFrame")
        button_container.pack(anchor="center")  # Centered to fit in wider window
        
        tick_values = [1, 25, 50, 75, 100, 125]
        for i, v in enumerate(tick_values):
            btn = ttk.Button(button_container, text=f"{v}×", 
                           command=lambda val=v: self.set_leverage(val),
                           style="Rounded.TButton", width=6)
            btn.grid(row=0, column=i, padx=2, pady=2)

        # Advanced Settings (Collapsible Cards)
        self.create_advanced_sections(main)
        # Calculate Button
        calc_frame = ttk.Frame(main, style="TFrame")
        calc_frame.pack(fill="x", pady=(12, 15))
        
        # Calculate button frame for left alignment
        calc_btn_frame = ttk.Frame(main, style="TFrame")
        calc_btn_frame.pack(fill="x", pady=8)
        
        calc_btn = ttk.Button(calc_btn_frame, text=get_text("calculate", self.current_language), command=self.calculate, style="Primary.TButton")
        calc_btn.pack(fill="x", padx=8)  # Centered padding

        # Results Card
        self.results_card = ttk.Frame(main, style="Card.TFrame", padding=12)
        self.results_card.pack(fill="x", pady=(0, 8))
        
        ttk.Label(self.results_card, text=get_text("results", self.current_language), style="Heading.TLabel").pack(anchor="w", pady=(0, 8))
        
        self.results_grid = ttk.Frame(self.results_card, style="Card.TFrame")
        self.results_grid.pack(fill="x")
        self.results_grid.columnconfigure(1, weight=1)

        def create_result_row(row, icon, label_text, key, color=TEXT):
            ttk.Label(self.results_grid, text=f"{icon} {label_text}:", font=("Segoe UI", 9, "bold")).grid(row=row, column=0, sticky="w", pady=5, padx=(0, 15))  # Smaller font
            
            result_frame = ttk.Frame(self.results_grid, style="Surface.TFrame")
            result_frame.grid(row=row, column=1, sticky="ew", pady=5)  # More vertical spacing
            result_frame.columnconfigure(0, weight=1)
            
            lbl = ttk.Label(result_frame, text="0.00", font=("Segoe UI", 11, "bold"), foreground=color)  # Larger font
            lbl.pack(side="left", padx=8, pady=4)  # Centered padding
            
            # Use copy button style matching result color
            if "nominal" in key or "margin" in key:
                button_style = "Success.Copy.TButton" if "nominal" in key else "Warning.Copy.TButton"
            elif "sl" in key:
                button_style = "Danger.Copy.TButton"
            else:  # TP buttons
                button_style = "Profit.Copy.TButton"
            
            def create_copy_command(label, button_ref):
                def copy_command():
                    self.copy_with_feedback(label.cget("text"), button_ref[0])
                return copy_command
            
            copy_btn = ttk.Button(result_frame, text="📋", style=button_style)
            button_ref = [copy_btn]  # Use list to allow modification
            copy_btn.configure(command=create_copy_command(lbl, button_ref))
            copy_btn.pack(side="right", padx=(10, 0))  # More spacing
            
            return lbl

        self.lbl_nominal = create_result_row(0, get_text("nominal", self.current_language), "", "nominal", SUCCESS)
        self.lbl_margin  = create_result_row(1, get_text("margin", self.current_language), "", "margin", WARNING)
        self.lbl_slp     = create_result_row(2, get_text("sl_price", self.current_language), "", "sl_price", DANGER)
        self.lbl_tp1     = create_result_row(3, get_text("tp1", self.current_language), "", "tp1", PROFIT)
        self.lbl_tp2     = create_result_row(4, get_text("tp2", self.current_language), "", "tp2", PROFIT)
        self.lbl_tp3     = create_result_row(5, get_text("tp3", self.current_language), "", "tp3", PROFIT)
        
        # P&L Info
        self.pnl_card = ttk.Frame(main, style="Card.TFrame", padding=16)
        self.pnl_card.pack(fill="x", pady=(0, 12))
        
        ttk.Label(self.pnl_card, text="💹 Profit & Loss Analyse", style="Heading.TLabel").pack(anchor="w", pady=(0, 8))
        
        self.extra = ttk.Label(main, text="", font=("Segoe UI", 9), foreground="#9598a1", justify="left")
        self.extra.pack(fill="x", pady=(12, 0))
        
    def update_direction_colors(self):
        """Update radio button colors based on selection using ttk styles"""
        selected = self.direction_var.get()
        style = ttk.Style()
        
        if selected == "Long":
            # Long selected - green for Long, muted for Short - even larger font
            style.configure("Long.TRadiobutton", foreground="#4CAF50", font=("Segoe UI", 12))  # Green, even larger font
            style.configure("Short.TRadiobutton", foreground="#9598a1", font=("Segoe UI", 12))  # Muted gray, even larger font
            self.rb_long.configure(style="Long.TRadiobutton")
            self.rb_short.configure(style="Short.TRadiobutton")
        else:
            # Short selected - red for Short, muted for Long - even larger font
            style.configure("Long.TRadiobutton", foreground="#9598a1", font=("Segoe UI", 12))  # Muted gray, even larger font
            style.configure("Short.TRadiobutton", foreground="#F44336", font=("Segoe UI", 12))  # Red, even larger font
            self.rb_long.configure(style="Long.TRadiobutton")
            self.rb_short.configure(style="Short.TRadiobutton")
        
    def create_advanced_sections(self, parent):
        # Collapsible Fees Section
        fees_section = Collapsible(parent, "💸 Handelsgebühren", initially_open=False)
        fees_section.pack(fill="x", pady=(0, 12))
        
        fees_grid = ttk.Frame(fees_section.body, style="Card.TFrame", padding=10)  # Reduced from 16 to 10
        fees_grid.pack(fill="x")
        fees_grid.columnconfigure(1, weight=1)
        fees_grid.columnconfigure(3, weight=1)
        
        ttk.Label(fees_grid, text="Entry:", font=("Segoe UI", 8, "bold")).grid(row=0, column=0, sticky="w", pady=6, padx=(0, 6))  # Scaled down
        self.cb_entry_side = ttk.Combobox(fees_grid, values=["Taker", "Maker"], state="readonly", width=10, font=("Segoe UI", 7))  # Scaled down
        self.cb_entry_side.grid(row=0, column=1, sticky="ew", pady=6, padx=(0, 12)); self.cb_entry_side.set("Taker")
        
        ttk.Label(fees_grid, text="Exit:", font=("Segoe UI", 8, "bold")).grid(row=0, column=2, sticky="w", pady=6, padx=(0, 6))  # Scaled down
        self.cb_exit_side = ttk.Combobox(fees_grid, values=["Taker", "Maker"], state="readonly", width=10, font=("Segoe UI", 7))  # Scaled down
        self.cb_exit_side.grid(row=0, column=3, sticky="ew", pady=6); self.cb_exit_side.set("Taker")
        
        # Collapsible Settings Section
        settings_section = Collapsible(parent, "⚙️ Gebühren-Einstellungen", initially_open=False)
        settings_section.pack(fill="x", pady=(0, 12))
        
        settings_content = ttk.Frame(settings_section.body, style="Card.TFrame", padding=10)  # Reduced from 16 to 10
        settings_content.pack(fill="x")
        
        settings_grid = ttk.Frame(settings_content, style="Card.TFrame")
        settings_grid.pack(fill="x")
        settings_grid.columnconfigure(1, weight=1)
        settings_grid.columnconfigure(3, weight=1)
        
        ttk.Label(settings_grid, text="Maker (%):", font=("Segoe UI", 8, "bold")).grid(row=0, column=0, sticky="w", pady=6, padx=(0, 6))  # Scaled down
        self.e_maker = ttk.Entry(settings_grid, width=10, font=("Segoe UI", 7))  # Scaled down
        self.e_maker.grid(row=0, column=1, sticky="ew", pady=6, padx=(0, 12))
        self.e_maker.insert(0, f"{self.settings.get('maker_fee', 0.03)}")
        self.e_maker.bind('<Return>', lambda e: self.calculate())
        self._add_context_menu(self.e_maker)
        
        ttk.Label(settings_grid, text="Taker (%):", font=("Segoe UI", 8, "bold")).grid(row=0, column=2, sticky="w", pady=6, padx=(0, 6))  # Scaled down
        self.e_taker = ttk.Entry(settings_grid, width=10, font=("Segoe UI", 7))  # Scaled down
        self.e_taker.grid(row=0, column=3, sticky="ew", pady=6)
        self.e_taker.insert(0, f"{self.settings.get('taker_fee', 0.07)}")
        self.e_taker.bind('<Return>', lambda e: self.calculate())
        self._add_context_menu(self.e_taker)
        
        # Add number format settings
        ttk.Label(settings_grid, text=get_text("number_format", self.current_language), font=("Segoe UI", 8, "bold")).grid(row=1, column=0, sticky="w", pady=6, padx=(0, 6))  # Scaled down
        self.cb_format = ttk.Combobox(settings_grid, values=["Deutsch (115.327,2)", "US (115,327.2)"], state="readonly", width=16, font=("Segoe UI", 7))  # Scaled down
        self.cb_format.grid(row=1, column=1, sticky="ew", pady=6, padx=(0, 12))
        self.cb_format.set("Deutsch (115.327,2)" if self.settings.get("number_format", "german") == "german" else "US (115,327.2)")
        self.cb_format.bind("<<ComboboxSelected>>", self._on_format_change)
        
        # Add language settings
        ttk.Label(settings_grid, text=get_text("language", self.current_language), font=("Segoe UI", 8, "bold")).grid(row=1, column=2, sticky="w", pady=6, padx=(0, 6))  # Scaled down
        self.cb_language = ttk.Combobox(settings_grid, values=["Deutsch", "English"], state="readonly", width=12, font=("Segoe UI", 7))  # Scaled down
        self.cb_language.grid(row=1, column=3, sticky="ew", pady=6)
        self.cb_language.set("Deutsch" if self.current_language == "german" else "English")
        self.cb_language.bind("<<ComboboxSelected>>", self._on_language_change)
        
        ttk.Button(settings_content, text=get_text("save", self.current_language), command=self.on_save_settings, style="Modern.TButton")\
            .pack(pady=(8, 0))  # Reduced padding
        
        # Collapsible Take-Profit Section
        tp_section = Collapsible(parent, "🎯 Take-Profit Konfiguration", initially_open=False)
        tp_section.pack(fill="x", pady=(0, 12))
        
        tp_content = ttk.Frame(tp_section.body, style="Card.TFrame", padding=10)  # Reduced from 16 to 10
        tp_content.pack(fill="x")
        
        tp_mode_frame = ttk.Frame(tp_content, style="Card.TFrame")
        tp_mode_frame.pack(fill="x", pady=(0, 8))  # Reduced padding
        
        ttk.Label(tp_mode_frame, text="Modus:", font=("Segoe UI", 8, "bold")).pack(side="left", padx=(0, 6))  # Scaled down
        self.cb_tp_mode = ttk.Combobox(tp_mode_frame, values=["R-Multiple", "Prozent"], state="readonly", width=12, font=("Segoe UI", 7))  # Scaled down
        self.cb_tp_mode.pack(side="left"); self.cb_tp_mode.set("R-Multiple")
        
        tp_grid = ttk.Frame(tp_content, style="Card.TFrame")
        tp_grid.pack(fill="x")
        tp_grid.columnconfigure(1, weight=1)
        tp_grid.columnconfigure(3, weight=1)
        tp_grid.columnconfigure(5, weight=1)
        
        # R-Multiple inputs
        ttk.Label(tp_grid, text="TP1 (R):", font=("Segoe UI", 7, "bold")).grid(row=0, column=0, sticky="w", pady=3, padx=(0, 3))  # Scaled down
        self.e_tp1r = ttk.Entry(tp_grid, width=6, font=("Segoe UI", 7)); self.e_tp1r.grid(row=0, column=1, sticky="ew", pady=3, padx=(0, 6)); self.e_tp1r.insert(0, "1")  # Scaled down
        self.e_tp1r.bind('<Return>', lambda e: self.calculate())
        self._add_context_menu(self.e_tp1r)
        ttk.Label(tp_grid, text="TP2 (R):", font=("Segoe UI", 7, "bold")).grid(row=0, column=2, sticky="w", pady=3, padx=(0, 3))  # Scaled down
        self.e_tp2r = ttk.Entry(tp_grid, width=6, font=("Segoe UI", 7)); self.e_tp2r.grid(row=0, column=3, sticky="ew", pady=3, padx=(0, 6)); self.e_tp2r.insert(0, "2")  # Scaled down
        self.e_tp2r.bind('<Return>', lambda e: self.calculate())
        self._add_context_menu(self.e_tp2r)
        ttk.Label(tp_grid, text="TP3 (R):", font=("Segoe UI", 7, "bold")).grid(row=0, column=4, sticky="w", pady=3, padx=(0, 3))  # Scaled down
        self.e_tp3r = ttk.Entry(tp_grid, width=6, font=("Segoe UI", 7)); self.e_tp3r.grid(row=0, column=5, sticky="ew", pady=3); self.e_tp3r.insert(0, "3")  # Scaled down
        self.e_tp3r.bind('<Return>', lambda e: self.calculate())
        self._add_context_menu(self.e_tp3r)
        
        # Percentage inputs
        ttk.Label(tp_grid, text="TP1 (%):", font=("Segoe UI", 7, "bold")).grid(row=1, column=0, sticky="w", pady=3, padx=(0, 3))  # Scaled down
        self.e_tp1p = ttk.Entry(tp_grid, width=6, font=("Segoe UI", 7)); self.e_tp1p.grid(row=1, column=1, sticky="ew", pady=3, padx=(0, 6)); self.e_tp1p.insert(0, "1.00")  # Scaled down
        self.e_tp1p.bind('<Return>', lambda e: self.calculate())
        self._add_context_menu(self.e_tp1p)
        ttk.Label(tp_grid, text="TP2 (%):", font=("Segoe UI", 7, "bold")).grid(row=1, column=2, sticky="w", pady=3, padx=(0, 3))  # Scaled down
        self.e_tp2p = ttk.Entry(tp_grid, width=6, font=("Segoe UI", 7)); self.e_tp2p.grid(row=1, column=3, sticky="ew", pady=3, padx=(0, 6)); self.e_tp2p.insert(0, "2.00")  # Scaled down
        self.e_tp2p.bind('<Return>', lambda e: self.calculate())
        self._add_context_menu(self.e_tp2p)
        ttk.Label(tp_grid, text="TP3 (%):", font=("Segoe UI", 7, "bold")).grid(row=1, column=4, sticky="w", pady=3, padx=(0, 3))  # Scaled down
        self.e_tp3p = ttk.Entry(tp_grid, width=6, font=("Segoe UI", 7)); self.e_tp3p.grid(row=1, column=5, sticky="ew", pady=3); self.e_tp3p.insert(0, "3.00")  # Scaled down
        self.e_tp3p.bind('<Return>', lambda e: self.calculate())
        self._add_context_menu(self.e_tp3p)
        
        self.cb_tp_mode.bind("<<ComboboxSelected>>", lambda _e: self.update_tp_visibility())
        self.update_tp_visibility()

    def on_window_resize(self, event):
        """Handle window resize with CSS-like zoom scaling"""
        if event.widget == self:
            # Immediate resize for better responsiveness
            if hasattr(self, '_resize_after_id'):
                self.after_cancel(self._resize_after_id)
            self._resize_after_id = self.after(10, self._do_css_zoom)
    
    def _do_css_zoom(self):
        """Apply CSS-like zoom to entire content"""
        window_height = self.winfo_height()
        window_width = self.winfo_width()
        
        # Calculate zoom factor based on window size - prioritize width for narrow windows
        base_height = 900
        base_width = 520
        
        # Zoom system: keep original size for wide windows, scale down for narrow windows
        if window_width >= base_width:
            # For wide windows: keep original size (1.0x zoom)
            zoom_factor = 1.0
        else:
            # For narrow windows: scale down to fit content
            zoom_factor = window_width / base_width
        
        zoom_factor = max(0.1, min(1.0, zoom_factor))  # Allow more aggressive scaling
        
        # Back to working font scaling approach
        self.apply_css_zoom_fonts(zoom_factor)
        
        # Adjust canvas width to fill window
        if hasattr(self, 'main_canvas'):
            canvas_width = window_width - 20
            self.main_canvas.configure(width=canvas_width)
        
        # Update scroll region
        if hasattr(self, 'main_canvas') and hasattr(self, 'scrollable_frame'):
            self.scrollable_frame.update_idletasks()
            self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
    
    def apply_css_zoom_fonts(self, zoom):
        """Apply uniform font scaling like CSS zoom - optimized for speed"""
        # Force update by removing cache check for debugging
        self._last_zoom = zoom
        
        # Scale all fonts proportionally - another 15% smaller
        title_size = max(3, int(14 * zoom))  # 16 * 0.85 = 13.6 ≈ 14
        heading_size = max(3, int(9 * zoom))  # 11 * 0.85 = 9.35 ≈ 9
        body_size = max(2, int(8 * zoom))  # 9 * 0.85 = 7.65 ≈ 8
        large_size = max(4, int(20 * zoom))  # 23 * 0.85 = 19.55 ≈ 20
        entry_size = max(2, int(7 * zoom))  # 8 * 0.85 = 6.8 ≈ 7
        
        # Scale button padding
        button_padding = max(1, int(6 * zoom))
        copy_padding_x = max(1, int(3 * zoom))
        copy_padding_y = max(1, int(2 * zoom))
        
        # Update all styles with zoom - batch operations
        style = ttk.Style()
        
        # Batch configure all styles at once
        style_configs = {
            "Title.TLabel": {"font": ("Segoe UI", title_size, "bold")},
            "Heading.TLabel": {"font": ("Segoe UI", heading_size, "bold")},
            "TLabel": {"font": ("Segoe UI", body_size)},
            "TEntry": {"font": ("Segoe UI", entry_size)},
            "TCombobox": {"font": ("Segoe UI", entry_size)},
            "TButton": {"font": ("Segoe UI", body_size)},
            "Action.TButton": {"font": ("Segoe UI", body_size, "bold"), "padding": (button_padding, button_padding)},
            "Copy.TButton": {"font": ("Segoe UI", max(4, int(10 * zoom))), "padding": (copy_padding_x, copy_padding_y)},
            "TRadiobutton": {"font": ("Segoe UI", body_size)},
            "TCheckbutton": {"font": ("Segoe UI", body_size)},
            "Responsive.Horizontal.TProgressbar": {
                "troughcolor": "#2A2A2A",
                "borderwidth": 0,
                "lightcolor": "#e2ff00",
                "darkcolor": "#e2ff00",
                "thickness": max(4, int(20 * zoom))
            }
        }
        
        for style_name, config in style_configs.items():
            style.configure(style_name, **config)
        
        # Update leverage display
        if hasattr(self, 'leverage_label'):
            self.leverage_label.config(font=("Segoe UI", large_size, "bold"))
        
        # Batch update widget dimensions - allow smaller minimum sizes
        entry_width = max(2, int(15 * zoom))
        button_width = max(1, int(6 * zoom))
        combo_width = max(2, int(12 * zoom))
        
        # Update widgets in batches
        widget_updates = [
            (['e_price', 'e_max_loss', 'e_sl_percent', 'e_leverage', 'e_maker_fee', 'e_taker_fee', 'e_tp1p', 'e_tp2p', 'e_tp3p', 'e_tp1r', 'e_tp2r', 'e_tp3r'], 'width', entry_width),
            (['btn_1x', 'btn_25x', 'btn_50x', 'btn_75x'], 'width', button_width),
            (['cb_number_format', 'cb_language', 'cb_tp_mode'], 'width', combo_width),
            (['progress_nominal', 'progress_units', 'progress_sl_price', 'progress_margin', 'progress_tp1', 'progress_tp2', 'progress_tp3'], 'style', "Responsive.Horizontal.TProgressbar")
        ]
        
        for widget_names, attr, value in widget_updates:
            for widget_name in widget_names:
                if hasattr(self, widget_name):
                    widget = getattr(self, widget_name)
                    if attr == 'style':
                        widget.configure(style=value)
                    else:
                        widget.config(**{attr: value})
        
        # Scale frame paddings dynamically
        frame_padding = max(2, int(16 * zoom))
        small_padding = max(1, int(8 * zoom))
        
        # Update card frame paddings
        for card_name in ['input_card', 'leverage_card', 'results_card', 'pnl_card']:
            if hasattr(self, card_name):
                try:
                    getattr(self, card_name).config(padding=frame_padding)
                except:
                    pass
        
        # Scale pady and padx for all grid elements by updating their configuration
        scaled_pady = max(1, int(4 * zoom))
        scaled_padx = max(1, int(8 * zoom))
        
        # Update main frame padding
        if hasattr(self, 'main_frame'):
            try:
                self.main_frame.config(padding=frame_padding)
            except:
                pass
        
        # Scale ALL hardcoded fonts in labels throughout the interface
        scaled_font_9 = max(2, int(9 * zoom))
        scaled_font_10 = max(2, int(10 * zoom))
        
        # Update all hardcoded font labels
        hardcoded_font_widgets = [
            # Basic Settings labels
            'Direction:', 'Order Price:', 'Max. Loss (€):', 'Stop-Loss (%):',
            # Leverage section labels  
            'TP1 (R):', 'TP2 (R):', 'TP3 (R):', 'TP1 (%):', 'TP2 (%):', 'TP3 (%):',
            # Settings labels
            'Maker Fee (%):', 'Taker Fee (%):', 'Number Format:', 'Language:',
            # Results labels
            'Nominal Value :', 'Margin :', 'Stop-Loss :', 'TP1 :', 'TP2 :', 'TP3 :'
        ]
        
        # Recursively find and update all widgets with hardcoded fonts
        self._scale_hardcoded_fonts_recursive(self, zoom)
    
    def _scale_hardcoded_fonts_recursive(self, widget, zoom):
        """Recursively find and scale all widgets with hardcoded fonts"""
        try:
            # Check if widget has font configuration
            if hasattr(widget, 'config'):
                try:
                    current_font = widget.cget('font')
                    if current_font and isinstance(current_font, tuple) and len(current_font) >= 2:
                        # Scale the font size
                        font_family = current_font[0]
                        original_size = current_font[1]
                        font_style = current_font[2] if len(current_font) > 2 else ""
                        
                        new_size = max(2, int(original_size * zoom))
                        new_font = (font_family, new_size, font_style) if font_style else (font_family, new_size)
                        widget.config(font=new_font)
                except:
                    pass
            
            # Recursively check all children
            if hasattr(widget, 'winfo_children'):
                for child in widget.winfo_children():
                    self._scale_hardcoded_fonts_recursive(child, zoom)
        except:
            pass
    
    def _brute_force_scale_everything(self, zoom):
        """Brute force scaling - modify every widget property directly"""
        # Store original zoom for reference
        if not hasattr(self, '_original_zoom'):
            self._original_zoom = 1.0
        
        # Calculate scale ratio from original
        scale_ratio = zoom / self._original_zoom if hasattr(self, '_original_zoom') else zoom
        
        # Scale ALL widgets recursively
        self._scale_widget_brutally(self, zoom)
        
        # Update original zoom
        self._original_zoom = zoom
    
    def _scale_widget_brutally(self, widget, zoom):
        """Scale widget with maximum force - no mercy"""
        try:
            # Scale fonts - handle ALL possible font formats
            if hasattr(widget, 'configure') and hasattr(widget, 'cget'):
                # Font scaling
                try:
                    font = widget.cget('font')
                    if font:
                        # Handle string fonts like "Segoe UI 10 bold"
                        if isinstance(font, str) and font:
                            parts = font.split()
                            if len(parts) >= 2:
                                try:
                                    size = int(parts[1])
                                    new_size = max(1, int(size * zoom))
                                    new_font = f"{parts[0]} {new_size}"
                                    if len(parts) > 2:
                                        new_font += " " + " ".join(parts[2:])
                                    widget.configure(font=new_font)
                                except:
                                    pass
                        # Handle tuple fonts like ("Segoe UI", 10, "bold")
                        elif isinstance(font, tuple) and len(font) >= 2:
                            try:
                                family, size = font[0], font[1]
                                new_size = max(1, int(size * zoom))
                                if len(font) > 2:
                                    widget.configure(font=(family, new_size, font[2]))
                                else:
                                    widget.configure(font=(family, new_size))
                            except:
                                pass
                except:
                    pass
                
                # Scale dimensions
                for prop in ['width', 'height']:
                    try:
                        value = widget.cget(prop)
                        if value and isinstance(value, (int, float)) and value > 0:
                            new_value = max(1, int(value * zoom))
                            widget.configure(**{prop: new_value})
                    except:
                        pass
                
                # Scale padding if it exists
                try:
                    padding = widget.cget('padding')
                    if padding:
                        if isinstance(padding, (int, float)):
                            new_padding = max(1, int(padding * zoom))
                            widget.configure(padding=new_padding)
                        elif isinstance(padding, (list, tuple)):
                            new_padding = [max(1, int(p * zoom)) for p in padding]
                            widget.configure(padding=new_padding)
                except:
                    pass
            
            # Recursively scale all children
            if hasattr(widget, 'winfo_children'):
                for child in widget.winfo_children():
                    self._scale_widget_brutally(child, zoom)
        except:
            pass
    
    def _force_complete_rescale(self, zoom):
        """Force rescale of ALL widgets by directly modifying their properties"""
        # Scale every single widget in the entire interface
        self._rescale_widget_tree(self, zoom)
    
    def _rescale_widget_tree(self, widget, zoom):
        """Recursively rescale every widget property"""
        try:
            widget_class = widget.__class__.__name__
            
            # Scale fonts for ALL widgets that have them
            if hasattr(widget, 'configure'):
                try:
                    # Try to get current font
                    current_font = widget.cget('font')
                    if current_font:
                        if isinstance(current_font, str):
                            # Parse string font format
                            parts = current_font.split()
                            if len(parts) >= 2:
                                family = parts[0]
                                try:
                                    size = int(parts[1])
                                    new_size = max(1, int(size * zoom))
                                    style = ' '.join(parts[2:]) if len(parts) > 2 else ''
                                    new_font = f"{family} {new_size} {style}".strip()
                                    widget.configure(font=new_font)
                                except:
                                    pass
                        elif isinstance(current_font, tuple) and len(current_font) >= 2:
                            # Tuple font format
                            family, size = current_font[0], current_font[1]
                            style = current_font[2] if len(current_font) > 2 else ''
                            new_size = max(1, int(size * zoom))
                            new_font = (family, new_size, style) if style else (family, new_size)
                            widget.configure(font=new_font)
                except:
                    pass
                
                # Scale widget dimensions
                try:
                    if hasattr(widget, 'cget'):
                        # Scale width if it exists
                        try:
                            width = widget.cget('width')
                            if width and isinstance(width, int) and width > 0:
                                new_width = max(1, int(width * zoom))
                                widget.configure(width=new_width)
                        except:
                            pass
                        
                        # Scale height if it exists
                        try:
                            height = widget.cget('height')
                            if height and isinstance(height, int) and height > 0:
                                new_height = max(1, int(height * zoom))
                                widget.configure(height=new_height)
                        except:
                            pass
                except:
                    pass
            
            # Recursively process all children
            if hasattr(widget, 'winfo_children'):
                for child in widget.winfo_children():
                    self._rescale_widget_tree(child, zoom)
        except:
            pass
    
    def apply_simple_scaling(self, scale):
        """Apply comprehensive scaling of all elements while maintaining proportions"""
        # Scale fonts
        title_size = max(8, int(18 * scale))
        heading_size = max(7, int(12 * scale))
        body_size = max(6, int(10 * scale))
        large_size = max(10, int(28 * scale))
        entry_size = max(6, int(9 * scale))
        
        # Update styles
        style = ttk.Style()
        style.configure("Title.TLabel", font=("Segoe UI", title_size, "bold"))
        style.configure("Heading.TLabel", font=("Segoe UI", heading_size, "bold"))
        style.configure("TLabel", font=("Segoe UI", body_size))
        style.configure("TEntry", font=("Segoe UI", entry_size))
        style.configure("TCombobox", font=("Segoe UI", entry_size))
        
        # Scale button fonts and padding
        button_padding = max(2, int(6 * scale))
        style.configure("Action.TButton", 
                      font=("Segoe UI", body_size, "bold"),
                      padding=(button_padding, button_padding))
        style.configure("Copy.TButton", 
                      font=("Segoe UI", max(5, int(10 * scale))),
                      padding=(max(1, int(3 * scale)), max(1, int(2 * scale))))
        style.configure("TRadiobutton", font=("Segoe UI", body_size))
        style.configure("TCheckbutton", font=("Segoe UI", body_size))
        
        # Scale progress bars
        progress_height = max(6, int(20 * scale))
        style.configure("Responsive.Horizontal.TProgressbar", 
                      troughcolor="#2A2A2A", 
                      borderwidth=0, 
                      lightcolor="#e2ff00", 
                      darkcolor="#e2ff00",
                      thickness=progress_height)
        
        # Update leverage display
        if hasattr(self, 'leverage_label'):
            self.leverage_label.config(font=("Segoe UI", large_size, "bold"))
        
        # Scale entry field widths
        entry_width = max(6, int(15 * scale))
        for widget_name in ['e_price', 'e_max_loss', 'e_sl_percent', 'e_leverage', 
                           'e_maker_fee', 'e_taker_fee', 'e_tp1p', 'e_tp2p', 'e_tp3p']:
            if hasattr(self, widget_name):
                widget = getattr(self, widget_name)
                widget.config(width=entry_width)
        
        # Scale leverage buttons
        button_width = max(3, int(6 * scale))
        for widget_name in ['btn_1x', 'btn_25x', 'btn_50x', 'btn_75x']:
            if hasattr(self, widget_name):
                widget = getattr(self, widget_name)
                widget.config(width=button_width)
        
        # Scale combobox widths
        combo_width = max(6, int(12 * scale))
        for widget_name in ['cb_number_format', 'cb_language', 'cb_tp_mode']:
            if hasattr(self, widget_name):
                widget = getattr(self, widget_name)
                widget.config(width=combo_width)
        
        # Scale frame paddings
        frame_padding = max(2, int(16 * scale))
        try:
            if hasattr(self, 'results_card'):
                self.results_card.config(padding=frame_padding)
            if hasattr(self, 'pnl_card'):
                self.pnl_card.config(padding=frame_padding)
        except:
            pass
        
        # Update all progress bars to use scaled style
        for widget_name in ['progress_nominal', 'progress_units', 'progress_sl_price', 
                           'progress_margin', 'progress_tp1', 'progress_tp2', 'progress_tp3']:
            if hasattr(self, widget_name):
                widget = getattr(self, widget_name)
                widget.configure(style="Responsive.Horizontal.TProgressbar")
        
        # Update scroll region after scaling
        if hasattr(self, 'main_canvas'):
            self.main_frame.update_idletasks()
            self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
    
    def apply_zoom(self, zoom):
        """Apply uniform zoom scaling to all UI elements"""
        # Scale fonts with zoom factor - allow extreme scaling for tiny windows
        title_size = max(4, int(18 * zoom))
        heading_size = max(4, int(12 * zoom))
        body_size = max(4, int(10 * zoom))
        large_size = max(6, int(28 * zoom))
        entry_size = max(4, int(9 * zoom))
        
        # Update all styles with zoomed fonts
        style = ttk.Style()
        style.configure("Title.TLabel", font=("Segoe UI", title_size, "bold"))
        style.configure("Heading.TLabel", font=("Segoe UI", heading_size, "bold"))
        style.configure("TLabel", font=("Segoe UI", body_size))
        style.configure("TEntry", font=("Segoe UI", entry_size))
        style.configure("TCombobox", font=("Segoe UI", entry_size))
        
        # Update leverage display
        if hasattr(self, 'leverage_label'):
            self.leverage_label.config(font=("Segoe UI", large_size, "bold"))
        
        # Scale padding and spacing - allow very small padding
        padding = max(1, int(16 * zoom))
        button_padding = max(1, int(6 * zoom))
        
        # Update button styles with zoom
        style.configure("Action.TButton", 
                      font=("Segoe UI", body_size, "bold"),
                      padding=(button_padding, button_padding))
        style.configure("Copy.TButton", 
                      font=("Segoe UI", max(4, int(10 * zoom))),
                      padding=(max(1, int(3 * zoom)), max(1, int(2 * zoom))))
        
        # Update frame paddings
        try:
            if hasattr(self, 'results_card'):
                self.results_card.config(padding=padding)
            if hasattr(self, 'pnl_card'):
                self.pnl_card.config(padding=padding)
        except:
            pass
        
        # Scale progress bar height - allow very thin bars
        progress_height = max(4, int(20 * zoom))
        style.configure("Responsive.Horizontal.TProgressbar", 
                      troughcolor="#2A2A2A", 
                      borderwidth=0, 
                      lightcolor="#e2ff00", 
                      darkcolor="#e2ff00",
                      thickness=progress_height)
        
        # Scale all progress bars
        for widget_name in ['progress_nominal', 'progress_units', 'progress_sl_price', 
                           'progress_margin', 'progress_tp1', 'progress_tp2', 'progress_tp3']:
            if hasattr(self, widget_name):
                widget = getattr(self, widget_name)
                widget.configure(style="Responsive.Horizontal.TProgressbar")
        
        # Scale leverage buttons with proper width
        button_width = max(2, int(8 * zoom))
        for widget_name in ['btn_1x', 'btn_25x', 'btn_50x', 'btn_75x']:
            if hasattr(self, widget_name):
                widget = getattr(self, widget_name)
                widget.config(width=button_width)
        
        # Scale entry field widths
        entry_width = max(5, int(18 * zoom))
        for widget_name in ['e_price', 'e_max_loss', 'e_sl_percent', 'e_leverage', 
                           'e_maker_fee', 'e_taker_fee', 'e_tp1p', 'e_tp2p', 'e_tp3p']:
            if hasattr(self, widget_name):
                widget = getattr(self, widget_name)
                widget.config(width=entry_width)
        
        # Scale combobox widths
        combo_width = max(6, int(15 * zoom))
        for widget_name in ['cb_number_format', 'cb_language', 'cb_tp_mode']:
            if hasattr(self, widget_name):
                widget = getattr(self, widget_name)
                widget.config(width=combo_width)
        
        # Scale all frame paddings dynamically
        frame_padding = max(2, int(16 * zoom))
        small_padding = max(1, int(8 * zoom))
        
        # Update all card paddings
        for widget_name in ['input_card', 'leverage_card', 'results_card', 'pnl_card']:
            if hasattr(self, widget_name):
                try:
                    getattr(self, widget_name).config(padding=frame_padding)
                except:
                    pass
        
        # Scale all other UI elements that might not be scaling
        # Update radio button fonts
        style.configure("TRadiobutton", font=("Segoe UI", body_size))
        
        # Update checkbutton fonts
        style.configure("TCheckbutton", font=("Segoe UI", body_size))
        
        # Update frame padding for all cards
        card_padding = max(1, int(16 * zoom))
        
        # Scale all frame paddings dynamically
        try:
            if hasattr(self, 'input_card'):
                self.input_card.config(padding=card_padding)
            if hasattr(self, 'leverage_card'):
                self.leverage_card.config(padding=card_padding)
            if hasattr(self, 'results_card'):
                self.results_card.config(padding=card_padding)
            if hasattr(self, 'pnl_card'):
                self.pnl_card.config(padding=card_padding)
        except:
            pass
        
        # Scale scroll indicator
        if hasattr(self, 'scroll_hint'):
            scroll_font_size = max(4, int(8 * zoom))
            self.scroll_hint.config(font=("Segoe UI", scroll_font_size))
        
        # Scale the zoom slider itself (but not its value)
        if hasattr(self, 'zoom_scale') and zoom != self.current_zoom:
            try:
                # Don't scale the zoom control to avoid recursion
                pass
            except:
                pass
        
        # Scale ALL widgets recursively - this catches everything
        self._scale_all_widgets_comprehensive(zoom)
    
    def _scale_all_widgets_comprehensive(self, zoom):
        """Comprehensive scaling of ALL UI elements"""
        # Scale every single widget in the entire application
        self._scale_widget_and_children(self, zoom)
    
    def _scale_widget_and_children(self, widget, zoom):
        """Scale a widget and all its children recursively"""
        try:
            widget_class = widget.winfo_class()
            
            # Scale buttons (all types)
            if 'Button' in widget_class:
                try:
                    # Scale button font
                    current_font = widget.cget("font")
                    if current_font:
                        if isinstance(current_font, tuple):
                            base_size = current_font[1] if len(current_font) > 1 else 10
                            new_size = max(4, int(base_size * zoom))
                            widget.config(font=(current_font[0], new_size, *current_font[2:]))
                        else:
                            # Default button font scaling
                            new_size = max(6, int(10 * zoom))
                            widget.config(font=("Segoe UI", new_size))
                    
                    # Scale button padding
                    padding = max(1, int(4 * zoom))
                    try:
                        widget.config(padx=padding, pady=padding)
                    except:
                        pass
                except:
                    pass
            
            # Scale labels (all types)
            elif 'Label' in widget_class:
                try:
                    current_font = widget.cget("font")
                    if current_font and current_font != "":
                        if isinstance(current_font, tuple):
                            base_size = current_font[1] if len(current_font) > 1 else 10
                            new_size = max(4, int(base_size * zoom))
                            widget.config(font=(current_font[0], new_size, *current_font[2:]))
                except:
                    pass
            
            # Scale entries
            elif 'Entry' in widget_class:
                try:
                    current_font = widget.cget("font")
                    if current_font:
                        if isinstance(current_font, tuple):
                            base_size = current_font[1] if len(current_font) > 1 else 9
                            new_size = max(4, int(base_size * zoom))
                            widget.config(font=(current_font[0], new_size, *current_font[2:]))
                    
                    # Scale entry width
                    try:
                        current_width = widget.cget("width")
                        if current_width:
                            new_width = max(3, int(current_width * zoom))
                            widget.config(width=new_width)
                    except:
                        pass
                except:
                    pass
            
            # Scale frames and their padding
            elif 'Frame' in widget_class:
                try:
                    # Scale frame padding if it has any
                    padding = max(1, int(8 * zoom))
                    try:
                        widget.config(padding=padding)
                    except:
                        pass
                except:
                    pass
            
            # Scale progressbars
            elif 'Progressbar' in widget_class:
                try:
                    # Already handled by style, but ensure it's applied
                    widget.configure(style="Responsive.Horizontal.TProgressbar")
                except:
                    pass
            
            # Scale radiobuttons and checkbuttons
            elif widget_class in ['Radiobutton', 'Checkbutton', 'TRadiobutton', 'TCheckbutton']:
                try:
                    current_font = widget.cget("font")
                    if current_font:
                        if isinstance(current_font, tuple):
                            base_size = current_font[1] if len(current_font) > 1 else 10
                            new_size = max(4, int(base_size * zoom))
                            widget.config(font=(current_font[0], new_size, *current_font[2:]))
                except:
                    pass
            
            # Recursively scale all children
            for child in widget.winfo_children():
                self._scale_widget_and_children(child, zoom)
                
        except Exception as e:
            # Continue scaling even if one widget fails
            pass
        
        # Force complete update
        try:
            self.update()
            self.update_idletasks()
        except:
            pass
    
    def _scale_widget_recursive(self, widget, zoom):
        """Recursively scale all widgets and their children"""
        try:
            # Scale labels with fixed fonts
            if isinstance(widget, tk.Label):
                current_font = widget.cget("font")
                if isinstance(current_font, tuple) and len(current_font) >= 2:
                    base_size = current_font[1] if current_font[1] > 20 else 10
                    new_size = max(4, int(base_size * zoom))
                    widget.config(font=(current_font[0], new_size, *current_font[2:]))
            
            # Scale ttk labels that might not be using styles
            elif hasattr(widget, 'winfo_class') and widget.winfo_class() == 'TLabel':
                try:
                    current_font = widget.cget("font")
                    if current_font and not current_font.startswith("TkDefault"):
                        if isinstance(current_font, tuple) and len(current_font) >= 2:
                            base_size = current_font[1] if current_font[1] > 20 else 10
                            new_size = max(4, int(base_size * zoom))
                            widget.config(font=(current_font[0], new_size, *current_font[2:]))
                except:
                    pass
            
            # Recursively scale children
            for child in widget.winfo_children():
                self._scale_widget_recursive(child, zoom)
        except:
            pass

    def create_scroll_indicator(self, canvas):
        """Create a subtle scroll indicator to show scrollable content"""
        # Create scroll hint at bottom right
        self.scroll_hint = tk.Label(self, text="⇅ Scroll", 
                                   font=("Segoe UI", 8), 
                                   fg="#666666", bg="#121212",
                                   relief="flat")
        self.scroll_hint.place(relx=0.98, rely=0.98, anchor="se")
        
        # Auto-hide after 3 seconds
        self.after(3000, lambda: self.scroll_hint.place_forget())
        
        # Show hint again when scrolling reaches top or bottom
        def check_scroll_position():
            try:
                top, bottom = canvas.yview()
                if bottom >= 1.0:  # At bottom
                    self.scroll_hint.config(text="⇈ Scroll Up")
                    self.scroll_hint.place(relx=0.98, rely=0.98, anchor="se")
                    self.after(2000, lambda: self.scroll_hint.place_forget())
                elif top <= 0.0:  # At top
                    self.scroll_hint.config(text="⇊ Scroll Down")
                    self.scroll_hint.place(relx=0.98, rely=0.98, anchor="se")
                    self.after(2000, lambda: self.scroll_hint.place_forget())
            except:
                pass
        
        # Bind scroll position check to canvas
        def on_scroll_check(event):
            self.after(100, check_scroll_position)
        
        canvas.bind("<Configure>", on_scroll_check)

    # ---------- UI helpers ----------
    def _on_leverage_slide(self, value):
        """Robuster Slider-Callback mit 1er Schritten."""
        try:
            leverage = int(float(value) + 0.5)  # Runden auf ganze Zahl
        except Exception:
            leverage = self.leverage_var.get()
        leverage = max(1, min(leverage, 125))
        self.leverage_var.set(leverage)
        self.leverage_label.config(text=f"{leverage}X")
        # Save leverage setting
        self.settings["leverage"] = leverage
        save_settings(self.settings)

    def set_leverage(self, value):
        """Set leverage to specific value via button click."""
        self.leverage_var.set(value)
        self.scale.set(value)
        self.leverage_label.config(text=f"{value}X")

    def _current_leverage(self):
        """Get current leverage value."""
        return self.leverage_var.get()
    
    def fee_for(self, side):
        """Get fee percentage for given side (Maker/Taker)."""
        if side == "Maker":
            return self.settings.get("maker_fee", 0.014)
        else:  # Taker
            return self.settings.get("taker_fee", 0.042)
    
    def _add_context_menu(self, entry_widget):
        """Add right-click context menu to entry widgets."""
        def show_context_menu(event):
            try:
                context_menu = tk.Menu(self, tearoff=0)
                context_menu.add_command(label="Ausschneiden", command=lambda: self._cut_text(entry_widget))
                context_menu.add_command(label="Kopieren", command=lambda: self._copy_text(entry_widget))
                context_menu.add_command(label="Einfügen", command=lambda: self._paste_text(entry_widget))
                context_menu.add_separator()
                context_menu.add_command(label="Alles auswählen", command=lambda: self._select_all(entry_widget))
                context_menu.tk_popup(event.x_root, event.y_root)
            except Exception:
                pass
            finally:
                try:
                    context_menu.destroy()
                except:
                    pass
        
        entry_widget.bind("<Button-3>", show_context_menu)  # Right-click
    
    def _cut_text(self, entry_widget):
        """Cut text from entry widget."""
        try:
            if entry_widget.selection_present():
                entry_widget.event_generate("<<Cut>>")
        except:
            pass
    
    def _copy_text(self, entry_widget):
        """Copy text from entry widget."""
        try:
            if entry_widget.selection_present():
                entry_widget.event_generate("<<Copy>>")
        except:
            pass
    
    def _paste_text(self, entry_widget):
        """Paste text to entry widget."""
        try:
            entry_widget.event_generate("<<Paste>>")
        except:
            pass
    
    def _select_all(self, entry_widget):
        """Select all text in entry widget."""
        try:
            entry_widget.select_range(0, tk.END)
        except:
            pass

    def update_tp_visibility(self):
        mode = self.cb_tp_mode.get()
        r_widgets = [self.e_tp1r, self.e_tp2r, self.e_tp3r]
        p_widgets = [self.e_tp1p, self.e_tp2p, self.e_tp3p]
        for w in r_widgets: w.configure(state=("normal" if mode == "R-Multiple" else "disabled"))
        for w in p_widgets: w.configure(state=("normal" if mode == "Prozent" else "disabled"))

    def copy_to_clipboard(self, text: str):
        """Copy text to clipboard"""
        if not text:
            return
        try:
            self.clipboard_clear()
            self.clipboard_append(text)
            self.update()
        except Exception:
            pass
    
    def copy_with_feedback(self, text: str, button=None):
        """Copy text to clipboard with visual feedback"""
        if not text:
            return
        
        # Copy to clipboard
        self.copy_to_clipboard(text)
        
        # Find the button that was clicked
        if button is None:
            # Find button by searching through all copy buttons
            import tkinter as tk
            def find_button(widget):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Button) and child.cget('text') == '📋':
                        return child
                    result = find_button(child)
                    if result:
                        return result
                return None
            button = find_button(self)
        
        if button:
            # Store original text and change to checkmark
            original_text = button.cget('text')
            button.configure(text='🟢✅')
            
            # Reset after 1 second
            self.after(1000, lambda: button.configure(text=original_text))

    def reset_inputs(self):
        """Reset all input fields to default values"""
        try:
            # Reset basic inputs
            self.e_price.delete(0, tk.END)
            self.e_max_loss.delete(0, tk.END)
            self.e_max_loss.insert(0, "10.00")
            self.e_sl_percent.delete(0, tk.END)
            self.e_sl_percent.insert(0, "0")
            
            # Reset direction to Long
            self.direction_var.set("Long")
            self.update_direction_colors()
            
            # Reset leverage to 1
            self.leverage_var.set(1)
            self.leverage_label.config(text="1X")
            self.leverage_scale.set(1)
            
            # Clear results
            if hasattr(self, 'lbl_nominal'):
                self.lbl_nominal.config(text="0.00")
            if hasattr(self, 'lbl_margin'):
                self.lbl_margin.config(text="0.00")
            if hasattr(self, 'lbl_slp'):
                self.lbl_slp.config(text="0.00")
            if hasattr(self, 'lbl_tp1'):
                self.lbl_tp1.config(text="0.00")
            if hasattr(self, 'lbl_tp2'):
                self.lbl_tp2.config(text="0.00")
            if hasattr(self, 'lbl_tp3'):
                self.lbl_tp3.config(text="0.00")
                
            # Clear extra info
            if hasattr(self, 'extra'):
                self.extra.config(text="")
                
        except Exception as e:
            print(f"Reset error: {e}")

    def copy_value(self, key: str):
        val = self._last_values.get(key, "")
        if not val:
            return
        try:
            self.clipboard_clear()
            self.clipboard_append(val)
            self.update()
        except Exception:
            pass

    def calculate(self):
        try:
            direction   = self.direction_var.get().lower()
            number_format = "german" if "Deutsch" in self.cb_format.get() else "us"
            entry_price = parse_num(self.e_price.get(), number_format)
            max_loss    = parse_num(self.e_max_loss.get(), number_format)
            sl_percent  = parse_num(self.e_sl_percent.get(), number_format)
            leverage    = self._current_leverage()
            if entry_price <= 0: raise ValueError("Entry price must be > 0.")
            if sl_percent <= 0:  raise ValueError("Stop-Loss % must be > 0.")

            entry_fee = self.fee_for(self.cb_entry_side.get())
            exit_fee  = self.fee_for(self.cb_exit_side.get())
            total_fee_pct = entry_fee + exit_fee

            # Calculate nominal value that respects max_loss with leverage
            # The actual loss should equal max_loss regardless of leverage
            
            effective_pct = (sl_percent + total_fee_pct) / 100.0
            
            # Calculate nominal so that: (nominal * sl_percent/100) = max_loss
            # This gives us the position size that loses exactly max_loss at SL
            nominal = max_loss / (sl_percent / 100.0)
            
            # With leverage, margin is reduced but nominal stays the same
            margin_required = nominal / leverage
            units = nominal / entry_price

            # SL
            sl_price = entry_price * (1.0 - sl_percent/100.0) if direction=="long" else entry_price * (1.0 + sl_percent/100.0)
            sl_distance = abs(entry_price - sl_price)

            # TPs
            mode = self.cb_tp_mode.get()
            if mode == "R-Multiple":
                tp1r = parse_num(self.e_tp1r.get(), number_format); tp2r = parse_num(self.e_tp2r.get(), number_format); tp3r = parse_num(self.e_tp3r.get(), number_format)
                tps = [(entry_price + m*sl_distance) if direction=="long" else (entry_price - m*sl_distance) for m in [tp1r, tp2r, tp3r]]
            else:
                tp1p = parse_num(self.e_tp1p.get(), number_format); tp2p = parse_num(self.e_tp2p.get(), number_format); tp3p = parse_num(self.e_tp3p.get(), number_format)
                sgn = 1 if direction=="long" else -1
                tps = [entry_price*(1.0 + sgn*tp1p/100.0),
                       entry_price*(1.0 + sgn*tp2p/100.0),
                       entry_price*(1.0 + sgn*tp3p/100.0)]
            tp1, tp2, tp3 = tps

            # Fees €
            entry_fee_amt = nominal * (entry_fee/100.0)
            exit_fee_amt  = nominal * (exit_fee/100.0)
            total_fees_amt = entry_fee_amt + exit_fee_amt

            # PnL
            def pnl_at(price: float):
                gross = (price - entry_price)*units if direction=="long" else (entry_price - price)*units
                return gross, gross - total_fees_amt

            sl_gross, sl_net = pnl_at(sl_price)
            tp1_gross, tp1_net = pnl_at(tp1)
            tp2_gross, tp2_net = pnl_at(tp2)
            tp3_gross, tp3_net = pnl_at(tp3)

            # Big outputs
            self._set_result(self.lbl_nominal, get_text("nominal", self.current_language), fmt_money(nominal, number_format), "nominal")
            self._set_result(self.lbl_margin,  get_text("margin", self.current_language), fmt_money(margin_required, number_format), "margin")
            self._set_result(self.lbl_slp,     get_text("sl_price", self.current_language), fmt_num(sl_price, 6, number_format), "sl_price")
            self._set_result(self.lbl_tp1,     get_text("tp1", self.current_language), fmt_num(tp1, 6, number_format), "tp1")
            self._set_result(self.lbl_tp2,     get_text("tp2", self.current_language), fmt_num(tp2, 6, number_format), "tp2")
            self._set_result(self.lbl_tp3,     get_text("tp3", self.current_language), fmt_num(tp3, 6, number_format), "tp3")

            lines = [
                f"{get_text('fees_info', self.current_language).format(entry_fee=fmt_num(entry_fee,3,number_format), exit_fee=fmt_num(exit_fee,3,number_format), total_fee=fmt_num(total_fee_pct,3,number_format))} "
                f"(≈ {fmt_money(entry_fee_amt,number_format)} + {fmt_money(exit_fee_amt,number_format)} = {fmt_money(total_fees_amt,number_format)})",
                f"{get_text('effective_risk', self.current_language).format(risk=fmt_num(sl_percent + total_fee_pct,3,number_format), leverage=int(leverage))}",
                "",
                f"{get_text('sl_pnl', self.current_language).format(gross=fmt_money(sl_gross,number_format), net=fmt_money(sl_net,number_format))}",
                f"{get_text('tp1_pnl', self.current_language).format(gross=fmt_money(tp1_gross,number_format), net=fmt_money(tp1_net,number_format))}",
                f"{get_text('tp2_pnl', self.current_language).format(gross=fmt_money(tp2_gross,number_format), net=fmt_money(tp2_net,number_format))}",
                f"{get_text('tp3_pnl', self.current_language).format(gross=fmt_money(tp3_gross,number_format), net=fmt_money(tp3_net,number_format))}",
            ]
            self.extra.config(text="\n".join(lines))

        except Exception as e:
            messagebox.showerror(get_text("error", self.current_language), f"{get_text('invalid_input', self.current_language)}\n{e}")

    # ---------- Actions ----------
    def on_save_settings(self):
        try:
            number_format = "german" if "Deutsch" in self.cb_format.get() else "us"
            maker = parse_num(self.e_maker.get(), number_format)
            taker = parse_num(self.e_taker.get(), number_format)
            self.settings["maker_fee"] = maker
            self.settings["taker_fee"] = taker
            self.settings["number_format"] = number_format
            self.settings["language"] = self.current_language
            self.settings["leverage"] = self.leverage_var.get()  # Save current leverage
            save_settings(self.settings)
            messagebox.showinfo(get_text("saved", self.current_language), get_text("saved", self.current_language))
        except Exception as e:
            messagebox.showerror(get_text("error", self.current_language), f"{get_text('invalid_input', self.current_language)}\n{e}")
    
    def _on_format_change(self, event=None):
        """Handle number format change and recalculate if needed."""
        try:
            number_format = "german" if "Deutsch" in self.cb_format.get() else "us"
            self.settings["number_format"] = number_format
            # Trigger recalculation if we have values
            if hasattr(self, 'e_price') and self.e_price.get().strip():
                self.calculate()
        except Exception:
            pass
    
    def _on_language_change(self, event=None):
        """Handle language change and rebuild UI."""
        try:
            new_language = "german" if "Deutsch" in self.cb_language.get() else "english"
            if new_language != self.current_language:
                self.current_language = new_language
                self.settings["language"] = new_language
                # Show message that restart is needed
                messagebox.showinfo(get_text("saved", self.current_language), 
                                  "Please restart the application to apply language changes." if new_language == "english" else "Bitte starten Sie die Anwendung neu, um die Sprachänderungen zu übernehmen.")
        except Exception:
            pass

    def _set_result(self, label_widget: ttk.Label, prefix: str, formatted: str, key: str):
        label_widget.config(text=formatted)
        self._last_values[key] = formatted

if __name__ == "__main__":
    NominalwertRechner().mainloop()
