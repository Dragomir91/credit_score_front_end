import pandas as pd
import streamlit as st
import requests
from streamlit_shap import st_shap
import numpy as np
import plotly.express as px
import shap


def liste_id(model_uri, data):
    headers = {"Content-Type": "application/json"}

    data_json = {}
    response = requests.request(
        method='GET', headers=headers, url=model_uri, json=data_json)

    if response.status_code != 200:
        raise Exception(
            "Request failed with status {}, {}".format(response.status_code, response.text))

    return response.json()
    

def request_prediction(model_uri, data):
    
    headers = {"Content-Type": "application/json"}

    data_json = {'id':data[0],
                 'decision_id': data[1],
                 'proba':data[2]}
    response = requests.request(
        method='POST', headers=headers, url=model_uri, json=data_json)

    if response.status_code != 200:
        raise Exception(
            "Request failed with status {}, {}".format(response.status_code, response.text))

    return response.json()
    

def request_explain_shap(model_uri, data2):
    
    headers = {"Content-Type": "application/json"}

    data_json = {'id':data2[0],
                 'decision_id': data2[1],
                 'proba':data2[2]}
    response = requests.request(
        method='GET', headers=headers, url=model_uri, json=data_json)

    if response.status_code != 200:
        raise Exception(
            "Request failed with status {}, {}".format(response.status_code, response.text))

    return response.json()
    

def request_prediction_shap(model_uri, data3):
    
    headers = {"Content-Type": "application/json"}
    
    data_json = {'id':data3[0],
                 'decision_id': data3[1],
                 'proba':data3[2]}
    response = requests.request(
        method='GET', headers=headers, url=model_uri, json=data_json)

    if response.status_code != 200:
        raise Exception(
            "Request failed with status {}, {}".format(response.status_code, response.text))

    return response.json()
    

def request_cout_metier(model_uri, data4):
    
    headers = {"Content-Type": "application/json"}

    data_json = {'id':data4[0],
                 'decision_id': data4[1],
                 'proba':data4[2]}
    response = requests.request(
        method='GET', headers=headers, url=model_uri, json=data_json)

    if response.status_code != 200:
        raise Exception(
            "Request failed with status {}, {}".format(response.status_code, response.text))

    return response.json()

