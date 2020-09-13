from datetime import datetime
from safira.models import Transacao

def get_historico_transacoes(safra_API, account_id: str, max_retorno: int) -> list:
    transacao = safra_API.transacoes_conta(account_id)

    api_transacoes = []
    if transacao:
         for _transacao in transacao['data']['transaction']:
             api_transacoes.append(
                 {
                    'tipo': _transacao['creditDebitIndicator'],
                    'data': datetime.strptime(_transacao['valueDateTime'], "%Y-%m-%dT%H:%M:%S%Z:00"),
                    'informacoes': _transacao['transactionInformation'],
                    'valor': float(_transacao['amount']['amount']),
                }
            )
    
    api_transacoes += Transacao.objects.filter(cliente=account_id).order_by('-data').values('data', 'tipo', 'informacoes', 'valor')[:max(0, max_retorno - len(api_transacoes))]

    return api_transacoes