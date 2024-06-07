import pandas as pd
import pymysql
import json
import os

#Dataframe of Aggregated Transactions
path1="C:/Users/siva Bharathi/OneDrive/Desktop/Python/phonepe_data/pulse/data/aggregated/transaction/country/india/state/"
agg_trans_list = os.listdir(path1)

columns1 = {'State': [], 'Year': [], 'Quarter': [], 'Transaction_type': [], 'Transaction_count': [],
            'Transaction_amount': []}
for state in agg_trans_list:
    cur_state = path1 + state + "/"
    agg_year_list = os.listdir(cur_state)
    
    for year in agg_year_list:
        cur_year = cur_state + year + "/"
        agg_file_list = os.listdir(cur_year)
        
        for file in agg_file_list:
            cur_file = cur_year + file
            data = open(cur_file, 'r')
            A = json.load(data)
            
            for i in A['data']['transactionData']:
                name = i['name']
                count = i['paymentInstruments'][0]['count']
                amount = i['paymentInstruments'][0]['amount']
                columns1['Transaction_type'].append(name)
                columns1['Transaction_count'].append(count)
                columns1['Transaction_amount'].append(amount)
                columns1['State'].append(state)
                columns1['Year'].append(year)
                columns1['Quarter'].append(int(file.strip('.json')))
                
df_agg_trans = pd.DataFrame(columns1)

# Dataframe of Aggregated User
path2="C:/Users/siva Bharathi/OneDrive/Desktop/Python/phonepe_data/pulse/data/aggregated/user/country/india/state/"
agg_user_list = os.listdir(path2)

columns2 = {'State': [], 'Year': [], 'Quarter': [], 'Brands': [], 'Count': [],
            'Percentage': []}
for state in agg_user_list:
    cur_state = path2 + state + "/"
    agg_year_list = os.listdir(cur_state)
    
    for year in agg_year_list:
        cur_year = cur_state + year + "/"
        agg_file_list = os.listdir(cur_year)

        for file in agg_file_list:
            cur_file = cur_year + file
            data = open(cur_file, 'r')
            B = json.load(data)
            
            try:
                for i in B["data"]["usersByDevice"]:
                    brand_name = i["brand"]
                    counts = i["count"]
                    percents = i["percentage"]
                    columns2["Brands"].append(brand_name)
                    columns2["Count"].append(counts)
                    columns2["Percentage"].append(percents)
                    columns2["State"].append(state)
                    columns2["Year"].append(year)
                    columns2["Quarter"].append(int(file.strip('.json')))
            except:
                pass
                
df_agg_user = pd.DataFrame(columns2)

# Dataframe of Aggregated Insurance

path3="C:/Users/siva Bharathi/OneDrive/Desktop/Python/phonepe_data/pulse/data/aggregated/insurance/country/india/state/"
agg_insur_list= os.listdir(path3)

columns3= {"States":[], "Years":[], "Quarter":[], "Insurance_type":[], "Insurance_count":[],"Insurance_amount":[] }

for state in agg_insur_list:
    cur_states =path3+state+"/"
    agg_year_list = os.listdir(cur_states)
    
    for year in agg_year_list:
        cur_years = cur_states+year+"/"
        agg_file_list = os.listdir(cur_years)

        for file in agg_file_list:
            cur_files = cur_years+file
            data = open(cur_files,"r")
            A = json.load(data)

            for i in A["data"]["transactionData"]:
                name = i["name"]
                count = i["paymentInstruments"][0]["count"]
                amount = i["paymentInstruments"][0]["amount"]
                columns3["Insurance_type"].append(name)
                columns3["Insurance_count"].append(count)
                columns3["Insurance_amount"].append(amount)
                columns3["States"].append(state)
                columns3["Years"].append(year)
                columns3["Quarter"].append(int(file.strip(".json")))


df_agg_ins = pd.DataFrame(columns3)

# Dataframe of Map Transaction

path4="C:/Users/siva Bharathi/OneDrive/Desktop/Python/phonepe_data/pulse/data/map/transaction/hover/country/india/state/"
map_tran_list = os.listdir(path4)

columns4 = {"States":[], "Years":[], "Quarter":[],"District":[], "Transaction_count":[],"Transaction_amount":[]}

for state in map_tran_list:
    cur_states = path4+state+"/"
    map_year_list = os.listdir(cur_states)
    
    for year in map_year_list:
        cur_years = cur_states+year+"/"
        map_file_list = os.listdir(cur_years)
        
        for file in map_file_list:
            cur_files = cur_years+file
            data = open(cur_files,"r")
            E = json.load(data)

            for i in E['data']["hoverDataList"]:
                name = i["name"]
                count = i["metric"][0]["count"]
                amount = i["metric"][0]["amount"]
                columns4["District"].append(name)
                columns4["Transaction_count"].append(count)
                columns4["Transaction_amount"].append(amount)
                columns4["States"].append(state)
                columns4["Years"].append(year)
                columns4["Quarter"].append(int(file.strip(".json")))

