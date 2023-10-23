import streamlit as st
from streamlit_folium import folium_static
import folium
import ast
import pymongo
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
import plotly.express as px
import seaborn as sns
import pandas as pd
from PIL import Image
import time


page_bg_img ="""
<style>
[data-testid="stAppViewContainer"]{
       background: #000000;
       
       font-family:courier;
       color:#ffffff;
}
</style>
"""
sidepage_bg_img ="""
<style>
[data-testid="stSidebar"][aria-expanded="true"]{
        background: #f66949;
 }        
</style>
"""

sidepadding_style ="""
<style>
[data-testid="stSidebar"][aria-expanded="true"]{
        padding-top:2rem;
        padding:0
 }       
</style>
"""


st.set_page_config(page_title="Airbnb",layout='wide')
st.write('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)
st.write('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)
padding_top = 0
st.markdown(page_bg_img,unsafe_allow_html=True)
st.markdown(sidepage_bg_img,unsafe_allow_html=True)
st.markdown(sidepadding_style,unsafe_allow_html=True)

with st.spinner("Loading..."):
    time.sleep(2)

dataset = pd.read_csv("C:\\Users\\Natarajan\\Desktop\\Dhivya\\DS\\capstone\\Airbnb\\Airbnb_csv")  
def barplot_1():              
        fig = px.bar(dataset, x='Property_type', y='Price', labels={'x': 'Property_type', 'y': 'Price'},range_y = [0,50000],title= 'Price Distribution with respect to Property_type')
        st.plotly_chart(fig,use_container_width=True)
def barplot_2():
        rev_df = dataset.groupby('Room_type',as_index=False)['Number_of_reviews'].mean().sort_values(by='Number_of_reviews')
        fig = px.bar(data_frame=rev_df,x='Room_type',y='Number_of_reviews',color='Number_of_reviews',title = "Number of reviews based on room type")
        st.plotly_chart(fig,use_container_width=True)                
def box():        
       fig = px.box(dataset,
                     x='No_of_bedrooms',
                     y='Price',
                     color='No_of_bedrooms',
                     title='Number of Bedrooms against Price'
                    )
        st.plotly_chart(fig,use_container_width=True)
def countplot_2():         
        ax = sns.countplot(data=dataset,y=dataset.Host_name,order=dataset.Host_name.value_counts().index[:10])
        ax.set_title("Top 10 Hosts with Highest number of Listings")
        st.pyplot(ax.get_figure())
def pieplot():
        
        fig = px.pie(dataset, names = 'Room_type', values = dataset.groupby('Room_type').value_counts(),hover_name ="Country", hole = 0.4,title = "Room types ")
        st.plotly_chart(fig,use_container_width=True)        
def scatter():
        country_df = dataset.groupby('Country',as_index=False)['Price'].mean()
        fig = px.scatter(data_frame=country_df,
           x='Country',y='Price',
           color='Country',
           size='Price',
           opacity=1,
           size_max=35,
           title='Avg Listing Price in each Countries')
        st.plotly_chart(fig,use_container_width=True) 
def catplot():
        # Number of different room type in  countries 
        roomtype = dataset.groupby(['Country','Room_type'])['Id'].count().reset_index().head(15)

        # Different neighbourhood group and room type
        ax = sns.catplot(
        data=roomtype, kind="bar",
        x="Country",y='Id', hue="Room_type"
        )
        ax.set(ylabel = "Number of listing")
        plt.xticks(rotation=90)
        plt.ioff()
        st.pyplot(ax)

with st.sidebar:  
        original_title = '<p style="font-family:Courier; color:White; font-size: 30px;">Airbnb</p>'
        st.markdown(original_title,unsafe_allow_html=True)      
        select = option_menu(
                                menu_title = None,
                                options = ["About","Insights","Explore Data"],
                                icons=["house","graph-up-arrow","bar-chart-line"],
                                default_index=0,
                                orientation="vertical"
                                ) 
client = pymongo.MongoClient("mongodb+srv://dhivya:Myworldd@cluster0.yjmzisp.mongodb.net/?retryWrites=true&w=majority")
db = client['sample_airbnb']
col = db['listingsAndReviews'] 

if select == "About":
        #st.image("title.png")
        col1,col2 = st.columns(2,gap= 'medium')
        with col2:
                header1 = '<p style="font-family:Times Roman; color:#FF5A5F; font-size: 24px;">Domain</p>'
                st.markdown(header1,unsafe_allow_html=True)
                st.markdown("##### Travel Industry, Property Management and Tourism")
                header2 = '<p style="font-family:Times Roman; color:#FF5A5F; font-size: 24px;">Technologies Used</p>'
                st.markdown(header2,unsafe_allow_html=True)
                st.markdown("##### Python,Streamlit,MongoDB,Tableau")
                header3 = '<p style="font-family:Times Roman; color:#FF5A5F; font-size: 24px;">Overview</p>'
                st.markdown(header3,unsafe_allow_html=True)
                st.markdown("##### To analyze Airbnb data using MongoDB Atlas, perform data cleaning and preparation, develop interactive visualizations, and create dynamic plots to gain insights into pricing variations, availability patterns, and location-based trends. ")
        with col1:
                image=Image.open("C:\\Users\\Natarajan\\Desktop\\Dhivya\\DS\\capstone\\Airbnb\\airbnb_img.jpg")
                new_image = image.resize((900,900))
                st.image(new_image)
if select == "Insights":
        tab1,tab2 = st.tabs(["Charts","Geo-Visualisation"])
        with tab1:
                col1, col2 = st.columns([4,4],gap = "medium")
                with col1:
                        country = st.multiselect('Select a Country', dataset["Country"].unique())
                with col2:        
                        room = st.multiselect('Select Room_type', dataset["Room_type"].unique())

                col3,col4 = st.columns([6,6],gap="medium")
                query=f'Country in {country} & Room_type in {room}'
                df1 = dataset.query(query).groupby(["Room_type","Country"],as_index=False)["Price"].sum()
                with col3:               
                        st.subheader("room_type_ViewData")
                        fig = px.bar(df1, x="Room_type", y="Price",hover_data=["Country"], text=['${:,.2f}'.format(x) for x in df1["Price"]],
                                        template="seaborn")
                        st.plotly_chart(fig, use_container_width=True)
                with col4:                
                        st.subheader("country_ViewData")
                        fig = px.pie(df1, values="Price", names="Country", hole=0.5)
                        fig.update_traces(text=df1["Country"], textposition="outside")
                        st.plotly_chart(fig, use_container_width=True)  

                with st.expander("room_type wise price"):
                        st.write(df1.style.background_gradient(cmap="Blues"))
                        csv = df1.to_csv(index=False).encode('utf-8')
                        st.download_button("Download Data", data=csv, file_name="room_type.csv", mime="text/csv",
                                        help='Click here to download the data as a CSV file')              
        with tab2:
                # TOTAL LISTINGS BY COUNTRY CHOROPLETH MAP

                country = st.multiselect('Select a Country',sorted(dataset.Country.unique()),sorted(dataset.Country.unique()))
                prop = st.multiselect('Select Property_type',sorted(dataset.Property_type.unique()),sorted(dataset.Property_type.unique()))
                room = st.multiselect('Select Room_type',sorted(dataset.Room_type.unique()),sorted(dataset.Room_type.unique()))
                price = st.slider('Select Price',dataset.Price.min(),dataset.Price.max(),(dataset.Price.min(),dataset.Price.max()))
                
                # CONVERTING THE USER INPUT INTO QUERY
                query1 = f'Country in {country} & Room_type in {room} & Property_type in {prop} & Price >= {price[0]} & Price <= {price[1]}'
                country_df = dataset.query(query1).groupby(['Country'],as_index=False)['Name'].count().rename(columns={'Name' : 'Total_Listings'})
                fig = px.choropleth(country_df,
                                title='Total Listings in each Country',
                                locations='Country',
                                locationmode='country names',
                                color='Total_Listings',
                                color_continuous_scale=px.colors.sequential.Plasma
                                
                                )
                st.plotly_chart(fig,use_container_width=True)        
               
if select == "Explore Data":     
    barplot_1()
    box()
    scatter()        
    barplot_2()
    #countplot_2()  
    pieplot()
    catplot() 



   

    





