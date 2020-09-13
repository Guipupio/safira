from safira.models import Transacao, Cliente
from safira.analytics.features_backend import input_df 
import pandas as pd
import joblib

REVERSE_MAP_DICT = {
        1:'Ultra Conservador',
        2:'Conservador',
        3:'Moderado',
        4:'Dinâmico',
    }

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
        'accountID': []
    }

    # Popula transacoes
    for transacao in historico_transacoes:
        pre_df['CreditDebitIndicator'].append(transacao['tipo'])
        pre_df['Limite_Credito'].append(float(limite_credito))
        pre_df['Renda_Mensal'].append(float(renda_mensal))
        pre_df['amount'].append(float(transacao['valor']))
        pre_df['accountID'].append(client_id)

    # Gera DF com transacoes passadas
    df = pd.DataFrame(pre_df)

    # extrai features das transacoes passadas
    features = input_df(df)

    modelo = joblib.load('safira/analytics/model_sklearn.pickle')

    analise = REVERSE_MAP_DICT[modelo.predict(features)[0]]

    return analise
