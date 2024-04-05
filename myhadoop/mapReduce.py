#! /usr/bin/env python

import sys

for line in sys.stdin:
    line = line.strip()
    
    # Sépare les champs dans la ligne
    fields = line.split(',')
    
    # Imprimer l'en-tête
    if fields[0] == "date":
        print(','.join(fields))
        continue
    
    try:
        # Si le champ magnitude n'est pas 0.0, imprimer la ligne
        if float(fields[3]) != 0.0:
            if fields[2] == "True":
                fields[2] = "1" # Transformer le champ en True en 1
                print(','.join(fields))
    except ValueError:
        continue
