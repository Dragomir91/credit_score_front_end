import pandas as pd
import streamlit as st
import requests


def request_prediction(model_uri, data):
    headers = {"Content-Type": "application/json"}

    data_json = {'id_client': data,
                 'information_client' : [0]}
    response = requests.request(
        method='GET', headers=headers, url=model_uri, json=data_json)

    if response.status_code != 200:
        raise Exception(
            "Request failed with status {}, {}".format(response.status_code, response.text))

    return response.json()


def main():
    API_URI = 'http://127.0.0.1:8000/id_client'



    st.title('Information client')

 

    predict_btn = st.button('list des clients')

    if predict_btn:

        data_client = request_prediction(API_URI, [0])
        #st.write('liste des clients disponibles',data_client['id_client'])

        
        st.write('liste des clients disponibles',pd.Series(data_client['id_client']))
        st.write('information client',pd.Series(data_client['information_client']))

    else : st.write('pas de liste')

if __name__ == '__main__':
    main()
