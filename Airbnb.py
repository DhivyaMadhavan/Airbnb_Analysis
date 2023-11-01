import streamlit as st
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
       background: #ffffff;
       
       font-family:courier;
       color:#000000;
}
</style>
"""
sidepage_bg_img ="""
<style>
[data-testid="stSidebar"][aria-expanded="true"]{
        background: #ffa07a;
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
        fig = px.bar(dataset, x='property_type', y='price', labels={'x': 'property_type', 'y': 'price'},range_y = [0,50000],
                     title= 'Price Distribution with respect to Property_type',
                     color="country",
                     color_discrete_map = {'German Shephard': 'rgb(0,0,0)'})
        st.plotly_chart(fig,use_container_width=True)
def barplot_2():
        rev_df = dataset.groupby('room_type',as_index=False)['number_of_reviews'].mean().sort_values(by='number_of_reviews')
        fig = px.bar(data_frame=rev_df,x='room_type',y='number_of_reviews',color='number_of_reviews',
                     title = "Number of reviews based on room type",
                     color_discrete_map = {'German Shephard': 'rgb(255,0,0)'})
        st.plotly_chart(fig,use_container_width=True)                
def box():        
        
        fig = px.box(dataset,
                     x='bedrooms',
                     y='price',
                     color='bedrooms',
                     title='Number of Bedrooms against Price'
                    )
        st.plotly_chart(fig,use_container_width=True)
def countplot_2():         
        ax = sns.countplot(data=dataset,y=dataset.host_name,order=dataset.host_name.value_counts().index[:10])
        ax.set_title("Top 10 Hosts with Highest number of Listings")
        st.pyplot(ax.get_figure())
def pieplot():
        
        fig = px.pie(dataset, names = 'room_type', values = dataset.groupby('room_type').value_counts(),
                      hole = 0.4,title = "Room types ")
        st.plotly_chart(fig,use_container_width=True)        
def scatter1():
        country_df = dataset.groupby('country',as_index=False)['price'].mean()
        fig = px.scatter(data_frame=country_df,
           x='country',y='price',
           color='country',
           size='price',
           opacity=1,
           size_max=35,
           title='Avg Listing Price in each Countries')
        st.plotly_chart(fig,use_container_width=True) 
def scatter2():
        country_df = dataset.groupby('country',as_index=False)['availability_365'].mean()
        country_df.availability_365 = country_df.availability_365.astype(int)
        fig = px.scatter_geo(data_frame=country_df,
                                       locations='country',
                                       color= 'availability_365', 
                                       hover_data=['availability_365'],
                                       locationmode='country names',
                                       size='availability_365',
                                       title= 'Avg Availability in each Country',
                                       color_continuous_scale='agsunset'
                            )
        st.plotly_chart(fig,use_container_width=True)        
def catplot():
        # Number of different room type in  countries 
        roomtype = dataset.groupby(['country','room_type'])['_id'].count().reset_index().head(15)

        # Different neighbourhood group and room type
        ax = sns.catplot(
        data=roomtype, kind="bar",
        x="country",y='_id', hue="room_type"
        )
        ax.set(ylabel = "Number of listing")
        plt.xticks(rotation=90)
        plt.ioff()
        st.pyplot(ax)
def barplot2():
        #Average price of AirBnb in different neighbourhood
        # Average price of top 10 most expensive neighbourhood
        n_avgprice1 = pd.DataFrame(dataset.groupby('host_neighbourhood')['price'].mean().reset_index().sort_values('price',ascending=False,ignore_index=True).head(10))
        # Average price of top 10 most cheapest neighbourhood
        n_avgprice2 = pd.DataFrame(dataset.groupby('host_neighbourhood')['price'].mean().reset_index().sort_values('price',ascending=False,ignore_index=True).tail(10))
        # combine the both 
        n_avgprice =pd.concat([n_avgprice1,n_avgprice2])
        # Barplotto see different neighbourhood by price
        fig = px.bar(n_avgprice,
                     x='price',
                     y='host_neighbourhood',                     
                     title='Average Price of Airbnb in different host neighbourhood',
                     
                    )
        
        st.plotly_chart(fig,use_container_width=True)
               

with st.sidebar:  
        original_title = '<p style="font-family:Courier; color:black; font-size: 30px;">Airbnb</p>'
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
                header1 = '<p style="color:#FF5A5F; font-size: 24px;text-decoration-line: underline;">Domain</p>'
                st.markdown(header1,unsafe_allow_html=True)
                #header2 = '<p style="color:White; font-size: 20px;">Travel Industry, Property Management and Tourism</p>'
                #st.markdown(header2,unsafe_allow_html=True)
                st.markdown("##### Travel Industry, Property Management and Tourism")
                header2 = '<p style="color:#FF5A5F; font-size: 24px;text-decoration-line: underline;">Technologies Used</p>'
                st.markdown(header2,unsafe_allow_html=True)
                #header4 = '<p style=" color:white; font-size: 20px;">Python,Streamlit,MongoDB,Tableau</p>'
                #st.markdown(header4,unsafe_allow_html=True)
                st.markdown("##### Python,Streamlit,MongoDB,Tableau")
                header3 = '<p style="color:#FF5A5F; font-size: 24px;text-decoration-line: underline;">Overview</p>'
                st.markdown(header3,unsafe_allow_html=True)
                #header6 = '<p style="color:white; font-size: 20px;">To analyze Airbnb data using MongoDB Atlas, perform data cleaning and preparation, develop interactive visualizations, and create dynamic plots to gain insights into pricing variations, availability patterns, and location-based trends.</p>'
                #st.markdown(header6,unsafe_allow_html=True)
                st.markdown("##### To analyze Airbnb data using MongoDB Atlas, perform data cleaning and preparation, develop interactive visualizations, and create dynamic plots to gain insights into pricing variations, availability patterns, and location-based trends. ")
        with col1:
                image=Image.open("C:\\Users\\Natarajan\\Desktop\\Dhivya\\DS\\capstone\\Airbnb\\airbnb_img.jpg")
                new_image = image.resize((900,900))
                st.image(new_image)
                st.write("Tableau:[link](https://public.tableau.com/app/profile/dhivya.n8887/viz/Airbnb_project_Final/Dashboard1?publish=yes)")

if select == "Insights":
        tab1,tab2 = st.tabs(["Charts","Geo-Visualisation"])
        with tab1:
                col1, col2 = st.columns([4,4],gap = "medium")
                with col1:
                        country = st.multiselect('Select a Country', dataset["country"].unique())
                with col2:        
                        room = st.multiselect('Select Room_type', dataset["room_type"].unique())

                col3,col4 = st.columns([6,6],gap="medium")
                query=f'country in {country} & room_type in {room}'
                df1 = dataset.query(query).groupby(["room_type","country"],as_index=False)["price"].sum()
                if country and room:
                        with col3:               
                                st.subheader("View of Room Type Data")
                                fig = px.bar(df1, x="room_type", y="price",hover_data=["country"], text=['${:,.2f}'.format(x) for x in df1["price"]],
                                                template="seaborn",color_continuous_scale=px.colors.sequential.Peach)
                                st.plotly_chart(fig, use_container_width=True)
                        with col4:                
                                st.subheader("View of Country wise Data")
                                fig = px.pie(df1, values="price", names="country", hole=0.5)
                                fig.update_traces(text=df1["country"], textposition="outside")
                                st.plotly_chart(fig, use_container_width=True)  

                        with st.expander("room_type wise price"):
                                st.write(df1.style.background_gradient(cmap="Blues"))
                                csv = df1.to_csv(index=False).encode('utf-8')
                                st.download_button("Download Data", data=csv, file_name="room_type.csv", mime="text/csv",
                                                help='Click here to download the data as a CSV file')          
                # TOTAL LISTINGS BY COUNTRY CHOROPLETH MAP
        with tab2:
                country = st.multiselect('Select a Country',sorted(dataset.country.unique()),sorted(dataset.country.unique()))
                prop = st.multiselect('Select Property_type',sorted(dataset.property_type.unique()),sorted(dataset.property_type.unique()))
                room = st.multiselect('Select Room_type',sorted(dataset.room_type.unique()),sorted(dataset.room_type.unique()))
                price = st.slider('Select Price',dataset.price.min(),dataset.price.max(),(dataset.price.min(),dataset.price.max()),key = "explore")
                
                # CONVERTING THE USER INPUT INTO QUERY
                query1 = f'country in {country} & room_type in {room} & property_type in {prop} & price >= {price[0]} & price <= {price[1]}'
                country_df = dataset.query(query1).groupby(['country',"property_type","room_type","price"],as_index=False)['name'].count().rename(columns={'name' : 'Total_Listings'})
                fig = px.choropleth(country_df,
                                title='Total Listings in each Country',
                                locations='country',
                                locationmode='country names',
                                color= 'property_type',
                                hover_data=["room_type","price"],                              
                                color_continuous_scale=px.colors.sequential.Reds_r                               
                                )
                st.plotly_chart(fig,use_container_width=True)  

                       
               
if select == "Explore Data":          
                barplot_1()
                box()
                scatter1()
                scatter2()        
                barplot_2()                 
                pieplot()
                catplot()
                barplot2() 



   

    





