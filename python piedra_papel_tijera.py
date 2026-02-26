import tkinter as tk
import random
from enum import Enum

# ----------------------------------------------------------------------
# Capa de Lógica (Core)
# ----------------------------------------------------------------------
class Move(Enum):
    ROCK = "Piedra"
    PAPER = "Papel"
    SCISSORS = "Tijera"

    @property
    def symbol(self):
        return {"Piedra": "✊", "Papel": "✋", "Tijera": "✌️"}[self.value]

class RulesEngine:
    @staticmethod
    def determine_winner(player: Move, cpu: Move) -> str:
        if player == cpu:
            return "Empate"
        winning_combos = {
            Move.ROCK: Move.SCISSORS,
            Move.PAPER: Move.ROCK,
            Move.SCISSORS: Move.PAPER
        }
        return "Jugador" if winning_combos[player] == cpu else "CPU"

class RNGService:
    @staticmethod
    def get_random_choice() -> Move:
        return random.choice(list(Move))

# ----------------------------------------------------------------------
# Capa de Control
# ----------------------------------------------------------------------
class GameController:
    def __init__(self):
        self.rules = RulesEngine()
        self.rng = RNGService()
        self.player_score = 0
        self.cpu_score = 0

    def play_round(self, player_choice: Move):
        cpu_choice = self.rng.get_random_choice()
        result = self.rules.determine_winner(player_choice, cpu_choice)
        if result == "Jugador":
            self.player_score += 1
        elif result == "CPU":
            self.cpu_score += 1
        return result, player_choice, cpu_choice

    def reset_scores(self):
        self.player_score = 0
        self.cpu_score = 0

