# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 09:39:08 2015

"""
from __future__ import print_function


import pandas as pd
from globals import path_insee, path_data, _read_file_or_download


def recensement_url(filename, year):
    part1 = 'rp' + str(year) + '/infracommunal'
    part2 = '/infra-' + filename + '-' + str(year)[-2:]
    part3 = '/infra-' + filename + '-' + str(year) + '.zip'
    return path_insee + part1 + part2 + part3


list_recensement = ['logement', 'formation',
                    'famille', 'population',
                    'activite-resident']

key = ['IRIS', 'LIBIRIS', 'COM', 'LIBCOM', 'REG', 'DEP', 'UU2010',
       'TRIRIS', 'GRD_QUART', 'TYP_IRIS', 'MODIF_IRIS', 'LAB_IRIS']


def fix_LIBGEO_12(x):
    """
    LIBGEO change between 2011 & 2012. It prevent merge (LIBGEO is a key)
    2011 : "Awala-Yalimapo"
    2012 : "Awala-Yalimapo (commune non irisée)"
    
    input: string
    output : Return string without " (commune non irisée)".
    """
    try:
        return x.encode('utf-8').replace(" (commune non irisée)", '').decode('utf-8')
    except Exception as er:
        print("Erreur : " + x + str(er))
        return x


def info_population(year):
    data = None
    for file in list_recensement:
        url_path = recensement_url(file, year)
        filename = 'base-ic-' + file + '-' + str(year) + '.xls'
        _read_file_or_download(filename, path_data, url_path)
        path_file_on_disk = path_data + filename
        df = pd.read_excel(path_file_on_disk, sheetname='IRIS', header=5)
        print(filename)
        assert all([x in df.columns for x in key])
        assert len(df) == df.IRIS.nunique()
        print("\t il y a ", len(df),
          " iris différentes pour et ",
          len(df.columns) - len(key), " features")
        if data is None:
            data = df
        else:
            assert len(data) == len(df)
            data = data.merge(df, on=key, how='outer')
            # Remarque : on a des variables qui s'appellent 'P11_POP1524', 'P11_POP2554', 'P11_POP5564'
            # dans plusieurs tables !!
            assert len(data) == len(df)
    
    data.rename(columns={'IRIS':'CODGEO', 'LIBIRIS': 'LIBGEO'}, inplace=True)
    if year == 2012:
        data['LIBGEO'] = data['LIBGEO'].apply(fix_LIBGEO_12)
    return 