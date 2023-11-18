import csv
import pandas as pd
import json

##for json##
# data = {}
# with open("paired_contributors.json", "r") as json_file:
#     data = json.load(json_file)
# for key in data.keys():
#     data[key]['no'] = data[key]['cfc']/(data[key]['tot_followers_c1']+data[key]['tot_followers_c2'])
#     data[key]['sim'] = data[key]['clc']/(data[key]['tot_labels_c1']+data[key]['tot_labels_c2'])

# no_value = 0
# sim_value = 0
# sim_no = 0
# for key in data.keys():
#     if(data[key]['no']!=0 and data[key]['sim']!=0):
#       sim_no = sim_no+1
#     if(data[key]['sim']!=0):
#         sim_value = sim_value+1
#     if(data[key]['no']!=0):
#         no_value= no_value+1      

# print(sim_value)
# print(sim_no) 
# print(no_value)       
# obs_prob = sim_no/sim_value
# obs_prob1 = sim_no/no_value
# print(obs_prob)            
# print(obs_prob1)


# exit()

##for csv##
# df = pd.read_csv('ContributorDetails.csv')
# new_df = df
# new_df['n_overlap'] = None
# new_df['similarity'] = None

# print(df.iloc[:, 1])
# exit()

# for i in range(0, len(df['contributor1'])):
#     no = df['cfc'][i]/(df['tot_followers_c1'][i]+df['tot_followers_c2'][i])
#     sim = df['clc'][i]/(df['tot_labels_c1'][i]+df['tot_labels_c2'][i])
#     new_df.at[i, 'n_overlap'] = no
#     new_df.at[i, 'similarity'] = sim  
# new_df.to_csv('check_similarity.csv')
# exit()
from ContributorDetails import get_contri_dict
# file_df = pd.read_csv("test.csv")
# contri_dict = get_contri_dict(file_df)
def create_labels_dict(contri_dict):
    labels1 = {}
    for each in contri_dict:
        if(contri_dict[each]['contributor1'] not in labels1):
            labels1[contri_dict[each]['contributor1']]=set(contri_dict[each]['c1_labels'])
        if(contri_dict[each]['contributor2'] not in labels1):
            labels1[contri_dict[each]['contributor2']]=set(contri_dict[each]['c2_labels'])
    return labels1
# labels = create_labels_dict(contri_dict)
# 
def create_followers_dict(contri_dict):
    followers1 = {}
    for each in contri_dict:
        if(contri_dict[each]['contributor1'] not in followers1):
            followers1[contri_dict[each]['contributor1']]=set(contri_dict[each]['c1_followers'])
        if(contri_dict[each]['contributor2'] not in followers1):
            followers1[contri_dict[each]['contributor2']]=set(contri_dict[each]['c2_followers'])
    return followers1            
# followers = create_followers_dict(contri_dict)
import networkx as nx

def common_follower_graph(contri_dict):
    G = nx.Graph()
    for each in contri_dict:
        if(contri_dict[each]['cfc']!=0):
            G.add_edge(contri_dict[each]['contributor1'],contri_dict[each]['contributor2'])
    return G     

def common_label_graph(contri_dict):
    G = nx.Graph()
    for each in contri_dict:
        if(contri_dict[each]['clc']!=0):
            G.add_edge(contri_dict[each]['contributor1'],contri_dict[each]['contributor2'])
    return G      

def observed_probability_followers(graph, labels):
    common_interests = []
    
    for u, v in graph.edges():
        if set(labels[u]).intersection(labels[v]):
            common_interests.append((u, v))
    common_neighbors= len(graph.edges())
    # print((common_neighbors))
    # print(len(common_interests))    
    return len(common_interests) / (common_neighbors) if common_interests else 0

def observed_probability_labels(graph, followers):
    common_followers = []
    for u, v in graph.edges():
        if set(followers[u]).intersection(followers[v]):
            common_followers.append((u, v))
        common_labels= len(graph.edges())
    # print((common_labels))
    # print(len(common_followers))    
    return len(common_followers) / (common_labels) if common_followers else 0

import numpy as np
import random

def get_expected_prob_followers(G,labels):
    expected_probs = []
    num_permutations = 1000
    all_interests = set(interest for interests in labels.values() for interest in interests)
    for _ in range(num_permutations):
        # Randomly shuffle user interests
        
        shuffled_interests = {}
        for user, interests in labels.items():
            shuffled_interests[user] = random.sample(all_interests, len(interests))
        # print(shuffled_interests)
        # Calculate the probability for the shuffled data
        expected_prob = observed_probability_followers(G, shuffled_interests)
        expected_probs.append(expected_prob)
    # print(expected_probs)    
    return expected_probs    
# labels = create_labels_dict(contri_dict)
# followers = create_followers_dict(contri_dict)

# follower_graph = common_follower_graph(contri_dict)
# label_graph = common_label_graph(contri_dict)
# follower_observed_prob = observed_probability_followers(follower_graph, labels)
# label_observed_prob = observed_probability_labels(label_graph, followers)
        
# expected_probs = get_expected_prob_followers(follower_graph,labels)
# num_permutations = 1000
# p_value = (np.sum(np.array(expected_probs) >= follower_observed_prob) + 1) / (num_permutations + 1)

# print(f"Observed Probability Followers: {follower_observed_prob}")
# print(f"P-Value: {p_value}")

# expected_probs_labels = get_expected_prob_labels(label_graph,followers)
# num_permutations = 1000
# p_value = (np.sum(np.array(expected_probs_labels) >= label_observed_prob) + 1) / (num_permutations + 1)

# print(f"Observed Probability Labels: {label_observed_prob}")
# print(f"P-Value: {p_value}")

