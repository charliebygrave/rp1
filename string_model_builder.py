#!/usr/bin/env python
# coding: utf-8

# In[5]:


import pandas as pd


# In[6]:


df = pd.read_csv('string-network-1.csv')
df.head()


# In[7]:


# get list of nodes

nodes = df.node1.unique()


# In[8]:


nodes


# In[9]:


# build dict of node inputs

node_inputs = {}
for node in nodes:
    inputs = list(df[df.node1 == node].node2)
    node_inputs[node] = inputs


# In[10]:


# construct boolean rules as list
rules = []
for key, value in node_inputs.items():
    rule = key + ' *= '
    rule = rule + ' and '.join(value)
    rules.append(rule)


# In[11]:


# construct initial conditions
initial_conditions = []
for node in nodes:
    initial_condition = node + ' = Random'
    initial_conditions.append(initial_condition)


# In[12]:


# export model
definition = '#initial conditions\n'+'\n'.join(initial_conditions)+'\n\n#rules\n'+'\n'.join(rules)
fp = open('model.txt', 'w')
fp.write(definition)
fp.close()


# In[13]:


inp = file('model.txt').read()


# In[34]:


# write export helper functions

def string2definition(tabular_text_output, initial_node_value, out='model.txt'):
    df = pd.read_csv(tabular_text_output)
    
    # get list of nodes
    nodes = df.node1.unique()
    
    # build dict of node inputs
    node_inputs = {}
    for node in nodes:
        inputs = list(df[df.node1 == node].node2)
        node_inputs[node] = inputs
        
    # construct boolean rules as list
    rules = []
    for key, value in node_inputs.items():
        rule = key + ' *= '
        rule = rule + ' or '.join(value)
        rules.append(rule)
        
    # construct initial conditions
    initial_conditions = []
    for node in nodes:
        initial_condition = node + ' = ' + initial_node_value
        initial_conditions.append(initial_condition)
        
    # definition
    definition = '#initial conditions\n'+'\n'.join(initial_conditions)+'\n\n#rules\n'+'\n'.join(rules)

#     # export
#     fp = open(out, 'w+')
#     fp.write(definition)
#     fp.close()
    
    return definition
        


# In[45]:


def add_process_edgelist(definition, edgelist, initial_process_value):
    df = pd.read_csv(edgelist)
    
    # get list of nodes
    nodes = df.process.unique()

    # build dict of node inputs
    node_inputs = {}
    for node in nodes:
        inputs = list(df[df.process == node].node)
        node_inputs[node] = inputs
        
    # construct boolean rules as list
    rules = []
    for key, value in node_inputs.items():
        rule = key + ' *= '
        rule = rule + ' and '.join(value)
        rules.append(rule)
        
    # construct initial conditions
    initial_conditions = []
    for node in nodes:
        initial_condition = node + ' = ' + initial_process_value
        initial_conditions.append(initial_condition)
        
    # definition
    return definition + '\n\n#process node initial conditions\n'+'\n'.join(initial_conditions)+'\n\n#process node rules\n'+'\n'.join(rules)


# In[63]:


def add_mtb_edgelist(definition, edgelist, initial_mtb_value):
    df = pd.read_csv(edgelist)

    # get list of nodes
    target_nodes = df.node.unique()
    mtb_nodes = df.mtb.unique()
    
    # build dict of node inputs
    node_inputs = {}
    for node in target_nodes:
        inputs = list(df[df.node == node].mtb)
        node_inputs[node] = inputs
    
    # construct boolean rules as list
    rules = []
    for key, value in node_inputs.items():
        rule = key + ' *= ' + key
        rule = rule + ' and not (' +' or '.join(value) + ')'
        rules.append(rule)

    # construct initial conditions
    initial_conditions = []
    for node in mtb_nodes:
        initial_condition = node + ' = ' + initial_mtb_value
        initial_conditions.append(initial_condition)
        
    # definition
    return definition + '\n\n#mtb node initial conditions\n'+'\n'.join(initial_conditions)+'\n\n#mtb update rules\n'+'\n'.join(rules)

    


# In[64]:


# print add_mtb_edgelist(definition, 'mtb-edgelist.csv', 'True')


# In[ ]:




