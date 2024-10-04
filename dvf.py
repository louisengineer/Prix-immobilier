import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Charger les données
@st.cache_data
def load_data():
    data_path = "dvf.csv"  # Mets ici le bon chemin vers ton fichier CSV
    DVF = pd.read_csv(data_path, encoding="UTF-8")
    return DVF

# Charger les données
df = load_data()

# Interface utilisateur avec Streamlit
st.title("Évolution du Prix au m² en France")

# Sélectionner la commune
communes = df['nom_commune'].unique()
commune_selectionnee = st.selectbox("Sélectionnez une commune :", communes)

# Filtrer les données pour la commune sélectionnée
data_commune = df[df['nom_commune'] == commune_selectionnee]

# Vérifier s'il y a des données
if not data_commune.empty:
    st.subheader(f"Évolution du prix au m² pour : {commune_selectionnee}")
    
    # Séparer les données pour Appartements et Maisons
    data_appartement = data_commune[data_commune['type'] == 'Appartement']
    data_maison = data_commune[data_commune['type'] == 'Maison']

    # Créer deux colonnes pour l'affichage
    col1, col2 = st.columns(2)

    # Graphique interactif pour les Appartements
    with col1:
        if not data_appartement.empty:
            # Vérification de l'existence de données pour éviter l'erreur
            if len(data_appartement) > 0:
                st.metric(label="Appartements - Prix au m² moyen", 
                          value=f"{data_appartement['prixm2'].iloc[-1]:,.0f}€/m²",
                          delta=f"{data_appartement['prixm2'].pct_change().iloc[-1] * 100:.2f}% depuis 12 mois")

                # Création de la courbe avec zone remplie et points (markers)
                fig_appartement = px.area(data_appartement, x='annee', y='prixm2',
                                          labels={'annee': 'Année', 'prixm2': 'Prix au m² (€)'},
                                          title='Appartements - Prix au m²',
                                          markers=True,
                                          line_shape='spline')

                # Ajout des informations de survol personnalisées
                fig_appartement.update_traces(hovertemplate='<b>%{x}</b>: %{y:,.0f}€/m²')

                # Mettre à jour les ticks de l'axe des années pour afficher des années pleines
                fig_appartement.update_layout(xaxis=dict(tickmode='linear', tick0=data_appartement['annee'].min(), dtick=1),
                                              yaxis=dict(range=[data_appartement['prixm2'].min() * 0.95, data_appartement['prixm2'].max() * 1.05]))

                # Afficher le graphique
                st.plotly_chart(fig_appartement, config={'modeBarButtonsToRemove': ['zoom', 'pan','lasso2d','select','zoomIn','zoomOut', 'autoScale'],
                                                         'displaylogo': False})
        else:
            st.write("Aucune donnée pour les appartements dans cette commune.")

    # Graphique interactif pour les Maisons
    with col2:
        if not data_maison.empty:
            # Vérification de l'existence de données pour éviter l'erreur
            if len(data_maison) > 0:
                st.metric(label="Maisons - Prix au m² moyen", 
                          value=f"{data_maison['prixm2'].iloc[-1]:,.0f}€/m²",
                          delta=f"{data_maison['prixm2'].pct_change().iloc[-1] * 100:.2f}% depuis 12 mois")

                # Création de la courbe avec zone remplie et points (markers)
                fig_maison = px.area(data_maison, x='annee', y='prixm2',
                                     labels={'annee': 'Année', 'prixm2': 'Prix au m² (€)'},
                                     title='Maisons - Prix au m²',
                                     markers=True,
                                     line_shape='spline')

                # Ajout des informations de survol personnalisées
                fig_maison.update_traces(hovertemplate='<b>%{x}</b>, %{y:,.0f}€/m²')

                # Mettre à jour les ticks de l'axe des années pour afficher des années pleines
                fig_maison.update_layout(xaxis=dict(tickmode='linear', tick0=data_maison['annee'].min(), dtick=1),
                                         yaxis=dict(range=[data_maison['prixm2'].min() * 0.95, data_maison['prixm2'].max() * 1.05]))

                # Afficher le graphique
                st.plotly_chart(fig_maison,config={'modeBarButtonsToRemove': ['zoom', 'pan','lasso2d','select','zoomIn','zoomOut', 'autoScale'],
                                                         'displaylogo': False})
        else:
            st.write("Aucune donnée pour les maisons dans cette commune.")

else:
    st.write("Aucune donnée disponible pour cette commune.")
