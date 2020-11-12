
# import libraries


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np



def get_map(df): 
    
    fips_df = pd.read_csv('EDA/hello_fips.csv', header=None)
    fips_df['CountyName'] = fips_df[1]  
    fips_df['code'] = fips_df[2].astype(object)
    fips_df.drop(columns=[0, 2, 1], axis=1, inplace=True)
    fips_df.drop(0, axis=0, inplace=True)
    
    
    for item in fips_df.code:
        item_new = str(item)
        item_new = item_new[4:]
        fips_df['code'] = fips_df['code'].replace(item, item_new)
        
    
    df_viz = df.merge(fips_df, on='CountyName', how='left')
    
    counties = list(df_viz.CountyName.unique())
    
    eng = []
    absent = []
    enroll = []
    englearner = []
    ssuburban = []
    srural = []
    stown = []
    scity = []
    socioecon = []

    for item in counties:
        c_df = df[df['CountyName'] == item]

        eng.append(c_df.ELAStdMetPct.mean())
        enroll.append(c_df.EnrollTotal.mean())
        englearner.append(c_df.EnglishLearnerPct.mean())
        absent.append(c_df.AbsentPct.mean())
        ssuburban.append(c_df.suburban.sum())
        srural.append(c_df.rural.sum())
        stown.append(c_df.town.sum())
        scity.append(c_df.city.sum())
        socioecon.append(c_df.SocioEconDisadvantagePct.mean())
        
        
        county_dict =  [{'CountyName':counties, 'Score':eng, 'Absent':absent, 'Enroll':enroll, 'EngLearner':englearner, 'Suburban':ssuburban, 'Rural':srural, 'Town':stown, 'City':scity, 'SocioEconDis':socioecon} for counties, eng, absent, enroll, englearner, ssuburban, srural, stown, scity, socioecon in zip(counties,eng,absent,enroll,englearner, ssuburban, srural, stown, scity, socioecon)]
        
        countydf = pd.DataFrame.from_dict(county_dict)
        countydf = countydf.merge(fips_df, on='CountyName', how='left')
        countydf['Score'] = countydf['Score'].round().astype('int64')

        
        return county_df



