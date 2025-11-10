import os
import threading
import tkinter as tk
from tkinter import filedialog, ttk
from tkinter import font as tkfont
from mutagen import File

class AudioBitrateApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Bitrate Calculator")

        # Basic window sizing and centering
        try:
            self.root.update_idletasks()
            width, height = 560, 420
            x = (self.root.winfo_screenwidth() - width) // 2
            y = (self.root.winfo_screenheight() - height) // 1.5
            self.root.geometry(f"{width}x{height}+{x}+{y}")
            self.root.minsize(520, 380)
            # Modest DPI scaling for readability
            try:
                self.root.tk.call('tk', 'scaling', 1.15)
            except Exception:
                pass
        except Exception:
            pass

        # Prepare styles/theme
        self._setup_style()

        self.folder_path = ""
        self.file_types = ["mp3", "flac", "wav", "aac", "ogg", "m4a"]
        self.is_processing = False
        self.stop_flag = False
        self.total_duration = 0  # in seconds

        self.create_widgets()

    def create_widgets(self):
        # Top-level content frame (adds padding and consistent background)
        self.content = ttk.Frame(self.root, style="Card.TFrame", padding=(16, 16, 16, 12))
        self.content.pack(fill=tk.BOTH, expand=True)

        # Header
        header = ttk.Label(self.content, text="Audio Bitrate Calculator", style="Header.TLabel")
        header.pack(anchor="w", pady=(0, 8))

        # Folder selection
        self.folder_frame = ttk.Frame(self.content)
        self.folder_frame.pack(pady=10)

        self.select_button = ttk.Button(self.folder_frame, text="Select Folder", command=self.select_folder)
        self.select_button.pack(side=tk.LEFT, padx=5)

        self.folder_label = ttk.Label(self.folder_frame, text="No folder selected", width=40)
        self.folder_label.pack(side=tk.LEFT, padx=10)

        # File type selection
        self.type_var = tk.StringVar()
        self.type_dropdown = ttk.Combobox(self.content, textvariable=self.type_var, values=["All"] + self.file_types, state="readonly", width=18)
        self.type_dropdown.current(0)
        self.type_dropdown.pack(pady=5)

        # Start and Cancel buttons
        self.button_frame = ttk.Frame(self.content)
        self.button_frame.pack(pady=5)

        self.start_button = ttk.Button(self.button_frame, text="Start", style="Accent.TButton", command=self.start_processing)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.cancel_button = ttk.Button(self.button_frame, text="Cancel", style="Danger.TButton", command=self.cancel_processing)
        self.cancel_button.pack(side=tk.LEFT, padx=5)
        self.cancel_button.pack_forget()

        # Progress bar
        self.progress = ttk.Progressbar(self.content, orient="horizontal", length=360, mode="determinate", style="Accent.Horizontal.TProgressbar")
        self.progress.pack(pady=8, fill=tk.X)

        # Results
        self.result_label = ttk.Label(self.content, text="Total Files: 0 | Total Size: 0 MB | Avg Bitrate: 0 kbps", anchor="center", style="Info.TLabel")
        self.result_label.pack(pady=10, fill=tk.X)

        # Bitrate recalculation panel
        self.recalc_frame = ttk.Frame(self.content, style="CardInner.TFrame", padding=(10, 8))
        self.recalc_label = ttk.Label(self.recalc_frame, text="New Bitrate (kbps):")
        self.recalc_entry = ttk.Entry(self.recalc_frame, width=10)
        self.recalc_result = ttk.Label(self.recalc_frame, text="Estimated New Size: 0 MB", style="Info.TLabel")

        self.recalc_entry.bind("<KeyRelease>", self.update_estimate)
        
        # Credits footer
        self.footer = ttk.Label(
            self.root,
            text="Concept and design by amol.more@hotmail.com • Built with help from Microsoft Copilot",
            style="Footer.TLabel"
        )
        self.footer.pack(side=tk.BOTTOM, pady=6)

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path = folder
            self.folder_label.config(text=os.path.basename(folder))

    def start_processing(self):
        if not self.folder_path:
            self.result_label.config(text="Please select a folder.")
            return

        # Reset UI
        self.result_label.config(text="Total Files: 0 | Total Size: 0 MB | Avg Bitrate: 0 kbps")
        self.progress["value"] = 0
        self.cancel_button.pack(side=tk.LEFT, padx=5)
        self.recalc_frame.pack_forget()
        self.is_processing = True
        self.stop_flag = False
        self.total_duration = 0

        threading.Thread(target=self.process_files).start()

    def cancel_processing(self):
        self.stop_flag = True

    def process_files(self):
        selected_type = self.type_var.get()
        extensions = self.file_types if selected_type == "All" else [selected_type]

        total_files = 0
        total_size = 0
        total_bitrate = 0
        audio_files = []

        for root_dir, _, files in os.walk(self.folder_path):
            for file in files:
                if self.stop_flag:
                    self.reset_ui()
                    return
                if any(file.lower().endswith(ext) for ext in extensions):
                    audio_files.append(os.path.join(root_dir, file))

        self.progress["maximum"] = len(audio_files)

        for idx, filepath in enumerate(audio_files):
            if self.stop_flag:
                self.reset_ui()
                return
            try:
                audio = File(filepath)
                if audio and audio.info:
                    bitrate = getattr(audio.info, 'bitrate', 0)
                    duration = getattr(audio.info, 'length', 0)
                    size = os.path.getsize(filepath)
                    total_files += 1
                    total_size += size
                    total_bitrate += bitrate
                    self.total_duration += duration
            except Exception:
                pass

            self.progress["value"] = idx + 1
            self.result_label.config(text=f"Total Files: {total_files} | Total Size: {round(total_size / (1024 * 1024), 2)} MB | Avg Bitrate: {round(total_bitrate / total_files / 1000, 2) if total_files else 0} kbps")
            self.root.update_idletasks()

        self.reset_ui()
        self.show_recalc_panel()

    def reset_ui(self):
        self.is_processing = False
        self.cancel_button.pack_forget()
        self.progress["value"] = 0

    def show_recalc_panel(self):
        self.recalc_frame.pack(pady=10, fill=tk.X)
        self.recalc_label.pack(side=tk.LEFT)
        self.recalc_entry.pack(side=tk.LEFT, padx=5)
        self.recalc_result.pack(side=tk.LEFT, padx=10)

    def _setup_style(self):
        """Configure a modern ttk look and feel without changing functionality."""
        try:
            style = ttk.Style()
            # Use a theme that respects custom colors
            try:
                style.theme_use('clam')
            except Exception:
                pass

            # Palette
            BG = "#32343C"
            CARD = "#252A32"
            TEXT = "#e9e9a0"
            MUTED = "#252930"
            ACCENT = '#fdbb2d'
            DANGER = '#d64545'

            # Window background
            self.root.configure(bg=BG)
            # Default font (use tk font object to handle families with spaces)
            try:
                default_font = tkfont.nametofont('TkDefaultFont')
                default_font.configure(family='Segoe UI', size=10)
            except Exception:
                # Fallback via option database with braces to protect space in family name
                try:
                    self.root.option_add('*Font', '{Segoe UI} 10')
                except Exception:
                    pass

            # Frames
            style.configure('TFrame', background=BG)
            style.configure('Card.TFrame', background=CARD)
            style.configure('CardInner.TFrame', background=CARD)

            # Labels
            style.configure('TLabel', background=CARD, foreground=TEXT)
            style.configure('Header.TLabel', background=CARD, foreground=ACCENT, font=('Segoe UI', 14, 'bold'))
            style.configure('Info.TLabel', background=CARD, foreground=TEXT)
            style.configure('Footer.TLabel', background=BG, foreground=MUTED, font=('Segoe UI', 9))

            # Buttons
            style.configure('TButton', padding=(10, 6))
            style.map('TButton', foreground=[('disabled', MUTED)])

            style.configure('Accent.TButton', background=ACCENT, foreground='#222', padding=(12, 6))
            style.map('Accent.TButton', background=[('active', '#ffcc44')])

            style.configure('Danger.TButton', background=DANGER, foreground='white', padding=(12, 6))
            style.map('Danger.TButton', background=[('active', '#b73a3a')])

            # Progressbar
            style.configure('Horizontal.TProgressbar', troughcolor='#2b2f3a', background='#5c93ff')
            style.configure('Accent.Horizontal.TProgressbar', troughcolor='#2b2f3a', background=ACCENT)

            # Combobox
            style.configure('TCombobox', fieldbackground=CARD, background=CARD, foreground=TEXT)
        except Exception:
            # If styling fails anywhere, keep defaults
            pass

    def update_estimate(self, event=None):
        try:
            new_bitrate = int(self.recalc_entry.get())
            new_size_mb = (self.total_duration * new_bitrate) / (8 * 1024)
            self.recalc_result.config(text=f"Estimated New Size: {round(new_size_mb, 2)} MB")
        except ValueError:
            self.recalc_result.config(text="Estimated New Size: —")

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioBitrateApp(root)
    root.mainloop()
