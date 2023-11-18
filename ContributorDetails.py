###Lists all contributors associated with each label###
import csv
from tokenize import Ignore
import pandas as pd
import json
import networkx as nx
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import itertools
import pickle

##for csv file###
# f = "test.csv"
# df = pd.read_csv(f)
#List Common Labels and Followers for each pair of contributors
def get_contri_dict(df):
    contributor_dict = {}
    for i in range(0, len(df['contrib_name'])):
        contributor1= df['contrib_name'][i]
        if(len(df['labels'][i].replace("[","").replace("]","").replace("'","").replace(" ","").split(",")[0])==0):
            c1_labels = []
        else:
            c1_labels = df['labels'][i].replace("[","").replace("]","").replace("'","").replace(" ","").split(",")

        if(len(df['followers'][i].replace("[","").replace("]","").replace("'","").replace(" ","").split(",")[0])==0):
            c1_followers = []
        else:
            c1_followers = df['followers'][i].replace("[","").replace("]","").replace("'","").replace(" ","").split(",")
        for j in range(0, len(df['contrib_name'])):
            contributor2 = df['contrib_name'][j]
            if(len(df['labels'][j].replace("[","").replace("]","").replace("'","").replace(" ","").split(",")[0])==0):
                c2_labels = []
            else:
                c2_labels = df['labels'][j].replace("[","").replace("]","").replace("'","").replace(" ","").split(",")

            if(len(df['followers'][j].replace("[","").replace("]","").replace("'","").replace(" ","").split(",")[0])==0):
                c2_followers = []
            else:
                c2_followers = df['followers'][j].replace("[","").replace("]","").replace("'","").replace(" ","").split(",")
            if(contributor1!=contributor2):
                if(set(c1_labels)&set(c2_labels)):
                    common_labels = set(c1_labels)&set(c2_labels)
                else:
                    common_labels = set()
                if(set(c1_followers)&set(c2_followers)):
                    common_followers = set(c1_followers)&set(c2_followers)
                else:
                    common_followers = set()    
                c1c2 = str(max(contributor1, contributor2))+"_"+str(min(contributor1, contributor2))
                if((c1c2 not in contributor_dict) and ((len(common_followers)!=0) or (len(common_labels)!=0)) 
                and (len(c1_labels)!=0 and len(c2_labels)!=0) and (len(c1_followers)!=0 and len(c2_followers)!=0)):
                    contributor_dict[c1c2]={}
                    contributor_dict[c1c2]['contributor1'] = contributor1
                    contributor_dict[c1c2]['contributor2'] = contributor2
                    contributor_dict[c1c2]['common_labels'] = common_labels
                    contributor_dict[c1c2]['common_followers'] = common_followers
                    contributor_dict[c1c2]['clc'] = len(common_labels)
                    contributor_dict[c1c2]['cfc'] = len(common_followers)
                    contributor_dict[c1c2]['tot_labels_c1'] = len(c1_labels)
                    contributor_dict[c1c2]['tot_labels_c2'] = len(c2_labels)
                    contributor_dict[c1c2]['tot_followers_c1'] = len(c1_followers)
                    contributor_dict[c1c2]['tot_followers_c2'] = len(c2_followers)
                    contributor_dict[c1c2]['c1_labels'] = (c1_labels)
                    contributor_dict[c1c2]['c2_labels'] = (c2_labels)
                    contributor_dict[c1c2]['c1_followers'] = (c1_followers)
                    contributor_dict[c1c2]['c2_followers'] = (c2_followers)
                    
    return contributor_dict
# contributor_dict = get_contri_dict(df)                
# new_df = pd.DataFrame(contributor_dict).transpose()
# print(new_df)
# new_df.to_csv("ContributorDetails.csv")



    