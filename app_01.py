import streamlit as st
import pickle
import numpy as np
import pandas as pd
import shap 


## Load the model
pipe=pickle.load(open('pipe.pkl','rb'))
df=pickle.load(open('df.pkl','rb'))

st.title('Laptop Price Predictor')

#3 Brand
company=st.selectbox('Brand',df['Company'].unique())

## Type of laptop
type=st.selectbox('Type',df['TypeName'].unique())

## Ram
ram=st.selectbox('Ram(in GB)',[2,4,6,8,12,16,32,64])

## Weight
weight=st.number_input('weight of the Laptop')

## Touch screen
touchscreen=st.selectbox('TouchScreen',['No','Yes'])

## IPS
ips=st.selectbox('IPS',['NO','Yes'])

## SCreen size
screen_size=st.number_input('Screen input')

## resolution
resolution=st.selectbox('Screen Resolution',['1920x1080','1366x768','1600x900','3840x2160','3200x1800','2880x1800','2560x1600','2560x1440','2304x1440'])

## cpu
cpu=st.selectbox('Cpu',df['Cpu_Brand'].unique())

# HDD
hdd=st.selectbox('HDD(in GB)',[0,128,256,512,1022,2048])

## SSD
ssd=st.selectbox('SSD(in GB)',[0,8,128,256,512,1024])

## Gpu
gpu=st.selectbox('Gpu',df['Gpu_brand'].unique())

## os
os=st.selectbox('OS',df['os'].unique())

def calculate_deal_score(predicted_price,ram,ssd,cpu,gpu):
    score=0
    ## Ram Scoring
    if ram >= 16 :score+=25
    elif ram >= 8: score += 15
    else:score += 5

    ## SSD Scoring
    if ssd>= 512:score+=25
    elif ssd>= 256:score+=15
    elif ssd >= 128:score+=10
    else: score += 3

    ## Price scoring
    if predicted_price <= 40000:score+=25
    elif predicted_price <= 70000:score+=15
    elif predicted_price <=100000:score+=10

    ## Cpu Scoring
    if 'i7' or 'i9' in cpu:score+= 25
    elif'i5' in cpu:score+= 15
    elif 'i3' in cpu:score+=8
    else:score+=5

    return min(score,100)


if st.button('Predict Price'):
    # query
    ppi=None
    if touchscreen == 'Yes':
        touchscreen =1
    else:
        touchscreen=0

    if ips == 'Yes':
        ips=1
    else:
        ips=0
    

    X_res=int(resolution.split('x')[0])
    Y_res=int(resolution.split('x')[1])
    if screen_size ==0:
        st.warning("Please enter a valid screen size")
    else:

        ppi=((X_res**2) +(Y_res**2))**0.5/screen_size
    #query=np.array([int(touchscreen),int(ips),float(ppi),int(hdd),int(ssd)])
        query_df=pd.DataFrame([[company,type,int(ram),float(weight),int(touchscreen),int(ips),float(ppi),cpu,int(hdd),int(ssd),gpu,os]],
                          columns=['Company','TypeName','Ram','Weight','Touchscreen','IPS','ppi','Cpu_Brand','HDD','SSD','Gpu_brand','os'])
        
        predicted_price=(int(np.exp(pipe.predict(query_df)[0])))

        ## Show the predicted Price
        st.title(f"Prediced price: {predicted_price}")
        ## Price Range Indicator
        if predicted_price <= 30000:
            st.success("Budget Laptop")
        elif predicted_price <= 60000:
            st.info("Mid -Range Laptop ")
        elif predicted_price <= 100000:
            st.warning("Preminum plaptop")
        else:
            st.error("Ultra preminum laptop")


        ## Deal Score
        st.subheader('Deal Score')
        score=calculate_deal_score(predicted_price,ram,ssd,cpu,gpu)

        st.metric('Value Score',f"{score}/100")

        if score >= 80:
            st.success("Excellent deal !! Must Buy")
        elif score >= 60:
            st.info("Good deal")
        elif score >= 40:
            st.warning("Average Deal")
        else:
            st.error("Poor Value for Money")


        ## Similar laptop
        st.subheader("Similar-Laptop")
        df['actual_price']=df['Price'].apply(lambda x: int(x))
        similar = df[
            (df['Company'] == company) &
            (df['Ram'] == ram)
        ][['Company','TypeName','Ram','Cpu_Brand','actual_price']].head(5)

        if similar.empty:
            similar=df[
                df['Ram']==ram
            ][['Company','TypeName','Ram','Cpu_Brand','actual_price']].head(5)

        st.dataframe(similar)

st.header("Find Best Laptop")
budget=st.number_input('Enter your Budget ₹ ',min_value=10000,
                       max_value=500000,value=50000)

if st.button('Find Best Laptop'):
        df['actual_price']=df['Price'].apply(lambda x: int(x)
        )
        budget_laptops = df[
            df['actual_price'] <= budget
        ].sort_values('actual_price',ascending=False)[
            ['Company','TypeName','Ram','Cpu_Brand','SSD','HDD','actual_price']
        ].head(5)

        if budget_laptops.empty:
            st.warning("No Laptop found in this budget !!")
        else:
            st.success(f"Top 5 Laptops under budget ₹{budget}")
            st.dataframe(budget_laptops)