df_map_transaction = pd.DataFrame(columns4)

# Dataframe of Map User

path5="C:/Users/siva Bharathi/OneDrive/Desktop/Python/phonepe_data/pulse/data/map/user/hover/country/india/state/"
map_user_list = os.listdir(path5)

columns5 = {"States":[], "Years":[], "Quarter":[], "Districts":[], "RegisteredUser":[], "AppOpens":[]}

for state in map_user_list:
    cur_states = path5+state+"/"
    map_year_list = os.listdir(cur_states)
    
    for year in map_year_list:
        cur_years = cur_states+year+"/"
        map_file_list = os.listdir(cur_years)
        
        for file in map_file_list:
            cur_files = cur_years+file
            data = open(cur_files,"r")
            F = json.load(data)

            for i in F["data"]["hoverData"].items():
                district = i[0]
                registereduser = i[1]["registeredUsers"]
                appopens = i[1]["appOpens"]
                columns5["Districts"].append(district)
                columns5["RegisteredUser"].append(registereduser)
                columns5["AppOpens"].append(appopens)
                columns5["States"].append(state)
                columns5["Years"].append(year)
                columns5["Quarter"].append(int(file.strip(".json")))

df_map_user = pd.DataFrame(columns5)

# Dataframe of Map Insurance

path6="C:/Users/siva Bharathi/OneDrive/Desktop/Python/phonepe_data/pulse/data/map/insurance/hover/country/india/state/"
map_insur_list= os.listdir(path6)

columns6= {"States":[], "Years":[], "Quarter":[], "Districts":[], "Transaction_count":[],"Transaction_amount":[] }

for state in map_insur_list:
    cur_states =path6+state+"/"
    agg_year_list = os.listdir(cur_states)
    
    for year in agg_year_list:
        cur_years = cur_states+year+"/"
        agg_file_list = os.listdir(cur_years)

        for file in agg_file_list:
            cur_files = cur_years+file
            data = open(cur_files,"r")
            D = json.load(data)

            for i in D["data"]["hoverDataList"]:
                name = i["name"]
                count = i["metric"][0]["count"]
                amount = i["metric"][0]["amount"]
                columns6["Districts"].append(name)
                columns6["Transaction_count"].append(count)
                columns6["Transaction_amount"].append(amount)
                columns6["States"].append(state)
                columns6["Years"].append(year)
                columns6["Quarter"].append(int(file.strip(".json")))


df_map_insurance = pd.DataFrame(columns6)

# Dataframe of Top Transaction

path7="C:/Users/siva Bharathi/OneDrive/Desktop/Python/phonepe_data/pulse/data/top/transaction/country/india/state/"
top_tran_list = os.listdir(path7)

columns7 = {"States":[], "Years":[], "Quarter":[], "Pincodes":[], "Transaction_count":[], "Transaction_amount":[]}

for state in top_tran_list:
    cur_states = path7+state+"/"
    top_year_list = os.listdir(cur_states)
    
    for year in top_year_list:
        cur_years = cur_states+year+"/"
        top_file_list = os.listdir(cur_years)
        
        for file in top_file_list:
            cur_files = cur_years+file
            data = open(cur_files,"r")
            H = json.load(data)

            for i in H["data"]["pincodes"]:
                entityName = i["entityName"]
                count = i["metric"]["count"]
                amount = i["metric"]["amount"]
                columns7["Pincodes"].append(entityName)
                columns7["Transaction_count"].append(count)
                columns7["Transaction_amount"].append(amount)
                columns7["States"].append(state)
                columns7["Years"].append(year)
                columns7["Quarter"].append(int(file.strip(".json")))

df_top_transaction = pd.DataFrame(columns7)

# Dataframe of Top User

path8="C:/Users/siva Bharathi/OneDrive/Desktop/Python/phonepe_data/pulse/data/top/user/country/india/state/"
top_user_list = os.listdir(path8)

columns8 = {"States":[], "Years":[], "Quarter":[], "Pincodes":[], "RegisteredUser":[]}

for state in top_user_list:
    cur_states = path8+state+"/"
    top_year_list = os.listdir(cur_states)

    for year in top_year_list:
        cur_years = cur_states+year+"/"
        top_file_list = os.listdir(cur_years)

        for file in top_file_list:
            cur_files = cur_years+file
            data = open(cur_files,"r")
            I = json.load(data)

            for i in I["data"]["pincodes"]:
                name = i["name"]
                registeredusers = i["registeredUsers"]
                columns8["Pincodes"].append(name)
                columns8["RegisteredUser"].append(registereduser)
                columns8["States"].append(state)
                columns8["Years"].append(year)
                columns8["Quarter"].append(int(file.strip(".json")))

df_top_user = pd.DataFrame(columns8)

# Dataframe of Top Insurance

path9="C:/Users/siva Bharathi/OneDrive/Desktop/Python/phonepe_data/pulse/data/top/insurance/country/india/state/"
top_insur_list = os.listdir(path9)

columns9 = {"States":[], "Years":[], "Quarter":[], "Pincodes":[], "Transaction_count":[], "Transaction_amount":[]}

