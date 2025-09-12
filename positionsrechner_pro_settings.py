import os, json, tkinter as tk
from tkinter import ttk, messagebox

# ---------------- Storage ----------------
def appdata_dir():
    base = os.getenv("APPDATA") or os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base, "Positionsrechner")
    os.makedirs(path, exist_ok=True)
    return path

SETTINGS_PATH = os.path.join(appdata_dir(), "settings.json")
DEFAULT_SETTINGS = {"maker_fee": 0.03, "taker_fee": 0.07}  # %

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

# ---------------- Number formatting (115,209.6) ----------------
def parse_num(s: str) -> float:
    s = s.strip().replace(",", "")
    if s == "":
        raise ValueError("Empty number.")
    return float(s)

def fmt_num(x: float, digits: int = 4) -> str:
    return f"{x:,.{digits}f}"

def fmt_money(x: float) -> str:
    return f"{x:,.2f}"

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
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Positionsrechner Pro – dark (SL, TP, Copy, P&L)")
        self.settings = load_settings()
        self._last_values = {}

        # --------- Dark Theme ----------
        style = ttk.Style(self)
        # Fallback auf 'clam', dann dunkle Farben manuell
        try:
            style.theme_use("clam")
        except Exception:
            pass
        BG = "#121212"; FG = "#EAEAEA"; CARD = "#1E1E1E"; ACCENT = "#C9F24A"  # Binance-Grün-ish
        DISABLED = "#6b6b6b"

        self.configure(bg=BG)
        style.configure(".", background=BG, foreground=FG)
        style.configure("TLabel", background=BG, foreground=FG)
        style.configure("TFrame", background=BG)
        style.configure("Card.TFrame", background=CARD)
        style.configure("TEntry", fieldbackground="#2A2A2A", foreground=FG)
        style.map("TEntry", fieldbackground=[("disabled", "#2A2A2A")], foreground=[("disabled", DISABLED)])
        style.configure("TCombobox", fieldbackground="#2A2A2A", foreground=FG, background=BG)
        style.configure("TButton", background="#2A2A2A", foreground=FG, padding=6)
        style.configure("Accent.TButton", background=ACCENT, foreground="#111", padding=8)
        style.map("Accent.TButton", background=[("active", "#b9e440")])
        style.configure("TSeparator", background="#333")
        style.configure("TLabelframe.Label", foreground=FG)

        main = ttk.Frame(self, padding=12, style="TFrame")
        main.pack(fill="both", expand=True)

        r = 0
        ttk.Label(main, text="Richtung:").grid(row=r, column=0, sticky="w", pady=4)
        self.cb_dir = ttk.Combobox(main, values=["Long", "Short"], state="readonly", width=17)
        self.cb_dir.grid(row=r, column=1, pady=4); self.cb_dir.set("Long")

        r += 1
        ttk.Label(main, text="Einstiegskurs").grid(row=r, column=0, sticky="w", pady=4)
        self.e_price = ttk.Entry(main, width=20); self.e_price.grid(row=r, column=1, pady=4)

        r += 1
        ttk.Label(main, text="Maximaler Verlust (€)").grid(row=r, column=0, sticky="w", pady=4)
        self.e_loss = ttk.Entry(main, width=20); self.e_loss.grid(row=r, column=1, pady=4); self.e_loss.insert(0, "10.00")

        r += 1
        ttk.Label(main, text="Stop-Loss (%)").grid(row=r, column=0, sticky="w", pady=4)
        self.e_sl = ttk.Entry(main, width=20); self.e_sl.grid(row=r, column=1, pady=4); self.e_sl.insert(0, "0.51")

        # ---------- Hebel: Slider 1× … 125× ----------
        r += 1
        ttk.Label(main, text="Hebel").grid(row=r, column=0, sticky="w", pady=(10, 2))
        lever_frame = ttk.Frame(main, style="Card.TFrame")
        lever_frame.grid(row=r, column=1, sticky="ew", pady=(6, 8))
        lever_frame.columnconfigure(0, weight=1)

        # Diskrete Schritte wie im Screenshot
        self.leverage_steps = [1, 25, 50, 75, 100, 125]
        self.leverage_var = tk.IntVar(value=5)  # Index 5 -> 125x default
        scale = ttk.Scale(
            lever_frame, from_=0, to=len(self.leverage_steps)-1,
            orient="horizontal", command=self._on_leverage_slide, length=260
        )
        # ttk.Scale arbeitet float-basiert; wir syncen über IntVar separat
        scale.set(self.leverage_var.get())
        scale.grid(row=0, column=0, sticky="ew", padx=8, pady=6)
        self.leverage_label = ttk.Label(lever_frame, text="125×", font=("TkDefaultFont", 10, "bold"))
        self.leverage_label.grid(row=0, column=1, padx=(8, 0))

        ticks = ttk.Frame(lever_frame, style="Card.TFrame")
        ticks.grid(row=1, column=0, columnspan=2, sticky="ew", padx=8)
        for i, v in enumerate(self.leverage_steps):
            lbl = ttk.Label(ticks, text=f"{v}X", foreground=DISABLED)
            lbl.grid(row=0, column=i, padx=(0 if i == 0 else 24, 0))

        # ---------- Collapsible: Entry/Exit fees ----------
        r += 1
        sec_fees = Collapsible(main, "Entry/Exit-Gebühren (Maker/Taker Auswahl)", initially_open=False)
        sec_fees.grid(row=r, column=0, columnspan=2, sticky="ew", pady=(10, 4))
        b = sec_fees.body
        ttk.Label(b, text="Entry-Gebühr").grid(row=0, column=0, sticky="w", pady=2)
        self.cb_entry_side = ttk.Combobox(b, values=["Taker", "Maker"], state="readonly", width=17)
        self.cb_entry_side.grid(row=0, column=1, pady=2); self.cb_entry_side.set("Taker")
        ttk.Label(b, text="Exit-Gebühr").grid(row=1, column=0, sticky="w", pady=2)
        self.cb_exit_side = ttk.Combobox(b, values=["Taker", "Maker"], state="readonly", width=17)
        self.cb_exit_side.grid(row=1, column=1, pady=2); self.cb_exit_side.set("Taker")

        # ---------- Collapsible: Settings ----------
        r += 1
        sec_settings = Collapsible(main, "Einstellungen (werden gespeichert)", initially_open=False)
        sec_settings.grid(row=r, column=0, columnspan=2, sticky="ew", pady=(6, 4))
        s = sec_settings.body
        ttk.Label(s, text="Maker-Gebühr (%)").grid(row=0, column=0, sticky="w", pady=2)
        self.e_maker = ttk.Entry(s, width=20); self.e_maker.grid(row=0, column=1, pady=2)
        self.e_maker.insert(0, f"{self.settings.get('maker_fee', 0.03)}")
        ttk.Label(s, text="Taker-Gebühr (%)").grid(row=1, column=0, sticky="w", pady=2)
        self.e_taker = ttk.Entry(s, width=20); self.e_taker.grid(row=1, column=1, pady=2)
        self.e_taker.insert(0, f"{self.settings.get('taker_fee', 0.07)}")
        ttk.Button(s, text="Einstellungen speichern", command=self.on_save_settings, style="TButton")\
            .grid(row=2, column=0, columnspan=2, sticky="ew", pady=(6, 2))

        # ---------- Collapsible: TP ----------
        r += 1
        sec_tp = Collapsible(main, "Take-Profit Einstellungen", initially_open=False)
        sec_tp.grid(row=r, column=0, columnspan=2, sticky="ew", pady=(6, 4))
        t = sec_tp.body
        ttk.Label(t, text="TP-Modus").grid(row=0, column=0, sticky="w", pady=2)
        self.cb_tp_mode = ttk.Combobox(t, values=["R-Multiple", "Prozent"], state="readonly", width=17)
        self.cb_tp_mode.grid(row=0, column=1, pady=2); self.cb_tp_mode.set("R-Multiple")
        ttk.Label(t, text="TP1 (R)").grid(row=1, column=0, sticky="w", pady=2)
        self.e_tp1r = ttk.Entry(t, width=20); self.e_tp1r.grid(row=1, column=1, pady=2); self.e_tp1r.insert(0, "1")
        ttk.Label(t, text="TP2 (R)").grid(row=2, column=0, sticky="w", pady=2)
        self.e_tp2r = ttk.Entry(t, width=20); self.e_tp2r.grid(row=2, column=1, pady=2); self.e_tp2r.insert(0, "2")
        ttk.Label(t, text="TP3 (R)").grid(row=3, column=0, sticky="w", pady=2)
        self.e_tp3r = ttk.Entry(t, width=20); self.e_tp3r.grid(row=3, column=1, pady=2); self.e_tp3r.insert(0, "3")
        ttk.Label(t, text="TP1 (%)").grid(row=4, column=0, sticky="w", pady=2)
        self.e_tp1p = ttk.Entry(t, width=20); self.e_tp1p.grid(row=4, column=1, pady=2); self.e_tp1p.insert(0, "1.00")
        ttk.Label(t, text="TP2 (%)").grid(row=5, column=0, sticky="w", pady=2)
        self.e_tp2p = ttk.Entry(t, width=20); self.e_tp2p.grid(row=5, column=1, pady=2); self.e_tp2p.insert(0, "2.00")
        ttk.Label(t, text="TP3 (%)").grid(row=6, column=0, sticky="w", pady=2)
        self.e_tp3p = ttk.Entry(t, width=20); self.e_tp3p.grid(row=6, column=1, pady=2); self.e_tp3p.insert(0, "3.00")
        self.cb_tp_mode.bind("<<ComboboxSelected>>", lambda _e: self.update_tp_visibility())
        self.update_tp_visibility()

        # ---------- Call-to-action ----------
        r += 1
        ttk.Button(main, text="Bestätigen", command=self.calculate, style="Accent.TButton")\
            .grid(row=r, column=0, columnspan=2, sticky="ew", pady=(8, 10))

        # ---------- Ergebnisse (groß + Copy) ----------
        r += 1
        self.results = ttk.Frame(main, style="Card.TFrame", padding=8)
        self.results.grid(row=r, column=0, columnspan=2, sticky="ew")
        self.results.columnconfigure(0, weight=1)

        def big_line(row, label_text, key):
            f = ttk.Frame(self.results, style="Card.TFrame")
            f.grid(row=row, column=0, sticky="ew", pady=2)
            f.columnconfigure(0, weight=1)
            lbl = ttk.Label(f, text=f"{label_text}: –", font=("TkDefaultFont", 11, "bold"))
            lbl.grid(row=0, column=0, sticky="w")
            ttk.Button(f, text="Copy", width=6, command=lambda: self.copy_value(key), style="TButton")\
                .grid(row=0, column=1, padx=(8, 0))
            return lbl

        self.lbl_nominal = big_line(0, "Nominal (€)", "nominal")
        self.lbl_units   = big_line(1, "Stückzahl", "units")
        self.lbl_slp     = big_line(2, "SL-Preis", "sl_price")
        self.lbl_tp1     = big_line(3, "TP1", "tp1")
        self.lbl_tp2     = big_line(4, "TP2", "tp2")
        self.lbl_tp3     = big_line(5, "TP3", "tp3")
        self.lbl_margin  = big_line(6, "Margin (€)", "margin")

        # Info (Gebühren & PnL)
        r += 1
        self.extra = ttk.Label(main, text="", justify="left")
        self.extra.grid(row=r, column=0, columnspan=2, sticky="w", pady=(6, 0))

    # ---------- UI helpers ----------
    def _on_leverage_slide(self, _):
        # Runde immer auf die nächsten diskreten Indizes
        w = self.nametowidget(self.focus_get().winfo_parent()).children  # not used, but keep scale responsive
        # get current focus scale via variable is tricky; just read from all Scales if needed.
        # We snap to int and update label.
        # Tk passes value as str float via _ parameter; get current from widget via 'get' is unreliable here.
        # Workaround: use this widget directly isn't simple; compute from passed value
        try:
            idx = int(float(_)+0.5)
        except Exception:
            idx = self.leverage_var.get()
        idx = max(0, min(idx, len(self.leverage_steps)-1))
        self.leverage_var.set(idx)
        self.leverage_label.config(text=f"{self.leverage_steps[idx]}×")

    def update_tp_visibility(self):
        mode = self.cb_tp_mode.get()
        r_widgets = [self.e_tp1r, self.e_tp2r, self.e_tp3r]
        p_widgets = [self.e_tp1p, self.e_tp2p, self.e_tp3p]
        for w in r_widgets: w.configure(state=("normal" if mode == "R-Multiple" else "disabled"))
        for w in p_widgets: w.configure(state=("normal" if mode == "Prozent" else "disabled"))

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

    # ---------- Actions ----------
    def on_save_settings(self):
        try:
            maker = parse_num(self.e_maker.get())
            taker = parse_num(self.e_taker.get())
            self.settings["maker_fee"] = maker
            self.settings["taker_fee"] = taker
            save_settings(self.settings)
            messagebox.showinfo("Saved", "Einstellungen gespeichert.")
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input:\n{e}")

    def fee_for(self, side: str) -> float:
        return float(self.settings.get("maker_fee" if side.lower()=="maker" else "taker_fee",
                                       DEFAULT_SETTINGS["maker_fee" if side.lower()=="maker" else "taker_fee"]))

    def _current_leverage(self) -> float:
        return float(self.leverage_steps[self.leverage_var.get()])

    def calculate(self):
        try:
            direction   = self.cb_dir.get().lower()
            entry_price = parse_num(self.e_price.get())
            max_loss    = parse_num(self.e_loss.get())
            sl_percent  = parse_num(self.e_sl.get())
            leverage    = self._current_leverage()
            if entry_price <= 0: raise ValueError("Entry price must be > 0.")
            if sl_percent <= 0:  raise ValueError("Stop-Loss % must be > 0.")

            entry_fee = self.fee_for(self.cb_entry_side.get())
            exit_fee  = self.fee_for(self.cb_exit_side.get())
            total_fee_pct = entry_fee + exit_fee

            effective_pct = (sl_percent + total_fee_pct) / 100.0
            nominal = max_loss / effective_pct
            margin_required = nominal / leverage
            units = nominal / entry_price

            # SL
            sl_price = entry_price * (1.0 - sl_percent/100.0) if direction=="long" else entry_price * (1.0 + sl_percent/100.0)
            sl_distance = abs(entry_price - sl_price)

            # TPs
            mode = self.cb_tp_mode.get()
            if mode == "R-Multiple":
                tp1r = parse_num(self.e_tp1r.get()); tp2r = parse_num(self.e_tp2r.get()); tp3r = parse_num(self.e_tp3r.get())
                tps = [(entry_price + m*sl_distance) if direction=="long" else (entry_price - m*sl_distance) for m in [tp1r, tp2r, tp3r]]
            else:
                tp1p = parse_num(self.e_tp1p.get()); tp2p = parse_num(self.e_tp2p.get()); tp3p = parse_num(self.e_tp3p.get())
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
            self._set_result(self.lbl_nominal, "Nominal (€)", fmt_money(nominal), "nominal")
            self._set_result(self.lbl_units,   "Stückzahl",    fmt_num(units, 4), "units")
            self._set_result(self.lbl_slp,     "SL-Preis",     fmt_num(sl_price, 6), "sl_price")
            self._set_result(self.lbl_tp1,     "TP1",          fmt_num(tp1, 6), "tp1")
            self._set_result(self.lbl_tp2,     "TP2",          fmt_num(tp2, 6), "tp2")
            self._set_result(self.lbl_tp3,     "TP3",          fmt_num(tp3, 6), "tp3")
            self._set_result(self.lbl_margin,  "Margin (€)",   fmt_money(margin_required), "margin")

            lines = [
                f"Gebühren: Entry {fmt_num(entry_fee,3)}% + Exit {fmt_num(exit_fee,3)}% = {fmt_num(total_fee_pct,3)}% "
                f"(≈ {fmt_money(entry_fee_amt)} + {fmt_money(exit_fee_amt)} = {fmt_money(total_fees_amt)})",
                f"Effektives Risiko: {fmt_num(sl_percent + total_fee_pct,3)}%   •   Hebel: {int(leverage)}×",
                "",
                f"SL  → Brutto: {fmt_money(sl_gross)}   | Netto: {fmt_money(sl_net)}",
                f"TP1 → Brutto: {fmt_money(tp1_gross)}  | Netto: {fmt_money(tp1_net)}",
                f"TP2 → Brutto: {fmt_money(tp2_gross)}  | Netto: {fmt_money(tp2_net)}",
                f"TP3 → Brutto: {fmt_money(tp3_gross)}  | Netto: {fmt_money(tp3_net)}",
            ]
            self.extra.config(text="\n".join(lines))

        except Exception as e:
            messagebox.showerror("Error", f"Invalid input:\n{e}")

    def _set_result(self, label_widget: ttk.Label, prefix: str, formatted: str, key: str):
        label_widget.config(text=f"{prefix}: {formatted}")
        self._last_values[key] = formatted

if __name__ == "__main__":
    App().mainloop()
