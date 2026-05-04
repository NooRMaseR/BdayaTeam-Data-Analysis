import plotly.express as px
import streamlit as st
import pandas as pd
import numpy as np
import pickle

with open("model.pkl", 'rb') as f:
    model = pickle.load(f)

df = pd.read_csv(
    "Telco-Customer-Churn.csv",
    true_values=['Yes'],
    false_values=['No'],
    dtype={
        "SeniorCitizen": np.bool_
    }
)
df['TotalCharges'] = np.where(df['TotalCharges'] == ' ', 0, df['TotalCharges'])

dummy_df = pd.get_dummies(df, columns=['gender', "MultipleLines" ,"InternetService" ,"OnlineSecurity" ,"OnlineBackup" ,"DeviceProtection" ,"TechSupport" ,"StreamingTV" ,"StreamingMovies" , "Contract", 'PaymentMethod'])
X = dummy_df.drop(columns=['Churn', 'customerID'])
Y = dummy_df['Churn']

payments = df['PaymentMethod'].value_counts()

importance = pd.DataFrame(
    {
        "Columns": X.columns,
        "Importance": np.round(model.feature_importances_ * 100, 2)
    }
).sort_values("Importance", ascending=False)


# ====================================================================


st.title("Customers Churn Analysis")

st.subheader("Importance")

bar = px.bar(
    importance, 
    y="Columns", 
    x="Importance",
    orientation='h',
    color="Importance",
    color_continuous_scale="Reds"
)
st.plotly_chart(bar)

col1, col2, col3 = st.columns(3)

with col1:
    # TotalCharges
    st.metric(
        label=importance["Columns"].iloc[0], 
        value=importance['Importance'].iloc[0],
        delta=importance['Importance'].iloc[0] - importance['Importance'].iloc[1]
    )
    st.markdown(
        """
        
        من اكثر الاسباب هى التكلفه الكليه
        
        ---
        
        #### الحل؟
        
        مراجعه تكاليف الخدمات لأنها عاليه
        """,
    )
    
    
with col2:
    # tenure
    st.metric(
        label=importance["Columns"].iloc[1], 
        value=importance['Importance'].iloc[1],
        delta=importance['Importance'].iloc[1] - importance['Importance'].iloc[0]
    )
    st.markdown(
        """
        مده بقاء العميل هى سبب اقل لألغاء الاشراك
        
        ---
        
        #### الحل؟
        
        إعطاء عروض للعملاء الذين يبقون اكثر
        """
    )
    
    
    
with col3:
    # MonthlyCharges
    st.metric(
        label=importance["Columns"].iloc[2], 
        value=importance['Importance'].iloc[2],
        delta=importance['Importance'].iloc[2] - importance['Importance'].iloc[1]
    ) 
    st.markdown(
        """
        التكلفه الشهريه او العقوك الشهريه هى سبب اخر
        
        ---
        
        #### الحل؟
        
        عمل عروض للذين لديهم عقود شهريه ليشتركوا فى عقود سنويه
        """
    )


pie = px.pie(
    payments,
    names=payments.index,
    values=payments.values,
    title="Payments Methods PCT",
    subtitle="a Pie for Paymenst Methods",
    hole=0.2
)

st.plotly_chart(pie)
