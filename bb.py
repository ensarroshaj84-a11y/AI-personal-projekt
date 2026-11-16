
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

from PIL import Image, ImageTk

from sport_classification import predict_sport

from gtts import gTTS
import os
import platform


# ============================================================
# SETTINGS
# ============================================================

APP_TITLE = "Sport Classification App"
UPLOAD_BUTTON_TEXT = "Choose Sport Image"
EMPTY_IMAGE_TEXT = "Upload a sport image"
RESULT_EMPTY_TEXT = "Sport result will appear here"

PREVIEW_SIZE = (320, 240)

# PREMIUM SPORTS DASHBOARD COLORS

BG_COLOR = "#101114"
PANEL_COLOR = "#191B20"
CARD_COLOR = "#22252B"
NEON_COLOR = "#C5F82A"
ORANGE_COLOR = "#FF7139"
WHITE_COLOR = "#F5F5F5"
GRAY_COLOR = "#858994"
GREEN_COLOR = "#A8E63D"


# ============================================================
# SPORT APPLICATION
# ============================================================

class SportApp:

    def __init__(self, root):

        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("1000x720")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)

        self.preview_image = None
        self.current_sport = None

        # ====================================================
        # MAIN LAYOUT
        # ====================================================

        self.sidebar = tk.Frame(
            root,
            bg=NEON_COLOR,
            width=210,
            height=720
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.main_frame = tk.Frame(
            root,
            bg=BG_COLOR,
            width=790,
            height=720
        )
        self.main_frame.pack(side="right", fill="both", expand=True)
        self.main_frame.pack_propagate(False)

        # ====================================================
        # SIDEBAR
        # ====================================================

        tk.Label(
            self.sidebar,
            text="S",
            font=("Segoe UI", 42, "bold"),
            bg=NEON_COLOR,
            fg=BG_COLOR
        ).pack(pady=(35, 0))

        tk.Label(
            self.sidebar,
            text="SPORT AI",
            font=("Segoe UI", 17, "bold"),
            bg=NEON_COLOR,
            fg=BG_COLOR
        ).pack(pady=(0, 5))

        tk.Label(
            self.sidebar,
            text="CLASSIFICATION",
            font=("Segoe UI", 8, "bold"),
            bg=NEON_COLOR,
            fg="#454C24"
        ).pack()

        tk.Frame(
            self.sidebar,
            bg="#899F27",
            height=2
        ).pack(fill="x", padx=25, pady=30)

        tk.Label(
            self.sidebar,
            text="01  /  UPLOAD",
            font=("Segoe UI", 10, "bold"),
            bg=NEON_COLOR,
            fg=BG_COLOR
        ).pack(anchor="w", padx=22, pady=12)

        tk.Label(
            self.sidebar,
            text="02  /  ANALYZE",
            font=("Segoe UI", 10, "bold"),
            bg=NEON_COLOR,
            fg=BG_COLOR
        ).pack(anchor="w", padx=22, pady=12)

        tk.Label(
            self.sidebar,
            text="03  /  LISTEN",
            font=("Segoe UI", 10, "bold"),
            bg=NEON_COLOR,
            fg=BG_COLOR
        ).pack(anchor="w", padx=22, pady=12)

        tk.Frame(
            self.sidebar,
            bg="#899F27",
            height=2
        ).pack(fill="x", padx=25, pady=30)

        tk.Label(
            self.sidebar,
            text="POWERED BY",
            font=("Segoe UI", 8, "bold"),
            bg=NEON_COLOR,
            fg="#454C24"
        ).pack(pady=(10, 3))

        tk.Label(
            self.sidebar,
            text="MACHINE\nLEARNING",
            font=("Segoe UI", 12, "bold"),
            bg=NEON_COLOR,
            fg=BG_COLOR,
            justify="left"
        ).pack()

        tk.Label(
            self.sidebar,
            text="SPORT AI SYSTEM\nVERSION 1.0",
            font=("Segoe UI", 8),
            bg=NEON_COLOR,
            fg="#454C24",
            justify="left"
        ).pack(side="bottom", anchor="w", padx=20, pady=25)

        # ====================================================
        # MAIN HEADER
        # ====================================================

        self.header = tk.Frame(
            self.main_frame,
            bg=BG_COLOR
        )
        self.header.pack(fill="x", padx=35, pady=(25, 5))

        tk.Label(
            self.header,
            text="SPORT RECOGNITION",
            font=("Segoe UI", 24, "bold"),
            bg=BG_COLOR,
            fg=WHITE_COLOR
        ).pack(anchor="w")

        tk.Label(
            self.header,
            text="INTELLIGENT IMAGE ANALYSIS SYSTEM",
            font=("Segoe UI", 9, "bold"),
            bg=BG_COLOR,
            fg=NEON_COLOR
        ).pack(anchor="w", pady=(5, 0))

        # ====================================================
        # CONTENT AREA
        # ====================================================

        self.content = tk.Frame(
            self.main_frame,
            bg=BG_COLOR
        )
        self.content.pack(fill="both", expand=True, padx=35, pady=15)

        # ====================================================
        # IMAGE SECTION
        # ====================================================

        self.image_section = tk.Frame(
            self.content,
            bg=PANEL_COLOR,
            padx=15,
            pady=15,
            highlightbackground="#343840",
            highlightthickness=1
        )
        self.image_section.pack(fill="x", pady=(0, 15))

        tk.Label(
            self.image_section,
            text="IMAGE PREVIEW",
            font=("Segoe UI", 10, "bold"),
            bg=PANEL_COLOR,
            fg=NEON_COLOR
        ).pack(anchor="w", pady=(0, 10))

        self.image_label = tk.Label(
            self.image_section,
            text=EMPTY_IMAGE_TEXT,
            width=42,
            height=10,
            bg="#292D34",
            fg=GRAY_COLOR,
            font=("Segoe UI", 12, "bold"),
            relief="flat"
        )
        self.image_label.pack()

        # ====================================================
        # UPLOAD BUTTON
        # ====================================================

        self.choose_button = tk.Button(
            self.content,
            text="＋  CHOOSE SPORT IMAGE",
            command=self.choose_image,
            font=("Segoe UI", 11, "bold"),
            bg=NEON_COLOR,
            fg=BG_COLOR,
            activebackground="#A6D21F",
            activeforeground=BG_COLOR,
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=12,
            borderwidth=0
        )
        self.choose_button.pack(fill="x", pady=(0, 15))

        # ====================================================
        # RESULT SECTION
        # ====================================================

        self.result_frame = tk.Frame(
            self.content,
            bg=CARD_COLOR,
            padx=20,
            pady=15,
            highlightbackground="#383C44",
            highlightthickness=1
        )
        self.result_frame.pack(fill="x", pady=(0, 12))

        tk.Label(
            self.result_frame,
            text="AI ANALYSIS RESULT",
            font=("Segoe UI", 9, "bold"),
            bg=CARD_COLOR,
            fg=GRAY_COLOR
        ).pack(anchor="w")

        self.result_label = tk.Label(
            self.result_frame,
            text=RESULT_EMPTY_TEXT,
            font=("Segoe UI", 20, "bold"),
            bg=CARD_COLOR,
            fg=NEON_COLOR
        )
        self.result_label.pack(anchor="w", pady=(8, 3))

        self.confidence_label = tk.Label(
            self.result_frame,
            text="CONFIDENCE: --",
            font=("Segoe UI", 11, "bold"),
            bg=CARD_COLOR,
            fg=ORANGE_COLOR
        )
        self.confidence_label.pack(anchor="w", pady=5)

        # ====================================================
        # IMAGE PATH
        # ====================================================

        self.path_label = tk.Label(
            self.content,
            text="",
            font=("Segoe UI", 8),
            wraplength=680,
            bg=BG_COLOR,
            fg=GRAY_COLOR
        )
        self.path_label.pack(anchor="w", pady=5)

        # ====================================================
        # TEXT TO SPEECH
        # ====================================================

        self.tts_frame = tk.Frame(
            self.content,
            bg=PANEL_COLOR,
            padx=18,
            pady=12,
            highlightbackground="#383C44",
            highlightthickness=1
        )
        self.tts_frame.pack(fill="x", pady=8)

        self.tts_title = tk.Label(
            self.tts_frame,
            text="AUDIO EXPERIENCE  /  TEXT TO SPEECH",
            font=("Segoe UI", 10, "bold"),
            bg=PANEL_COLOR,
            fg=WHITE_COLOR
        )
        self.tts_title.pack(anchor="w", pady=(0, 8))

        self.listen_button = tk.Button(
            self.tts_frame,
            text="▶   LISTEN TO SPORT RESULT",
            command=self.text_to_speech,
            font=("Segoe UI", 11, "bold"),
            bg=ORANGE_COLOR,
            fg=WHITE_COLOR,
            activebackground="#E65B28",
            activeforeground=WHITE_COLOR,
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=11,
            borderwidth=0,
            state="disabled"
        )
        self.listen_button.pack(fill="x")

        # ====================================================
        # FOOTER
        # ====================================================

        tk.Label(
            self.main_frame,
            text="SPORT AI  ©  IMAGE CLASSIFICATION TECHNOLOGY",
            font=("Segoe UI", 8, "bold"),
            bg=BG_COLOR,
            fg="#646871"
        ).pack(side="bottom", pady=12)


    # ========================================================
    # CHOOSE IMAGE
    # ========================================================

    def choose_image(self):

        image_path = filedialog.askopenfilename(
            title="Choose Sport Image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.webp"),
                ("All files", "*.*"),
            ],
        )

        if not image_path:
            return

        try:
            self.show_preview(image_path)
            self.classify(image_path)

        except Exception as error:
            messagebox.showerror(
                "Image Error",
                str(error)
            )


    # ========================================================
    # SHOW IMAGE PREVIEW
    # ========================================================

    def show_preview(self, image_path):

        image = Image.open(image_path).convert("RGB")

        image.thumbnail(PREVIEW_SIZE)

        self.preview_image = ImageTk.PhotoImage(image)

        self.image_label.configure(
            image=self.preview_image,
            text=""
        )

        self.path_label.configure(
            text=str(Path(image_path))
        )


    # ========================================================
    # SPORT CLASSIFICATION
    # ========================================================

    def classify(self, image_path):

        try:

            result = predict_sport(image_path)

        except Exception as error:

            messagebox.showerror(
                "Classification Error",
                str(error)
            )

            return

        self.current_sport = result["sport_class"]

        self.result_label.configure(
            text=f"SPORT: {result['sport_class']}"
        )

        self.confidence_label.configure(
            text=f"CONFIDENCE: {result['confidence']:.2%}"
        )

        self.listen_button.configure(
            state="normal"
        )


    # ========================================================
    # TEXT TO SPEECH
    # ========================================================

    def text_to_speech(self):

        if not self.current_sport:
            return

        user_text = self.current_sport

        language = "en"
        filename = "sport_result.mp3"

        try:

            tts = gTTS(
                text=user_text,
                lang=language
            )

            tts.save(filename)

            if platform.system() == "Windows":

                os.startfile(filename)

            elif platform.system() == "Darwin":

                os.system(f'open "{filename}"')

            else:

                os.system(f'xdg-open "{filename}"')

        except Exception as error:

            messagebox.showerror(
                "Text to Speech Error",
                str(error)
            )


# ============================================================
# MAIN
# ============================================================

def main():

    root = tk.Tk()

    app = SportApp(root)

    root.mainloop()


if __name__ == "__main__":
    main()
