from django.http import JsonResponse
from django.shortcuts import redirect, render
from safira.api.manager import SafraAPI
from safira.models import Transacao

def home(request):
    return render(request,'safira/home.html')
    
def index(request):
    return render(request,'safira/index.html')
       
def login(request):
    def _login(request, context= {}):
        return render(request,'safira/login.html', context=context)

    if request.method == "GET":
        return _login(request)

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
                return _login(request, context={'msg': "Cliente não encontrado"})
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

    context = request.session['usuario'].copy()
    
    context['linhas_tabela'] = Transacao.objects.filter(id=1).order_by('-data').values('data', 'tipo', 'informacoes', 'valor')

    return render(request,'safira/dashboard.html', context=context)