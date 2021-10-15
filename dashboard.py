import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
st.set_page_config(page_title="My Dashboard",layout='wide')
st.title("**Post-PhD activities for US Science and Engineering Grads**")
st.header("Gender Level Analysis")
st.caption("Data from https://ncses.nsf.gov/pubs/nsf19301/data")

DATA_URL=('sed17-sr-tab055.xlsx')
@st.cache(persist=True)
def load_data():
    data=pd.read_excel("sed17-sr-tab055.xlsx",header=3,index_col=0)
    female_data = data[-42:]
    male_data = data[42:-42]
    full_data = data[:42]
    return male_data, female_data, full_data

def clean_filter(df):
    sci_eng = (
        df.
        filter(regex='(science|Engineer)').
        rename({"Life sciencesa":"Life sciences"}, axis=1).
        dropna(axis=0).
        T.
        reset_index().
        rename_axis(None, axis=1).
        rename({"index":"Field",
                "All doctorate recipients (number)c": "Total doctorate recipients",
                "Male doctorate recipients (number)": "Total doctorate recipients",
                "Female doctorate recipients (number)": "Total doctorate recipients"},axis=1)
    )
    return sci_eng   


male_data, female_data, full_data = load_data()
male_data_clean = clean_filter(male_data)
female_data_clean = clean_filter(female_data)
full_data_clean = clean_filter(full_data)

total_phd_recipients = full_data_clean.iloc[:,0:1].columns.append(full_data_clean.iloc[:,1:2].columns)
post_grad_location = full_data_clean.iloc[:,0:1].columns.append(full_data_clean.iloc[:,-12:-1].columns)
post_grad_status = full_data_clean.iloc[:,0:1].columns.append(full_data_clean.iloc[:,2:6].columns)
post_grad_study_type = full_data_clean.iloc[:,0:1].columns.append(full_data_clean.iloc[:,6:8].columns)
post_grad_employment_type = full_data_clean.iloc[:,0:1].columns.append(full_data_clean.iloc[:,8:13].columns)

categories = {
    "Total Recipients": total_phd_recipients,
    "Post Grad Status (#)": post_grad_status,
    'Post Grad Employment Type (%)': post_grad_employment_type,
    "Post Grad Study Type (%)": post_grad_study_type,
    "Post Grad Location (%)": post_grad_location
}


data_split = {
    "male": male_data_clean,
    "female": female_data_clean,
    "combined": full_data_clean
}


select_gender = st.sidebar.selectbox('Select Gender',["male","female","combined"],key=1)

select_category = st.sidebar.selectbox("Analysis Category", ["Total Recipients", "Post Grad Status (#)",'Post Grad Employment Type (%)',"Post Grad Study Type (%)","Post Grad Location (%)"])

#get the state selected in the selectbox
select_data = data_split[select_gender][categories[select_category]]
select_variable = st.sidebar.radio("Variable", select_data.drop("Field",axis=1).columns)

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.dataframe(select_data)

col1, col2 = st.columns(2)
if not st.checkbox('Hide Graph', False, key=1):
    col1.markdown(f"### {select_variable}: {select_gender}")
    graph = px.bar(
        select_data.sort_values(select_variable, ascending=False), 
        x='Field',
        y=select_variable,
        labels={'Number of cases':'Number of cases in %s'},
        color='Field')
    graph.update_layout(width=700)
    graph.layout.update(showlegend=False)
    col1.plotly_chart(graph,width=700)

    if st.sidebar.checkbox("Compare",True, key=2):
        select2 = st.sidebar.selectbox('Select Gender',["female","male","combined"],key=2)
        select_data2 = data_split[select2]
        
        col2.markdown(f"### {select_variable}: {select2}")
        graph2 = px.bar(
            select_data2.sort_values(select_variable, ascending=False), 
            x='Field',
            y=select_variable,
            labels={'Number of cases':'Number of cases in %s'},
            color='Field')
        graph2.layout.update(showlegend=False)
        col2.plotly_chart(graph2)    

