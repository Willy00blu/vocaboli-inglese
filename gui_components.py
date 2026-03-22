import tkinter as tk


def crea_pulsanti(parent, on_verifica, on_prossima, on_skip, on_mistakes, on_reset):
    frame = tk.Frame(parent)
    frame.pack(pady=10)

    btn_verifica = tk.Button(frame, text="Verifica", font=("Helvetica", 12), command=on_verifica)
    btn_verifica.grid(row=0, column=0, padx=5)

    btn_skip = tk.Button(frame, text="Salta", font=("Helvetica", 12), command=on_skip)
    btn_skip.grid(row=0, column=1, padx=5)

    # il testo di questo pulsante cambia dinamicamente in main.py a seconda della modalita
    btn_mistakes = tk.Button(frame, text="Solo Sbagliate", font=("Helvetica", 12), command=on_mistakes)
    btn_mistakes.grid(row=0, column=2, padx=5)

    btn_reset = tk.Button(frame, text="Reset Totale", font=("Helvetica", 12), fg="red", command=on_reset)
    btn_reset.grid(row=0, column=3, padx=5)

    return btn_verifica, btn_skip, btn_mistakes, btn_reset
