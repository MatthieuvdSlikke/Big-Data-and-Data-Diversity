
# coding: utf-8

# # Task 3
# # Q1

# In[ ]:


#the code below is directly inspired by the code given in the tutorial 10.


# In[ ]:


import requests
import json
import csv 
import time
from itertools import islice

base_url = 'http://maps.googleapis.com/maps/api/geocode/json'

with open('geoNeighbourhoods.csv', 'w') as csvfile:
    
    fieldnames = ['area_name', 'northeast_lat', 'northeast_lng','southwest_lat', 'southwest_lng']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
   
    with open('Neighbourhoods.csv', newline='') as File:  
        
        reader = csv.reader(File)
        next(reader, None)  
        
        for row in reader:   
                count=0
                string = row[1]
                print(string)
                count = string.count(' - ')
                print(count)
                maxNhood_Nlat=0
                maxNhood_Nlng=0
                maxNhood_Slat=0
                maxNhood_Slng=0

                if count==0: 
                    
                    my_params= {'address':"%s, Australia" %(row[1] ),'language':'en'}
                    response = requests.get(base_url, params = my_params)
                    results      = response.json()['results']
                    time.sleep(2)
                    if results :
                        maxNhood_Nlat=results[0]['geometry']['bounds']['northeast']['lat']
                        maxNhood_Nlng=results[0]['geometry']['bounds']['northeast']['lng']
                        maxNhood_Slat=results[0]['geometry']['bounds']['southwest']['lat']
                        maxNhood_Slng=results[0]['geometry']['bounds']['southwest']['lng']

                else:
                   
                    mylist = string.split(" - ")
                    for word in mylist:

                        my_params= {'address':"%s, Australia" %(word),'language':'en'}
                        response = requests.get(base_url, params = my_params)
                        results      = response.json()['results']
                        time.sleep(2)
                        if results :
                            nNhood_Nlat=results[0]['geometry']['bounds']['northeast']['lat']
                            nNhood_Nlng=results[0]['geometry']['bounds']['northeast']['lng']
                            nNhood_Slat=results[0]['geometry']['bounds']['southwest']['lat']
                            nNhood_Slng=results[0]['geometry']['bounds']['southwest']['lng']
                            if maxNhood_Nlat==0:
                                maxNhood_Nlat=nNhood_Nlat
                            else:
                                if nNhood_Nlat<maxNhood_Nlat:
                                    maxNhood_Nlat=nNhood_Nlat
                            if maxNhood_Nlng==0:
                                maxNhood_Nlng=nNhood_Nlng
                            else:
                                if nNhood_Nlng<maxNhood_Nlng:
                                    maxNhood_Nlng=nNhood_Nlng
                            if maxNhood_Slat==0:
                                maxNhood_Slat=nNhood_Slat
                            else:
                                if nNhood_Slat>maxNhood_Slat:
                                    maxNhood_Slat=nNhood_Slat
                            if maxNhood_Slng==0:
                                maxNhood_Slng=nNhood_Slng
                            else:
                                if nNhood_Slng>maxNhood_Slng:
                                    maxNhood_Slng=nNhood_Slng

            #the max_values are used to calculate the furthest boundaries. This way we can find the points within these boundaries

                print("northeast lat", maxNhood_Nlat)
                print("northeast lng", maxNhood_Nlng)
                print("southwest lat", maxNhood_Slat)
                print("southwest lng", maxNhood_Slng)

                writer.writerow({'area_name':row[1], 'northeast_lat':maxNhood_Nlat, 'northeast_lng':maxNhood_Nlng,'southwest_lat':maxNhood_Slat, 'southwest_lng':maxNhood_Slng})


# In[ ]:


#We than processed to clean the data by changing thecode accordingly. 
#Go through the created csv file and check where there where 0 boundaries to recalculate them
#the problem we mostly we encountered is that the request json wouldn't be fast enough so we had to change the sleep.time function accordingly too
#once we cleaned the data, we use it to do the spatial join by checking if the point would lie between the boundaries 

