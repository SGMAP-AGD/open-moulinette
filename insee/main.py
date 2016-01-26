# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 09:38:28 2015

"""


from globals import path_data

print("Initialisation...")
from equipements import info_equipement
from revenus import info_revenus
from census import info_population

# create distinct tables
equipement = info_equipement(2013)
revenu = info_revenus(2011)
population = info_population(2011)
population12 = info_population(2012)


## correction
# TODO: have a test on upper case for first letter of each word.
for table in [equipement, revenu, population, population12]:
    table['LIBCOM'] = table['LIBCOM'].str.replace(' - ', '-')
    table['LIBGEO'] = table['LIBGEO'].str.replace('CENTRE VILLE', 'Centre Ville')

for table in [equipement, population, population12]:
    table['LIBGEO'] = table['LIBGEO'].str.replace('CENTRE VILLE', 'Centre Ville')

# une table de comparaison
def compare_geo(tab1, tab2, debug=False):
    assert max(tab1.CODGEO.value_counts()) == 1
    assert max(tab2.CODGEO.value_counts()) == 1
    cond_1_in_2 = tab1.CODGEO.isin(tab2.CODGEO)
    cond_2_in_1 = tab2.CODGEO.isin(tab1.CODGEO)
    tab1.CODGEO[~cond_1_in_2]
    tab2.CODGEO[~cond_2_in_1]
    commun_col = [x for x in tab1.columns if x in tab2.columns]
    commun_col.remove('CODGEO')
    merge_tab = tab1.merge(tab2, on='CODGEO')

    tab1_commun = merge_tab[[x + '_x' for x in commun_col] + ['CODGEO']]
    tab1_commun.columns = commun_col+ ['CODGEO']
    tab2_commun = merge_tab[[x + '_y' for x in commun_col] + ['CODGEO']]
    tab2_commun.columns = commun_col+ ['CODGEO']
    if all((tab1_commun != tab2_commun).sum() == 0):
        return
    for col in commun_col:
        diff = tab1_commun[col] != tab2_commun[col]
        if diff.sum() == 0:
            print("aucune différence sur " + col)
        elif all(tab1_commun.loc[diff, 'DEP'].isin(['13','69','75'])):
            print("des différences dans " + col + 
                " uniquement dans les communes à arrondissement")
        else:
            cond_autres = ~tab1_commun.loc[diff, 'DEP'].isin(['13','69','75'])
            count = diff.sum()
            print("il y a " + str(count) + " problèmes pour " + col)
            if debug:
                pb = tab1_commun[diff].merge(tab2_commun[diff], on='CODGEO', 
                                            suffixes=('_1', '_2'))
                pb.sort(axis=1, inplace=True)
                import pdb; pdb.set_trace()
        


compare_geo(equipement, revenu)
data = equipement.merge(revenu, on="CODGEO", suffixes=('','_to_remove'), how='outer')

compare_geo(data, population, debug=True)
data = data.merge(population,on='CODGEO', how='outer')
## petit bout de code pour voir ce qui s'ajoute
#cond = equip_data.CODGEO.isin(revenu.CODGEO)
#equip_data[cond]
#cond = revenu.CODGEO.isin(equip_data.CODGEO)
#revenu[~cond]

new_reg_dict = {'01' : '01',
                '02' : '02',
                '03' : '03',
                '04' : '04',
                '11' : '11',
                '21' : '44',
                '22' : '32',
                '23' : '28',
                '24' : '24',
                '25' : '28',
                '26' : '27',
                '31' : '32',
                '41' : '44',
                '42' : '44',
                '43' : '27',
                '52' : '52',
                '53' : '53',
                '54' : '75',
                '72' : '75',
                '73' : '76',
                '74' : '75',
                '82' : '84',
                '83' : '84',
                '91' : '76',
                '93' : '93',
                '94' : '94'}

data['REG2016'] = data.REG.map(new_reg_dict)

data.to_csv('data/output_dev.csv', sep=';', encode='utf8')
