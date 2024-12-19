# Programme1.py

def lire_fichier_ics(chemin_fichier):
    """Lit le contenu d'un fichier ICS."""
    try:
        with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
            contenu = fichier.readlines()
        return contenu
    except FileNotFoundError:
        print(f"Erreur : Le fichier {chemin_fichier} est introuvable.")
        return None

def extraire_donnees_ics(contenu):
    """Extrait les données pertinentes d'un fichier ICS."""
    donnees = {}
    for ligne in contenu:
        if ligne.startswith("SUMMARY:"):
            donnees["Résumé"] = ligne[len("SUMMARY:"):].strip()
        elif ligne.startswith("DTSTART:"):
            donnees["Date de début"] = ligne[len("DTSTART:"):].strip()
        elif ligne.startswith("DTEND:"):
            donnees["Date de fin"] = ligne[len("DTEND:"):].strip()
        elif ligne.startswith("DESCRIPTION:"):
            donnees["Description"] = ligne[len("DESCRIPTION:"):].strip()
    return donnees

def convertir_en_csv(donnees):
    """Convertit les données en format CSV."""
    if not donnees:
        return ""
    colonnes = ["Résumé", "Date de début", "Date de fin", "Description"]
    ligne_csv = ",".join([donnees.get(col, "") for col in colonnes])
    return ligne_csv

def main():
    chemin_fichier = "evenementSAE_15GroupeA1.ics"  # Nom du fichier à traiter
    contenu = lire_fichier_ics(chemin_fichier)
    if contenu is None:
        return
    
    donnees = extraire_donnees_ics(contenu)
    chaine_csv = convertir_en_csv(donnees)
    
    if chaine_csv:
        print("Contenu au format CSV :")
        print("Résumé,Date de début,Date de fin,Description")  # En-têtes
        print(chaine_csv)
    else:
        print("Aucune donnée pertinente n'a été trouvée dans le fichier.")

if __name__ == "__main__":
    main()
