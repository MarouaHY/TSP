import streamlit as st 
from streamlit import logger as _logger
from streamlit import config as _config
from streamlit.deprecation_util import deprecate_func_name as _deprecate_func_name
from streamlit.version import STREAMLIT_VERSION_STRING as _STREAMLIT_VERSION_STRING
########################################################################################
import streamlit as st

import pandas as pd

import plotly.graph_objs as go

import numpy as np

 

def main():

    st.title("Traveling Salesman Problem Solver")

 

    # Nombre de sommets

    num_nodes = st.number_input("Nombre de sommets :", min_value=1, step=1)

 

    # Entrée des distances entre les sommets

    st.subheader("Entrée des distances entre les sommets")

    distances = []

    for i in range(num_nodes):

        row = []

        for j in range(num_nodes):

            if i == j:

                row.append(0)

            elif j > i:

                distance = st.number_input(f"Distance entre le sommet {i+1} et le sommet {j+1} :", value=0.0, step=0.1)

                row.append(distance)

            else:

                row.append(distances[j][i])

        distances.append(row)

 

    # Afficher les distances comme une matrice d'adjacence

    df = pd.DataFrame(distances, columns=[f"Sommet {i+1}" for i in range(num_nodes)], index=[f"Sommet {i+1}" for i in range(num_nodes)])

    st.subheader("Matrice d'adjacence des distances")

    st.write(df)

 

    # Dessiner le graphe des sommets avec les distances associées

    draw_3d_graph(distances)

 

    # Calcul de la tournée optimale avec l'algorithme du plus proche voisin

    tour = nearest_neighbor(distances)

 

    # Calcul de la distance totale de la tournée

    total_distance = sum(distances[tour[i]][tour[i+1]] for i in range(num_nodes-1)) + distances[tour[-1]][tour[0]]

 

    # Affichage de la tournée optimale

    st.subheader("Tournée optimale (Algorithme du plus proche voisin)")

    st.write(f"Chemin : {tour}")

    st.write(f"Distance totale : {total_distance}")

 

    # Dessiner le graphe de la tournée optimale

    draw_optimal_tour_graph(distances, tour)

 

def draw_3d_graph(distances):

    num_nodes = len(distances)

 

    # Création des coordonnées des sommets en 3D

    nodes_coords = np.random.rand(num_nodes, 3)

 

    # Création des lignes entre les sommets avec les distances associées

    lines = []

    annotations = []

    for i in range(num_nodes):

        for j in range(num_nodes):

            if i != j:

                lines.append(go.Scatter3d(

                    x=[nodes_coords[i, 0], nodes_coords[j, 0]],

                    y=[nodes_coords[i, 1], nodes_coords[j, 1]],

                    z=[nodes_coords[i, 2], nodes_coords[j, 2]],

                    mode='lines',

                    line=dict(color='blue', width=2),

                    hoverinfo='none'

                ))

                annotations.append(go.Scatter3d(

                    x=[(nodes_coords[i, 0] + nodes_coords[j, 0]) / 2],

                    y=[(nodes_coords[i, 1] + nodes_coords[j, 1]) / 2],

                    z=[(nodes_coords[i, 2] + nodes_coords[j, 2]) / 2],

                    mode='text',

                    text=f"{distances[i][j]}",

                    textposition='middle center',

                    hoverinfo='none'

                ))

 

    fig = go.Figure(data=lines + annotations)

 

    fig.update_layout(

        title="Graphe 3D des sommets avec distances associées",

        scene=dict(

            xaxis_title="X",

            yaxis_title="Y",

            zaxis_title="Z"

        )

    )

 

    st.plotly_chart(fig)

 

def draw_optimal_tour_graph(distances, tour):

    num_nodes = len(distances)

 

    # Création des coordonnées des sommets en 3D

    nodes_coords = np.random.rand(num_nodes, 3)

 

    # Création des lignes entre les sommets de la tournée optimale

    lines = []

    for i in range(len(tour) - 1):

        lines.append(go.Scatter3d(

            x=[nodes_coords[tour[i], 0], nodes_coords[tour[i+1], 0]],

            y=[nodes_coords[tour[i], 1], nodes_coords[tour[i+1], 1]],

            z=[nodes_coords[tour[i], 2], nodes_coords[tour[i+1], 2]],

            mode='lines',

            line=dict(color='red', width=4),

            hoverinfo='none'

        ))

 

    # Lier le dernier sommet au premier pour fermer la boucle

    lines.append(go.Scatter3d(

        x=[nodes_coords[tour[-1], 0], nodes_coords[tour[0], 0]],

        y=[nodes_coords[tour[-1], 1], nodes_coords[tour[0], 1]],

        z=[nodes_coords[tour[-1], 2], nodes_coords[tour[0], 2]],

        mode='lines',

        line=dict(color='red', width=4),

        hoverinfo='none'

    ))

 

    fig = go.Figure(data=lines)

 

    fig.update_layout(

        title="Graphe 3D de la tournée optimale",

        scene=dict(

            xaxis_title="X",

            yaxis_title="Y",

            zaxis_title="Z"

        )

    )

 

    st.plotly_chart(fig)

 

def nearest_neighbor(distances):

    num_nodes = len(distances)

    visited = [False] * num_nodes

    tour = [0]  # Commencer par le premier sommet

 

    current_node = 0

    visited[current_node] = True

 

    while len(tour) < num_nodes:

        nearest_dist = float('inf')

        nearest_node = None

 

        for next_node in range(num_nodes):

            if not visited[next_node]:

                dist = distances[current_node][next_node]

                if dist < nearest_dist:

                    nearest_dist = dist

                    nearest_node = next_node

 

        tour.append(nearest_node)

        visited[nearest_node] = True

        current_node = nearest_node

 

    # Ajouter le premier sommet à la fin du chemin pour revenir au point de départ

    tour.append(tour[0])

 

    return tour

 

if __name__ == "__main__":

    main()
    
    
    
    
    
    #python -m streamlit run TSP_APP.py