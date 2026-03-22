import csv
import os

# la root del progetto è la cartella padre di utilities/
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def pulisci_vocabolario(input_file=None, output_file=None):
    """
    Estrae solo 'Parola' e 'Significato in Italiano' da voc_completo.csv
    e genera vocabolario_pronto.csv usato dall'app.
    Da eseguire ogni volta che si aggiorna il vocabolario sorgente.
    """
    if input_file is None:
        input_file = os.path.join(ROOT_DIR, "voc_completo.csv")
    if output_file is None:
        output_file = os.path.join(ROOT_DIR, "vocabolario_pronto.csv")

    if not os.path.exists(input_file):
        print(f"ERRORE: Non trovo '{input_file}'.")
        return

    print(f"Lettura di '{input_file}'...")

    try:
        with open(input_file, mode='r', encoding='utf-8-sig', newline='') as csv_in:
            reader = csv.DictReader(csv_in)
            # utf-8-sig gestisce il BOM dei CSV esportati da Excel
            reader.fieldnames = [col.strip() for col in reader.fieldnames]

            colonne_richieste = ["Parola", "Significato in Italiano"]
            for col in colonne_richieste:
                if col not in reader.fieldnames:
                    print(f"ERRORE: colonna '{col}' non trovata. Colonne presenti: {reader.fieldnames}")
                    return

            count = 0

            with open(output_file, mode='w', encoding='utf-8', newline='') as csv_out:
                writer = csv.DictWriter(csv_out, fieldnames=colonne_richieste)
                writer.writeheader()

                for row in reader:
                    parola = row["Parola"]
                    significato = row["Significato in Italiano"]
                    if parola and significato:
                        writer.writerow({
                            "Parola": parola.strip(),
                            "Significato in Italiano": significato.strip()
                        })
                        count += 1

        print(f"Fatto. {count} parole salvate in '{output_file}'.")

    except Exception as e:
        print(f"Errore: {e}")


if __name__ == "__main__":
    pulisci_vocabolario()
