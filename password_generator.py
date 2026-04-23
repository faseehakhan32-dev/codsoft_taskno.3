"""
╔══════════════════════════════════════════╗
║        🔐 PASSWORD GENERATOR 🔐          ║
║   Strong & Random Password Creator       ║
╚══════════════════════════════════════════╝
"""

import random
import string
import re
import customtkinter as ctk

# ─────────────────────────────────────────
#  Character Sets
# ─────────────────────────────────────────
LOWERCASE   = string.ascii_lowercase          # a-z
UPPERCASE   = string.ascii_uppercase          # A-Z
DIGITS      = string.digits                   # 0-9
SYMBOLS     = "!@#$%^&*()_+-=[]{}|;:,.<>?"   # special chars

# Color Palette
SPACE_CADET = "#25344F"
SLATE_GRAY = "#617B91"
TAN = "#D5B893"
COFFEE = "#6F4D38"
CAPUT_MORTUUM = "#632024"

def build_charset(use_upper: bool, use_digits: bool, use_symbols: bool) -> str:
    """Combine chosen character groups into one pool."""
    pool = LOWERCASE
    if use_upper:
        pool += UPPERCASE
    if use_digits:
        pool += DIGITS
    if use_symbols:
        pool += SYMBOLS
    return pool

def generate_password(length: int, charset: str,
                      use_upper: bool, use_digits: bool,
                      use_symbols: bool) -> str:
    """
    Generate a password of `length` characters from `charset`.
    Guarantees at least one character from every enabled group.
    """
    guaranteed = [random.choice(LOWERCASE)]          # always include lowercase
    if use_upper:
        guaranteed.append(random.choice(UPPERCASE))
    if use_digits:
        guaranteed.append(random.choice(DIGITS))
    if use_symbols:
        guaranteed.append(random.choice(SYMBOLS))

    # Fill the rest randomly
    remaining = [random.choice(charset) for _ in range(length - len(guaranteed))]
    password_list = guaranteed + remaining

    # Shuffle so guaranteed chars aren't always at the start
    random.shuffle(password_list)
    return "".join(password_list)

def password_strength(password: str) -> tuple[int, str]:
    """
    Rate password strength and return (score_out_of_4, label).
    """
    score = 0
    if len(password) >= 8:   score += 1
    if len(password) >= 12:  score += 1
    if len(password) >= 16:  score += 1
    if re.search(r"[A-Z]", password):          score += 1
    if re.search(r"[0-9]", password):          score += 1
    if re.search(r"[^a-zA-Z0-9]", password):  score += 1

    if score <= 2:
        return 1, "Weak"
    elif score <= 4:
        return 2, "Fair"
    elif score == 5:
        return 3, "Strong"
    else:
        return 4, "Very Strong"

class PasswordGeneratorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Advanced Password Generator")
        self.geometry("450x600")
        self.resizable(False, False)
        
        # Appearance configuration
        ctk.set_appearance_mode("Dark")
        self.configure(fg_color=SPACE_CADET)
        
        # Main Frame
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Title
        self.title_label = ctk.CTkLabel(
            self.main_frame, 
            text="🔐 Password Generator", 
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=TAN
        )
        self.title_label.pack(pady=(0, 20))
        
        # Password Display Frame
        self.display_frame = ctk.CTkFrame(self.main_frame, fg_color=SLATE_GRAY)
        self.display_frame.pack(fill="x", pady=(0, 20))
        
        self.password_var = ctk.StringVar(value="Click Generate...")
        self.password_entry = ctk.CTkEntry(
            self.display_frame, 
            textvariable=self.password_var, 
            font=ctk.CTkFont(size=20),
            state="readonly",
            height=50,
            justify="center",
            fg_color=SPACE_CADET,
            text_color=TAN,
            border_color=TAN,
            border_width=1
        )
        self.password_entry.pack(fill="x", padx=10, pady=10)
        
        # Copy Button
        self.copy_button = ctk.CTkButton(
            self.main_frame,
            text="📋 Copy to Clipboard",
            command=self.copy_to_clipboard,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=COFFEE,
            hover_color=CAPUT_MORTUUM,
            text_color=TAN
        )
        self.copy_button.pack(fill="x", pady=(0, 20))
        
        # Options Frame
        self.options_frame = ctk.CTkFrame(self.main_frame, fg_color=SLATE_GRAY)
        self.options_frame.pack(fill="x", pady=(0, 20))
        
        # Length Slider
        self.length_frame = ctk.CTkFrame(self.options_frame, fg_color="transparent")
        self.length_frame.pack(fill="x", padx=15, pady=(15, 5))
        
        self.length_var = ctk.IntVar(value=16)
        self.length_label = ctk.CTkLabel(
            self.length_frame, 
            text=f"Password Length: {self.length_var.get()}",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=SPACE_CADET
        )
        self.length_label.pack(anchor="w")
        
        self.length_slider = ctk.CTkSlider(
            self.length_frame, 
            from_=4, 
            to=128, 
            variable=self.length_var,
            command=self.update_length_label,
            button_color=SPACE_CADET,
            button_hover_color=SPACE_CADET,
            progress_color=COFFEE
        )
        self.length_slider.pack(fill="x", pady=(5, 10))
        
        # Switches
        self.upper_var = ctk.BooleanVar(value=True)
        self.upper_switch = ctk.CTkSwitch(
            self.options_frame, 
            text="Include Uppercase Letters",
            variable=self.upper_var,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=SPACE_CADET,
            progress_color=COFFEE,
            button_color=SPACE_CADET,
            button_hover_color=SPACE_CADET
        )
        self.upper_switch.pack(anchor="w", padx=15, pady=5)
        
        self.digits_var = ctk.BooleanVar(value=True)
        self.digits_switch = ctk.CTkSwitch(
            self.options_frame, 
            text="Include Digits (0-9)",
            variable=self.digits_var,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=SPACE_CADET,
            progress_color=COFFEE,
            button_color=SPACE_CADET,
            button_hover_color=SPACE_CADET
        )
        self.digits_switch.pack(anchor="w", padx=15, pady=5)
        
        self.symbols_var = ctk.BooleanVar(value=True)
        self.symbols_switch = ctk.CTkSwitch(
            self.options_frame, 
            text="Include Symbols (!@#...)",
            variable=self.symbols_var,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=SPACE_CADET,
            progress_color=COFFEE,
            button_color=SPACE_CADET,
            button_hover_color=SPACE_CADET
        )
        self.symbols_switch.pack(anchor="w", padx=15, pady=(5, 15))
        
        # Strength Meter
        self.strength_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.strength_frame.pack(fill="x", pady=(0, 20))
        
        self.strength_label = ctk.CTkLabel(
            self.strength_frame, 
            text="Strength: -",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=TAN
        )
        self.strength_label.pack(anchor="w", pady=(0, 5))
        
        self.strength_bar = ctk.CTkProgressBar(self.strength_frame, height=10)
        self.strength_bar.set(0)
        self.strength_bar.pack(fill="x")
        
        # Generate Button
        self.generate_button = ctk.CTkButton(
            self.main_frame, 
            text="GENERATE PASSWORD", 
            command=self.on_generate,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50,
            fg_color=COFFEE,
            hover_color=CAPUT_MORTUUM,
            text_color=TAN
        )
        self.generate_button.pack(fill="x", side="bottom")
        
        # Initial generation
        self.on_generate()
        
    def update_length_label(self, value):
        self.length_label.configure(text=f"Password Length: {int(value)}")
        
    def copy_to_clipboard(self):
        password = self.password_var.get()
        if password and password != "Click Generate...":
            self.clipboard_clear()
            self.clipboard_append(password)
            self.update() # Required for clipboard on some systems
            
            # Temporarily change button text to indicate success
            original_text = self.copy_button.cget("text")
            self.copy_button.configure(text="✅ Copied!")
            self.after(1500, lambda: self.copy_button.configure(text=original_text))

    def update_strength_meter(self, password):
        level, label = password_strength(password)
        self.strength_label.configure(text=f"Strength: {label}")
        
        # Update progress bar value (level is 1 to 4)
        self.strength_bar.set(level / 4.0)
        
        # Update progress bar color
        if level == 1:
            color = CAPUT_MORTUUM
        elif level == 2:
            color = COFFEE
        elif level == 3:
            color = SLATE_GRAY
        else:
            color = TAN
            
        self.strength_bar.configure(progress_color=color)

    def on_generate(self):
        length = self.length_var.get()
        use_upper = self.upper_var.get()
        use_digits = self.digits_var.get()
        use_symbols = self.symbols_var.get()
        
        enabled_count = 1 + int(use_upper) + int(use_digits) + int(use_symbols)
        if length < enabled_count:
            self.length_var.set(enabled_count)
            self.update_length_label(enabled_count)
            length = enabled_count
            
        charset = build_charset(use_upper, use_digits, use_symbols)
        
        try:
            password = generate_password(length, charset, use_upper, use_digits, use_symbols)
            self.password_var.set(password)
            self.update_strength_meter(password)
        except Exception as e:
            self.password_var.set("Error generating password")

if __name__ == "__main__":
    app = PasswordGeneratorApp()
    app.mainloop()
