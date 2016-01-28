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
# revenu
revenu = info_revenus(2011)
revenu['LIBCOM'] = revenu['LIBCOM'].str.replace(' - ', '-')
# => on prend pour les villes à arrondissement, les valeurs population et equipement
# juse parce qu'elles sont deux et que revenu est tout seul
del revenu['LIBCOM']; del revenu['COM'];
# population
population = info_population(2011)
population['LIBGEO'] = population['LIBGEO'].str.replace(u"Jean Bart Guynemer", u"Jean Bart,Guynemer")
population['LIBGEO'] = population['LIBGEO'].str.replace(u"Nouveau Siècle", u"Nouveau Siecle")
population['LIBGEO'] = population['LIBGEO'].str.replace(u"Labuissière", u"Labuissiere")
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


data.to_csv('data/output11_dev.csv', sep=';', index=False, encoding='utf-8')

www

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

data.to_csv('data/output.csv')