def main():

    
    API_URI = 'https://credit-score-backend.onrender.com/predict'
    API_URI2 = 'https://credit-score-backend.onrender.com/predict/feature_id'
    API_URI3 = 'https://credit-score-backend.onrender.com/predict/explain'
    API_URI4 = 'https://credit-score-backend.onrender.com/predict/graph_id'
    API_URI5 = 'https://credit-score-backend.onrender.com/id_client'
 
    st.title('Information client')

    data_client = liste_id(API_URI5, [0])
        #st.write('liste des clients disponibles',data_client['id_client'])

    df = {
        "list_id": data_client["list_id"],
         }

    id = st.multiselect('choisir un seul id compris entre 100001 et 101356',df["list_id"])
    st.title('Scores clients')
    st.subheader('Decison credit')

    # Affiche le score de probabilité pour l'accord de l'emprunt bancaire (le score doit être supérieur à 0.50 pour l'accord du crédit)
    try :
        predict_btn = st.checkbox('Décision sur la demande d emprunt')
        if predict_btn:
            data = [id[0], 0,0]
            pred = None

            pred = request_prediction(API_URI, data)

            df = {
            "id_client":[pred["id"]],
            "decision":[pred["decision_id"]],
            "proba":[round(pred["proba"],2)]
            }
            
            st.write('',pd.DataFrame(df))
            if df['decision'][0] == 0:
                st.subheader('le crédit peut être accordé')

            else :
                st.subheader('le crédit est refusé')
            
    ##############################################Information personnel sur le client demandant le crédit##############################################

        info_btn = st.checkbox('Informations sur cet id')
        if info_btn:
            data2 = [id[0], 0,0]
            data_shap = request_explain_shap(API_URI2, data2) 
            df_json = pd.read_json(data_shap)
            
            st.write(pd.DataFrame(df_json.values,columns=df_json.columns, index = [id]))
                
                    
    ##############################################SHAP_VALUE##############################################
        
        # La méthode shap.Explanation permet d'apporter des explications sur les variables contribuant à un score de probabilité positif et celles affaiblisant ce score. 
        shap_btn = st.checkbox('Détail sur le score attribué au client')
       
        if shap_btn:

    # Affichage des shap value permettant d'expliquer au client le choix d'accord ou de refus de l'emprunt
                data3 = [id[0],0,0]
                data_shap = request_prediction_shap(API_URI3, data3)                            
                shap_values = shap.Explanation(values=np.array(data_shap["values"]),
                base_values=data_shap["base_values"],
                data = data_shap["data"],
                feature_names=data_shap["feature_names"])
                shap_values.base_values = 1 - shap_values.base_values 
                shap_values.values = -shap_values.values
                st_shap(shap.plots.waterfall(shap_values,max_display=10),height=500, width=1100)
                st.markdown("Pour interpréter les résultats du graphique ci-dessus")
                st.markdown("- La flèche de couleur bleue pénalise le score client")
                st.markdown("- La flèche de couleur rouge améliore le score client")


                btn = st.button('Comparaison des données clients sur l ensemble des clients')
    # Affichage graphique 
                if btn:
                                
                        data4 = [id[0], 0,0]
                        data = request_explain_shap(API_URI4, data4) 
                        df = pd.read_json(data)
                        
                        EXT_SOURCE2 = df.loc[df.SK_ID_CURR == id[0],"EXT_SOURCE_2"]
                        EXT_SOURCE2_MEAN = df.loc[:,"EXT_SOURCE_2"].mean()
                        AMT_ANNUITY = df.loc[df.SK_ID_CURR == id[0],"AMT_ANNUITY"]
                        AMT_ANNUITY_MEAN = df.loc[:,"AMT_ANNUITY"].mean()
                        EXT_SOURCE2_ACCEPT = df.loc[df['Y_PRED_PV_ID'] == 0,'EXT_SOURCE_2_PV_ID'].mean()
                        EXT_SOURCE2_REFUSE = df.loc[df['Y_PRED_PV_ID'] == 1,'EXT_SOURCE_2_PV_ID'].mean()
                        AMT_ANNUITY_ACCEPT = df.loc[df['Y_PRED_PV_ID'] == 0,'AMT_ANNUITY_PV_ID'].mean()
                        AMT_ANNUITY_REFUSE = df.loc[df['Y_PRED_PV_ID'] == 1,'AMT_ANNUITY_PV_ID'].mean()
                    
# Visualisation des données personnels du demandeur d'emprunt
                        chart_data = pd.DataFrame({
                                        'ID' : ['ID_EXT_SOURCE_2','EXT_SOURCE2_MEAN','EXT_SOURCE2_ACCEPT','EXT_SOURCE2_REFUSE'],
                                        'RESULTAT' : [EXT_SOURCE2.values[0], EXT_SOURCE2_MEAN,EXT_SOURCE2_ACCEPT,EXT_SOURCE2_REFUSE],
                                        'COLOR' : [2,3,4,5]})
                        
                        chart_data2 = pd.DataFrame({
                                        'ID' : ['ID_AMT_ANNUITY','AMT_ANNUITY','AMT_ANNUITY_ACCEPT','AMT_ANNUITY_REFUSE'],
                                        'RESULTAT' : [ AMT_ANNUITY.values[0], AMT_ANNUITY_MEAN,AMT_ANNUITY_ACCEPT,AMT_ANNUITY_REFUSE],
                                        'COLOR' : [2,3,4,5]})
                        

                        fig = px.bar(
                                chart_data,
                                x="ID",
                                y="RESULTAT",
                                color='ID',
                                hover_name="ID",
                                )
                        
                        fig2 = px.bar(
                                chart_data2,
                                x="ID",
                                y="RESULTAT",
                                color = 'ID',
                                hover_name="ID")                       
                        tab1, tab2 = st.tabs(["EXT_SOURCE2", "AMT_ANNUITY"])
                    
                        with tab1:
                            # Use the Streamlit theme.
                            # This is the default. So you can also omit the theme argument.
                            st.plotly_chart(fig)
                            
                        with tab2:
                            # Use the native Plotly theme.
                            st.plotly_chart(fig2)


    except: 'un seul id doit être séléctionner'

if __name__ == '__main__':
    main()
