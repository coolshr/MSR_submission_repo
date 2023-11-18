import csv
from genericpath import isfile
from tokenize import Ignore
import pandas as pd
import json
import networkx as nx
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import itertools
import pickle
from metrics import *
##for pkl file###
#f = "bitnami_containers"


# data[con]['total'] 
# data[con]['labels'][label]


def create_contributor_dict(processed_data):
    # [
    #     ["c1" , data[c1]]
    # ]
    contributor_dict = {}
    for a in range(0,len(processed_data)):
        contributor1 = processed_data[a][0]
        try:
            c1_labels =  processed_data[a][1]['labels'].keys()
            # c1_issues_num = processed_data[a][1]['labels']
        except Exception as e:
            if('labels' not in processed_data[a][1].keys()):
                c1_labels = ''
                # c1_issues_num = {}  
            else:
                print(e)    
        try:
            c1_followers =  processed_data[a][1]['followers']
        except Exception as e:
            
            if('followers' not in processed_data[a][1].keys()):
                c1_followers = '' 
            else:
                print(e)           
        # break
        for b in range(a+1, len(processed_data)):
            contributor2 = processed_data[b][0]
            if(contributor1!=contributor2):
                try:
                    c2_labels =  processed_data[b][1]['labels'].keys()
                    # c2_issues_num = processed_data[b][1]['labels']
                except Exception as e:
                    if('labels' not in processed_data[b][1].keys()):
                        c2_labels = ''
                        # print(len(c2_labels))
                    else:
                        print(e)    
                try:
                    c2_followers =  processed_data[b][1]['followers']
                except Exception as e:
                    if('followers' not in processed_data[b][1].keys()):
                        c2_followers = '' 
                        # print(len(c2_followers))
                    else:
                        print(e)           
                common_followers = set(c1_followers)&set(c2_followers)
                common_labels = set(c1_labels)&set(c2_labels) 
                common_label_issues_c1 = 0
                common_label_issues_c2 = 0
                for label in common_labels:
                    for i in processed_data[a][1]['labels'].keys():
                        if i == label:
                            common_label_issues_c1 += processed_data[a][1]['labels'][i]
                    for i in processed_data[b][1]['labels'].keys():
                        if i == label:
                            common_label_issues_c2 += processed_data[b][1]['labels'][i]
                common_label_issues_c2 = min(common_label_issues_c2, processed_data[b][1]['total'])
                common_label_issues_c1 = min(common_label_issues_c1, processed_data[a][1]['total'])
                c1c2 = str(max(contributor1, contributor2))+"_"+str(min(contributor1, contributor2))
                if((c1c2 not in contributor_dict) and (len(common_followers)!=0 or len(common_labels)!=0) 
                and (len(c1_labels)!=0 and len(c2_labels)!=0) and (len(c1_followers)!=0 and len(c2_followers)!=0)):
                    contributor_dict[c1c2]={}
                    contributor_dict[c1c2]['contributor1'] = contributor1
                    contributor_dict[c1c2]['contributor2'] = contributor2
                    contributor_dict[c1c2]['common_labels'] = list(common_labels)
                    contributor_dict[c1c2]['common_followers'] = list(common_followers)
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
                    contributor_dict[c1c2]['no'] = len(common_followers)/(len(set(c1_followers).union(set(c2_followers))))
                    # contributor_dict[c1c2]['sim'] = (common_label_issues_c1 + common_label_issues_c2)/(processed_data[a][1]['total'] + processed_data[b][1]['total']) # after taking min total issues solved with common labels/total of both contributors
                    contributor_dict[c1c2]['sim'] = len(common_labels)/(len(set(c1_labels).union(set(c2_labels))))
    return contributor_dict

import os
from scipy.stats import spearmanr

import pandas as pd
folder = "./to_copy/"

f_max_no = open("Max_no.csv", 'w')
f_max_sm = open("Max_sm.csv", 'w')


with open('nosm_results_nums.csv','w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Repo','Spearman', 'Pvalue', 'NO', 'SM', 'NO_max', 'SM_max'])
    files = os.listdir(folder)
    # files = ["denoland_deno"]
    for filename in files:
        print(filename)
        f = os.path.join(folder, filename)
        
        if os.path.isfile(f):
            data = {}
            with open(f, 'rb') as ff:
                data = pickle.load(ff)


            processed_data = []
            for contributor in data.keys():
                processed_data.append([contributor, data[contributor]])

            contri_dict = create_contributor_dict(processed_data)
            new_df = pd.DataFrame(columns=['id','no','sim'])
            i = 0
            for each in contri_dict:
                new_df.loc[i] = [each, contri_dict[each]['no'], contri_dict[each]['sim']]
                i = i+1
            # print(new_df)       
            correlation, p_value = spearmanr(new_df['no'], new_df['sim'])
            # sp_corr = new_df['no'].corr(new_df['sim'], method='spearman')
            # pearson_corr = new_df['no'].corr(new_df['sim'])
            # sp_corr1 = new_df['sim'].corr(new_df['no'], method='spearman')
            # pearson_corr1 = new_df['sim'].corr(new_df['no'])
            # print(new_df['no'].corr(new_df['sim'], method='spearman'))
            # print(new_df['no'].corr(new_df['sim']))
            # NO(mean), SM(mean), NO(lowest) corresponding SM, NO(highest) corresponding SM, NO corresponding SM(highest), NO corresponding SM(lowest)
            # total issues scraped
            # num of good issues per repo
            # num of cintributors per repo
            # Remove repos with < 10 cotributors
            max_no = new_df[new_df.no == new_df.no.max()]
            to_write_max_no = max_no['id'].values[0] + " " + str(max_no['no'].values[0]) + " " + str(max_no['sim'].values[0]) 
            # print("max:", max_no)
            min_no = new_df[new_df.no == new_df.no.min()]
            to_write_min_no = min_no['id'].values[0] + " " + str(min_no['no'].values[0]) + " " +str(min_no['sim'].values[0]) 
            max_sim = new_df[new_df.sim == new_df.sim.max()]
            to_write_max_sim = max_sim['id'].values[0] + " " + str(max_sim['no'].values[0]) + " " +str(max_sim['sim'].values[0])
            min_sim = new_df[new_df.sim == new_df.sim.min()]
            to_write_min_sim = min_sim['id'].values[0] + " " + str(min_sim['no'].values[0]) + " " +str(min_sim['sim'].values[0])
            # print(new_df.head())
            csvwriter.writerow([filename, correlation,p_value, new_df['no'].mean(), new_df['sim'].mean(), to_write_max_no, to_write_max_sim])
            print("max_no")
            for i, row in max_no.iterrows():
                # print(str(i))
                f_max_no.write(filename + "," +str(row['id']) + "," +str(row['no']) + "," + str(row['sim']) + "\n" )
            for i, row in max_sim.iterrows():
                f_max_sm.write(filename + "," +str(row['id']) + "," +str(row['no']) + "," + str(row['sim']) + "\n" )
                
f_max_no.close()
f_max_sm.close()