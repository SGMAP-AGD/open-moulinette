# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 09:40:36 2015

"""
from __future__ import print_function

import pandas as pd
from globals import path_insee, path_data, _read_file_or_download


def equipement_url(filename, year):
    if year == 2013:
        year_str = str(year)[-2:]
    if year == 2014:
        year_str = str(year)
    url_path = path_insee + filename + '/' + filename + '-infra-' + year_str + '.zip'
    return url_path


def read_equipement_file(filename, year):
    url_path = equipement_url(filename, year)
    path_file_on_disk = path_data + filename + '-infra' + str(year) + '.xls'
    _read_file_or_download(filename + '-infra' + str(year) + '.xls', path_data, url_path)
    return pd.read_excel(path_file_on_disk, sheetname='IRIS', header=5)


def sum_of_all_features(iris_df, colname, list_to_sum=None):
    ''' iris_df is an iris data frame
        colname is the name of the sum of columns'''
    header = [x for x in iris_df.columns if str(x) != 'nan'] # remove NaN to header to create new sum feature
    # creating new feature : sum of all feature
    if list_to_sum is None:
        features = [x for x in header if x not in columns_not_to_sum]
    else:
        features = list_to_sum
    iris_df[colname] = iris_df[features].applymap(lambda x: float(x)).sum(axis=1)
    nb_features = len(features)
    print("\t il y a ", iris_df.CODGEO.nunique(),
          " iris différentes pour et ", nb_features, " features")
    return iris_df


#key = ['CODGEO', 'LIBGEO', 'COM', 'LIBCOM', 'REG', 'DEP', 'UU2010']

columns_not_to_sum = ['CODGEO', 'LIBGEO', 'COM', 'LIBCOM', 'REG', 'DEP', 'ARR', 'CV',
             'ZE2010', 'UU2010', 'UU12010', 'ID_MODIF_GEO']

# The list of variables is useless now
equipements = dict(
    commerce = ('equip-serv-commerce', None),
    sport = ('equip-sport-loisir-socio',
                      ['NB_F101', 'NB_F102', 'NB_F103', 'NB_F104',
                     'NB_F105', 'NB_F106', 'NB_F107', 'NB_F108',
                     'NB_F109', 'NB_F110', 'NB_F111', 'NB_F112',
                     'NB_F113', 'NB_F114', 'NB_F115', 'NB_F117', 'NB_F118']),
    enseignement_degre_1 = ('equip-serv-ens-1er-degre', ['NB_C101', 'NB_C102', 'NB_C104', 'NB_C105']),
    enseignement_degre_2 = ('equip-serv-ens-2eme-degre', ['NB_C201', 'NB_C301', 'NB_C302', 'NB_C303',
                              'NB_C304', 'NB_C305']),
    enseignement_sup = ('equip-serv-ens-sup-form-serv',
                                ['NB_C401', 'NB_C402', 'NB_C403',
                                'NB_C409', 'NB_C501', 'NB_C502',
                                'NB_C503', 'NB_C504', 'NB_C509',
                                'NB_C601', 'NB_C602', 'NB_C603',
                                'NB_C604', 'NB_C605', 'NB_C609',
                                'NB_C701', 'NB_C702']),
     social = ('equip-serv-action-sociale', None),
     sante = ('equip-serv-sante', None),
     medical = ('equip-serv-medical-para', None),
     service_particulier = ('equip-serv-particuliers', None),
     transport_tourisme = ('equip-tour-transp', None),
    )


def routine1(name, year):
    assert name in equipements
    filename, list_to_sum = equipements[name]
    df = read_equipement_file(filename, year)
    # a bug in one excel... 'equip-serv-commerce'
    df.dropna(how='any', axis=1, inplace=True)
    assert all(df.isnull().sum() == 0)
#    df = sum_of_all_features(df, 'nb_' + name, list_to_sum)
    assert len(df) == df.CODGEO.nunique()
    nb_features = len(df.columns) - len(columns_not_to_sum)
    print("\t il y a ", df.CODGEO.nunique(), " iris différentes pour et ",
          nb_features, " features")
    df['nb_' + name] = df[[x for x in df.columns if x not in columns_not_to_sum]].sum(axis=1)
    return df


def info_equipement(year):
    equipement = None
    for table in equipements:
        print('* lecture de ' + table)
        if equipement is None:
            equipement = routine1(table, year)
        else:
            equipement = equipement.merge(routine1(table, year), how='outer')

    sport = [x for x in equipement.columns if x[:5] == 'NB_F1' and len(x) == 7]
    airjeu_sport = [x for x in equipement.columns if x[:5] == 'NB_F1' and x[-10:] == 'NB_AIREJEU']
    nb_enseignement_1 = [x for x in equipement.columns if x[:5] == 'NB_C1'  and len(x) == 7]
    nb_enseignement_2 = [x for x in equipement.columns if x[:5] in ['NB_C2', 'NB_C3']  and len(x) == 7]
    enseignement_sup = [x for x in equipement.columns if x[:5] in ['NB_C4', 'NB_C5', 'NB_C6', 'NB_C7']  and len(x) == 7]
    equipement['nb_sport'] = equipement[sport].sum(axis=1)
    equipement['nb_airjeu_sport'] = equipement[airjeu_sport].sum(axis=1)
    equipement['nb_enseignement_1'] = equipement[nb_enseignement_1].sum(axis=1)
    equipement['nb_enseignement_2'] = equipement[nb_enseignement_2].sum(axis=1)
    equipement['nb_enseignement_sup'] = equipement[enseignement_sup].sum(axis=1)
    equipement['nb_service_particulier'] = equipement[enseignement_sup].sum(axis=1)
    return equipement