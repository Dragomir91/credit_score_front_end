import pandas as pd
import streamlit as st
import requests


def request_prediction(model_uri, data):
    headers = {"Content-Type": "application/json"}
    print('id :', data)
    data_json = {
        "id_client": data,
        "age" : 0,
        "revenu_annuel":0,
        "days_employed": 0,
        "credit" : 0,
        "good_price": 0,
        "annuity": 0}
    response = requests.request(
        method='POST', headers=headers, url=model_uri, json=data_json)

    if response.status_code != 200:
        raise Exception(
            "Request failed with status {}, {}".format(response.status_code, response.text))

    return response.json()


def main():
    API_URI = 'https://credit-score-backend.onrender.com/info_client/id'


    st.title('Information client')
    #st.subheader('Number of pickups by hour')

    
    id = st.number_input('saisir id client', value=100002., step=1.)
    st.write('id = ', id)
    predict_btn = st.button('list des clients')

    if predict_btn:
    
        info_client = request_prediction(API_URI, id)
        df = {
        "id_client":[info_client["id_client"]],
        "age":[-info_client["age"]/365],
        "revenu_annuel":[info_client["revenu_annuel"]],
        "days_employed":[info_client["days_employed"]],
        "credit":[info_client["credit"]],
        "good_price":[info_client["good_price"]],
        "annuity":[info_client["annuity"]]
        }
        st.write('informations client',pd.DataFrame(df))
    else : st.write('pas de liste')


if __name__ == '__main__':
    main()
