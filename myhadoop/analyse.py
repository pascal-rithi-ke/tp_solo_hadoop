import csv, sys
from itertools import combinations
from collections import defaultdict

# Fonction pour calculer l'amplitude à partir de la magnitude et de la tension entre les plaques
def calculer_amplitude(magnitude, tension_entre_plaques):
    constante_station_sismique = 0.0

    # Calcul de l'amplitude
    amplitude = 10 ** (magnitude - constante_station_sismique - tension_entre_plaques)
    return amplitude

# Redirection de la sortie standard vers un fichier texte
sys.stdout = open('app/resultats_seismes.txt', 'w')

# Lecture des données à partir du fichier CSV
donnees_seismes = []
with open('app/csv/clean_data.csv', 'r') as fichier_csv:
    lecteur_csv = csv.DictReader(fichier_csv)
    for ligne in lecteur_csv:
        donnees_seismes.append({
            'date': ligne['date'],
            'ville': ligne['ville'],
            'secousse': int(ligne['secousse']),
            'magnitude': float(ligne['magnitude']),
            'tension entre plaque': float(ligne['tension entre plaque'])
        })

# Dictionnaire pour stocker les amplitudes maximales et les dates correspondantes pour chaque ville
amplitudes_max_ville = {}

# Calcul de l'amplitude maximale pour chaque ville
for seisme in donnees_seismes:
    amplitude = calculer_amplitude(seisme['magnitude'], seisme['tension entre plaque'])
    print(f"Pour le séisme à {seisme['ville']} le {seisme['date']}, l'amplitude est : {amplitude}")
    
    ville = seisme['ville']
    if ville not in amplitudes_max_ville or amplitude > amplitudes_max_ville[ville]['amplitude']:
        amplitudes_max_ville[ville] = {'date': seisme['date'], 'amplitude': amplitude}
        
print("--------------------")
        
# Affichage des amplitudes maximales pour chaque ville
for ville, data in amplitudes_max_ville.items():
    print(f"Pour la ville {ville}, la plus forte amplitude est de {data['amplitude']} le {data['date']}")
    
print("--------------------")

# Correlation entre les événements sismiques

# Mapper
def mapper(seisme):
    return (seisme['ville'], (seisme['magnitude'], seisme['date']))

# Reducer
def reducer(key, values):
    correlations = []
    for pair in combinations(values, 2):
        # Comparaison de chaque paire d'événements sismiques
        event1, event2 = pair
        if event1[0] < event2[0] and event1[1] < event2[1]:
            correlations.append((event1[1], event2[1]))

    return correlations

# Mapper et Reducer ensemble
def map_reduce(data):
    mapped = map(mapper, data)
    grouped = defaultdict(list)
    for key, value in mapped:
        grouped[key].append(value)
    
    result = {}
    for key, values in grouped.items():
        result[key] = reducer(key, values)
    
    return result

# Exécution de MapReduce
result = map_reduce(donnees_seismes)

# Affichage des corrélations pour chaque ville
for ville, correlations in result.items():
    if correlations:
        print(f"Corrélations pour la ville {ville}:")
        for correlation in correlations:
            print(f"   Événement sismique précurseur le {correlation[0]} précède l'événement le {correlation[1]}")

print("--------------------")

intervalles_temps = defaultdict(lambda: defaultdict(int))
for seisme in donnees_seismes:
    date = seisme['date']
    intervalle = date[:7]
    intervalles_temps[seisme['ville']][intervalle] += 1

# Analyse des tendances pour chaque ville
for ville, intervalles in intervalles_temps.items():
    print(f"Tendances de l'activité sismique pour la ville {ville}:")
    for intervalle, nombre_seismes in intervalles.items():
        print(f"   Période : {intervalle}, Nombre d'événements sismiques : {nombre_seismes}")
    print()  # Ajout d'une ligne vide entre chaque ville

# Fermeture du fichier de sortie
sys.stdout.close()