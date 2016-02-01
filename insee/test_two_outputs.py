# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 16:30:50 2016

@author: Alexis Eidelman
"""

import pandas as pd

name1 = 'output11_master.csv'
name2 = 'output11_dev.csv'

tab1 = pd.read_csv('data\\' + name1, sep=';')
tab2 = pd.read_csv('data\\' + name2, sep=';')

## étude du nom des colonnes
def _compare(list1, list2):
        set1 = set(list1)
        set2 = set(list2)
        removed = set1 - set2
        added = set2 - set1
        return removed, added

# correction :
tab2.rename(columns={
    'nb_sante': 'nb_equipement_sante',
    'nb_medical': 'nb_fonction_medical',
    'nb_social': 'nb_equipement_social',
    'nb_enseignement_degre_1'
    'nb_enseignement_degre_2'
    'nb_airjeu_sport': 'nb_airjeu_sport',
    }, inplace=True)

tab1['REG'] = tab1['REG'].astype(int)

in_1_not_in_2, in_2_not_in_1 = _compare(tab1.columns, tab2.columns)
print('dans 1 et pas dans 2', in_1_not_in_2)
print('dans 2 et pas dans 1', in_2_not_in_1)
tab1.drop(in_1_not_in_2, axis=1, inplace=True)
tab2.drop(in_2_not_in_1, axis=1, inplace=True)


# order tab2 as tab1 (may be useless)
tab2 = tab2[tab1.columns]

# differents types
string_columns = tab1.dtypes[tab1.dtypes == 'object'].index.tolist()
float_columns = [x for x in tab1.columns if x not in string_columns]

# comparaison des types
pb_dtypes = tab1.dtypes != tab2.dtypes
sum(pb_dtypes)

## étude des index
_compare(tab1.index, tab2.index)
len(tab2) - len(tab1) #0 différences

tab1.CODGEO = tab1.CODGEO.astype(str)
tab2.CODGEO = tab2.CODGEO.astype(str)

in_2_not_in_1, in_1_not_in_2 = _compare(tab1.CODGEO, tab2.CODGEO)
# CODGEO => OK

tab1.sort_values('CODGEO', inplace=True)
tab2.sort_values('CODGEO', inplace=True)

assert (tab1['CODGEO'].value_counts().max() == 1) #normalement, c'est vérifié avant mais bon

## test sur les NaN
# valeurs numériques
diff = tab2[float_columns].isnull() == tab1[float_columns].isnull()
assert all(diff.sum() == len(diff))
# => les nan sont distribué de la même façon dans les deux tables

# valeurs caractères
diff = tab2[string_columns].isnull() == tab1[string_columns].isnull()
assert all(diff.sum() == len(diff))

## test sur les valeurs
# valeurs numériques
tab1.fillna(0, inplace=True)
tab2.fillna(0, inplace=True)
diff = tab2[float_columns] == tab1[float_columns]
if not all(diff.sum() == len(diff)):
    pb = diff.sum()[diff.sum() != len(diff)]
    print(pb)
    for col in pb.index:
        print(col)
    import pdb; pdb.set_trace()

assert all(diff.sum() == len(diff))

# valeurs caractère
diff = tab2[string_columns] == tab1[string_columns]
assert all(diff.sum() == len(diff))