# ----------------------------------------------------------------------
# Popups personalizados
# ----------------------------------------------------------------------
class BasePopup(tk.Toplevel):
    def __init__(self, parent, title, message, button_texts, button_commands):
        super().__init__(parent)
        self.title(title)
        self.geometry("400x200")
        self.resizable(False, False)
        self.configure(bg="#2c3e50")
        self.grab_set()
        self.center_window()

        tk.Label(
            self,
            text=message,
            font=("Segoe UI", 14, "bold"),
            bg="#2c3e50",
            fg="#ecf0f1",
            wraplength=350
        ).pack(pady=30)

        button_frame = tk.Frame(self, bg="#2c3e50")
        button_frame.pack(pady=10)

        for text, cmd in zip(button_texts, button_commands):
            btn = tk.Button(
                button_frame,
                text=text,
                font=("Segoe UI", 12),
                bg="#3498db",
                fg="white",
                activebackground="#2980b9",
                relief="flat",
                padx=20,
                pady=5,
                command=lambda c=cmd: self.on_button_click(c)
            )
            btn.pack(side="left", padx=10)

        self.protocol("WM_DELETE_WINDOW", self.default_close)

    def center_window(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")

    def on_button_click(self, command):
        self.destroy()
        if command:
            command()

    def default_close(self):
        self.destroy()

class ResultPopup(BasePopup):
    def __init__(self, parent, result, player_score, cpu_score, on_new_round, on_quit):
        if result == "Jugador":
            message = f"🎉 ¡Ganaste! 🎉"
            color = "#2ecc71"
        elif result == "CPU":
            message = f"💻 Perdiste contra la CPU 💻"
            color = "#e74c3c"
        else:
            message = f"🤝 Empate 🤝"
            color = "#f39c12"

        super().__init__(
            parent,
            title="Resultado",
            message=message,
            button_texts=["🔁 Nueva ronda", "🚪 Salir"],
            button_commands=[on_new_round, on_quit]
        )
        for child in self.winfo_children():
            if isinstance(child, tk.Label) and child.cget("text").startswith(("🎉", "💻", "🤝")):
                child.config(fg=color)
                break

class WelcomePopup(BasePopup):
    def __init__(self, parent, on_new_round, on_quit):
        super().__init__(
            parent,
            title="Bienvenido",
            message="¡Bienvenido a Piedra, Papel o Tijera!\n\nElige una opción para comenzar.",
            button_texts=["🎮 Nueva ronda", "🚪 Salir"],
            button_commands=[on_new_round, on_quit]
        )

# ----------------------------------------------------------------------
# Interfaz principal
# ----------------------------------------------------------------------
class RockPaperScissorsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Piedra, Papel o Tijera ✊✋✌️")
        self.root.geometry("600x600")  # <--- AUMENTADO A 600x600
        self.root.resizable(False, False)
        self.root.configure(bg="#2c3e50")
        self.center_main_window()

        self.controller = GameController()

        self.font_large = ("Segoe UI", 18, "bold")
        self.font_medium = ("Segoe UI", 12)
        self.bg_color = "#2c3e50"
        self.fg_color = "#ecf0f1"
        self.accent_color = "#3498db"
        self.success_color = "#2ecc71"
        self.error_color = "#e74c3c"
        self.warning_color = "#f39c12"

        self._create_widgets()
        self.disable_move_buttons()
        self.root.after(100, self.show_welcome_popup)

    def center_main_window(self):
        self.root.update_idletasks()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (w // 2)
        y = (self.root.winfo_screenheight() // 2) - (h // 2)
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def _create_widgets(self):
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        tk.Label(main_frame, text="Piedra, Papel o Tijera", font=("Segoe UI", 24, "bold"),
                 bg=self.bg_color, fg=self.fg_color).pack(pady=(0, 10))
        tk.Label(main_frame, text="Elige tu movimiento y vence a la CPU", font=self.font_medium,
                 bg=self.bg_color, fg="#bdc3c7").pack(pady=(0, 20))

        # Jugadas
        moves_frame = tk.Frame(main_frame, bg=self.bg_color)
        moves_frame.pack(pady=10)
        self.player_move_label = tk.Label(moves_frame, text="Tu jugada: —", font=self.font_large,
                                          bg=self.bg_color, fg=self.fg_color)
        self.player_move_label.grid(row=0, column=0, padx=20)
        tk.Label(moves_frame, text="VS", font=("Segoe UI", 20, "bold"),
                 bg=self.bg_color, fg=self.warning_color).grid(row=0, column=1, padx=20)
        self.cpu_move_label = tk.Label(moves_frame, text="CPU: —", font=self.font_large,
                                       bg=self.bg_color, fg=self.fg_color)
        self.cpu_move_label.grid(row=0, column=2, padx=20)

        # Resultado
        self.result_label = tk.Label(main_frame, text="¡Comienza el juego!", font=self.font_large,
                                      bg=self.bg_color, fg=self.accent_color)
        self.result_label.pack(pady=20)

        # Botones de movimiento
        btn_frame = tk.Frame(main_frame, bg=self.bg_color)
        btn_frame.pack(pady=20)
        self.btn_rock = tk.Button(btn_frame, text=f"Piedra {Move.ROCK.symbol}", font=self.font_large,
                                   bg=self.accent_color, fg="white", activebackground="#2980b9",
                                   relief="flat", padx=20, pady=10,
                                   command=lambda: self._on_move_selected(Move.ROCK))
        self.btn_rock.grid(row=0, column=0, padx=10)
        self.btn_paper = tk.Button(btn_frame, text=f"Papel {Move.PAPER.symbol}", font=self.font_large,
                                    bg=self.accent_color, fg="white", activebackground="#2980b9",
                                    relief="flat", padx=20, pady=10,
                                    command=lambda: self._on_move_selected(Move.PAPER))
        self.btn_paper.grid(row=0, column=1, padx=10)
        self.btn_scissors = tk.Button(btn_frame, text=f"Tijera {Move.SCISSORS.symbol}", font=self.font_large,
                                       bg=self.accent_color, fg="white", activebackground="#2980b9",
                                       relief="flat", padx=20, pady=10,
                                       command=lambda: self._on_move_selected(Move.SCISSORS))
        self.btn_scissors.grid(row=0, column=2, padx=10)

        # Puntuación
        score_frame = tk.Frame(main_frame, bg=self.bg_color)
        score_frame.pack(pady=10)
        self.player_score_label = tk.Label(score_frame, text="Rondas ganadas jugador: 0", font=self.font_medium,
                                           bg=self.bg_color, fg=self.success_color)
        self.player_score_label.grid(row=0, column=0, padx=20)
        self.cpu_score_label = tk.Label(score_frame, text="Rondas ganadas CPU: 0", font=self.font_medium,
                                        bg=self.bg_color, fg=self.error_color)
        self.cpu_score_label.grid(row=0, column=1, padx=20)

        # Botones de control
        control_frame = tk.Frame(main_frame, bg=self.bg_color)
        control_frame.pack(pady=20)
        tk.Button(control_frame, text="Reiniciar puntuación", font=self.font_medium,
                  bg="#95a5a6", fg="white", activebackground="#7f8c8d",
                  relief="flat", padx=10, pady=5, command=self._reset_scores).grid(row=0, column=0, padx=10)
        tk.Button(control_frame, text="Salir", font=self.font_medium,
                  bg=self.error_color, fg="white", activebackground="#c0392b",
                  relief="flat", padx=10, pady=5, command=self.root.quit).grid(row=0, column=1, padx=10)

    def disable_move_buttons(self):
        self.btn_rock.config(state="disabled")
        self.btn_paper.config(state="disabled")
        self.btn_scissors.config(state="disabled")

    def enable_move_buttons(self):
        self.btn_rock.config(state="normal")
        self.btn_paper.config(state="normal")
        self.btn_scissors.config(state="normal")

    def clear_moves_display(self):
        self.player_move_label.config(text="Tu jugada: —")
        self.cpu_move_label.config(text="CPU: —")
        self.result_label.config(text="Elige una opción", fg=self.accent_color)

    def show_welcome_popup(self):
        WelcomePopup(self.root, on_new_round=self.start_new_round, on_quit=self.root.quit)

    def start_new_round(self):
        self.enable_move_buttons()
        self.clear_moves_display()

    def _on_move_selected(self, player_move):
        result, player, cpu = self.controller.play_round(player_move)
        self._update_ui(result, player, cpu)
        self.disable_move_buttons()
        self.show_result_popup(result)

    def _update_ui(self, result=None, player=None, cpu=None):
        if result and player and cpu:
            self.player_move_label.config(text=f"Tu jugada: {player.value} {player.symbol}")
            self.cpu_move_label.config(text=f"CPU: {cpu.value} {cpu.symbol}")
            if result == "Jugador":
                self.result_label.config(text="🎉 ¡Ganaste! 🎉", fg=self.success_color)
            elif result == "CPU":
                self.result_label.config(text="💻 Perdiste contra la CPU 💻", fg=self.error_color)
            else:
                self.result_label.config(text="🤝 Empate 🤝", fg=self.warning_color)
        else:
            self.player_move_label.config(text="Tu jugada: —")
            self.cpu_move_label.config(text="CPU: —")
            self.result_label.config(text="¡Comienza el juego!", fg=self.accent_color)

        self.player_score_label.config(text=f"Rondas ganadas jugador: {self.controller.player_score}")
        self.cpu_score_label.config(text=f"Rondas ganadas CPU: {self.controller.cpu_score}")

    def show_result_popup(self, result):
        ResultPopup(self.root, result, self.controller.player_score, self.controller.cpu_score,
                    on_new_round=self.start_new_round, on_quit=self.root.quit)

    def _reset_scores(self):
        self.controller.reset_scores()
        self._update_ui()
        self.clear_moves_display()
        self.enable_move_buttons()

# ----------------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = RockPaperScissorsGUI(root)
    root.mainloop()