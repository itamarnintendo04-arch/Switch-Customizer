import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from PIL import Image, ImageTk

APP = "Switch Customizer by ItamarOS"
GAMES = ["The Legend of Zelda", "Super Mario Odyssey", "Mario Kart 8 Deluxe", "Animal Crossing", "Kirby", "Splatoon"]
BG, PANEL, FG = "#10131b", "#1b2030", "#f4f7ff"

class App:
    def __init__(self, root):
        self.root = root
        root.title(APP + " - v0.1 Alpha")
        root.geometry("1150x720")
        root.configure(bg=BG)
        self.data = {"console": "Both (V1 / V2)", "background": "", "games": {g: {"image": "", "music": ""} for g in GAMES}}
        self.game = tk.StringVar(value=GAMES[0])
        self.console = tk.StringVar(value=self.data["console"])
        self.images = []
        self.ui()
        root.after(100, self.preview)

    def button(self, parent, title, command):
        return tk.Button(parent, text=title, command=command, bg="#293850", fg=FG, relief="flat", padx=12, pady=9)

    def ui(self):
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", padx=18, pady=15)
        tk.Label(header, text="SWITCH CUSTOMIZER  /  ItamarOS", bg=BG, fg="#42c8ff", font=("Segoe UI", 19, "bold")).pack(side="left")
        self.button(header, "Save Project", self.save).pack(side="right", padx=4)
        self.button(header, "Open Project", self.load).pack(side="right", padx=4)
        main = tk.Frame(self.root, bg=BG)
        main.pack(fill="both", expand=True, padx=18, pady=8)
        left = tk.Frame(main, bg=PANEL, width=310)
        left.pack(side="left", fill="y", padx=(0, 15))
        left.pack_propagate(False)
        def heading(text):
            tk.Label(left, text=text, bg=PANEL, fg=FG, anchor="w", font=("Segoe UI", 11, "bold")).pack(fill="x", padx=15, pady=(18, 6))
        heading("Console")
        combo = ttk.Combobox(left, textvariable=self.console, state="readonly", values=["Both (V1 / V2)", "Switch V1", "Switch V2"])
        combo.pack(fill="x", padx=15)
        heading("Home Background")
        self.button(left, "Choose 16:9 Background", lambda: self.pick("background")).pack(fill="x", padx=15)
        heading("Selected Game")
        combo = ttk.Combobox(left, textvariable=self.game, state="readonly", values=GAMES)
        combo.pack(fill="x", padx=15)
        combo.bind("<<ComboboxSelected>>", lambda e: self.preview())
        heading("Per-Game Assets")
        self.button(left, "Choose Artwork", lambda: self.pick("image")).pack(fill="x", padx=15)
        self.button(left, "Choose Music", lambda: self.pick("music")).pack(fill="x", padx=15, pady=6)
        self.music_info = tk.Label(left, bg=PANEL, fg="#b5bfd0", wraplength=270)
        self.music_info.pack(padx=15, pady=8)
        heading("Export")
        self.button(left, "Export JSON Manifest", self.save).pack(fill="x", padx=15)
        tk.Label(left, text="Preview editor only. Does not modify a real Switch or execute Windows EXE files.", bg=PANEL, fg="#b5bfd0", wraplength=275).pack(side="bottom", pady=20)
        right = tk.Frame(main, bg=BG)
        right.pack(side="left", fill="both", expand=True)
        tk.Label(right, text="LIVE PREVIEW", bg=BG, fg=FG, font=("Segoe UI", 14, "bold")).pack(anchor="w")
        self.canvas = tk.Canvas(right, bg="#151c2b", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, pady=10)
        self.canvas.bind("<Configure>", lambda e: self.preview())

    def photo(self, path, width, height):
        try:
            if not path or not Path(path).is_file():
                return None
            image = Image.open(path).convert("RGB")
            image.thumbnail((max(1, width), max(1, height)), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            self.images.append(photo)
            return photo
        except Exception:
            return None

    def preview(self):
        c = self.canvas
        c.delete("all")
        self.images = []
        width, height = c.winfo_width(), c.winfo_height()
        if width < 100 or height < 100:
            return
        scale = min((width - 20) / 960, (height - 20) / 540)
        w, h = int(960 * scale), int(540 * scale)
        x, y = (width - w) // 2, (height - h) // 2
        c.create_rectangle(x, y, x + w, y + h, fill="#26374e", outline="#65758e", width=2)
        photo = self.photo(self.data["background"], w, h)
        if photo:
            c.create_image(x + w // 2, y + h // 2, image=photo)
        c.create_rectangle(x, y, x + w, y + 65 * scale, fill="#101b2c", outline="")
        c.create_text(x + 24 * scale, y + 33 * scale, text="Switch Home", fill="white", anchor="w", font=("Segoe UI", max(10, int(19 * scale)), "bold"))
        size, gap = int(132 * scale), int(16 * scale)
        start = x + (w - (len(GAMES) * size + (len(GAMES) - 1) * gap)) // 2
        for i, name in enumerate(GAMES):
            xx, yy = start + i * (size + gap), y + int(175 * scale)
            selected = name == self.game.get()
            c.create_rectangle(xx - 3, yy - 3, xx + size + 3, yy + size + 3, fill="#43d0ff" if selected else "#536277", outline="white" if selected else "#536277")
            image = self.photo(self.data["games"][name]["image"], size, size)
            if image:
                c.create_image(xx + size // 2, yy + size // 2, image=image)
            else:
                c.create_rectangle(xx, yy, xx + size, yy + size, fill=["#33649c", "#b95044", "#d89430", "#57946c", "#9959a5", "#6263bd"][i], outline="")
                c.create_text(xx + size // 2, yy + size // 2, text=name, fill="white", width=size - 8, font=("Segoe UI", max(7, int(11 * scale)), "bold"))
            if selected:
                c.create_text(xx + size // 2, yy + size + 22 * scale, text=name, fill="white", font=("Segoe UI", max(7, int(10 * scale))))
        c.create_text(x + w // 2, y + h - 48 * scale, text="News     Album     Controllers     Settings     Power", fill="white", font=("Segoe UI", max(9, int(14 * scale))))
        music = self.data["games"][self.game.get()]["music"]
        self.music_info.config(text="Music: " + (Path(music).name if music else "None") + "\nAudio playback is planned for v0.2.")

    def pick(self, field):
        types = [("Audio", "*.mp3 *.wav *.ogg")] if field == "music" else [("Images", "*.png *.jpg *.jpeg *.webp")]
        path = filedialog.askopenfilename(filetypes=types)
        if path:
            if field == "background":
                self.data[field] = path
            else:
                self.data["games"][self.game.get()][field] = path
            self.preview()

    def save(self):
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
        if path:
            self.data["console"] = self.console.get()
            Path(path).write_text(json.dumps({"format": "switch-customizer-v0.1", "project": self.data}, indent=2), encoding="utf-8")

    def load(self):
        path = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if not path:
            return
        try:
            value = json.loads(Path(path).read_text(encoding="utf-8"))
            if value.get("format") != "switch-customizer-v0.1":
                raise ValueError("Unsupported project format")
            data = value["project"]
            if not isinstance(data["games"], dict) or not all(g in data["games"] for g in GAMES):
                raise ValueError("Missing game data")
            self.data = data
            self.console.set(data.get("console", "Both (V1 / V2)"))
            self.preview()
        except (OSError, ValueError, KeyError, TypeError) as exc:
            messagebox.showerror("Open Project", str(exc))

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
