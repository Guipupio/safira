from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import redirect, render

from safira.api.manager import SafraAPI
from safira.models import Transacao


def home(request):
    return redirect('/login')
    

def index(request):
    return render(request,'safira/index.html')


def logout(request):
    request.session['usuario'] = {}
    redirect('/login')


def login(request):
    def _login(request, context= {}):
        return render(request,'safira/login.html', context=context)

    # Validamos uma requiscao GET
    if request.method == "GET":

        # Verificamos se o Usuario já nao esta logado
        if request.session.get('usuario', {}):
            return _login(request)
        else:
            return redirect('/dashboard')

    elif request.method == "POST":
        account_id = request.POST.get('codigo_cliente', '')
        safra_api = SafraAPI()

        # Obtem dados da conta
        client_data = safra_api.dados_conta(account_id)
        
        # Verifica se o account_id existe
        try:
            if client_data:
                request.session['usuario'] = {}
                account_info = client_data['Data']['Account'][0]
                
                # Grava na sessao do usuario suas principais informacoes
                request.session['usuario']['Nickname'] = account_info.get('Nickname', "")
                request.session['usuario']['Account'] = account_info.get('Account', {}).get("Name", "")
                request.session['usuario']['AccountId'] = account_info.get('AccountId', '')

                return redirect('/dashboard')
            else:
                return _login(request, context={'msg': "Ops! Cliente ID não encontrado!"})
        except Exception as error:
           return _login(request, context={'msg': "Ops, parece que estamos passando por alguma instabilidade", 'log': error.__str__()})
        
    else:
        return JsonResponse({"message": "Method Not Allowed", "code": 405}, status=405)



def dashboard(request):
    account_id = request.session.get('usuario', {}).get('AccountId', {})
    if not account_id:
        return redirect('/login')
    
    safra_api = SafraAPI()

    # Obtem informacoes do saldo da conta do cliente
    saldo_conta = safra_api.saldo_conta(account_id)

    if saldo_conta:
        saldo_infos = saldo_conta['Data']['Balance'][0]
        request.session['usuario']["saldo"] = saldo_infos['Amount']["Amount"]
        request.session['usuario']["linha_credito"] = saldo_infos['CreditLine'][0]["Amount"]["Amount"]

    transacao = safra_api.transacoes_conta(account_id)

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
    
    context = request.session['usuario'].copy()
    context['linhas_tabela'] = api_transacoes
    context['linhas_tabela'] += Transacao.objects.filter(cliente=account_id).order_by('-data').values('data', 'tipo', 'informacoes', 'valor')[:max(0, 10 - len(api_transacoes))]

    return render(request,'safira/dashboard.html', context=context)
