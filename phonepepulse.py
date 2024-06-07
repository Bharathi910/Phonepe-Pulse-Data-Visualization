import streamlit as st
import plotly.express as px
import pymysql
import pandas as pd
import requests
import json

# MySQL connection details
username = 'root'
password = '1234'
host = '127.0.0.1'
database_name = 'phonepe'

# Connect to MySQL server and create the database if it doesn't exist
connection = pymysql.connect(host=host, user=username, password=password,db='phonepe')
cursor = connection.cursor()

# ****************** Sreamlit ******************


st.set_page_config(layout= "wide")

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background: rgb(195, 177, 225);
background-size: cover;
background-position: center center;
background-repeat: no-repeat;
background-attachment: local;
}}
[data-testid="stHeader"] {{
background: rgb(128, 0, 128);
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

st.header(':violet[Phonepe Pulse Data Visualization ]')
option = st.radio('**Select your option**',('India Data', 'State Data','Top Charts'),horizontal=True)

# ******** India Data ********
if option == 'India Data':
    tab1, tab2, tab3 = st.tabs(['Transaction','User','Insurance'])
    # ***** India Data Transaction
    with tab1:
        col1, col2, col3 = st.columns(3)
        with col1:
            in_tr_yr = st.selectbox('**Select Year**', ('2018','2019','2020','2021','2022','2023','2024'),key='in_tr_yr')
        with col2:
            in_tr_qtr = st.selectbox('**Select Quarter**', ('1','2','3','4'),key='in_tr_qtr')
        with col3:
            in_tr_tr_typ = st.selectbox('**Select Transaction type**', ('Recharge & bill payments','Peer-to-peer payments',
            'Merchant payments','Financial Services','Others'),key='in_tr_tr_typ')

        # SQL Query

        # Transaction Analysis query

        cursor.execute(f"SELECT State, Transaction_amount FROM aggregated_transactions WHERE Year = '{in_tr_yr}' AND Quarter = '{in_tr_qtr}' AND Transaction_type = '{in_tr_tr_typ}';")
        trans_rslt = cursor.fetchall()
        df_trans_rslt = pd.DataFrame(trans_rslt, columns=['State', 'Transaction_amount'])

        tab1_1, tab1_2 , tab1_3= st.tabs(['Geo Visualization','Bar Chart Visualization', 'Pie Chart Visualization'])
        with tab1_1:
            # Drop a State column from df_in_tr_tab_qry_rslt
            df_trans_rslt.drop(columns=['State'], inplace=True)

            # Clone the gio data
            url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
            response = requests.get(url)
            data1 = json.loads(response.content)

             # Extract state names and sort them in alphabetical order
            state_names_tra = [feature['properties']['ST_NM'] for feature in data1['features']]
            state_names_tra.sort()

            # Create a DataFrame with the state names column
            df_state_names_tra = pd.DataFrame({'State': state_names_tra})

            # Combine the Gio State name with df_in_tr_tab_qry_rslt
            df_state_names_tra['Transaction_amount']=df_trans_rslt

            # convert dataframe to csv file
            df_state_names_tra.to_csv('State_trans.csv', index=False)

            # Read csv
            df_tra = pd.read_csv('State_trans.csv')
            fig = px.choropleth(
                            df_tra,
                            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                            featureidkey='properties.ST_NM',
                            locations='State',
                            color='Transaction_amount',
                            color_continuous_scale='Blues',
                            title = 'Aggregated Transaction ',
                            width=1500
                        )

            fig.update_geos(fitbounds="locations", visible=False)
            fig.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
            st.plotly_chart(fig,use_container_width=True)
        # Bar chart visualization
        with tab1_2:
            cursor.execute(f"SELECT States, Transaction_amount, Transaction_count FROM map_transactions WHERE Years = '{in_tr_yr}' AND Quarter = '{in_tr_qtr}' ;")
            map_agg = cursor.fetchall()
            df_trans_rslt = pd.DataFrame(map_agg, columns=['State', 'Transaction_amount', 'Transaction_count'])

            bar_fig= px.bar(df_trans_rslt, 
                            x='State',
                            y='Transaction_amount',
                            color='Transaction_count',
                            color_continuous_scale = 'sunsetdark',
                            title= 'Map Transaction'
                            )
            bar_fig.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
            st.plotly_chart(bar_fig,use_container_width=True)

        # Pie chart visualization
        with tab1_3:
            cursor.execute(f"SELECT States, Transaction_amount, Transaction_count FROM top_transactions WHERE Years = '{in_tr_yr}' AND Quarter = '{in_tr_qtr}' ;")
            top_trans = cursor.fetchall()
            df_trans_top = pd.DataFrame(top_trans, columns=['State', 'Transaction_amount', 'Transaction_count'])

            pie_fig= px.pie(df_trans_top, 
                            names='State',
                            values='Transaction_amount',
                            color='Transaction_count',
                            title= 'Top Transaction'
                            )
            pie_fig.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
            st.plotly_chart(pie_fig)
            

    # India Data User
    with tab2:
        col_1, col_2 = st.columns(2)
        with col_1:
            in_us_yr = st.selectbox('**Select Year**', ('2018','2019','2020','2021','2022','2023','2024'),key='in_us_yr')
        with col_2:
            in_us_qtr = st.selectbox('**Select Quarter**', ('1','2','3','4'),key='in_us_qtr')

        tab2_1, tab2_2, tab2_3 = st.tabs(['Geo Visualization','Bar Chart Visualization','Pie Chart Visualization'])

        with tab2_1:
            try:
                cursor.execute(f"SELECT State, SUM(Count) FROM aggregated_users  WHERE Year = '{in_us_yr}' AND Quarter = '{in_us_qtr}' GROUP BY State;")
                user_rslt = cursor.fetchall()
                df_user_rslt = pd.DataFrame(user_rslt, columns=['State', 'User Count'])

                # Drop a State column 
                df_user_rslt.drop(columns=['State'], inplace=True)

                # Clone the geo data
                url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
                response = requests.get(url)
                data2 = json.loads(response.content)

                # Extract state names and sort them in alphabetical order
                state_names_user = [feature['properties']['ST_NM'] for feature in data2['features']]
                state_names_user.sort()

                # Create a DataFrame with the state names column
                df_state_names_user = pd.DataFrame({'State': state_names_user})

                # Combine the Gio State name with df_in_tr_tab_qry_rslt
                df_state_names_user['User Count']=df_user_rslt

                # convert dataframe to csv file
                df_state_names_user.to_csv('State_user.csv', index=False)

                # Read csv
                df_user = pd.read_csv('State_user.csv')
                user_fig = px.choropleth(
                                df_user,
                                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                featureidkey='properties.ST_NM',
                                locations='State',
                                color='User Count',
                                color_continuous_scale='Blues',
                                title = 'User Analysis',
                                width=1500
                            )

                user_fig.update_geos(fitbounds="locations", visible=False)
                user_fig.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
                st.plotly_chart(user_fig,use_container_width=True)
            except:
                st.error("where the aggregated_user data from 2022 (Qtr 2,3,4) to 2023 (Qtr 1,2,3) are not same like previous year Phonepe Pluse data, so can't feed data to sql and can't visualize ")          
        # Bar chart visualization
        with tab2_2:
            cursor.execute(f"SELECT States, RegisteredUser, AppOpens  FROM map_users  WHERE Years = '{in_us_yr}' AND Quarter = '{in_us_qtr}';")
            map_user = cursor.fetchall()
            df_map_user = pd.DataFrame(map_user, columns=['State', 'RegisteredUser', 'AppOpens'])

            bar_fig_user= px.bar(df_map_user, 
                            x='State',
                            y='RegisteredUser',
                            color='AppOpens',
                            color_continuous_scale = 'sunsetdark',
                            title= 'Map user'
                            )
            bar_fig_user.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
            st.plotly_chart(bar_fig_user,use_container_width=True)

        # Pie chart visualization
        with tab2_3:
            cursor.execute(f"SELECT States, Pincodes, RegisteredUser FROM top_users  WHERE Years = '{in_us_yr}' AND Quarter = '{in_us_qtr}' ;")
            top_user = cursor.fetchall()
            df_user_top = pd.DataFrame(top_user, columns=['State', 'Pincodes', 'RegisteredUser'])

            pie_fig_user= px.pie(df_user_top, 
                            names='State',
                            values='RegisteredUser',
                            color='Pincodes',
                            title= 'Top user'
                            )
            pie_fig_user.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
            st.plotly_chart(pie_fig_user)

    # India Data Insurance
    with tab3:
        st.write('**(Note)**:-This data available from **2020** **Quater 2** in **INDIA**')
        col3_1, col3_2 = st.columns(2)
        with col3_1:
            ins_yr = st.selectbox('**Select Year**', ('2021','2020','2022','2023','2024'),key='ins_yr')
        with col3_2:
            ins_qtr = st.selectbox('**Select Quarter**', ('1','2','3','4'),key='ins_qtr')

        tab3_1, tab3_2, tab3_3 = st.tabs(['Geo Visualization','Bar Chart Visualization','Pie Chart Visualization'])


        with tab3_1:
            try:
                cursor.execute(f"select States, Insurance_amount from aggregated_insurance where Years= '{ins_yr}' AND Quarter = '{ins_qtr}' ; ")
                agg_ins = cursor.fetchall()
                df_agg_ins = pd.DataFrame(agg_ins, columns=['State', 'Insurance_amount'])

                # Drop a State column 
                df_agg_ins.drop(columns=['State'], inplace=True)

                # Clone the geo data
                url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
                response = requests.get(url)
                data3 = json.loads(response.content)

                # Extract state names and sort them in alphabetical order
                state_names_ins = [feature['properties']['ST_NM'] for feature in data3['features']]
                state_names_ins.sort()

                # Create a DataFrame with the state names column
                df_state_names_ins = pd.DataFrame({'State': state_names_ins})

                # Combine the Geo State name with df_in_tr_tab_qry_rslt
                df_state_names_ins['Insurance_amount']=df_agg_ins

                # convert dataframe to csv file
                df_state_names_ins.to_csv('State_ins.csv', index=False)

                # Read csv
                df_ins = pd.read_csv('State_ins.csv')
                ins_fig = px.choropleth(
                                df_ins,
                                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                featureidkey='properties.ST_NM',
                                locations='State',
                                color='Insurance_amount',
                                color_continuous_scale='Blues',
                                title = 'Aggregated Insurance',
                                width=1500
                            )

                ins_fig.update_geos(fitbounds="locations", visible=False)
                ins_fig.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
                st.plotly_chart(ins_fig,use_container_width=True)
            except:
                st.error("No Data Available for selected year and quater")
        # Bar chart visualization
        with tab3_2:
            cursor.execute(f"select States, Transaction_amount, Transaction_count from map_insurance where Years= '{ins_yr}' AND Quarter = '{ins_qtr}' ; ")
            map_ins = cursor.fetchall()
            df_map_ins = pd.DataFrame(map_ins, columns=['State', 'Transaction_amount','Transaction_count'])

            bar_fig_ins= px.bar(df_map_ins, 
                            x='State',
                            y='Transaction_count',
                            color='Transaction_amount',
                            color_continuous_scale = 'sunsetdark',
                            title= 'Map insurance'
                            )
            bar_fig_ins.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
            st.plotly_chart(bar_fig_ins,use_container_width=True)

        # Pie chart visualization
        with tab3_3:
            cursor.execute(f"select States, Transaction_amount, Transaction_count from map_insurance where Years= '{ins_yr}' AND Quarter = '{ins_qtr}' ; ")
            top_ins = cursor.fetchall()
            df_top_ins = pd.DataFrame(top_ins, columns=['State', 'Transaction_amount','Transaction_count'])

            pie_fig_ins= px.pie(df_top_ins, 
                            names='State',
                            values='Transaction_count',
                            color='Transaction_amount',
                            title= 'Top Insurance'
                            )
            pie_fig_ins.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
            st.plotly_chart(pie_fig_ins)

# ******** State Data ********
elif option =='State Data':
    tab_st, tab_su, tab_si = st.tabs(['Transaction','User','Insurance'])
    # transaction data
    with tab_st:
        col1, col2,col3 = st.columns(3)
        with col1:
            st_tr_st = st.selectbox('**Select State**',('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh','assam', 'bihar', 
            'chandigarh', 'chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat', 'haryana', 'himachal-pradesh', 
            'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh','maharashtra', 'manipur', 
            'meghalaya', 'mizoram', 'nagaland','odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim', 'tamil-nadu', 'telangana', 
            'tripura', 'uttar-pradesh', 'uttarakhand', 'west-bengal'),key='st_tr_st')
        with col2:
            st_tr_yr = st.selectbox('**Select Year**', ('2018','2019','2020','2021','2022','2023','2024'),key='st_tr_yr')
        with col3:
            st_tr_qtr = st.selectbox('**Select Quarter**', ('1','2','3','4'),key='st_tr_qtr')
        
        tab_t_bar, tab_t_bub, tab_t_pie = st.tabs(['Aggregated Analysis','Map Analysis','Top Analysis'])

        with tab_t_bar:
            cursor.execute(f"select Transaction_type,Transaction_count,Transaction_amount from aggregated_transactions where Year='{st_tr_yr}' and State='{st_tr_st}' and Quarter='{st_tr_qtr}'  ;")
            agg_t = cursor.fetchall()
            df_agg_t = pd.DataFrame(agg_t, columns=['Transaction_type', 'Transaction_count','Transaction_amount'])

            bar_fig_at= px.bar(df_agg_t, 
                            x='Transaction_type',
                            y='Transaction_count',
                            color='Transaction_amount',
                            color_continuous_scale = 'sunsetdark'
                            
                            )
            st.plotly_chart(bar_fig_at,use_container_width=True)

        with tab_t_bub:
            cursor.execute(f"select District,Transaction_count,Transaction_amount from map_transactions where Years='{st_tr_yr}' and States='{st_tr_st}' and Quarter='{st_tr_qtr}'  ;")
            map_t = cursor.fetchall()
            df_map_t = pd.DataFrame(map_t, columns=['District', 'Transaction_count','Transaction_amount'])

            bub_fig_mt= px.scatter(df_map_t,
                                x='District',
                                y= 'Transaction_count',
                                color='Transaction_amount',
                                color_continuous_scale = 'sunsetdark'
                                )
            st.plotly_chart(bub_fig_mt,use_container_width=True)

        with tab_t_pie:
            cursor.execute(f"select Pincodes,Transaction_count,Transaction_amount from top_transactions where Years='{st_tr_yr}' and States='{st_tr_st}' and Quarter='{st_tr_qtr}'  ;")
            top_t = cursor.fetchall()
            df_top_t = pd.DataFrame(top_t, columns=['Pincodes','Transaction_count','Transaction_amount'])

            pie_fig_t= px.pie(df_top_t, 
                            names='Pincodes',
                            values='Transaction_count',
                            color='Transaction_amount',
                            
                            )
            
            st.plotly_chart(pie_fig_t)

    # User Data
    with tab_su:
        col5, col6 = st.columns(2)
        with col5:
            st_us_st = st.selectbox('**Select State**',('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh','assam', 'bihar', 
            'chandigarh', 'chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat', 'haryana', 'himachal-pradesh', 
            'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh','maharashtra', 'manipur', 
            'meghalaya', 'mizoram', 'nagaland','odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim', 'tamil-nadu', 'telangana', 
            'tripura', 'uttar-pradesh', 'uttarakhand', 'west-bengal'),key='st_us_st')
        with col6:
            st_us_yr = st.selectbox('**Select Year**', ('2018','2019','2020','2021','2022','2023'),key='st_us_yr')

        tab_u_bar, tab_u_bub, tab_u_pie = st.tabs(['Aggregated Analysis','Map Analysis','Top Analysis'])

        with tab_u_bar:
            cursor.execute(f"select Quarter,Brands,Count from aggregated_users where State='{st_us_st}' and Year='{st_us_yr}';  ")
            agg_u = cursor.fetchall()
            df_agg_u = pd.DataFrame(agg_u, columns=['Quarter','Brands','Count'])

            bar_fig_au= px.bar(df_agg_u, 
                            x='Brands',
                            y='Count',
                            color='Quarter',
                            color_continuous_scale = 'sunsetdark'
                            
                            )
            st.plotly_chart(bar_fig_au,use_container_width=True)

        with tab_u_bub:
            cursor.execute(f"select Quarter,RegisteredUser,Districts from map_users where States='{st_us_st}' and Years='{st_us_yr}';  ")
            map_u = cursor.fetchall()
            df_map_u = pd.DataFrame(map_u, columns=['Quarter','RegisteredUser','Districts'])

            bub_fig_mu= px.scatter(df_map_u,
                                x='Districts',
                                y= 'RegisteredUser',
                                color='Quarter',
                                size='Quarter',
                                color_continuous_scale = 'sunsetdark'
                                )
            st.plotly_chart(bub_fig_mu,use_container_width=True)

        with tab_u_pie:
            cursor.execute(f"select Quarter,RegisteredUser from map_users where States='{st_us_st}' and Years='{st_us_yr}';  ")
            top_u = cursor.fetchall()
            df_top_u = pd.DataFrame(top_u, columns=['Quarter','RegisteredUser'])

            pie_fig_u= px.pie(df_top_u, 
                            names='Quarter',
                            values='RegisteredUser',
                            
                            
                            )
            
            st.plotly_chart(pie_fig_u)

    # Insurance Data
    with tab_si:
        col7, col8 = st.columns(2)
        with col7:
            st_ins_st = st.selectbox('**Select State**',('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh','assam', 'bihar', 
            'chandigarh', 'chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat', 'haryana', 'himachal-pradesh', 
            'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh','maharashtra', 'manipur', 
            'meghalaya', 'mizoram', 'nagaland','odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim', 'tamil-nadu', 'telangana', 
            'tripura', 'uttar-pradesh', 'uttarakhand', 'west-bengal'),key='st_ins_st')
        with col8:
            st_ins_yr = st.selectbox('**Select Year**', ('2020','2021','2022','2023'),key='st_ins_yr')

        tab_i_bar, tab_i_bub, tab_i_pie = st.tabs(['Aggregated Analysis','Map Analysis','Top Analysis'])

        with tab_i_bar:
            cursor.execute(f"select Quarter,Insurance_count,Insurance_amount from aggregated_insurance where States='{st_ins_st}' and Years='{st_ins_yr}';  ")
            agg_i = cursor.fetchall()
            df_agg_i = pd.DataFrame(agg_i, columns=['Quarter','Insurance_count','Insurance_amount'])

            bar_fig_ai= px.bar(df_agg_i, 
                            x='Quarter',
                            y='Insurance_count',
                            color='Insurance_amount',
                            color_continuous_scale = 'sunsetdark'
                            
                            )
            st.plotly_chart(bar_fig_ai,use_container_width=True)

        with tab_i_bub:
            cursor.execute(f"select Quarter,Districts,Transaction_count,Transaction_amount from map_insurance where States='{st_ins_st}' and Years='{st_ins_yr}';  ")
            map_i = cursor.fetchall()
            df_map_i = pd.DataFrame(map_i, columns=['Quarter','Districts','Transaction_count','Transaction_amount'])

            bub_fig_mi= px.scatter(df_map_i,
                                x='Districts',
                                y= 'Transaction_count',
                                color='Quarter',
                                size='Transaction_amount',
                                color_continuous_scale = 'sunsetdark'
                                )
            st.plotly_chart(bub_fig_mi,use_container_width=True)

        with tab_i_pie:
            cursor.execute(f"select Quarter,Transaction_count,Transaction_amount from top_insurance where States='{st_ins_st}' and Years='{st_ins_yr}';  ")
            top_i = cursor.fetchall()
            df_top_i = pd.DataFrame(top_i, columns=['Quarter','Transaction_count','Transaction_amount'])

            pie_fig_i= px.pie(df_top_i, 
                            names='Quarter',
                            values='Transaction_count',
                            color='Transaction_amount',
                            
                            )
            
            st.plotly_chart(pie_fig_i)

# ********* Top Charts *********


elif option == 'Top Charts':
    question= st.selectbox("Select the Question",["1. Transaction Amount and Count of Aggregated Insurance",
                                                    "2. Transaction Amount and Count of Map Insurance",
                                                    "3. Transaction Amount and Count of Top Insurance",
                                                    "4. Transaction Amount and Count of Aggregated Transaction",
                                                    "5. Transaction Amount and Count of Map Transaction",
                                                    "6. Transaction Amount and Count of Top Transaction",
                                                    "7. Transaction Count of Aggregated User",
                                                    "8. Registered users of Map User",
                                                    "9. App opens of Map User",
                                                    "10. Device(Brands) Count of Aggregated User",
                                                    ])
    if question == "1. Transaction Amount and Count of Aggregated Insurance":
        col1,col2 = st.columns(2)
        with col1:
            cursor.execute(f'''  SELECT States, SUM(Insurance_amount) AS Transaction_amount
                FROM aggregated_insurance
                GROUP BY States
                ORDER BY Transaction_amount DESC
                LIMIT 10; ''')     
            q1_amt = cursor.fetchall()
            df_q1_amt = pd.DataFrame(q1_amt, columns=['states','Transaction_amount'])

            df_q1_amt_bar= px.bar(df_q1_amt, 
                            x='states',
                            y='Transaction_amount',
                            hover_name= 'states',
                            color_discrete_sequence=px.colors.sequential.Purp_r,
                            title='Top 10 Transaction Amount'
                            )
            df_q1_amt_bar.update_layout(title_font=dict(size=23),title_font_color='#6739b7')
            st.plotly_chart(df_q1_amt_bar,use_container_width=True)

        with col2:
            cursor.execute(f'''  SELECT States, SUM(Insurance_count) AS Transaction_count
                FROM aggregated_insurance
                GROUP BY States
                ORDER BY Transaction_count DESC
                LIMIT 10; ''')     
            q1_cnt = cursor.fetchall()
            df_q1_cnt = pd.DataFrame(q1_cnt, columns=['states','Transaction_count'])

            df_q1_cnt_bar= px.bar(df_q1_cnt, 
                            x='states',
                            y='Transaction_count',
                            hover_name= 'states',
                            color_discrete_sequence=px.colors.sequential.Aggrnyl,
                            title='Top 10 Transaction Count'
                            )
            df_q1_cnt_bar.update_layout(title_font=dict(size=23),title_font_color='#6739b7')
            st.plotly_chart(df_q1_cnt_bar,use_container_width=True)

    elif question == "2. Transaction Amount and Count of Map Insurance":
        col1,col2 = st.columns(2)
        with col1:
            cursor.execute(f'''  SELECT States, SUM(Transaction_amount) AS Transaction_amount
                FROM map_insurance
                GROUP BY States
                ORDER BY Transaction_amount DESC
                LIMIT 10; ''')     
            q2_amt = cursor.fetchall()
            df_q2_amt = pd.DataFrame(q2_amt, columns=['States','Transaction_amount'])

            df_q2_amt_bar= px.bar(df_q2_amt, 
                            x='States',
                            y='Transaction_amount',
                            hover_name= 'States',
                            color_discrete_sequence=px.colors.sequential.Purp_r,
                            title='Top 10 Transaction Amount'
                            )
            df_q2_amt_bar.update_layout(title_font=dict(size=23),title_font_color='#6739b7')
            st.plotly_chart(df_q2_amt_bar,use_container_width=True)

        with col2:
            cursor.execute(f'''  SELECT States, SUM(Transaction_count) AS Transaction_count
                FROM map_insurance
                GROUP BY States
                ORDER BY Transaction_count DESC
                LIMIT 10; ''')     
            q2_cnt = cursor.fetchall()
            df_q2_cnt = pd.DataFrame(q2_cnt, columns=['States','Transaction_count'])

            df_q2_cnt_bar= px.bar(df_q2_cnt, 
                            x='States',
                            y='Transaction_count',
                            hover_name= 'States',
                            color_discrete_sequence=px.colors.sequential.Aggrnyl,
                            title='Top 10 Transaction Count'
                            )
            df_q2_cnt_bar.update_layout(title_font=dict(size=23),title_font_color='#6739b7')
            st.plotly_chart(df_q2_cnt_bar,use_container_width=True)

    elif question == "3. Transaction Amount and Count of Top Insurance":
        col1,col2 = st.columns(2)
        with col1:
            cursor.execute(f'''  SELECT States, SUM(Transaction_amount) AS Transaction_amount
                FROM top_insurance
                GROUP BY States
                ORDER BY Transaction_amount DESC
                LIMIT 10; ''')     
            q3_amt = cursor.fetchall()
            df_q3_amt = pd.DataFrame(q3_amt, columns=['States','Transaction_amount'])

            df_q3_amt_bar= px.bar(df_q3_amt, 
                            x='States',
                            y='Transaction_amount',
                            hover_name= 'States',
                            color_discrete_sequence=px.colors.sequential.Purp_r,
                            title='Top 10 Transaction Amount'
                            )
            df_q3_amt_bar.update_layout(title_font=dict(size=23),title_font_color='#6739b7')
            st.plotly_chart(df_q3_amt_bar,use_container_width=True)

        with col2:
            cursor.execute(f'''  SELECT States, SUM(Transaction_count) AS Transaction_count
                FROM top_insurance
                GROUP BY States
                ORDER BY Transaction_count DESC
                LIMIT 10; ''')     
            q3_cnt = cursor.fetchall()
            df_q3_cnt = pd.DataFrame(q3_cnt, columns=['States','Transaction_count'])

            df_q3_cnt_bar= px.bar(df_q3_cnt, 
                            x='States',
                            y='Transaction_count',
                            hover_name= 'States',
                            color_discrete_sequence=px.colors.sequential.Aggrnyl,
                            title='Top 10 Transaction Count'
                            )
            df_q3_cnt_bar.update_layout(title_font=dict(size=23),title_font_color='#6739b7')
            st.plotly_chart(df_q3_cnt_bar,use_container_width=True)

    elif question == "4. Transaction Amount and Count of Aggregated Transaction":
        col1,col2 = st.columns(2)
        with col1:
            cursor.execute(f'''  SELECT State, SUM(Transaction_amount) AS Transaction_amount
                FROM aggregated_transactions
                GROUP BY State
                ORDER BY Transaction_amount DESC
                LIMIT 10; ''')     
            q4_amt = cursor.fetchall()
            df_q4_amt = pd.DataFrame(q4_amt, columns=['States','Transaction_amount'])

            df_q4_amt_bar= px.bar(df_q4_amt, 
                            x='States',
                            y='Transaction_amount',
                            hover_name= 'States',
                            color_discrete_sequence=px.colors.sequential.Purp_r,
                            title='Top 10 Transaction Amount'
                            )
            df_q4_amt_bar.update_layout(title_font=dict(size=23),title_font_color='#6739b7')
            st.plotly_chart(df_q4_amt_bar,use_container_width=True)

        with col2:
            cursor.execute(f'''  SELECT State, SUM(Transaction_count) AS Transaction_count
                FROM aggregated_transactions
                GROUP BY State
                ORDER BY Transaction_count DESC
                LIMIT 10; ''')     
            q4_cnt = cursor.fetchall()
            df_q4_cnt = pd.DataFrame(q4_cnt, columns=['States','Transaction_count'])

            df_q4_cnt_bar= px.bar(df_q4_cnt, 
                            x='States',
                            y='Transaction_count',
                            hover_name= 'States',
                            color_discrete_sequence=px.colors.sequential.Aggrnyl,
                            title='Top 10 Transaction Count'
                            )
            df_q4_cnt_bar.update_layout(title_font=dict(size=23),title_font_color='#6739b7')
            st.plotly_chart(df_q4_cnt_bar,use_container_width=True)

    elif question == "5. Transaction Amount and Count of Map Transaction":
        col1,col2 = st.columns(2)
        with col1:
            cursor.execute(f'''  SELECT States, SUM(Transaction_amount) AS Transaction_amount
                FROM map_transactions
                GROUP BY States
                ORDER BY Transaction_amount DESC
                LIMIT 10; ''')     
            q5_amt = cursor.fetchall()
            df_q5_amt = pd.DataFrame(q5_amt, columns=['States','Transaction_amount'])

            df_q5_amt_bar= px.bar(df_q5_amt, 
                            x='States',
                            y='Transaction_amount',
                            hover_name= 'States',
                            color_discrete_sequence=px.colors.sequential.Purp_r,
                            title='Top 10 Transaction Amount'
                            )
            df_q5_amt_bar.update_layout(title_font=dict(size=23),title_font_color='#6739b7')
            st.plotly_chart(df_q5_amt_bar,use_container_width=True)

        with col2:
            cursor.execute(f'''  SELECT States, SUM(Transaction_count) AS Transaction_count
                FROM map_transactions
                GROUP BY States
                ORDER BY Transaction_count DESC
                LIMIT 10; ''')     
            q5_cnt = cursor.fetchall()
            df_q5_cnt = pd.DataFrame(q5_cnt, columns=['States','Transaction_count'])

            df_q5_cnt_bar= px.bar(df_q5_cnt, 
                            x='States',
                            y='Transaction_count',
                            hover_name= 'States',
                            color_discrete_sequence=px.colors.sequential.Aggrnyl,
                            title='Top 10 Transaction Count'
                            )
            df_q5_cnt_bar.update_layout(title_font=dict(size=23),title_font_color='#6739b7')
            st.plotly_chart(df_q5_cnt_bar,use_container_width=True)

    elif question == "6. Transaction Amount and Count of Top Transaction":
        col1,col2 = st.columns(2)
        with col1:
            cursor.execute(f'''  SELECT States, SUM(Transaction_amount) AS Transaction_amount
                FROM top_transactions
                GROUP BY States
                ORDER BY Transaction_amount DESC
                LIMIT 10; ''')     
            q6_amt = cursor.fetchall()
            df_q6_amt = pd.DataFrame(q6_amt, columns=['States','Transaction_amount'])

            df_q6_amt_bar= px.bar(df_q6_amt, 
                            x='States',
                            y='Transaction_amount',
                            hover_name= 'States',
                            color_discrete_sequence=px.colors.sequential.Purp_r,
                            title='Top 10 Transaction Amount'
                            )
            df_q6_amt_bar.update_layout(title_font=dict(size=23),title_font_color='#6739b7')
            st.plotly_chart(df_q6_amt_bar,use_container_width=True)

        with col2:
            cursor.execute(f'''  SELECT States, SUM(Transaction_count) AS Transaction_count
                FROM top_transactions
                GROUP BY States
                ORDER BY Transaction_count DESC
                LIMIT 10; ''')     
            q6_cnt = cursor.fetchall()
            df_q6_cnt = pd.DataFrame(q6_cnt, columns=['States','Transaction_count'])

            df_q6_cnt_bar= px.bar(df_q6_cnt, 
                            x='States',
                            y='Transaction_count',
                            hover_name= 'States',
                            color_discrete_sequence=px.colors.sequential.Aggrnyl,
                            title='Top 10 Transaction Count'
                            )
            df_q6_cnt_bar.update_layout(title_font=dict(size=23),title_font_color='#6739b7')
            st.plotly_chart(df_q6_cnt_bar,use_container_width=True)

    elif question == "7. Transaction Count of Aggregated User":
        cursor.execute(f'''  select State,  sum( Count) as Transaction_count
                       from aggregated_users 
                        group by State
                       order by Transaction_count desc
                       limit 10; ''')     
        q7_cnt = cursor.fetchall()
        df_q7_cnt = pd.DataFrame(q7_cnt, columns=['States','Transaction_count'])

        df_q7_cnt_bar= px.bar(df_q7_cnt, 
                            x='States',
                            y='Transaction_count',
                            hover_name= 'States',
                            color_discrete_sequence=px.colors.sequential.Aggrnyl,
                            title='Top 10 Transaction Count'
                            )
        df_q7_cnt_bar.update_layout(title_font=dict(size=23),title_font_color='#6739b7')
        st.plotly_chart(df_q7_cnt_bar,use_container_width=True)

    elif question == "8. Registered users of Map User":
        cursor.execute(f'''  select States, sum(RegisteredUser) as reg_count 
                       from map_users 
                       group by States 
                       order by reg_count desc 
                       limit 10; ''')     
        q8_cnt = cursor.fetchall()
        df_q8_cnt = pd.DataFrame(q8_cnt, columns=['States','Registered_users'])

        df_q8_cnt_bar= px.bar(df_q8_cnt, 
                            x='States',
                            y='Registered_users',
                            hover_name= 'States',
                            color_discrete_sequence=px.colors.sequential.Greens_r,
                            title='Top 10 Registered users'
                            )
        df_q8_cnt_bar.update_layout(title_font=dict(size=23),title_font_color='#6739b7')
        st.plotly_chart(df_q8_cnt_bar,use_container_width=True)

    elif question == "9. App opens of Map User":
        cursor.execute(f'''  select States, sum(AppOpens) as app_count 
                       from map_users 
                       group by States 
                       order by app_count desc 
                       limit 10; ''')     
        q9_cnt = cursor.fetchall()
        df_q9_cnt = pd.DataFrame(q9_cnt, columns=['States','AppOpens'])

        df_q9_cnt_bar= px.bar(df_q9_cnt, 
                            x='States',
                            y='AppOpens',
                            hover_name= 'States',
                            color_discrete_sequence=px.colors.sequential.Redor,
                            title='Top 10 App opens'
                            )
        df_q9_cnt_bar.update_layout(title_font=dict(size=23),title_font_color='#6739b7')
        st.plotly_chart(df_q9_cnt_bar,use_container_width=True)

    elif question == "10. Device(Brands) Count of Aggregated User":
        cursor.execute(f'''  select  Brands, sum(Count) from aggregated_users group by Brands; ''')     
        q10_cnt = cursor.fetchall()
        df_q10_cnt = pd.DataFrame(q10_cnt, columns=['Brands','Counts'])

        df_q10_cnt_bar= px.bar(df_q10_cnt, 
                            x='Brands',
                            y='Counts',
                            
                            color_discrete_sequence=px.colors.sequential.Aggrnyl,
                            title='Device Counts'
                            )
        df_q10_cnt_bar.update_layout(title_font=dict(size=23),title_font_color='#6739b7')
        st.plotly_chart(df_q10_cnt_bar,use_container_width=True)


