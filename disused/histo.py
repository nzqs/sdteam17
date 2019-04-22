
# coding: utf-8

# In[1]:


import plotly
import plotly.graph_objs as go
import pandas as pd
from math import log
plotly.offline.init_notebook_mode(connected = True)


# In[2]:


df = pd.read_csv('Metrics.csv')
gb = df.groupby('InvDescription')
groups = [gb.get_group(x) for x in gb.groups]
materials = []
for dataframe in groups:
    if len(dataframe) > 30:
        materials.append(dataframe.reset_index())
del groups
len(materials)


# In[3]:


df.head(5)


# In[7]:


data = []
for dataframe in materials:
    #datum = go.Histogram(x = dataframe['Run per Set'], name = dataframe['InvDescription'].sample().to_string())
    #datum = go.Histogram(x = dataframe['Run per Set'], name = dataframe['InvDescription'][0])
    #data.append(datum)

    dataframe['Weighted Run'] = dataframe['SetLengthFt'] / dataframe['Run per Set']
    #dataframe['Weighted Run'] = dataframe['Weighted Run'].apply(log)
    datum = go.Histogram(x = dataframe['Weighted Run'], name = dataframe['InvDescription'][0])
    data.append(datum)
fig = plotly.tools.make_subplots(rows = 2, cols = 3)
fig.append_trace(data[0], 1, 1)
fig.append_trace(data[1], 1, 2)
fig.append_trace(data[2], 1, 3)
fig.append_trace(data[3], 2, 1)
fig.append_trace(data[4], 2, 2)
fig.append_trace(data[5], 2, 3)
plotly.offline.iplot(fig)
plotly.offline.plot(fig, filename = 'Processing time histograms.html')

