import requests
from django.shortcuts import render
import folium
import os
import pandas as pd
import csv

url ='https://covid-193.p.rapidapi.com/statistics'
querystring = {"country":'India'}
headers = {
        'x-rapidapi-host': "covid-193.p.rapidapi.com",
        'x-rapidapi-key': "aaa971c2e7mshf8dba774ebf94d1p186cdbjsn3446a9a0fc8e"
        } 
r = requests.request("GET", url, headers=headers).json()





url = "https://covid19-data.p.rapidapi.com/geojson-ww"

headers = {
    'x-rapidapi-host': "covid19-data.p.rapidapi.com",
    'x-rapidapi-key': "aaa971c2e7mshf8dba774ebf94d1p186cdbjsn3446a9a0fc8e"
    }

response = requests.request("GET", url, headers=headers).json()

with open('kk.csv' , 'w' , newline='') as f:
   
    thewriter = csv.writer(f)
    thewriter.writerow(['Countries' , 'Cases'])
    for i in range(175):
       # k= abs(float(response['features'][i]['properties']['pop_est']) / 1000000.0)
       # g= (abs(float(response['features'][i]['properties']['confirmed'])/k))
        k= (response['features'][i]['properties']['pop_est'] / 1000000.0)
        g=abs(float(response['features'][i]['properties']['confirmed'])/k)    
        if(g>1500):
            thewriter.writerow([ str(response['features'][i]['properties']['iso_a2']) , '1500' ])
            continue
        thewriter.writerow([ str(response['features'][i]['properties']['iso_a2']) ,  str(g) ])   

a=[]
for i in range(175):
    k= (response['features'][i]['properties']['pop_est'] / 1000000.0)
    g=abs(float(response['features'][i]['properties']['confirmed'])/k) 
    n=("%.2f" % round(g, 2))
    data={
        'country' : response['features'][i]['properties']['name'],
        'total' :  response['features'][i]['properties']['confirmed'],
        'active':  n,
        'recovered' : response['features'][i]['properties']['recovered'],
        'deaths' : response['features'][i]['properties']['deaths'],
        'new' :   response['features'][i]['properties']['iso_a2'],
    }
    a.append(data)
a=sorted(a , key= lambda i : int(i['total']))
a=a[::-1]
b=[]
for i in range(0,217):
    data={
        'country' : r['response'][i]['country'],
        'total' :  r['response'][i]['cases']['total'],
        'active':  r['response'][i]['cases']['active'],
        'recovered' : r['response'][i]['cases']['recovered'],
        'deaths' : r['response'][i]['deaths']['total'],
        'new' :  r['response'][i]['cases']['new'],
    }
    b.append(data)
b=sorted(b , key= lambda i : int(i['total']))
b=b[::-1]
b=b[2:11:]


def table(request):
    return render(request,'index.html' , { 'a' : a })   

#context={'b' :b , 'a' : a} 
#def charts(request):
 #   return render(request,'base.html' , context)
c=[]
for i in range(0,217):
    data={
        'country' :  r['response'][i]['country'],
        'new' :  (str(r['response'][i]['cases']['new']).replace("+" , "" ,1)),
                  }
    if(data['new'] == 'None'):
        data['new']='0'
    c.append(data)
                  
c=sorted(c , key= lambda i : int(i['new']))
c=c[::-1]
e=c[0]

def charts(request):  
    #creation of map comes here + business logic
    states = os.path.join(r"world.json")
    unemployement_data = os.path.join("kk.csv")
    state_data = pd.read_csv(unemployement_data)

    h = folium.Map(location=[50.0365 , -5.25], tiles="OpenStreetMap",  zoom_start=2 )

    h.choropleth(
        geo_data=states,
        name='Choropleth',
        data=state_data,
        columns=['Countries' , 'Cases'],
        key_on='feature.properties.iso_a2',
        fill_color='YlGnBu',
        nan_fill_color="#FFFFFF",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Cases per million'
    )

    folium.LayerControl().add_to(h)

    h=h._repr_html_() #updated
    context={'b' :b , 'a' : a, 'my_map': h,'e':e} 

    return render(request,'base.html' , context)
    