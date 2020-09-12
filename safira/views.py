from django.http import JsonResponse
from django.shortcuts import redirect, render
from safira.api.manager import SafraAPI

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
                account_info = client_data['Data']['Account'][0]
                return dashboard(request, dados = account_info)
            else:
                return _login(request, context={'msg': "Cliente não encontrado"})
        except Exception as error:
           return _login(request, context={'msg': "Ops, parece que estamos passando por alguma instabilidade", 'log': error.__str__()})
        
    else:
        return JsonResponse({"message": "Method Not Allowed", "code": 405}, status=405)



def dashboard(request, dados: dict= {}):
    if not dados:
        return redirect('/login')

    # Obtem informacoes do Dashboard
    context = {}
    context['nickname'] = dados.get('Nickname', "")
    context['nome_completo'] = dados.get('Account', {}).get("Name", "")
    context['account_id'] = dados.get('AccountId', '')
    
    safra_api = SafraAPI()

    saldo_conta = safra_api.saldo_conta(context['account_id'])

    if saldo_conta:
        saldo_infos = saldo_conta['Data']['Balance'][0]
        context["saldo"] = saldo_infos['Amount']["Amount"]
        context["linha_credito"] = saldo_infos['CreditLine'][0]["Amount"]["Amount"]


    return render(request,'safira/dashboard.html', context=context)