
# coding: utf-8

# In[3]:

import pickle
import geopandas
import time
import pandas as pd
import itertools
import difflib
from collections import defaultdict
from difflib import get_close_matches as gcm
import re

import operator


# In[4]:

scan_fh = open('/home/matt/scans.pkl.good','r')
scans = pickle.load(scan_fh)


# In[5]:

all_cells = pd.DataFrame()
for key, scan in scans.items():
    scan_cells = pd.DataFrame([ pd.Series(cell, name = key) for cell in scan if type(cell) is dict ])
    all_cells = pd.concat((all_cells, scan_cells))
    
scan_cells.head()
#pd.DataFrame(all_cells{:])
#pd.DataFrame([ pd.Series(get_cell(vals), name=key) for key, vals in scans.items()])


# In[6]:

def is_useless(ssid):
    if not ssid:
        return True
    
    ignores = ['^NETGEAR.*', '^XFINITY$', '^ATT[0-9A-Z]', '.*HOME.*', '.*PRINT.*', '.*OFFICEJET.*', '^DIRECT']
    ignore_iter = [ ssid for ignore in ignores if re.match(ignore, ssid) ]
    if ignore_iter:
        return True
    else:
        return False

def clean_ssid(ssid):
    return re.sub('[^A-Z0-9]+','', ssid).upper()

all_ssids = set([ clean_ssid(ssid) for ssid in all_cells.ssid if not is_useless(ssid)])



# In[7]:

businesses = pd.read_csv('/home/matt/Business_Licenses.csv', low_memory=False)


# In[10]:

#Gathered with some old, deprecated code and this line from the depths of laziness:
#cat above sorted output | awk '{print $2}' | sed 's/[^A-Za-z0-9]//g' | grep . | tr '\n' ' ' | sed "s/ /','/g" && echo

banned_toks = [ 'INC.','INC','LLC','CORPORATION','CORP','CO',
  'COMPANY','SERVICES','CORP','INCORPORATED', 'LTD','GROUP',
  'SERVICE','LIMITED','HOME',  'CO','MANAGEMENT', 'LA',
  'ENTERPRISES','DEVELOPMENT','INTERNATIONAL', 'COMPANY',
  'IN','ASSOCIATES','AIR','CAPITAL','CONSULTING','SOLUTIONS']


def get_bname_chunks(business_names):
    ret_chunks = defaultdict(set)
    for bname in business_names:
        bname = re.sub('[^A-Z ]', '', bname) #numbers in the way, potentially
        bname = ' '.join([ name for name in bname.split() if name not in banned_toks ])
        
        chunks_split = itertools.combinations(bname.split(), 2) #get forward combo of tokens, max:2
        chunks = [ ''.join(chunk) for chunk in chunks_split ] #re-combine business names, minus spaces.
        [ ret_chunks[bname].add(chunk) for chunk in chunks if len(chunk) > 13 ]
        
        if re.search('[0-9]', bname):
            nonum_chunks = [ ''.join(re.sub( '[0-9]','',chunk)) for chunk in chunks_split ]
    
    return pd.Series(ret_chunks)

business_names = list(set([str(name).upper() for name in set(businesses["LEGAL NAME"]) ]))
business_chunks = get_bname_chunks(business_names)


# In[11]:

business_chunks.head()


# In[12]:

ssids = [ ssid.replace(' ','') for ssid in all_ssids ]


# In[ ]:

def sim_max(ssid, max_val):
    ret_sims = defaultdict(float)
    for chunk in business_chunks:
        #print chunk
        s = difflib.SequenceMatcher(a=ssid,b=''.join(chunk))
        gcm_precheck = s.ratio()

        
        #gcm_precheck = gcm(ssid, chunk, len(chunk), .7)
        if gcm_precheck > max_val:
            chunk_str = ''.join(chunk)
            ret_sims[chunk_str] = gcm_precheck
            
    return ret_sims

count = 0
for ssid in ssids:
    if len(ssid) <5:
        continue
    sims = sim_max(ssid, .7)
    print sims
    if sims:
        print ssid, sims
    count+=1
#    if count % 10 == 0:
#        time.sleep(.2)
    #break
    
##Progress March 4 
#22:35


# In[14]:

ssids_nospaces = [ ssid.replace(' ','') for ssid in all_ssids ]
print "hey"
valid_list = []
for ssid in ssids_nospaces:
    valid_ssid = [ sim_max(ssid) for subname in business_names ]
    if len(valid_ssid) > 0:
        print ssid, valid_ssid


# In[ ]:

test = "test test test"


# In[ ]:

re.sub('[^A-Z0-9]','','test test test')


# In[3]:

gdt = geopandas.GeoDataFrame()


# In[1]:

#gdt.from_file('/home/matt/buildings/geo_export_b73642cc-6bfb-4921-935e-826988e13412.shp')

