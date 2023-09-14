import pandas as pd
import streamlit as st
import requests


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
    

    data_json = {
                 'shap_values':0
                 }
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
    API_URI2 = 'https://credit-score-backend.onrender.com/predict/shap_id'
    API_URI3 = 'https://credit-score-backend.onrender.com/predict/explain'
    API_URI4 = 'https://credit-score-backend.onrender.com/predict/cout_metier'
    #API_URI = 'http://127.0.0.1:8000/predict'
    #API_URI2 = 'http://127.0.0.1:8000/predict/shap_id'
    #API_URI3 = 'http://127.0.0.1:8000/predict/explain'
    #API_URI4 = 'http://127.0.0.1:8000/predict/cout_metier'

    st.title('Scores clients')
    st.subheader('Decison credit')

    id = st.number_input('saisir id client', value=100002., step=1.)

    predict_btn = st.button('Predire')
    if predict_btn:
        data = [id, 0,0]
        pred = None

        pred = request_prediction(API_URI, data)

        df = {
        "id_client":[pred["id"]],
        "decision":[pred["decision_id"]],
        "proba":[round(pred["proba"],2)]
        }

        st.write('liste des clients disponibles',pd.DataFrame(df))
         
        #st.write('y_pred {}'.format(pred))
#######################################################################""""


    shap_btn = st.button('informations sur cet id')
    if shap_btn:
        data2 = [id, 0,0]
        data_shap = request_explain_shap(API_URI2, data2) 
        df_json = pd.read_json(data_shap)
        
        st.write(pd.DataFrame(df_json.values,columns=df_json.columns, index = [str(id)]))
            
                 
##############################################SHAP_VALUE###################################################
    shap_btn = st.button('shap_value')
    with st.form("my_form"):
        if shap_btn:
            data3 = [[id],[0],[0]]
            data_shap = request_prediction_shap(API_URI3, data3)        
            try :
                df = pd.DataFrame(data_shap)
                st.write('df index',df.loc[df.ID == id,:].iloc[:,1:])
                df2 = df.loc[df.ID == id,:].iloc[:,1:]
                st.bar_chart(df2.iloc[0,:])
                #st.write(data_shap['shap_values'])  
                #st.write('liste disponibles',pd.DataFrame([data_shap['shap_values']],index=data_shap['id'], columns=data_shap['top_features']))
                submitted = st.form_submit_button("Submit")
  

            except:
                st.write('error')
##############################################COUT_METIER#####################################################



    shap_btn = st.button('coût du portefeuille clients')
    if shap_btn:
        data4 = [id, 0,0]
        data = request_explain_shap(API_URI4, data4) 
        
        df =  {"gain" : [data["gain"] ],
              "perte" : [data["perte"]],
              "roc_auc_0" : [data["roc_auc_0"]],
              "roc_auc_1" : [data["roc_auc_1"]],
              "threshold" : [data["threshold"]]}
        st.write(pd.DataFrame(df))

if __name__ == '__main__':
    main()
