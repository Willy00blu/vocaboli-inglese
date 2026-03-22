import tkinter as tk
from tkinter import messagebox
import sys
import os

try:
    from quiz_logic import VocabolarioQuiz
    from gui_components import crea_pulsanti
except ImportError as e:
    sys.exit(1)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

COLORE_SFONDO = "#2E2E2E"
COLORE_TESTO = "#FFFFFF"
COLORE_INPUT_BG = "#454545"
COLORE_INPUT_FG = "#FFFFFF"
COLORE_COUNTER = "#AAAAAA"
COLORE_SUCCESS = "#00FF00"
COLORE_ERROR = "#FF5555"
COLORE_INFO = "#4FC3F7"


class VocabolarioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Test Vocabolario")
        self.root.geometry("900x550")
        self.root.configure(bg=COLORE_SFONDO)

        self.iterazioni = 0

        try:
            self.quiz = VocabolarioQuiz(os.path.join(BASE_DIR, "vocabolario_pronto.csv"))
        except Exception as e:
            messagebox.showerror("Errore Dati", f"Errore: {e}")
            return

        self.lbl_parola = tk.Label(
            root,
            text="Caricamento...",
            font=("Helvetica", 26, "bold"),
            bg=COLORE_SFONDO,
            fg=COLORE_TESTO
        )
        self.lbl_parola.pack(pady=20)

        self.entry_trad = tk.Entry(
            root,
            font=("Helvetica", 18),
            bg=COLORE_INPUT_BG,
            fg=COLORE_INPUT_FG,
            insertbackground="white"
        )
        self.entry_trad.pack(pady=20)
        self.entry_trad.bind("<Return>", lambda event: self.verifica())

        self.lbl_risultato = tk.Label(
            root,
            text="",
            font=("Helvetica", 16),
            bg=COLORE_SFONDO,
            fg=COLORE_TESTO
        )
        self.lbl_risultato.pack(pady=10)

        self.lbl_counter = tk.Label(
            root,
            text="In attesa...",
            font=("Consolas", 12),
            bg=COLORE_SFONDO,
            fg=COLORE_COUNTER
        )
        self.lbl_counter.pack(pady=10)

        self.btn_verifica, self.btn_skip, self.btn_mistakes, self.btn_reset = crea_pulsanti(
            parent=root,
            on_verifica=self.verifica,
            on_prossima=self.chiedi_parola,
            on_skip=self.skip,
            on_mistakes=self.toggle_mistakes,
            on_reset=self.reset_totale
        )

        self.aggiorna_counter()
        self.chiedi_parola()

    def chiedi_parola(self):
        parola = self.quiz.pull_dalla_lista()

        if parola is None:
            if self.quiz.in_mistakes_mode:
                self.lbl_parola.config(text="Ripasso Finito!")
                self.lbl_risultato.config(text="Torna al test principale.", fg=COLORE_INFO)
            else:
                self.lbl_parola.config(text="Test Completato!")
                self.lbl_risultato.config(text="Hai fatto tutte le parole!", fg=COLORE_INFO)

            self.entry_trad.delete(0, tk.END)
            self.entry_trad.config(state='disabled', disabledbackground=COLORE_SFONDO)
            return

        self.entry_trad.config(state='normal')
        self.lbl_parola.config(text=parola)
        self.lbl_risultato.config(text="")
        self.entry_trad.delete(0, tk.END)
        self.entry_trad.focus()

    def verifica(self):
        if self.entry_trad['state'] == 'disabled':
            return

        risposta = self.entry_trad.get()
        giusto, significato = self.quiz.verifica_risposta(risposta)

        if giusto:
            self.lbl_risultato.config(text="Giusto!", fg=COLORE_SUCCESS)
            self.root.after(600, self.chiedi_parola)
        else:
            self.lbl_risultato.config(text=f"Era: {significato}", fg=COLORE_ERROR)
            self.root.after(2000, self.chiedi_parola)

        self.aggiorna_counter()

    def skip(self):
        if self.entry_trad['state'] == 'disabled':
            return

        # passa una risposta vuota per registrare l'errore e andare avanti
        _, significato = self.quiz.verifica_risposta("")
        self.lbl_risultato.config(text=f"Era: {significato}", fg=COLORE_ERROR)
        self.aggiorna_counter()
        self.root.after(2000, self.chiedi_parola)

    def aggiorna_counter(self):
        errori = self.quiz.sbagliate_counter
        tentativi_totali = len(self.quiz.risolte) + errori

        if tentativi_totali > 0:
            accuratezza = (len(self.quiz.risolte) / tentativi_totali) * 100
        else:
            accuratezza = 0.0

        rimanenti = self.quiz.conta_rimanenti()
        streak = self.quiz.streak
        best = self.quiz.best_streak

        stats_text = (f"Rimanenti: {rimanenti} | "
                      f"Err: {errori} | "
                      f"Acc: {accuratezza:.1f}% | "
                      f"Streak: {streak} (Best: {best})")

        self.lbl_counter.config(text=stats_text)

    def toggle_mistakes(self):
        stato = self.quiz.toggle_mistakes_mode()

        if stato is None:
            messagebox.showinfo("Info", "Nessuna parola sbagliata (o tutte corrette)!")
            return

        if stato is True:
            self.btn_mistakes.config(text="Torna al Test", bg="orange", fg="black")
            self.lbl_risultato.config(text="Modalita Ripasso Attiva", fg=COLORE_INFO)
        else:
            self.btn_mistakes.config(text="Solo Sbagliate", bg="SystemButtonFace", fg="black")
            self.lbl_risultato.config(text="Ritorno al Test Principale", fg=COLORE_INFO)

        self.entry_trad.config(state='normal')
        self.aggiorna_counter()
        self.chiedi_parola()

    def reset_totale(self):
        risposta = messagebox.askyesno("Reset", "Vuoi ricominciare tutto da capo?\nPerderai i progressi attuali.")
        if risposta:
            self.quiz.reset_totale()
            self.iterazioni = 0

            self.btn_mistakes.config(text="Solo Sbagliate", bg="SystemButtonFace", fg="black")
            self.entry_trad.config(state='normal')
            self.aggiorna_counter()
            self.chiedi_parola()


if __name__ == "__main__":
    root = tk.Tk()
    app = VocabolarioApp(root)
    root.mainloop()
