import os


def scrittura_file(file_path, sbagliata):
    """
    Scrive o aggiorna la riga relativa a una parola sbagliata.
    Formato riga: "parola = significato (n_errori)"
    """
    parola, significato, count = sbagliata
    riga_nuova = f"{parola} = {significato} ({count})\n"

    # prima volta: semplice append, non serve rileggere tutto il file
    if count == 1:
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(riga_nuova)
        return

    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(riga_nuova)
        return

    # errore ripetuto: bisogna aggiornare il contatore nella riga esistente
    nuove_righe = []
    trovata = False

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            linee = f.readlines()

        for line in linee:
            # confronto su "parola =" per evitare falsi positivi con parole che si contengono
            if line.startswith(parola + " ="):
                nuove_righe.append(riga_nuova)
                trovata = True
            else:
                nuove_righe.append(line)

        if not trovata:
            nuove_righe.append(riga_nuova)

        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(nuove_righe)

    except IOError as e:
        print(f"Errore durante la scrittura del file: {e}")
