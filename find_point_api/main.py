#find missing point easy api
#
#
# W.Netpuggana (wongsaton05@gmail.com)
# History : v.0.1 , 25/09/2022
#
#


import json
import math
import pyproj 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://127.0.0.1",
    "http://localhost",
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




@app.get("/")
def root():
    json_result = {'hello':'world'}
    return json_result

@app.get("/{e1}/{n1}/{e2}/{n2}/{from1}/{from2}/{zone}")

def get_intersections(e1: float, e2: float,n2: float,n1: float,from1: float, from2: float,zone:int):
    # circle 1: (x0, y0), radius r0
    # circle 2: (x1, y1), radius r1

    d=math.sqrt((e2-e1)**2 + (n2-n1)**2)
    
    # non intersecting
    if d > from1 + from2 :
        return None
    # One circle within other
    if d < abs(from1-from2):
        return None
    # coincident circles
    if d == 0 and from1 == from2:
        return None
    else:
        a=(from1**2-from2**2+d**2)/(2*d)
        h=math.sqrt(from1**2-a**2)
        x2=e1+a*(e2-e1)/d   
        y2=n1+a*(n2-n1)/d   
        x3=x2+h*(n2-n1)/d     
        y3=y2-h*(e2-e1)/d 

        x4=x2-h*(n2-n1)/d
        y4=y2+h*(e2-e1)/d
        

        proj_wgs84 = pyproj.Proj(init="epsg:4326")
        if zone == 47:
            proj_in  = pyproj.Proj(init="epsg:32647")
        else:
            proj_in = pyproj.Proj(init="epsg:32648")
        lonp1, latp1 = pyproj.transform(proj_in, proj_wgs84, e1,n1)
        lonp2, latp2 = pyproj.transform(proj_in, proj_wgs84, e2,n2)
        lonf1, latf1 = pyproj.transform(proj_in, proj_wgs84, x3,y3)
        lonf2, latf2 = pyproj.transform(proj_in, proj_wgs84, x4,y4)
        
        json_result = {'lonp1':lonp1 , 'latp1': latp1,'lonp2':lonp2,'latp2':latp2 ,'latp2':latp2,'lonf1':lonf1 , 'latf1': latf1,'lonf2':lonf2,'latf2': latf2,'ep1':e1,'np1':n1 ,'ep2': e2,'np2':n2, 'ef1': x3,'nf1':y3, 'ef2': x4,'nf2':y4}

    return json_result
