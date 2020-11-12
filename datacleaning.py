# Import Libraries

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import warnings; warnings.simplefilter('ignore')
pd.set_option('display.max_columns', 300)
from sklearn.model_selection import train_test_split
import statsmodels.api as sm
import scipy.stats as stats
from statsmodels.formula.api import ols
from sklearn.model_selection import train_test_split 
from sklearn.dummy import DummyClassifier
from statsmodels.graphics.regressionplots import abline_plot
from sklearn.metrics import mean_squared_error
sns.set_style('darkgrid')
from sklearn import metrics
from sklearn.metrics import recall_score
from sklearn.model_selection import cross_validate
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import PolynomialFeatures


#Import data set
df = pd.read_csv('data/California_School_District_Areas_2018-19.csv')
pd.set_option('display.max_columns', None)

def clean(df):
    #rename columns to make easier to understand
    df.rename(columns=
           {'DistrictName': 'SchoolName',
            'DistrictType': 'SchoolType',
            'AAcount': 'AfricanAmerican',
            'AApct': 'AfricanAmericanPct',
            'AIcount': 'AmericanIndian',
            'AIpct': 'AmericanIndianPct',
            'AScount': 'Asian',
            'ASpct': 'AsianPct',
            'FIcount': 'Filipino',
            'FIpct': 'FilipinoPct',
            'HIcount': 'Hispanic',
            'HIpct': 'HispanicPct',
            'MRcount': 'MultipleRace',
            'MRpct': 'MultipleRacePct',
            'PIcount': 'PacificIslander',
            'PIpct': 'PacificIslanderPct',
            'WHcount': 'White',
            'WHpct': 'WhitePct',
            'NRcount': 'RaceNotReported',
            'NRpct': 'RaceNotReportedPct',
            'ELcount': 'EnglishLearner',
            'ELpct': 'EnglishLearnerPct',
            'FOScount': 'Foster',
            'FOSpct': 'FosterPct',
            'HOMcount': 'Homeless',
            'HOMpct': 'HomelessPct',
            'MIGcount': 'Migrant',
            'MIGpct': 'MigrantPct',
            'SWDcount': 'Disability',
            'SWDpct': 'DisabilityPct',
            'SEDcount': 'SocioEconDisadvantage',
            'SEDpct': 'SocioEconDisadvantagePct',
            'UPcount': 'Unduplicated',
            'UPpct': 'UnduplicatedPct'
            },
              inplace=True)
    
    #scale outliers down to highest non-outlier value
    df.loc[df['AfricanAmericanPct'] >= 30, 'AfricanAmericanPct'] = 30
    df.loc[df['AmericanIndianPct'] >= 40, 'AmericanIndianPct'] = 40
    df.loc[df['MultipleRacePct'] >= 30, 'MultipleRacePct'] = 30
    df.loc[df['PacificIslanderPct'] >= 10, 'PacificIslanderPct'] = 10
    df.loc[df['HomelessPct'] >= 40, 'HomelessPct'] = 40
    df.loc[df['MigrantPct'] >= 22, 'MigrantPct'] = 22
    df.loc[df['Unduplicated'] >= 50000, 'Unduplicated'] = 50000
    df.loc[df['EnrollCumulative'] >= 100000, 'EnrollCumulative'] = 100000
        
    df['AbsentPct'] = df['AbsentPct'].replace(np.NaN, 0)
    df['EnrollCumulative'] = df['EnrollCumulative'].replace(np.NaN, 0) 
    df['SuspPct'] = df['SuspPct'].replace(np.NaN, 0) 
    
    return df 


