import re
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# Fichiers d'entrée/sortie
tcpdump_file = "wireshark.txt"  # Fichier texte contenant les données capturées par Wireshark/tcpdump
csv_output_file = "network_traffic.csv"  # Fichier de sortie pour les données CSV
suspicious_report_file = "suspicious_activity_report.md"  # Fichier de sortie pour le rapport Markdown
graph_output_file = "network_traffic_graphs.png"  # Fichier de sortie pour les graphiques


def charger_donnees(tcpdump_file):
    """Charger les données du fichier tcpdump et extraire les informations nécessaires."""
    with open(tcpdump_file, 'r', encoding="utf-8") as file:
        data = file.readlines()  # Lire toutes les lignes du fichier tcpdump
    return data


def analyser_donnees(data):
    """Analyser les données pour extraire les informations pertinentes avec une expression régulière."""
    pattern = r"(\d{2}:\d{2}:\d{2}\.\d+)\s+IP\s+(\S+)\s>\s(\S+):\sFlags\s+\[(\S+)\],.*length\s+(\d+)"
    records = []

    for line in data:
        match = re.search(pattern, line)
        if match:
            time, src_ip, dest_ip, flags, length = match.groups()  # Extraire les groupes correspondant aux données
            records.append({
                "Heure": time,  # Heure du paquet
                "IP Source": src_ip,  # Adresse IP source
                "IP Destination": dest_ip,  # Adresse IP destination
                "Flags": flags,  # Flags TCP
                "Longueur": int(length)  # Longueur du paquet
            })

    # Convertir les données extraites en DataFrame pandas
    return pd.DataFrame(records)


def sauvegarder_csv(df, csv_output_file):
    """Sauvegarder les données dans un fichier CSV."""
    df.to_csv(csv_output_file, index=False)  # Enregistrer le DataFrame sous forme de fichier CSV


def detecter_menaces(df):
    """Détecter les menaces potentielles (DDoS, Flood, anomalies TCP) dans les données."""
    suspicious_activity = []  # Liste pour stocker les descriptions des activités suspectes

    # Détection DDoS : Identifier les IPs avec un grand nombre de connexions
    connections_per_source = df["IP Source"].value_counts()  # Compter les connexions par IP source
    threshold_ddos = 100  # Seuil pour identifier un DDoS
    suspicious_ips_ddos = connections_per_source[connections_per_source > threshold_ddos].index.tolist()

    if suspicious_ips_ddos:
        suspicious_activity.append("*DDoS possible :* IP(s) source avec trop de connexions")
        for ip in suspicious_ips_ddos:
            suspicious_activity.append(f"- {ip} : {connections_per_source[ip]} connexions détectées")

    # Détection de flood : IPs envoyant beaucoup de paquets courts
    short_packets = df[df["Longueur"] < 50]  # Filtrer les paquets de courte longueur
    short_packet_counts = short_packets["IP Source"].value_counts()
    threshold_flood = 50  # Seuil pour identifier un flood
    suspicious_ips_flood = short_packet_counts[short_packet_counts > threshold_flood].index.tolist()

    if suspicious_ips_flood:
        suspicious_activity.append("*Flood possible :* IP(s) envoyant beaucoup de paquets courts")
        for ip in suspicious_ips_flood:
            suspicious_activity.append(f"- {ip} : {short_packet_counts[ip]} paquets courts détectés")

    # Anomalies TCP : Analyse des flags TCP pour détecter une activité inhabituelle
    flag_counts = Counter(df["Flags"])  # Compter les occurrences de chaque type de flag TCP
    suspicious_activity.append("*Statistiques des flags TCP :*")
    for flag, count in flag_counts.items():
        suspicious_activity.append(f"- {flag} : {count} occurrences")

    return suspicious_activity, connections_per_source, short_packet_counts


