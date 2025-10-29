
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout= 'wide', page_title= 'Suicide Rates EDA',page_icon='🔪')
# Set Title
html_title = """<h1 style="color:red;text-align:left;"> Suicide Rates Exploratory Data Analysis </h1>"""
st.markdown(html_title, unsafe_allow_html=True)

# Insert Image
st.image('https://user-images.githubusercontent.com/53637541/83379224-a691a080-a3f8-11ea-833e-c3f6bdea209a.jpg',width=1000)

# Read data
df = pd.read_csv('master_final.csv', index_col= 0)

page = st.sidebar.radio('Pages', ['Home', "KPI's Dashboard", "Suicide Report"])

if page == 'Home':
    st.subheader('Dataset Overview')
    st.dataframe(df.head())
    column_descriptions = {
        "country": "The name of the country where the data was collected.",
        "year": "The year when the suicide statistics were recorded.",
        "sex": "Gender of the population group — either male or female.",
        "age": "Age group of the population .",
        "suicides_no": "The total number of recorded suicides in that demographic group for the given year.",
        "population": "The total population of that demographic group (defined by country, year, sex, and age).",
        "suicides/100k pop": "The number of suicides per 100,000 people in that demographic group — a normalized rate for comparison.",
        "gdp_for_year($)": "The country's total Gross Domestic Product (GDP) for that year, measured in U.S. dollars.",
        "gdp_per_capita ($)": "GDP per person for that year — total GDP divided by total population, in U.S. dollars.",
        "generation": "Generational classification based on the birth year range (e.g., Generation X, Boomers, Silent, etc.)."}

    # Create a table for descriptions
    desc_df = pd.DataFrame(list(column_descriptions.items()), columns=["Column Name", "Description"])

    # Display table
    st.subheader("📝 Column Descriptions")
    st.table(desc_df)
    if st.checkbox('Show All Data'):
        
        st.subheader('Show All Dataframe')
        st.dataframe(df)


elif page == "KPI's Dashboard":
    
    # Basic KPIs
    total_country = df['country'].nunique()
    total_suicides_no = df['suicides_no'].sum()
    years_no = df['year'].nunique()

    avg_suicides_year = total_suicides_no / years_no
    avg_suicides_country = total_suicides_no / total_country
    avg_age_per_country = df.groupby('country')['age'].count().mean()

    # Display KPIs in columns
    col1, col2, col3,col4, col5 = st.columns(5)
    col1.metric(" 🗺  Total Countries", f"{total_country:,}")
    col2.metric("🔪 Total Suicides", f"{total_suicides_no:,}")
    col3.metric("👥 Total Years", f"{years_no:,}")

    #col4, col5 = st.columns(2)
    col5.metric(" Avg Suicides per Year", f"{avg_suicides_year:,.2f}")
    col4.metric(" Avg Suicides Per Country", f"{avg_suicides_country:,.2f}")

    st.write("---")

        # Top Countries by Suicides
    st.subheader("🏙️ Top Countries by Suicides #")
    df_sorted=df.groupby(['country','age'])['suicides_no'].sum().sort_values(ascending=False).reset_index().head(30)
    st.plotly_chart(px.bar(data_frame=df_sorted,x='country',y='suicides_no',color='age',barmode='group',text_auto=True))


            # Top Gender / Age Group by Suicides
    st.subheader("🏙️ Top Gender / Age Group by Suicides #")
    df_sorted_gender=df.groupby(['sex','age'])['suicides_no'].sum().sort_values(ascending=False).reset_index().head(30)
    st.plotly_chart(px.bar(data_frame=df_sorted_gender,x='sex',y='suicides_no',color='age',barmode='group',text_auto=True))

            #  Suicides Progress Over Years
    st.subheader("🏙️ Suicides Progress Over Years #")
    df_sorted_year=df.groupby('year')['suicides_no'].sum().reset_index()
    st.plotly_chart(px.line(data_frame=df_sorted_year,x='year',y='suicides_no'))

            #  Suicides Progress Over Years / Age Group
    st.subheader("🏙️ Suicides Progress Over Years / Age Group#")
    df_sorted_year_age=df.groupby(['year','age'])['suicides_no'].sum().reset_index()
    st.plotly_chart(px.line(data_frame=df_sorted_year_age,x='year',y='suicides_no',color='age'))


            #  Suicides Progress Over Years / Gender
    st.subheader("🏙️ Suicides Progress Over Years /Gender #")
    df_sorted_year_gender=df.groupby(['year','sex'])['suicides_no'].sum().reset_index()
    st.plotly_chart(px.line(data_frame=df_sorted_year_gender,x='year',y='suicides_no',color='sex'))


                #  Top Suicides Age Groups
    st.subheader("🏙️ Top Suicides Age Groups #")
    df_age_grouped=df.groupby('age')['suicides_no'].sum().reset_index().sort_values(by='suicides_no',ascending=False)
    st.plotly_chart(px.bar(data_frame=df_age_grouped,x='age',y='suicides_no',text_auto=True))



                #  Top Contries in Suicides#
    st.subheader("🏙️ Top Contries in Suicides #")
    df_country_grouped=df.groupby('country')['suicides_no'].sum().reset_index().sort_values(by='suicides_no',ascending=False).head(10)
    st.plotly_chart(px.bar(data_frame=df_country_grouped,x='country',y='suicides_no',text_auto=True))


               #  Top Years  in Suicides#
    st.subheader("🏙️ Top Years in Suicides #")
    df_year_grouped=df.groupby('year')['suicides_no'].sum().reset_index().sort_values(by='suicides_no',ascending=False).head(10)
    df_year_grouped['year']=df_year_grouped.year.astype('string')
    st.plotly_chart(px.bar(data_frame=df_year_grouped,x='year',y='suicides_no',text_auto=True),key="chart2")
    st.plotly_chart(px.pie(data_frame=df_year_grouped,names='year',values='suicides_no'),key="chart3")         

elif page == 'Suicide Report':

    start_year=st.sidebar.number_input('Start Year', min_value = df.year.min(), max_value = df.year.max(), value = df.year.min())


    end_year=st.sidebar.number_input('End Year', min_value = df.year.min(), max_value = df.year.max(), value = df.year.max())


    df_filtered = df[(df.year >= start_year) & (df.year <= end_year)]

    #gender=st.sidebar.selectbox('Gender', ['Choose','Male', 'Female'])
    age_group=st.sidebar.selectbox('Age Group', ['All Age Groups','5-14', '15-24','25-34','35-54','55-74','75+'])


    All_gender =  ['Choose'] + df_filtered.sex.unique().tolist() 

    #All_Age =  ['All Age Groups'] + df_filtered.age.unique().tolist() 

    All_countries =  ['All Countries'] + df_filtered.country.unique().tolist() 


    Gender = st.sidebar.selectbox('Gender', All_gender)
    #Age_Group=st.sidebar.selectbox('Age Group', All_Age)
    country = st.sidebar.selectbox('country', All_countries)


    if country != 'All Countries':

        df_filtered = df_filtered[df_filtered.country == country]


    if Gender != 'Choose':

        df_filtered = df_filtered[df_filtered.sex == Gender]

    if age_group != 'All Age Groups':

        df_filtered = df_filtered[df_filtered.age == age_group]

    st.dataframe(df_filtered)
