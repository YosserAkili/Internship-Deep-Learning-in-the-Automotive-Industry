# -*- coding: utf-8 -*-
"""

@author: Yosser
"""
import pickle
import json
import numpy as np
import pandas as pd
import streamlit as st
import tensorflow as tf
from PIL import Image
from sklearn.preprocessing import MinMaxScaler
from tensorflow import keras

# Load the saved model
loaded_model = tf.keras.models.load_model("C:\\Users\\Yosr\\DLCars\\deploy_dl\\my_classifier.h5")


# Define a function for making a prediction on new data

def make_prediction(new_data):
    df2=pd.read_excel('data_cars2.xlsx')
    df2=df2.drop(['Car','Unnamed: 0','Comfort','Performance','Quality','Value','Reliability','Styling','integrated_garage_door_opener','Drivetrain','led_headlights','Model','max_miles_warrantly'],axis=1)
    # Convert input data to Pandas DataFrame
    new_data = pd.DataFrame(new_data, columns=['Price','max_seating_capacity','alloy_wheels','nb_doors','Engine','max_years_warrantly','max_years_powertrain','max_miles_powertrain','trunk_cap_categ','Year','Brand'])
    # Applying the mapping to the 'alloy_wheels' column

    


    new_data = pd.DataFrame(new_data, columns=['Price','max_seating_capacity','alloy_wheels','nb_doors','Engine','max_years_warrantly','max_years_powertrain','max_miles_powertrain','trunk_cap_categ','Year','Brand'])
    df2=df2.append(new_data, ignore_index=True)
    df2=df2.fillna(0)

    df2=df2.drop(['Target','Unnamed: 0.1'], axis=1)
    print(df2)
     # Mapping for transforming values
    mapping = {'Not Available': 0, 'Available': 1}


# Applying the mapping to the 'alloy_wheels' column
    
    df2['alloy_wheels'] = df2['alloy_wheels'].map(mapping)


# Mapping for transforming values
    mapping = {
    'Very Small': 0,
    'Small': 1,
    'Moderate': 2,
    'Spacious': 3,
    'Very Spacious': 4
              }

# Appliquez la correspondance à la colonne 'trunk_cap_categ'
    df2['trunk_cap_categ'] = df2['trunk_cap_categ'].replace(mapping)


    categorical_features =[feature for feature in df2.columns if df2[feature].dtypes == 'object']

    df2 = pd.get_dummies(df2, columns=categorical_features,drop_first=True)
    print(df2)
# Sélectionner les caractéristiques numériques
    numeric_features = ['Price', 'max_seating_capacity', 'max_years_warrantly', 'max_years_powertrain', 'max_miles_powertrain', 'trunk_cap_categ', 'Year','nb_doors']

# Créer un DataFrame contenant uniquement les caractéristiques numériques


    numeric_data = df2[numeric_features]
# Initialiser le StandardScaler
    scaler = MinMaxScaler()

# Appliquer le Standard Scaling aux caractéristiques numériques
    scaled_data = scaler.fit_transform(numeric_data)

# Remplacer les caractéristiques numériques dans le DataFrame original par les données mises à l'échelle
    df2[numeric_features] = scaled_data
    print(df2)
    x=df2.iloc[-1]
    print(x)
    x = x.values.reshape(1, -1)
# Faire une prédiction sur les nouvelles données
    prediction = loaded_model.predict(x)
    return prediction[0]