def generer_rapport_markdown(suspicious_activity, connections_per_source, short_packet_counts, df, suspicious_report_file):
    """Générer un rapport Markdown avec les informations de menaces détectées."""
    markdown_content = f"""
    # Rapport de Détection de Menaces Réseau

    ## Résumé des Résultats
    - Nombre total de paquets analysés : *{len(df)}*
    - Nombre d'adresses IP sources uniques : *{df["IP Source"].nunique()}*
    - Nombre d'adresses IP destinations uniques : *{df["IP Destination"].nunique()}*

    ## Menaces Potentielles Détectées
    {''.join([f"<br>{item}" for item in suspicious_activity])}

    ## Statistiques Complètes
    ### Connexions par IP Source (Top 10)
    {connections_per_source.head(10).to_markdown(index=False)}

    ### Paquets Courts par IP Source (Top 10)
    {short_packet_counts.head(10).to_markdown(index=False)}
    """

    with open(suspicious_report_file, "w", encoding="utf-8") as file:
        file.write(markdown_content)


def generer_graphiques(connections_per_source, short_packet_counts, graph_output_file):
    """Générer des graphiques pour illustrer les résultats de l'analyse."""
    plt.figure(figsize=(12, 6))

    # Graphique 1: Connexions par IP Source (Top 10)
    plt.subplot(1, 2, 1)
    connections_per_source.head(10).plot(kind="pie", autopct='%1.1f%%', title="Top 10 des Connexions par IP Source", ylabel="")
    plt.ylabel("")

    # Graphique 2: Paquets Courts par IP Source (Top 10)
    plt.subplot(1, 2, 2)
    short_packet_counts.head(10).plot(kind="pie", autopct='%1.1f%%', title="Top 10 des Paquets Courts par IP Source", ylabel="")
    plt.ylabel("")

    plt.tight_layout()
    plt.savefig(graph_output_file)  # Enregistrer les graphiques dans un fichier image


def generer_page_web(suspicious_activity, connections_per_source, short_packet_counts, df, graph_output_file):
    """Générer une page web HTML avec le rapport et les graphiques."""
    html_content = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Rapport de Détection de Menaces Réseau</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f9;
                color: #333;
            }}
            h1 {{
                background-color: #0066cc;
                color: white;
                padding: 10px;
                text-align: center;
            }}
            h2 {{
                color: #0066cc;
            }}
            p {{
                font-size: 14px;
                line-height: 1.6;
            }}
            ul {{
                list-style-type: none;
                padding-left: 0;
            }}
            li {{
                margin: 5px 0;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background-color: white;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }}
            img {{
                max-width: 100%;
                height: auto;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Rapport de Détection de Menaces Réseau</h1>
            <p><strong>Résumé des résultats :</strong></p>
            <ul>
                <li>Nombre total de paquets analysés : {len(df)}</li>
                <li>Nombre d'adresses IP sources uniques : {df["IP Source"].nunique()}</li>
                <li>Nombre d'adresses IP destinations uniques : {df["IP Destination"].nunique()}</li>
            </ul>
            <h2>Menaces Potentielles Détectées</h2>
            <p>{''.join([f"<br>{item}" for item in suspicious_activity])}</p>

            <h2>Graphiques :</h2>
            <img src="{graph_output_file}" alt="Graphiques de détection de menaces réseau">

            <h2>Tableaux des Connexions et Paquets Courts par IP Source</h2>
            <h3>Top 10 des Connexions par IP Source</h3>
            {connections_per_source.head(10).to_markdown(index=False)}

            <h3>Top 10 des Paquets Courts par IP Source</h3>
            {short_packet_counts.head(10).to_markdown(index=False)}
        </div>
    </body>
    </html>
    """
    html_report_file = "network_traffic_report.html"
    with open(html_report_file, "w", encoding="utf-8") as file:
        file.write(html_content)
    print(f"Page Web générée : {html_report_file}.")


# Exécution du script
data = charger_donnees(tcpdump_file)
df = analyser_donnees(data)
sauvegarder_csv(df, csv_output_file)
suspicious_activity, connections_per_source, short_packet_counts = detecter_menaces(df)
generer_rapport_markdown(suspicious_activity, connections_per_source, short_packet_counts, df, suspicious_report_file)
generer_graphiques(connections_per_source, short_packet_counts, graph_output_file)
generer_page_web(suspicious_activity, connections_per_source, short_packet_counts, df, graph_output_file)

print(f"Fichier Markdown sauvegardé dans {suspicious_report_file}.")
print(f"Fichier CSV sauvegardé dans {csv_output_file}.")
print(f"Graphiques sauvegardés dans {graph_output_file}.")