for state in top_insur_list:
    cur_states = path9+state+"/"
    top_year_list = os.listdir(cur_states)

    for year in top_year_list:
        cur_years = cur_states+year+"/"
        top_file_list = os.listdir(cur_years)

        for file in top_file_list:
            cur_files = cur_years+file
            data = open(cur_files,"r")
            G = json.load(data)

            for i in G["data"]["pincodes"]:
                entityName = i["entityName"]
                count = i["metric"]["count"]
                amount = i["metric"]["amount"]
                columns9["Pincodes"].append(entityName)
                columns9["Transaction_count"].append(count)
                columns9["Transaction_amount"].append(amount)
                columns9["States"].append(state)
                columns9["Years"].append(year)
                columns9["Quarter"].append(int(file.strip(".json")))

df_top_insur = pd.DataFrame(columns9)



# MySQL connection details
username = 'root'
password = '1234'
host = '127.0.0.1'
database_name = 'phonepe'

# Connect to MySQL server and create the database if it doesn't exist
connection = pymysql.connect(host=host, user=username, password=password)
cursor = connection.cursor()
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
connection.select_db(database_name)

# Function to create table and insert data
def create_table_and_insert_data(df, table_name, create_table_query):
    cursor.execute(create_table_query)
    for _, row in df.iterrows():
        placeholders = ', '.join(['%s'] * len(row))
        columns = ', '.join(row.index)
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        cursor.execute(sql, tuple(row))

# Define table creation queries
#Aggregated Transaction Table Query
agg_trans_table = """
CREATE TABLE IF NOT EXISTS aggregated_transactions (
    State VARCHAR(50),
    Year INT,
    Quarter INT,
    Transaction_type VARCHAR(50),
    Transaction_count INT,
    Transaction_amount DOUBLE
)
"""
create_table_and_insert_data(df_agg_trans, 'aggregated_transactions', agg_trans_table)

#Aggregated User Table Query
agg_user_table = """
CREATE TABLE IF NOT EXISTS aggregated_users (
    State VARCHAR(50),
    Year INT,
    Quarter INT,
    Brands VARCHAR(50),
    Count INT,
    Percentage DOUBLE
)
"""
create_table_and_insert_data(df_agg_user, 'aggregated_users', agg_user_table)

#Aggregated Insurance Table Query
agg_ins_table = """
CREATE TABLE IF NOT EXISTS aggregated_insurance (
    States VARCHAR(50),
    Years INT,
    Quarter INT,
    Insurance_type VARCHAR(50),
    Insurance_count INT,
    Insurance_amount DOUBLE
)
"""
create_table_and_insert_data(df_agg_ins, 'aggregated_insurance', agg_ins_table)

#Map Transaction Table Query
map_trans_table = """
CREATE TABLE IF NOT EXISTS map_transactions (
    States VARCHAR(50),
    Years INT,
    Quarter INT,
    District VARCHAR(50),
    Transaction_count INT,
    Transaction_amount DOUBLE
)
"""
create_table_and_insert_data(df_map_transaction, 'map_transactions', map_trans_table)

#Map User Table Query
map_user_table = """
CREATE TABLE IF NOT EXISTS map_users (
    States VARCHAR(50),
    Years INT,
    Quarter INT,
    Districts VARCHAR(50),
    RegisteredUser INT,
    AppOpens INT
)
"""
create_table_and_insert_data(df_map_user, 'map_users', map_user_table)

#Map Insurance Table Query
map_ins_table = """
CREATE TABLE IF NOT EXISTS map_insurance (
    States VARCHAR(50),
    Years INT,
    Quarter INT,
    Districts VARCHAR(50),
    Transaction_count INT,
    Transaction_amount DOUBLE
)
"""
create_table_and_insert_data(df_map_insurance, 'map_insurance', map_ins_table)

#Top Transaction Table Query 
top_trans_table = """
CREATE TABLE IF NOT EXISTS top_transactions (
    States VARCHAR(50),
    Years INT,
    Quarter INT,
    Pincodes VARCHAR(50),
    Transaction_count INT,
    Transaction_amount DOUBLE
)
"""
create_table_and_insert_data(df_top_transaction, 'top_transactions', top_trans_table)

#Top User Table Query 
top_user_table = """
CREATE TABLE IF NOT EXISTS top_users (
    States VARCHAR(50),
    Years INT,
    Quarter INT,
    Pincodes VARCHAR(50),
    RegisteredUser INT
)
"""
create_table_and_insert_data(df_top_user, 'top_users', top_user_table)

#Top Insurance Table Query 
top_ins_table = """
CREATE TABLE IF NOT EXISTS top_insurance (
    States VARCHAR(50),
    Years INT,
    Quarter INT,
    Pincodes VARCHAR(50),
    Transaction_count INT,
    Transaction_amount DOUBLE
)
"""
create_table_and_insert_data(df_top_insur, 'top_insurance', top_ins_table)

connection.commit()
cursor.close()
connection.close()