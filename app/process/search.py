import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import AgglomerativeClustering
from sklearn.model_selection import train_test_split
from django.db import connection 
crsr = connection.cursor()

def scaler():
    dataframe=pd.read_sql_query("select * from lgl_address",connection)
    dataframe.to_csv("app/process/data/original.csv",index=False)
    scaledinfo=calculateScaler(dataframe,dataframe[['lgl_address_latitude']],dataframe[['lgl_address_longitude']])
    lat=np.array(scaledinfo[0][0])
    long=np.array(scaledinfo[0][1])
    data=np.concatenate((lat,long),axis=1)
    df = pd.DataFrame(data, columns = ['lgl_address_latitude','lgl_address_longitude'])
    return df

def calculateScaler(dataframe,latitude,longitude): 
    minlatitude=dataframe['lgl_address_latitude'].min()
    minlongitude=dataframe['lgl_address_longitude'].min()
    maxlatitude=dataframe['lgl_address_latitude'].max()
    maxlongitude=dataframe['lgl_address_longitude'].max()
    latitudeScaled=(latitude-minlatitude)/(maxlatitude-minlatitude)
    longitudeScaled=(longitude-minlongitude)/(maxlongitude-minlongitude)
    infoScaled=[[latitudeScaled,longitudeScaled]]
    return infoScaled

def clusterAddresses():
    dataframe=pd.read_sql_query("select * from lgl_address",connection)
    dataframe.to_csv("app/process/data/original.csv",index=False)
    ids=dataframe[['lgl_address_id']]
    df1=scaler()
    clustering_model_no_cluster = AgglomerativeClustering()
    clustering_model_no_cluster.fit(df1[['lgl_address_latitude','lgl_address_longitude']])
    df1['lgl_address_cluster'] = clustering_model_no_cluster.labels_
    hist,bin_edges= np.histogram(df1['lgl_address_cluster'],bins=2)
    b=True
    nClust=2
    j=0
    while b:
        n=nClust 
        for i in range(0,n):
            if (hist[i]>30):
                dft2=df1[df1['lgl_address_cluster']==i]
                clt = AgglomerativeClustering()
                clt.fit(dft2[['lgl_address_latitude','lgl_address_longitude']])
                dft2['lgl_address_cluster'] = (clt.labels_*(nClust))+((clt.labels_-1)*dft2['lgl_address_cluster']*-1)
                df1[df1['lgl_address_cluster']==i]=dft2
                nClust +=1
                j +=1
        hist,bin_edges= np.histogram(df1['lgl_address_cluster'],bins=nClust)  
        if (hist.max()<=30):
            b=False
        df1['lgl_address_id']=ids
        df1.to_csv("app/process/data/addressClustred.csv",index=False)


def getNearestNeigbors(latitude,longitude):
    addressClusterd=pd.read_csv("app/process/data/addressClustred.csv")
    dataframe=pd.read_csv("app/process/data/original.csv")
    infoScaled=calculateScaler(dataframe,latitude,longitude)
    X=addressClusterd[['lgl_address_latitude','lgl_address_longitude']]
    y=addressClusterd["lgl_address_cluster"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)
    knn = KNeighborsClassifier()
    knn.fit(X_train, y_train) 
    knn.score(X_test,y_test)
    pred=knn.predict(infoScaled) 
    return pred 

def setClusterInDB():
    addressClusterd=pd.read_csv("app/process/data/addressClustred.csv")
    cluster=addressClusterd['lgl_address_cluster']
    ids=addressClusterd['lgl_address_id']
    query='update lgl_address set lgl_address_cluster =%s where (lgl_address_id = %s)'
    for (i,j) in zip(ids,cluster):
        dt=(j,i)
        crsr.execute(query,dt)
    connection.commit()
    

def ClusterAndClassifyToDB():
    clusterAddresses()
    setClusterInDB()