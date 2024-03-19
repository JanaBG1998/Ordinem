import tkinter as tk

    def __init__(self):

def submit():
    data = {
        "name": name_entry.get(),
        "menge": menge_entry.get(),
        "eigenschaft": eigenschaft_entry.get(),
        "gewicht": gewicht_entry.get(),
        "barcode": barcode_entry.get(),
        "nummer": nummer_entry.get(),
        "farbe": farbe_entry.get(),
        "preis": preis_entry.get(),
        "lagerort": lagerort_entry.get(),
        "picture": picture_entry.get(),
        "link": link_entry.get()
    }
    print(data)  # Hier könntest du die Daten in eine Datenbank speichern oder anderweitig verwenden

# GUI erstellen
root = tk.Tk()
root.title("Produktinformationen")

# Labels und Inputfelder erstellen
labels = ["Name:", "Menge:", "Eigenschaft:", "Gewicht:", "Barcode:", "Nummer:", "Farbe:", "Preis:", "Lagerort:", "Picture:", "Link:"]
entries = {}

for i, label in enumerate(labels):
    tk.Label(root, text=label).grid(row=i, column=0, sticky="e")
    entry = tk.Entry(root)
    entry.grid(row=i, column=1)
    entries[label[:-1].lower()] = entry  # Key in Kleinbuchstaben ohne ':' hinzufügen

# Submit-Button erstellen
submit_button = tk.Button(root, text="Submit", command=submit)
submit_button.grid(row=len(labels), columnspan=2)

root.mainloop()

