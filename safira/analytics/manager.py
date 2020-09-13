from safira.models import Transacao, Cliente
from safira.analytics.features_backend import input_df 
import pandas as pd
import joblib

def requisitar_analise(client_id: str, limite_credito: float):

    # Obtem renda mensal (comum em todos so campos)
    renda_mensal = Cliente.objects.get(account_id=client_id).renda
    # Obtem historico de transacoes
    historico_transacoes = Transacao.objects.filter(cliente=client_id).values('tipo', 'valor')

    # Define Pre DataFrame
    pre_df = {
        'CreditDebitIndicator': [],
        'Limite_Credito': [],
        'Renda_Mensal': [],
        'amount':[],
    }

    # Popula transacoes
    for transacao in historico_transacoes:
        pre_df['CreditDebitIndicator'].append(transacao['tipo'])
        pre_df['Limite_Credito'].append(limite_credito)
        pre_df['Renda_Mensal'].append(renda_mensal)
        pre_df['amount'].append(transacao['valor'])

    # Gera DF com transacoes passadas
    df = pd.DataFrame(pre_df)

    # extrai features das transacoes passadas
    features = input_df(df)

    modelo = joblib.loads('model.pickle')

    analise = modelo.predict(features)

    return analise

def funcao_do_custodio(df):

    # Seu codigo TOP

    features = None

    analise = pkl_lucas.predict(features)

    return analise

    from safira.analytics.manager import *
    model = joblib.load('safira/analytics/model_sklearn.pickle')
    

    # df[['CreditDebitIndicator', 'amount', 'transactionInformation', 'accountID', 'valueDateTime']]