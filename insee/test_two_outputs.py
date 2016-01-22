# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 16:30:50 2016

@author: Alexis Eidelman
"""

import pandas as pd

name1 = 'output.csv'
name2 = 'output_dev.csv'

tab1 = pd.read_csv('data\\' + name1, sep=';')
tab2 = pd.read_csv('data\\' + name2, sep=',') #why is it a ','

## étude du nom des colonnes
def _compare(list1, list2):
        set1 = set(list1)
        set2 = set(list2)
        removed = set1 - set2
        added = set2 - set1
        return added, removed

in_2_not_in_1, in_1_not_in_2 = _compare(tab1.columns, tab2.columns)
print('dans 1 et pas dans 2', in_1_not_in_2)
print('dans 2 et pas dans 1', in_2_not_in_1)
tab1.drop(in_1_not_in_2, axis=1, inplace=True)
tab2.drop(in_2_not_in_1, axis=1, inplace=True)

# comparaison des types
pb_dtypes = tab1.dtypes != tab2.dtypes


## étude des index
_compare(tab1.index, tab2.index)
len(tab2) - len(tab1) #1534 différences

tab1.CODGEO = tab1.CODGEO.astype(str)
tab2.CODGEO = tab2.CODGEO.astype(str)

tab1['CODGEO'][tab1.CODGEO.str.len() == 8] = '0' + tab1['CODGEO'][tab1.CODGEO.str.len() == 8]
tab2['CODGEO'][tab2.CODGEO.str.len() == 8] = '0' + tab2['CODGEO'][tab2.CODGEO.str.len() == 8]
in_2_not_in_1, in_1_not_in_2 = _compare(tab1.CODGEO, tab2.CODGEO)
# CODGEO => OK

tab1.sort_values('CODGEO', inplace=True)

tab2.sort_values('CODGEO', inplace=True)

# order tab2 as tab1 (may be useless)
tab2 = tab2[tab1.columns]
string_columns = tab1.dtypes[tab1.dtypes == 'object'].index.tolist()
float_columns = [x for x in tab1.columns if x not in string_columns]

# test sur les NaN
diff = tab2[float_columns].isnull() == tab1[float_columns].isnull()

# test sur les valeurs
diff = tab2[float_columns] - tab1[float_columns]
