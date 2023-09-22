import streamlit as st
import pickle as pkl
import numpy as np
import locale
import time
import datetime
st.set_page_config(
   page_title="Car Price Prediction",
   page_icon="🚗",
   layout="wide",
   initial_sidebar_state="expanded",
)
model = pkl.load(open('G:\Ashish Yadav\Backup Google Drive\Documents-Lecture\Github\ML-Mini-Project\data\\trained_models\\rfr_model.pkl','rb'))

df = pkl.load(open('G:\Ashish Yadav\Backup Google Drive\Documents-Lecture\Github\ML-Mini-Project\config\dataframe.pkl','rb'))

mapping = pkl.load(open('G:\Ashish Yadav\Backup Google Drive\Documents-Lecture\Github\ML-Mini-Project\config\car_model_mapping.pkl','rb'))

# ['Make','Model','Year','Kilometer','Fuel Type','Transmission','Owner','Engine', 'Length','Seating Capacity', 'Fuel Tank Capacity','Price']
locale.setlocale(locale.LC_ALL, 'en_IN')
st.title('Car Price Prediction')
company = st.selectbox('Manufacturer',sorted(mapping.keys()))
car_model = st.selectbox('Model',sorted(mapping[company]))
year = st.number_input('Purchase Year',min_value=1930,max_value=datetime.date.today().year,value=datetime.date.today().year,step=1)
km = st.number_input('Kilometers Driven',step=1000)
fuel_type = st.selectbox('Fuel Type',df['Fuel Type'].unique())
transmission = st.selectbox('Transmission Type',df['Transmission'].unique())
ownership = st.selectbox('Ownership Type',df['Owner'].unique())
engine_size = st.number_input('Engine Size',step=50)
length = st.number_input('Length in meters',step=0.5)*1000
st.write(length)
seat_capacity = st.number_input('Seating Capacity',step=1)
fuel_capacity = st.number_input('Fuel Tank Capacity',step=5)

if st.button('Predict Price'):
    with st.spinner('Thinking'):
        time.sleep(5)
        
    query = np.array([[company,car_model,year,km,fuel_type,transmission,ownership,engine_size,length,seat_capacity,fuel_capacity]])
    prediction = model.predict(query)[0]
    lower_bound = prediction - ((prediction*8)/100)
    upper_bound = prediction + ((prediction*8)/100)
    f1 = locale.currency(lower_bound, grouping=True)
    f2 = locale.currency(upper_bound, grouping=True)
    avg = locale.currency(prediction, grouping=True)
    st.markdown(f"Average: {str(avg)}")    
    st.header(f1+" - "+f2)