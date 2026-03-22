import csv
import random
import os
from scrittura_sbagliate import scrittura_file

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PAROLE_SBAGLIATE_PATH = os.path.join(BASE_DIR, "parole_sbagliate.txt")


class VocabolarioQuiz:
    def __init__(self, csv_file=None):
        if csv_file is None:
            csv_file = os.path.join(BASE_DIR, "vocabolario_pronto.csv")
        self.csv_file = csv_file

        self.streak = 0
        self.best_streak = 0

        self.sbagliate = []
        self.sbagliate_counter = 0
        self.risolte = set()

        self.indice = 0
        self.in_mistakes_mode = False

        self.parole_backup = []
        self.indice_backup = 0

        self.dati_dict = {}
        self.carica_dati()

    def carica_dati(self):
        self.parole = []
        self.dati_dict = {}

        if not os.path.exists(self.csv_file):
            print(f"File {self.csv_file} non trovato. Ne creo uno di prova.")
            try:
                with open(self.csv_file, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(["Parola", "Significato in Italiano"])
                    writer.writerow(["Hello", "Ciao"])
                    writer.writerow(["World", "Mondo"])
            except Exception as e:
                print(f"Errore creazione file dummy: {e}")

        try:
            with open(self.csv_file, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                # strip per gestire CSV esportati da Excel con spazi nelle intestazioni
                reader.fieldnames = [name.strip() for name in reader.fieldnames]

                if "Parola" not in reader.fieldnames or "Significato in Italiano" not in reader.fieldnames:
                    return

                for row in reader:
                    p = row["Parola"]
                    s = row["Significato in Italiano"]
                    if p and s:
                        p = p.strip()
                        self.parole.append(p)
                        self.dati_dict[p] = s.strip()

            random.shuffle(self.parole)

        except Exception as e:
            self.parole = ["ERRORE"]
            self.dati_dict["ERRORE"] = str(e)

    def pull_dalla_lista(self):
        # salta le parole già risolte senza estrarle dalla lista (mantiene l'ordine)
        while self.indice < len(self.parole):
            parola = self.parole[self.indice]
            if parola in self.risolte:
                self.indice += 1
                continue
            return parola
        return None

    def conta_rimanenti(self):
        count = 0
        for p in self.parole:
            if p not in self.risolte:
                count += 1
        return count

    def verifica_risposta(self, risposta):
        if self.finito():
            return None, None

        parola_corr = self.parole[self.indice]
        significato_str = self.dati_dict.get(parola_corr, "Errore dati")

        risposta = risposta.strip().lower()
        # il CSV può contenere più traduzioni separate da virgola (tutte accettate)
        varianti = [s.strip().lower() for s in significato_str.split(",")]
        giusto = risposta in varianti

        if giusto:
            self.risolte.add(parola_corr)
            self.streak += 1
            if self.streak > self.best_streak:
                self.best_streak = self.streak
        else:
            self.gestisci_errore(parola_corr, significato_str)
            self.streak = 0

        self.indice += 1
        return giusto, significato_str

    def gestisci_errore(self, parola, significato):
        self.sbagliate_counter += 1
        trovata = False
        idx = 0
        for i, (p, s, n) in enumerate(self.sbagliate):
            if p == parola:
                self.sbagliate[i] = (p, s, n + 1)
                trovata = True
                idx = i
                break

        if not trovata:
            self.sbagliate.append((parola, significato, 1))
            idx = len(self.sbagliate) - 1

        scrittura_file(PAROLE_SBAGLIATE_PATH, self.sbagliate[idx])

    def finito(self):
        temp_idx = self.indice
        while temp_idx < len(self.parole):
            if self.parole[temp_idx] not in self.risolte:
                return False
            temp_idx += 1
        return True

    def toggle_mistakes_mode(self):
        if self.in_mistakes_mode:
            # ripristina il mazzo principale dal backup
            self.parole = self.parole_backup
            self.indice = self.indice_backup
            self.in_mistakes_mode = False
            return False
        else:
            if not self.sbagliate:
                return None

            # esclude le parole sbagliate che nel frattempo sono state risolte
            lista_errori = [p for (p, _, _) in self.sbagliate if p not in self.risolte]

            if not lista_errori:
                return None

            self.parole_backup = self.parole
            self.indice_backup = self.indice
            self.parole = lista_errori
            self.indice = 0
            self.in_mistakes_mode = True
            return True

    def reset_totale(self):
        self.risolte.clear()
        self.sbagliate = []
        self.sbagliate_counter = 0
        self.streak = 0
        self.best_streak = 0
        self.in_mistakes_mode = False
        self.carica_dati()
        self.indice = 0
