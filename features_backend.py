# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 20:09:53 2020

@author: custo
"""

import pandas as pd
import numpy as np

def trans_analysis(data):
    """ Determines which band a transaction belongs to

    Args:
        data (DataFrame): customer transaction details

    Returns:
        bands (numpy): percent of transations in each band.
        risk_profile (string): true label.

    """
    
    income = data.iloc[0]['Renda_Mensal']
    credit_limit = data.iloc[0]['Limite_Credito']
    risk_profile = data.iloc[0]['Perfil']
    debit = data[(data['CreditDebitIndicator'] == 'Debit')]
    credit = data[(data['CreditDebitIndicator'] == 'Credit')]
    num_trans = len(data)
    # Faixa de Gasto Baixa Crédito G<10%LC
    selected_trans = (credit['amount'] < 0.1*credit_limit)
    FGBC = credit[selected_trans]['amount'].count()
    # Faixa de Gasto Média Crédito -> 10%R<G<30%LC
    selected_trans = (credit['amount'] < 0.3*credit_limit) &  (credit['amount'] > 0.1*credit_limit)
    FGMC = credit[selected_trans]['amount'].count()
    # Faixa de Gasto Alta Crédito -> 30%R<G<70%LC
    selected_trans = (credit['amount'] < 0.7*credit_limit) &  (credit['amount'] > 0.3*credit_limit)
    FGAC = credit[selected_trans]['amount'].count()
    # Faixa de Gasto Muito Alta Crédito -> G>70%LC
    selected_trans = (credit['amount'] > 0.7*credit_limit)
    FGMAC = credit[selected_trans]['amount'].count()
    # Faixa de Gasto Baixa Débito -> G<10%R
    selected_trans = (debit['amount'] < 0.1*income)
    FGBD = debit[selected_trans]['amount'].count()
    # Faixa de Gasto Média Débito -> 10%R<G<30%R
    selected_trans = (debit['amount'] < 0.3*income) &  (debit['amount'] > 0.1*income)
    FGMD = debit[selected_trans]['amount'].count()
    # Faixa de Gasto Alta Débito -> 30%R<G<70%R
    selected_trans = (debit['amount'] < 0.7*income) &  (debit['amount'] > 0.3*income)
    FGAD = debit[selected_trans]['amount'].count()
    # Faixa de Gasto Muito Alta Débito -> G>70%R
    selected_trans = (debit['amount'] > 0.7*income)
    FGMAD = debit[selected_trans]['amount'].count()
    bands = np.array([FGBC,FGMC,FGAC,FGMAC,FGBD,FGMD,FGAD,FGMAD])/num_trans

    return bands, risk_profile

def input(df):
    '''Receives inputs from backend 

    Args:
        df (dataframe): customer transaction history

    Returns:
        None.

    '''
    # Count Number of Customers
    clients_id = pd.unique(df['accountID'])
    aggreg_trans = []
    risk_profiles = []
    
    for i, ID in enumerate(clients_id):
        
        bands, risk_profile = trans_analysis(df.loc[df['accountID'] == ID]) 
        aggreg_trans.append(bands)
        risk_profiles.append(risk_profile)

    df = pd.DataFrame(aggreg_trans, index=clients_id, columns=[
                        'Faixa de Gasto Baixa Credito',
                        'Faixa de Gasto Media Credito',
                        'Faixa de Gasto Alta Credito',
                        'Faixa de Gasto Muito Alta Credito',
                        'Faixa de Gasto Baixa Debito',
                        'Faixa de Gasto Media Debito',
                        'Faixa de Gasto Alta Debito',
                        'Faixa de Gasto Muito Alta Debito'
        ])
    
    df['Perfil de Investimento'] = risk_profiles

    return df
