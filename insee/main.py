# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 09:38:28 2015

"""


from globals import path_data

print("Initialisation...")
from equipements import info_equipement
from revenus import info_revenus
from census import info_population

equipement = info_equipement(2013)
revenu = info_revenus(2011)
population = info_population(2011)
population12 = info_population(2012)

data = equipement.merge(revenu, how='outer')
## petit bout de code pour voir ce qui s'ajoute
#cond = equip_data.CODGEO.isin(revenu.CODGEO)
#equip_data[cond]
#cond = revenu.CODGEO.isin(equip_data.CODGEO)
#revenu[~cond]


data = data.merge(population, how='outer')
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

data.to_csv('data/output.csv')
