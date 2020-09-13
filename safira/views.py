import random
from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import redirect, render

from safira.analytics.manager import requisitar_analise
from safira.api.manager import SafraAPI
from safira.models import Transacao, Cliente
from safira.utils import get_historico_transacoes


def home(request):
    return redirect('/login')
    

def index(request):
    return render(request,'safira/index.html')


def logout(request):
    request.session['usuario'] = {}
    return redirect('/login')



def login(request):
    def _login(request, context= {}):
        return render(request,'safira/login.html', context=context)

    # Validamos uma requiscao GET
    if request.method == "GET":

        # Verificamos se o Usuario já nao esta logado
        if not request.session.get('usuario', {}):
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
    # Simula um comportamento de Middleware
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
    
    # Registra e atualiza o limite de credito do cliente no banco de dados, para utilizacao nos modelos
    cliente = Cliente.objects.get(account_id=account_id)
    cliente.limite_credito = request.session['usuario']["linha_credito"]
    cliente.save()
    
    context = request.session['usuario'].copy()
    context['linhas_tabela'] = get_historico_transacoes(safra_api, account_id, 10)
    
    context['perfil_investidor'] = random.choices(["dinâmico", "conservador","ultra conservador", "moderado"])[0]

    return render(request,'safira/dashboard.html', context=context)


def requisitar_perfil(request, account_id: str):
    """Utiliza o Modelo já treinado para inferir o perfil do cliente

    Args:
        request (request): requisicao
        account_id (str): identificador do cliente
    """
    linha_credito = request.POST.get('linha_credito')

    analise = requisitar_analise(account_id, linha_credito)
    dados = {'recomendacao_safira': analise}
    return JsonResponse(dados)
