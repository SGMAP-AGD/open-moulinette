# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 09:38:28 2015

"""


from globals import path_data

from comparison import compare_geo, fillna_with_other_table

print("Initialisation...")
from equipements import info_equipement
from revenus import info_revenus
from census import info_population

# equipement
equipement = info_equipement(2013)
equipement['CODGEO'] = equipement['CODGEO'].astype(str).str.lstrip('0')
# revenu
revenu = info_revenus(2011)
revenu['LIBCOM'] = revenu['LIBCOM'].str.replace(' - ', '-')
# => on prend pour les villes à arrondissement, les valeurs population et equipement
# juse parce qu'elles sont deux et que revenu est tout seul
revenu['CODGEO'] = revenu['CODGEO'].astype(str).str.lstrip('0')

del revenu['LIBCOM']; del revenu['COM'];
# population
population = info_population(2011)
population['LIBGEO'] = population['LIBGEO'].str.replace(u"Jean Bart Guynemer", u"Jean Bart,Guynemer")
population['LIBGEO'] = population['LIBGEO'].str.replace(u"Nouveau Siècle", u"Nouveau Siecle")
population['LIBGEO'] = population['LIBGEO'].str.replace(u"Labuissière", u"Labuissiere")
population['CODGEO'] = population['CODGEO'].astype(str).str.lstrip('0')
#population12 = info_population(2012)

for table in [equipement, population]:
    table['LIBGEO'] = table['LIBGEO'].str.title()

# première fusion de table
compare_geo(equipement, revenu)
data = equipement.merge(revenu, how='outer')

# seconde fusion de table
data = fillna_with_other_table(data, population, 'CODGEO')
compare_geo(data, population, debug=True)
data = data.merge(population, how='outer')
## Ce cogeo n'est que dans revenu, on ajoute les valeur COM et LIBCOM que l'on a retiré
data.loc[data['CODGEO'] == '893870113', ['LIBCOM','COM']] = [['Sens', '89387']]


population12 = info_population(2012)
population12['LIBGEO'] = population12['LIBGEO'].str.replace(u"Jean Bart Guynemer", u"Jean Bart,Guynemer")
population12['LIBGEO'] = population12['LIBGEO'].str.replace(u"Nouveau Siècle", u"Nouveau Siecle")
population12['LIBGEO'] = population12['LIBGEO'].str.replace(u"Labuissière", u"Labuissiere")

string_columns = population12.dtypes[population12.dtypes == 'object'].index.tolist()
for col in string_columns:
    population12[col] = population12[col].str.lstrip('0')
data['MODIF_IRIS'] = data['MODIF_IRIS'].str.replace('00', '')

string_columns = data.dtypes[data.dtypes == 'object'].index.tolist()
for col in string_columns:
    data[col] = data[col].str.lstrip('0')
data['MODIF_IRIS'] = data['MODIF_IRIS'].str.replace('00', '')

population12['LIBGEO'] = population12['LIBGEO'].str.title()


data['GRD_QUART'] = data['GRD_QUART'].astype(str)
population12['GRD_QUART'] = population12['GRD_QUART'].astype(str)
population12['GRD_QUART']

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


compare_geo(data, population12, debug=True)
data2 = data.merge(population12, how='outer')

data2['REG2016'] = data.REG.map(new_reg_dict)
# recommandation: merge on CODGEO only and take 2012 LIBGEO.
# LIBGEO12 seems an update of LIBGEO11
# examples : Mendela => Mandela; Anne Franck => Anne Frank,...
# pareil pour LIBCOM ?

#data2.to_csv('data/output_dev12.csv', sep=';', index=False, encoding='utf-8')