# Define the Streamlit app
def app():
    


    #Ajouter des icônes pour les champs d'entrée de données
    col1, col2, col3 = st.columns(3)
    with col1:

       #rating = st.text_input('Note de la voiture (sur 5)')
       brand = ['Acura', 'Alfa', 'Audi', 'BMW', 'Buick', 'Cadillac', 'Chevrolet',
       'Chrysler', 'Dodge', 'Eagle', 'FIAT', 'Ford', 'Freightliner',
       'Genesis', 'GMC', 'Honda', 'HUMMER', 'Hyundai', 'INFINITI',
       'Isuzu', 'Jeep', 'Kia', 'Land', 'Lincoln', 'Lotus', 'MAZDA',
       'Mercedes-Benz', 'Mercury', 'MINI', 'Mitsubishi', 'Nissan',
       'Oldsmobile', 'Panoz', 'Plymouth', 'Polestar', 'Pontiac', 'Saab',
       'smart', 'Subaru', 'Suzuki', 'Toyota', 'Volkswagen']
       brand = st.selectbox('**Car Brand**', brand)


    with col2:

       #review_count = st.text_input('Nombre d\'avis sur la voiture')
       year = st.selectbox('**Car Manufacturing Year**', range(1992, 2025))


    with col3:

       price = st.number_input('**Car Price**', value=10000)

    # Ajouter des suggestions automatiques pour la marque et le modèle

    max_seating_capacity = st.selectbox('**Car Manufacturing Max Seating Capacity**', range(2, 11))

    alloy_wheels=['Available', 'Not Available']
    alloy_wheels = st.selectbox('**Car Alloy Wheels**', alloy_wheels)
       
    nb_doors = st.selectbox('**Car Number of Doors**', range(2, 6)) 

    engine=['V6', '4-Cyl', '5-Cyl', 'Dual', '6-Cyl', 'V8', 'V10', 'AC',
       '3-Cyl', 'V12', 'Electric', 'Voltec', '4-CYL', '4Cyl', 'Rotary',
       'H6', 'Hydrogen', 'H-Cell']
    engine = st.selectbox('**Car Engine**', engine) 

    max_years_warrantly = st.selectbox('**Car max_years_warrantly**', range(3, 8))  
    max_years_powertrain = st.selectbox('**Car max_years_powertrain**', range(3, 8)) 
    max_miles_powertrain = st.number_input('**Car  max_miles_powertrain**', value=50000)

    trunk_cap_categ=['Very Small', 'Small', 'Moderate', 'Spacious', 'Very Spacious']
    trunk_cap_categ=st.selectbox('**Car Trunk Capacity**',trunk_cap_categ)
 
    brand_models = {'Acura': ['MDX', 'RDX', 'TLX', 'ILX', 'Hybrid', 'RLX', 'TSX', 'TL', 'ZDX',
        'RL', 'RSX', 'CL', 'Integra', 'NSX', 'SLX', 'Legend', 'Vigor'],
     
 'Alfa': ['Giulia', 'Stelvio', 'Spider', '4C', '164'], 
 'Audi': ['A3', 'Q3', 'A5', 'Q7', 'A7', 'A4', 'Q5', 'Sportback', 'SQ5',
        'allroad', 'A6', 'Q8', 'TT', 'e-tron', 'S3', 'S4', 'S5', 'S6', '5',
        'S7', 'A8', 'S', 'SQ7', 'SQ8', 'S8', '3', '7', 'Sport', 'R8', '4',
        '(2005.5)', '6', 'Cabriolet', '90', '100', 'Quattro', '80'],
   
 'BMW': ['X5', 'X6', 'Series', 'X7', 'M4', 'X3', 'X4', 'M', 'iX', 'Z4',
        'X2', 'X1', 'i4', 'i3', 'M2', 'M5', 'M8', 'i8', 'M6', 'M3', 'B7',
        'Z3'], 
 'Buick': ['GX', 'Enclave', 'Envision', 'Encore', 'Sportback', 'TourX',
        'Cascada', 'LaCrosse', 'Verano', 'Regal', 'Lucerne', 'Rendezvous',
        'Terraza', 'Rainier', 'Avenue', 'Century', 'LeSabre', 'Riviera',
        'Skylark', 'Roadmaster'], 
 'Cadillac': ['XT4', 'CT5', 'XT5', 'CT4', 'XT6', 'Escalade', 'ESV', 'CT6',
        'CT6-V', 'CTS', 'CTS-V', 'ATS', 'ATS-V', 'XTS', 'SRX', 'ELR',
        'EXT', 'STS', 'DTS', 'XLR', 'DeVille', 'Seville', 'Eldorado',
        'Catera', 'Fleetwood', 'Special', 'Allante', 'Brougham'],
     
 'Chevrolet': ['Cab', 'Trailblazer', 'Camaro', 'Equinox', 'Malibu', 'Blazer',
        'Corvette', 'EV', 'EUV', 'Tahoe', 'Suburban', 'Traverse', 'Cargo',
        'Passenger', 'Spark', 'Trax', 'Impala', 'Sonic', 'Volt', 'Cruze',
        '3500HD', 'Express', 'SS', 'Limited', 'Sport', '1500', '2500',
        'Avalanche', 'Aveo', 'HHR', 'Cobalt', '(Classic)', 'Carlo', 'SSR',
        'Cavalier', 'Classic', 'Tracker', 'Prizm', 'Lumina', 'Metro',
        '(New)', '3500', 'Corsica', 'Beretta', 'G30', 'G20', 'G10', 'APV',
        'Caprice'], 
 'Chrysler': ['Pacifica', 'Hybrid', '300', 'Voyager', '200', 'Country',
        'Cruiser', 'Sebring', 'Aspen', 'Crossfire', 'Concorde', '300M',
        'Prowler', 'LHS', 'Cirrus', 'Yorker', 'LeBaron', 'Ave', 'Imperial'],
 
 'Dodge': ['Durango', 'Charger', 'Challenger', 'Passenger', 'Journey', 'Dart',
        'Avenger', 'Caliber', 'Cargo', 'Nitro', 'Cab', 'Viper', 'Magnum',
        'Stratus', 'Neon', 'Intrepid', '1500', '2500', '3500', 'Stealth',
        'Spirit', 'Colt', 'Shadow', 'B150', 'B250', 'B350', 'Dynasty',
        'Daytona', 'Ramcharger', 'Monaco'],
 'Eagle': ['Talon', 'Vision', 'Summit', 'Premier'], 
 'FIAT': ['500X', 'Spider', '500L', '500', '500e', '500c', 'Abarth'],
     
 'Ford': ['Expedition', 'MAX', 'Edge', 'Lightning', 'Cab', 'Sport', 'MACH-E',
        'Maverick', 'Mustang', 'SuperCab', 'SuperCrew', 'Bronco', 'Escape',
        'Hybrid', 'Explorer', 'Van', 'Wagon', 'EcoSport', 'Fusion',
        'Fiesta', 'Energi', 'Flex', 'Taurus', 'Passenger', 'Cargo',
        'Focus', 'EL', 'ST', 'Victoria', 'Trac', 'X', 'Freestyle',
        'Hundred', 'Excursion', 'Thunderbird', 'ZX2', 'Escort', 'Contour',
        'Aspire', 'Probe', 'Tempo', 'Festiva'],
 'Freightliner': ['Cargo', 'Crew'], 
 'GMC': ['Cab', 'Terrain', 'Yukon', 'XL', 'Acadia', 'Cargo', 'Passenger',
        'Limited', '1500', '2500', 'Envoy', 'XUV', 'Jimmy', 'Denali',
        'Coupe', 'G3500', 'G2500', 'G1500', '3500'], 
 'Genesis': ['GV80', 'GV70', 'G70', 'G80', 'G90'],
 'HUMMER': ['H3', 'H3T', 'H2', 'H1'], 
 'Honda': ['HR-V', 'Civic', 'Odyssey', 'Ridgeline', 'Passport', 'Accord',
        'CR-V', 'Hybrid', 'Pilot', 'Insight', 'R', 'Fit', 'CR-Z',
        'Crosstour', 'Element', 'S2000', 'Prelude', 'Sol'], 
 'Hyundai':['Palisade', 'Tucson', 'Hybrid', 'Cruz', 'Fe', 'Elantra', 'Kona',
        'Sonata', 'Venue', 'Electric', 'N', 'Accent', '5', 'Veloster',
        'GT', 'XL', 'Sport', 'Azera', 'Genesis', 'Coupe', 'Equus',
        'Veracruz', 'Tiburon', 'Entourage', 'XG350', 'XG300', 'Scoupe',
        'Excel'],
 'INFINITI': ['QX80', 'QX50', 'QX55', 'QX60', 'Q50', 'Q60', 'QX30', 'Q70',
        'QX70', 'Q40', 'JX', 'M', 'G', 'EX', 'QX', 'FX', 'Q', 'I', 'J'],
    
 'Isuzu': ['Cab', 'Ascender', 'Rodeo', 'Axiom', 'Sport', 'Trooper',
        'VehiCROSS', 'Amigo', 'Spacecab', 'Oasis', 'Stylus', 'Impulse'],
     
 'Jeep': ['Door', 'Wagoneer', 'L', 'Cherokee', '4xe', 'Gladiator', 'Compass',
        'Wrangler', 'Unlimited', 'Renegade', 'Patriot', 'Liberty',
        'Commander', 'Cab'],
 'Kia': ['Seltos', 'K5', 'Carnival', 'Telluride', 'Sorento', 'Hybrid',
        'Sportage', 'EV6', 'Soul', 'Rio', 'Stinger', 'Forte', 'Niro', 'EV',
        'Sedona', 'Optima', 'Cadenza', 'K900', 'Forte5', 'Koup', 'Rondo',
        'Spectra', 'Amanti', 'Borrego', '(2006.5)', 'Sephia'], 
 'Land': ['110', 'Sport', 'Velar', 'Evoque', '90', 'Discovery', 'Rover',
        'LR4', 'LR2', 'LR3', 'Freelander', 'II'], 
 'Lincoln':['Continental', 'MKZ', 'MKT', 'MKC', 'MKX', 'L', 'Navigator', 'MKS',
        'Car', 'LT', 'LS', 'Zephyr', 'Aviator', 'Blackwood', 'VIII', 'VII'],
   
 'Lotus': ['400', 'Evora', 'Elise'], 
 'MAZDA':['MAZDA3', 'Miata', 'RF', 'CX-5', 'CX-30', 'CX-9', 'MAZDA6', 'CX-3',
        'MAZDA5', 'MAZDA2', 'CX-7', 'Tribute', 'RX-8', 'Cab', 'MPV',
        'Plus', 'Protege', 'Protege5', 'Millenia', '626', 'MX-6', 'MX-3',
        '929', 'RX-7', '323', 'Navajo'], 
 'MINI': ['Countryman', 'Clubman', 'Door', 'Convertible', 'Paceman',
        'Roadster', 'Coupe', 'Hardtop', 'Cooper'], 
 'Mercedes-Benz': ['GLE', 'E-Class', 'C-Class', 'GLA', 'CLA', 'GLB', 'Coupe', 'CLS',
        'GLS', 'Cargo', 'Passenger', 'Crew', 'A-Class', 'GLC', 'S-Class',
        'GT', 'SLC', 'SL', 'G-Class', 'B-Class', 'CLS-Class', 'SLK',
        'GL-Class', 'CLA-Class', 'SLK-Class', 'SL-Class', 'M-Class',
        'GLK-Class', 'GLA-Class', 'CL-Class', 'R-Class', 'CLK-Class', 'E',
        'TE', 'CE', 'SE', 'SEL', 'SEC', 'D', 'SD'], 
 'Mercury': ['Milan', 'Mariner', 'Marquis', 'Mountaineer', 'Sable', 'Monterey',
        'Montego', 'Marauder', 'Villager', 'Cougar', 'Mystique', 'Tracer',
        'Topaz', 'Capri'],
 'Mitsubishi': ['Cross', 'PHEV', 'Sport', 'Outlander', 'Mirage', 'G4', 'Lancer',
        'i-MiEV', 'Evolution', 'Galant', 'Eclipse', 'Endeavor', 'Cab',
        'Montero', 'Diamante', '3000GT', 'Expo', 'Precis'], 
 'Nissan':['Ariya', 'Rogue', 'Versa', 'Kicks', 'Sentra', 'Altima',
        'Pathfinder', 'Cab', 'Armada', 'LEAF', 'Maxima', 'Murano', 'Sport',
        'NV200', 'Cargo', 'Passenger', '370Z', 'Note', 'Taxi', 'GT-R',
        'Quest', 'JUKE', 'Select', 'Xterra', 'cube', '350Z', '200SX',
        '240SX', '300ZX', 'NX', 'Stanza'],
 'Oldsmobile': ['Alero', 'Silhouette', 'Bravada', 'Aurora', 'Intrigue', '88',
        'Cutlass', 'LSS', 'Achieva', 'Regency', 'Supreme', '98', 'Ciera',
        'Cruiser', 'Toronado'], 
 'Panoz': ['Esperante'],
 'Plymouth': ['Neon', 'Voyager', 'Breeze', 'Prowler', 'Acclaim', 'Vista', 'Colt',
        'Laser', 'Sundance'],
 'Polestar': ['2'],
 'Pontiac': ['G3', 'G6', 'Vibe', 'G5', 'Torrent', '(2009.5)', 'Solstice', 'G8',
        'Prix', 'SV6', 'GTO', 'Aztek', 'Bonneville', 'Am', 'Sunfire',
        'Montana', 'Firebird', 'Sport', 'Sunbird', 'LeMans'],
 'Saab': ['9-5', '9-3', '9-4X', '9-7X', '9-2X', '900', '9000'],
 'Subaru': ['Outback', 'Legacy', 'Ascent', 'BRZ', 'Forester', 'Crosstrek',
        'WRX', 'Impreza', 'Tribeca', 'Baja', 'SVX', 'Justy', 'Loyale'],
       
 'Suzuki': ['Kizashi', 'SX4', 'Vitara', 'Cab', 'XL7', 'Forenza', 'Reno',
        'Aerio', 'Verona', 'XL-7', 'Esteem', 'Swift', 'X-90', 'Sidekick',
        'Samurai'],
 'Toyota': ['Sienna', 'Camry', 'Cab', 'RAV4', 'Hybrid', 'Prime', 'Cross',
        'Highlander', 'Corolla', 'Venza', 'Supra', 'Hatchback', 'GR86',
        'CrewMax', 'Mirai', '4Runner', 'Avalon', 'Prius', 'Sequoia',
        'C-HR', 'Cruiser', '86', 'Yaris', 'c', 'iA', 'iM', 'v', 'Matrix',
        'Solara', 'Echo', 'Celica', 'MR2', 'Xtracab', 'Tercel', 'Paseo',
        'Previa', 'Cressida'],
 'Volkswagen': ['ID.4', 'Taos', 'Arteon', 'Tiguan', 'Sport', 'Jetta', 'Atlas',
        'GTI', 'GLI', 'Passat', 'Golf', 'Alltrack', 'e-Golf', 'SportWagen',
        'R', 'Beetle', 'Limited', 'Touareg', 'CC', 'Eos', 'Routan',
        'Rabbit', '2', 'R32', 'Phaeton', '(New)', 'Eurovan', 'Cabrio',
        'III', 'Corrado', 'Cabriolet', 'Fox'],
 'smart': ['coupe', 'cabrio', 'drive', 'fortwo']}

    # Obtenir les modèles de voiture correspondant à la marque sélectionnée
    models = brand_models[brand]

    # Afficher une liste déroulante pour sélectionner le modèle de la voiture
    model = st.selectbox('**Car Model**', models)   

    # Convert the user input to a list
    new_data = [[price,max_seating_capacity,alloy_wheels,nb_doors,engine,max_years_warrantly,max_years_powertrain,max_miles_powertrain,trunk_cap_categ,year,brand]]

    # Make a prediction on the new data
    if st.button('Predict'):
        prediction = make_prediction(new_data)
        print(prediction)
        # Interpret the prediction
        try:
            
            if prediction>=0.8 :
                result = "Good Deal"
                result_color = "green"                

            else:
                result = "Fair Deal"
                result_color = "red"                
                

                
        except:
            st.warning('Something Went Wrong please try again!')

        # Display the prediction result
        #st.success(result)
        
        st.markdown("---")
        st.write('## The prediction Result:')
        st.write(f"**According to the provided data, the prediction of the car is as follows {result}**", f"**for the given car with the Brand and the Moddel specified : {brand}{model}.**", 
             unsafe_allow_html=True, )
        st.write(f"**This prediction is generated based on the input features and the trained model used for car sales prediction**", unsafe_allow_html=True, )
        st.markdown(f"<p style='color:{result_color}; font-size: 32px;'>{result}</p>", unsafe_allow_html=True)



# Run the app
if __name__ == '__main__':

        app()