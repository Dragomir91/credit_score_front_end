import pandas as pd
import streamlit as st
import requests


def request_prediction(model_uri, data):
    headers = {"Content-Type": "application/json"}
    print('id :', data)
    data_json = {"id_client": data[0],
                 "infos_id" : data[1]}
    
    print('data[1] dans function : ',data[1])
    response = requests.request(
        method='GET', headers=headers, url=model_uri, json=data_json)

    if response.status_code != 200:
        raise Exception(
            "Request failed with status {}, {}".format(response.status_code, response.text))

    return response.json()


def main():
    #API_URI = 'https://credit-score-backend.onrender.com/info_client/id'
    API_URI = 'http://127.0.0.1:8000/info_client/id'

    st.title('Information client')
    #st.subheader('Number of pickups by hour')

    
    options = st.multiselect(
        'Selectionner les informations client',
        ['SK_ID_CURR','TARGET','CODE_GENDER','FLAG_OWN_CAR','FLAG_OWN_REALTY','CNT_CHILDREN','AMT_INCOME_TOTAL','AMT_CREDIT','AMT_ANNUITY','AMT_GOODS_PRICE','REGION_POPULATION_RELATIVE',
         'DAYS_BIRTH','DAYS_EMPLOYED','DAYS_REGISTRATION','DAYS_ID_PUBLISH','OWN_CAR_AGE','FLAG_MOBIL','FLAG_EMP_PHONE','FLAG_WORK_PHONE','FLAG_CONT_MOBILE','FLAG_PHONE','FLAG_EMAIL',
         'CNT_FAM_MEMBERS','REGION_RATING_CLIENT','REGION_RATING_CLIENT_W_CITY','HOUR_APPR_PROCESS_START','REG_REGION_NOT_LIVE_REGION','REG_REGION_NOT_WORK_REGION','LIVE_REGION_NOT_WORK_REGION',
         'REG_CITY_NOT_LIVE_CITY','REG_CITY_NOT_WORK_CITY','LIVE_CITY_NOT_WORK_CITY','EXT_SOURCE_1','EXT_SOURCE_2','EXT_SOURCE_3','APARTMENTS_AVG','BASEMENTAREA_AVG','YEARS_BEGINEXPLUATATION_AVG',
         'YEARS_BUILD_AVG','COMMONAREA_AVG','ELEVATORS_AVG'])
    
    print(options)

    id = st.number_input('saisir id client', value=100002., step=1.)
    st.write('id = ', id)
    predict_btn = st.button('list des clients')

    if predict_btn:
        data_ = [id,options]
        info_client = request_prediction(API_URI, data_)
        df = pd.read_json(info_client)
        st.write('informations client',pd.DataFrame(df.values,index =['100002'],columns=options))
    else : st.write('pas de liste')


if __name__ == '__main__':
    main()
