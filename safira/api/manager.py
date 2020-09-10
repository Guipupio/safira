import json
from base64 import b64decode as decode
from base64 import b64encode as encode

import requests

from safira.api.constantes import list_client_id_string


class SafraAPI():
    def __init__(self, token=None):
        """Gera uma secao para uso da API do Safra, caso um token

        Args:
            token ([type], optional): [description]. Defaults to None.
        """
        self.token = token or self.generate_oauth_token(list_client_id_string)
        self.common_headers = {
            "Authorization": f"Bearer {self.token}",
            'cache-control': "no-cache",
        }

    def health_check(self, token: str = '') -> bool:
        """Valida se a o servico de API está OK

        Args:
            token (str): Token Bearer para consulta /health

        Returns:
            bool: if status requisicao == 200; else False
        """
        url = "https://af3tqle6wgdocsdirzlfrq7w5m.apigateway.sa-saopaulo-1.oci.customer-oci.com/fiap-sandbox/health"

        headers = {
            'authorization': f"Bearer {token or self.token}",
            'cache-control': "no-cache",
            }

        response = requests.request("GET", url, headers=headers)

        return response.status_code == 200 # TODO - Talvez dar um destaque ao status 401?

    def generate_oauth_token(self, list_secrets: list) -> str:
        """Gera Token Beare com base em um secreat

        Args:
            list_secrets (list): screat em b''

        Returns:
            str: token Beare
        """
        url = "https://idcs-902a944ff6854c5fbe94750e48d66be5.identity.oraclecloud.com/oauth2/v1/token"

        payload = "grant_type=client_credentials&scope=urn:opc:resource:consumer::all"

        headers = {
            'cache-control': "no-cache",
            'content-type': "application/x-www-form-urlencoded",
            }

        for secret in list_secrets:
            # Gera token base64
            headers['authorization'] = f"Basic {encode(secret).decode('utf-8')}"
            
            response = requests.request("POST", url, data=payload, headers=headers)

            try:
                # Verifica se a requisicao foi bem sucedida
                if response.status_code == 200:
                    # Carrega informacoes do request
                    response_infos = json.loads(response.content)
                    
                    # Obtem token
                    token = response_infos.get('access_token', '')

                    # Valida saude do token e aplicacao
                    if self.health_check(token):
                        # Se Saude OK, retornamos o token valido
                        return token

                    # Caso contrario, tentamos um novo token

            except Exception as error:
                pass # TODO - Pensar em algum LOG?

        return None


    def load_response(self, tipo_request, url, **kwargs) -> dict:
        response_infos = {}
        
        response = requests.request(tipo_request, url, **kwargs)

        if response.status_code == 200:
            response_infos = json.loads(response.content)

        return response_infos


    def dados_conta(self, conta_id: str) -> dict:
        
        # Exemplo de conta_id = 00711234522
        url = f"https://af3tqle6wgdocsdirzlfrq7w5m.apigateway.sa-saopaulo-1.oci.customer-oci.com/fiap-sandbox/open-banking/v1/accounts/{str(conta_id)}"

        return self.load_response(tipo_request="GET", url=url, headers=self.common_headers)


    def saldo_conta(self, conta_id: str) -> dict:
        # Exemplo de conta_id = 00711234522
        url = f"https://af3tqle6wgdocsdirzlfrq7w5m.apigateway.sa-saopaulo-1.oci.customer-oci.com/fiap-sandbox/open-banking/v1/accounts/{str(conta_id)}/balances"

        return self.load_response(tipo_request="GET", url=url, headers=self.common_headers)
    

    def transacoes_conta(self, conta_id: str) -> dict:
        # Exemplo de conta_id = 00711234522
        url = f"https://af3tqle6wgdocsdirzlfrq7w5m.apigateway.sa-saopaulo-1.oci.customer-oci.com/fiap-sandbox/open-banking/v1/accounts/{str(conta_id)}/transactions"

        return self.load_response(tipo_request="GET", url=url, headers=self.common_headers)


    def transferencia_entre_contas(self, conta_id_origem: str) -> dict:

        # Exemplod e conta origem 00711234511
        url = f"https://af3tqle6wgdocsdirzlfrq7w5m.apigateway.sa-saopaulo-1.oci.customer-oci.com/fiap-sandbox/accounts/v1/accounts/{str(conta_id_origem)}/transfers"

        payload = {
            "Type": "TEF",
            "TransactionInformation": "Mensalidade Academia",
            "DestinyAccount": {
                "Bank": "422",
                "Agency": "0071",
                "Id": "1234533",
                "Cpf": "12345678933",
                "Name": "Mark Zuckerberg da Silva",
                "Goal":"Credit"
            },
            "Amount": {
                "Amount": "250.00",
                "Currency": "BRL"
                }  
        }

        return self.load_response(tipo_request="POST", url=url, data=json.dumps(payload), headers=self.common_headers)