st.header("Laptop vs Laptop Comparator")

col1,col2 = st.columns(2)
with col1:
        st.markdown("#### Laptop 1")
        company1=st.selectbox('Brand',df['Company'].unique(),key='c1')

        type1=st.selectbox('Type',df['TypeName'].unique(),key='t1')

        ram1=st.selectbox('Ram(GB)',[2,4,6,8,16,32,64],key='r1')

        weight1=st.number_input('Weight',min_value=0.5,max_value=5.0,value=2.0,key='w1')

        touchscreen1=st.selectbox('TouchScreen',['Yes','No'],key='ts1')

        ips1=st.selectbox('IPS',['No','Yes'],key='ips1')

        screen1=st.number_input('Screen Size',min_value=10.0,max_value=20.0,value=15.6,key='s1')

        resolution1=st.selectbox('Resolution',['1920x1080','1366x768','1600x900','3840x2160'],key='res1')

        cpu1=st.selectbox('Cpu',df['Cpu_Brand'].unique(),key='cpu1')

        hdd1=st.selectbox('HDD(GB)',[0,128,256,512,1022,2048],key='hdd1')

        ssd1=st.selectbox('SSD(GB)',[0,8,128,256,512,1024],key='ssd1')

        gpu1=st.selectbox('GPU',df['Gpu_brand'].unique(),key='gpu1')

        os1=st.selectbox('OS',df['os'].unique(),key='os1')

with col2:
        st.markdown('##### Laptop 2')
        company2=st.selectbox('Brand',df['Company'].unique(),key='c2')

        type2=st.selectbox('Type',df['TypeName'].unique(),key='t2')

        ram2=st.selectbox('RAM(GB)',[2,4,6,8,16,32,64],key='r2')

        weight2=st.number_input('Weight',min_value=0.5,max_value=5.0,value=2.0,key='w2')

        touchscreen2=st.selectbox('TouchScreen',['Yes','No'],key='ts2')

        ips2=st.selectbox('IPS',['No','Yes'],key='ips2')

        screen2=st.number_input('Screen Size',min_value=10.0,max_value=20.0,value=15.6,key='s2')

        resolution2=st.selectbox('Resolution',['1920x1080','1366x768','1600x900','3840x2160'],key='res2')

        cpu2=st.selectbox('Cpu',df['Cpu_Brand'].unique(),key='cpu2')

        hdd2=st.selectbox('HDD(GB)',[0,128,256,512,1022,2048],key='hdd2')

        ssd2=st.selectbox('SSD(GB)',[0,8,128,256,512,1024],key='ssd2')

        gpu2=st.selectbox('GPU',df['Gpu_brand'].unique(),key='gpu2')

        os2=st.selectbox('OS',df['os'].unique(),key='os2')

if st.button('Compare laptop'):
        ## Process laptop1
        ts1= 1 if touchscreen1 =='Yes' else 0
        i1=1 if ips1 =='Yes' else 0
        xr1=int(resolution1.split('x')[0])
        yr1=int(resolution1.split('x')[1])
        ppi1=((xr1**2) + (yr1**2))**0.5/screen1

        q1=pd.DataFrame([[company1,type1,int(ram1),float(weight1),ts1,i1,float(ppi1),cpu1,int(hdd1),int(ssd1),gpu1,os1]],
                        columns=['Company','TypeName','Ram','Weight','Touchscreen','IPS','ppi','Cpu_Brand','HDD','SSD','Gpu_brand','os'])
        price1=int(np.exp(pipe.predict(q1)[0]))

        ## Process laptop 2
        ts2=1 if touchscreen2 == 'Yes' else 0
        i2=1 if ips2 == 'Yes' else 0
        xr2=int(resolution2.split('x')[0])
        yr2=int(resolution2.split('x')[1])
        ppi2=((xr2**2) +(yr2**2))**0.5/screen2

        q2=pd.DataFrame([[company2,type2,int(ram2),float(weight2),ts2,i2,float(ppi2),cpu2,int(hdd2),int(ssd2),gpu2,os2]],
                        columns=['Company','TypeName','Ram','Weight','Touchscreen','IPS','ppi','Cpu_Brand','HDD','SSD','Gpu_brand','os'])
        
        price2=int(np.exp(pipe.predict(q2)[0]))

        ## Show the comparison table
        st.subheader("Comparison Result")
        comp_df=pd.DataFrame({
            'Feature':['Brand','Type','Ram','Weight','TouchScreen','IPS','CPU','HDD','SSD','GPU','OS','Predicted Price'],
            'Laptop1':[company1,type1,f"{ram1}in GB",f"{weight1}kg",touchscreen1,ips1,cpu1,f"{hdd1}GB",f"{ssd1}GB",gpu1,os1,f"₹{price1}"],
            'Laptop2':[company2,type2,f"{ram2}GB",f"{weight2}kg",touchscreen2,ips2,cpu2,f"{hdd2}GB",f"{ssd2}GB",gpu2,os2,f"₹{price2}"]

        })
        st.dataframe(comp_df)

        ## Winner Announcement
        if price1 < price2:
            st.success(f"Laptop 1 is cheaper  by {price2-price1}")
        elif price2 < price1:
            st.success(f"Laptop 2 is cheaper by {price1-price2}")
        else:
            st.info("Both laptops are similar priced")

                        

        






















