# Vocaboli Inglese

App desktop per studiare e testare il vocabolario inglese. Costruita con Python e Tkinter, tiene traccia degli errori sessione per sessione e permette di ripassare solo le parole sbagliate.

---

## Funzionalità

- Quiz a risposta libera: viene mostrata la parola inglese, si digita la traduzione italiana
- Supporto a più traduzioni valide per la stessa parola (separate da virgola nel CSV)
- Tracciamento errori persistente su file — le parole sbagliate vengono salvate con il contatore degli errori
- Modalità ripasso: filtra automaticamente solo le parole sbagliate nella sessione corrente
- Statistiche in tempo reale: parole rimanenti, errori, accuratezza percentuale, streak attuale e migliore
- Reset completo con conferma

---

## Struttura

```
vocaboli-inglese/
├── main.py                  # GUI e gestione eventi
├── quiz_logic.py            # Logica del quiz, caricamento CSV, verifica risposte
├── gui_components.py        # Factory dei pulsanti
├── scrittura_sbagliate.py   # Scrittura e aggiornamento del log errori
├── vocabolario_pronto.csv   # Vocabolario usato dall'app (Parola + Significato)
├── voc_completo.csv         # Sorgente con colonne extra (esempio, pronuncia, tipo)
└── utilities/
    └── pulisci_csv.py       # Genera vocabolario_pronto.csv da voc_completo.csv
```

---

## Utilizzo

```bash
python3 main.py
```

Non richiede dipendenze esterne — usa solo la libreria standard Python (tkinter, csv, os).

---

## Formato CSV

Il file `vocabolario_pronto.csv` deve avere esattamente queste due colonne:

```
Parola,Significato in Italiano
clumsy,"goffo, maldestro"
eager,desideroso
```

Se una parola ha più traduzioni valide, separale con una virgola all'interno della cella. Tutte le varianti vengono accettate come risposta corretta.

Per aggiornare il vocabolario partendo da `voc_completo.csv`:

```bash
python3 utilities/pulisci_csv.py
```

---

## Log errori

Gli errori vengono salvati in `parole_sbagliate.txt` nel formato:

```
clumsy = goffo, maldestro (2)
eager = desideroso (1)
```

Il numero tra parentesi indica quante volte la parola è stata sbagliata nella sessione. Il file viene aggiornato in tempo reale durante il quiz.
