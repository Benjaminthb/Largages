#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 18:32:48 2023

@author: bthoby
"""
import os
import json
import simplekml

# =============================================================================
# # Ouvrir le fichier GeoJSON et le charger en tant que dictionnaire
# with open("output.geojson") as f:
#     data = json.load(f)
# 
# # Créer un nouvel objet KML
# kml = simplekml.Kml()
# 
# 
# # Parcourir chaque entité dans la collection de fonctionnalités GeoJSON
# for feature in data["features"]:
#     # Récupérer les propriétés et la géométrie de l'entité
#     properties = feature["properties"]
#     geometry = feature["geometry"]
# 
#     # Créer un nouvel objet de polygone pour représenter la géométrie
#     polygon = kml.newpolygon()
# 
#     # Définir les propriétés du polygone
#     polygon.name = f"Zone {properties['area']}"
#     polygon.description = f"Date : {properties['date']}"
#     polygon.outerboundaryis = geometry["coordinates"][0][0]
# 
# # for i in range(len(geometry["coordinates"][0][0])):
# #     geometry["coordinates"][0][0][i][0], geometry["coordinates"][0][0][i][1] = geometry["coordinates"][0][0][i][1], geometry["coordinates"][0][0][i][0]
# 
# # Enregistrer le fichier KML
# kml.save("output.kml")
# 
# =============================================================================


# chemin du dossier contenant les fichiers
path = "/home/bthoby/firefront-master/examples/aullene"

# obtenir la liste de tous les fichiers dans le dossier
files = os.listdir(path)

# filtrer les fichiers pour ne prendre que ceux avec l'extension .geojson
files = [file for file in files if file.endswith('.geojson')]

# Parcourir chaque fichier GeoJSON
for file in files:
    with open(os.path.join(path, file), 'r') as f:
        # Charger le fichier en tant que dictionnaire JSON
        content = f.read()
        if content.strip():
            data = json.loads(content)
        
            # Créer un nouvel objet KML
            kml = simplekml.Kml()

            # Parcourir chaque entité dans la collection de fonctionnalités GeoJSON
            for feature in data["features"]:
                # Récupérer les propriétés et la géométrie de l'entité
                properties = feature["properties"]
                geometry = feature["geometry"]

                # Créer un nouvel objet de polygone pour représenter la géométrie
                polygon = kml.newpolygon()

                # Définir les propriétés du polygone
                polygon.name = f"Zone {properties['area']}"
                polygon.description = f"Date : {properties['date']}"
                polygon.outerboundaryis = geometry["coordinates"][0][0]

            # Enregistrer le fichier KML
            output_file = os.path.splitext(file)[0] + '.kml'
            kml.save(os.path.join(path, output_file))
        else:
            print(f"Le fichier {file} est vide.")