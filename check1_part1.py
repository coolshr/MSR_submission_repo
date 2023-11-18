###Lists all contributors associated with each label###
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


def create_contributor_dict(processed_data):
    contributor_dict = {}
    for a in range(0,len(processed_data)):
        contributor1 = processed_data[a][0]
        try:
            c1_labels =  processed_data[a][1]['labels'].keys()
        except Exception as e:
            if('labels' not in processed_data[a][1].keys()):
                c1_labels = ''
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
    return contributor_dict

import os
folder = "to_copy"
with open('check_results3.csv','w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Repo','ObsProbFollowers', 'PvalueFollowers','Edge count', 'node count'])
    for filename in os.listdir(folder):
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

            follower_graph = common_follower_graph(contri_dict)
            label_graph = common_label_graph(contri_dict)
            labels = create_labels_dict(contri_dict)
            followers = create_followers_dict(contri_dict)
            follower_observed_prob = observed_probability_followers(follower_graph, labels)
            # label_observed_prob = observed_probability_labels(label_graph, followers)
                    
            expected_probs = get_expected_prob_followers(follower_graph,labels)
            num_permutations = 1000
            p_value = (np.sum(np.array(expected_probs) >= follower_observed_prob) + 1) / (num_permutations + 1)
            print(f"Observed Probability Followers: {follower_observed_prob}")
            print(f"P-Value: {p_value}")

            # expected_probs_labels = get_expected_prob_labels(label_graph,followers)
            # num_permutations = 1000
            # p_value_l = (np.sum(np.array(expected_probs_labels) >= label_observed_prob) + 1) / (num_permutations + 1)
            # print(f"Observed Probability Labels: {label_observed_prob}")
            # print(f"P-Value: {p_value_l}")
            csvwriter.writerow([filename,follower_observed_prob, p_value,len(follower_graph.edges()), len(follower_graph.nodes())])

# print(len(get_contributor_dict))

# with open("paired_contributors.json", "w") as outfile: 
#     json.dump(contributor_dict, outfile)
# exit()

