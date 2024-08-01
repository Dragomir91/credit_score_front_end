import pandas as pd
import streamlit as st
import requests

# Fonction pour envoyer une requête à l'API pour obtenir les informations d'un client spécifique
def request_prediction(model_uri, data):
    headers = {"Content-Type": "application/json"}  # Définir le type de contenu de la requête comme JSON
    print('id :', data)  # Afficher l'identifiant du client pour le débogage
    data_json = {"id_client": data[0],  # Construire le corps de la requête avec l'ID du client
                 "infos_id": data[1]}  # et les informations sélectionnées
    
    print('data[1] dans function : ', data[1])  # Afficher les informations sélectionnées pour le débogage
    # Envoyer la requête GET à l'API avec les en-têtes et les données JSON
    response = requests.request(
        method='GET', headers=headers, url=model_uri, json=data_json)

    # Vérifier si la requête a échoué et lever une exception si c'est le cas
    if response.status_code != 200:
        raise Exception(
            "Request failed with status {}, {}".format(response.status_code, response.text))

    return response.json()  # Retourner la réponse de l'API en format JSON

# Fonction pour envoyer une requête à l'API pour obtenir les informations de plusieurs clients
def request_prediction2(model_uri, data):
    headers = {"Content-Type": "application/json"}  # Définir le type de contenu de la requête comme JSON
    info_list = []  # Initialiser une liste pour stocker les informations sélectionnées
    info_list.append('SK_ID_CURR')  # Ajouter l'identifiant du client à la liste des informations
    _ = [info_list.append(col) for col in data[1]]  # Ajouter les informations sélectionnées par l'utilisateur
    data_json = {"id_client": data[0],  # Construire le corps de la requête avec l'ID du client
                 "infos_id": info_list}  # et la liste des informations à récupérer
    # Envoyer la requête GET à l'API avec les en-têtes et les données JSON
    response = requests.request(method='GET', headers=headers, url=model_uri, json=data_json)

    # Vérifier si la requête a échoué et lever une exception si c'est le cas
    if response.status_code != 200:
        raise Exception(
            "Request failed with status {}, {}".format(response.status_code, response.text))

    return response.json()  # Retourner la réponse de l'API en format JSON

# Fonction principale de l'application Streamlit
def main():
    # URLs des API pour récupérer les informations d'un client ou de plusieurs clients
    API_URI = 'https://credit-score-backend.onrender.com/info_client'
    API_URI2 = 'https://credit-score-backend.onrender.com/info_clients/id_all'

    st.title('Information client')  # Titre de l'application
    # st.subheader('Number of pickups by hour')  # Sous-titre (commenté, donc non utilisé)

    # Interface pour sélectionner les informations du client à récupérer
    options = st.multiselect(
        'Selectionner les informations client',
        ['CODE_GENDER', 'FLAG_OWN_CAR', 'FLAG_OWN_REALTY', 'CNT_CHILDREN', 'AMT_INCOME_TOTAL', 'AMT_CREDIT',
         'AMT_ANNUITY', 'AMT_GOODS_PRICE', 'REGION_POPULATION_RELATIVE', 'DAYS_BIRTH', 'DAYS_EMPLOYED',
         'DAYS_REGISTRATION', 'DAYS_ID_PUBLISH', 'OWN_CAR_AGE', 'FLAG_MOBIL', 'FLAG_EMP_PHONE', 'FLAG_WORK_PHONE',
         'FLAG_CONT_MOBILE', 'FLAG_PHONE', 'FLAG_EMAIL', 'CNT_FAM_MEMBERS', 'REGION_RATING_CLIENT',
         'REGION_RATING_CLIENT_W_CITY', 'HOUR_APPR_PROCESS_START', 'REG_REGION_NOT_LIVE_REGION',
         'REG_REGION_NOT_WORK_REGION', 'LIVE_REGION_NOT_WORK_REGION', 'REG_CITY_NOT_LIVE_CITY',
         'REG_CITY_NOT_WORK_CITY', 'LIVE_CITY_NOT_WORK_CITY', 'EXT_SOURCE_1', 'EXT_SOURCE_2', 'EXT_SOURCE_3',
         'APARTMENTS_AVG', 'BASEMENTAREA_AVG', 'YEARS_BEGINEXPLUATATION_AVG', 'YEARS_BUILD_AVG', 'COMMONAREA_AVG',
         'ELEVATORS_AVG'])

    print(options)  # Afficher les options sélectionnées pour le débogage

    # Interface pour entrer l'ID du client
    id = st.number_input('saisir id client', value=100001., step=1.)
    st.write('id = ', id)  # Afficher l'ID du client saisi
    predict_btn = st.checkbox('information sur le client')  # Case à cocher pour déclencher la requête d'informations sur un client
    try:
        if predict_btn:
            data_ = [id, options]  # Créer la liste des données à envoyer à l'API
            info_client = request_prediction(API_URI, data_)  # Appeler la fonction pour récupérer les informations du client
            df = pd.read_json(info_client)  # Convertir la réponse JSON en DataFrame pandas
            # Afficher les informations du client dans un tableau
            st.write('informations client', pd.DataFrame(df.values, index=[id], columns=options))
    except:
        st.write('id pas de liste')  # Afficher un message d'erreur si l'ID du client est invalide

    # Bouton pour récupérer les informations de plusieurs clients
    predict_btn = st.button('information sur plusieurs clients')

    if predict_btn:
        data_ = [id, options]  # Créer la liste des données à envoyer à l'API
        info_client = request_prediction2(API_URI2, data_)  # Appeler la fonction pour récupérer les informations de plusieurs clients
        df = pd.read_json(info_client)  # Convertir la réponse JSON en DataFrame pandas
        # Afficher les informations des clients dans un tableau, en omettant la première colonne (SK_ID_CURR)
        st.write('informations client', pd.DataFrame(df.values, index=df.SK_ID_CURR, columns=df.columns).iloc[:, 1:])
    else:
        st.write('pas de liste')  # Afficher un message si aucun client n'a été sélectionné

if __name__ == '__main__':
    main()  # Exécuter l'application Streamlit