def dataprep(df):
    
    #create bins for district enrollment size based on quartile ranges
    df['smallenrollment'] = np.where( 
                            df['EnrollTotal'] <= df['EnrollTotal'].quantile(0.25), 1, 0)
    
    df['mediumenrollment'] = np.where(
                            ((df['EnrollTotal'] > df['EnrollTotal'].quantile(0.25)) & 
                            (df['EnrollTotal'] <= df['EnrollTotal'].quantile(0.5))), 1, 0)
    df['largeenrollment'] = np.where(
                            ((df['EnrollTotal'] > df['EnrollTotal'].quantile(0.5)) & 
                             (df['EnrollTotal'] <= df['EnrollTotal'].quantile(0.75))), 1, 0)
    df['xlenrollment'] = np.where(
                        (df['EnrollTotal'] > df['EnrollTotal'].quantile(0.75)), 1, 0)
    
    
    #convert charter school enrollment into percentages of total enrollment
    df['charterpct'] = df['EnrollCharter'] / df['EnrollTotal'] * 100
    df['noncharterpct'] = df['EnrollNonCharter'] / df['EnrollTotal'] * 100
    
    #convert the type of district into dummy variables
    df['unified'] = np.where(df['SchoolType'] == 'Unified', 1, 0)
    df['elem'] = np.where(df['SchoolType'] == 'Elementary', 1, 0)
    df['high'] = np.where(df['SchoolType'] == 'High', 1, 0)
    
    #group locale district types by classification and create dummy variables
    df['LocaleDistrict'] = [ x[:2] for x in df['LocaleDistrict']]
    df['suburban'] = np.where(
                            ((df['LocaleDistrict'] == '21') | 
                            (df['LocaleDistrict'] == '23')), 1, 0)
    
    df['rural'] = np.where(
                    ((df['LocaleDistrict'] == '41') | 
                     (df['LocaleDistrict'] == '42') | 
                     (df['LocaleDistrict'] == '43')), 1, 0)
    
    df['town'] = np.where(
                    ((df['LocaleDistrict'] == '32') | 
                     (df['LocaleDistrict'] == '33')), 1, 0)
    df['city'] = np.where(
                    ((df['LocaleDistrict'] == '12') | 
                     (df['LocaleDistrict'] == '11') | 
                     (df['LocaleDistrict'] == '13')), 1, 0)
    
    #create categorical variable for grouped locales
    df['Locale'] = df['LocaleDistrict'].map(
                    {'41' : 'Rural', '42' : 'Rural', '42' : 'Rural', 
                     '21' : 'Suburban', '22' : 'Suburban', 
                     '32' : 'Town', '33' : 'Town', 
                     '12': 'City', '11': 'City', '13' : 'City'})
    
    #create dummy variable for government assistance
    df['assistance'] = np.where(df['AssistStatus'] == 'Differentiated Assistance', 1, 0)
    
    #create target variable by binning using the 75% quantile value as the metric for if the school is 'on track'
    df['target'] = np.where(df.ELAStdMetPct >= 61.225, 1, 0)
    
    #drop all columns that have been used to create dummies or other variables
    df = df.drop(columns = 
            ['EnrollTotal', 'EnrollCharter', 'EnrollNonCharter', 'SchoolType', 
             'AssistStatus', 'ELATested'], axis = 1)
    
    #drop columns that will not be used or are repetitive 
    df = df.drop(columns=['OBJECTID', 'FedID', 'CDCode', 'CDSCode', 'UpdateNotes', 
                     'AfricanAmerican', 'AmericanIndian', 'Asian', 'Filipino', 
                     'Hispanic', 'MultipleRace', 'PacificIslander', 'White', 
                     'RaceNotReported', 'EnglishLearner', 'Foster', 'Homeless', 
                     'Migrant', 'Disability', 'SocioEconDisadvantage', 'MathTested', 
                     'MathStdMetPct', 'CCPrepCohortCount', 'AbsentEligCount', 
                     'GradCohortCount', 'GradeLowCensus', 'GradeHighCensus'], axis = 1)
    
    #drop columns that contain significant null values and are criteria that only apply to high schools
    df = df.drop(columns = 
            ['CCPrepPct', 'GradPct', 'UCCSUReqMetPct', 'DropOutPct'], axis = 1)
    
    
    return df
    

    
    
    