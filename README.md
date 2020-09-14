# Safira
A Safira é uma assistente financeira virtual do Safra que por meio do uso de técnicas de inteligência artificial traça um perfil de investidor personalizado, de acordo com os hábitos de consumo de cada cliente

- Visando proporcionar uma experiência mais ágil, o sistema estará temporariamente disponível em: https://technee-safira.herokuapp.com/
> Para acessar, utilize os mesmos clientes disponíveis nos exemplos da [API](https://github.com/banco-safra/technee) fornecida, que são eles: `00711234511` e `00711234522`. 

## Dependencias do Projeto
### Windowns
- Python 3.6+

### Debian ou Ubuntu /  Red Hat ou CentOS
- Python 3.6+
- libpq-dev / libpq-devel


### Dependencias python
- Todas as bibliotecas utilizadas para a execução do projeto encontram-se listadas no arquivo `requirements.txt`
- Para instalar as dependencias do projeto, utilize:
```shell
python -m pip install -r requirements.txt
```
> Nota: Recomenda-se o o uso d4e uma [virtualenv](https://virtualenv.pypa.io/en/latest/) visando ambiente isolado para a execução do projeto

### Execução do projeto

Estando no diretório de mesmo nivel que o arquivo `manage.py`, execute:

```shell
python manage.py runserver
```

Desta forma, será possível ter acesso à página através do link [http://127.0.0.1:8000](http://127.0.0.1:8000)


# Aspectos Gerais

### /login

Para fins de demonstração de conceito, visamos a `Safira` como um sistema interno e integrado ao Banco Safra onde não nos preocupamos, em um primeiro momento, com autenticação e criação de novos usuários.

Como mencionado anteriormente, a realização do login é dada a partir dos dois códigos de clientes presentes nos exemplos da [API](https://github.com/banco-safra/technee) fornecida, que são eles: `00711234511` e `00711234522`. 

Ao clicar em Login, é verificado os dados da conta do cliente utilizando a API. Caso o ClientID um dos dois casos citados a página `/dashboard` é iniciada


### /dashboard

O Dashboard apresenta os dados da conta do cliente e um historico de transações 

- Dados como `Saldo`, `Linha de Crédito`, `Nome` e a `transação mais recente` do cliente são de origem da API disponibilizada para o Hackathon. As demais transações foram Mockadas com o intuito visual e, principalmente, com o objetivo de atuar como insumo para a Inteligência Artificial determinar o perfil do Cliente

- Ao aceitar que a safira analise o perfil de investimento por meio de seus gastos, uma API interna da Safira é requisitada, consolidando o histórico de transações do cliente como insumo do modelo de classificação já treinado e presente no sistema. Ao final do processamento é retornado, para o cliente, o perfil sugerido pela Safira, bem como algumas sugestões de produtos do Banco Safra.


## Aspectos Tecnicos importantes

### Adapter API
- Foi construido um Objeto facilitador do uso da API fornecida, que abstrai os passos de geração de token e definição de acessos da API. O Objeto `SafraAPI` está disponível em `safira/api/manager.py`. A seguir tem-se um breve exemplo de uso que obtem o JSON dos dados da conta do cliente `00711234511`:

```python
from safira.api.manager import SafraAPI

client_id = "00711234511"

safra_api = SafraAPI()
dados_de_conta = safra_api.dados_conta(client_id)
```

## Integração Modelo Dados - BackEnd Aplicação
- O modelo utilizado no back-end corresponde a um classificador `Random Forest`. O modelo é um objeto Python da classe `sklearn.ensemble.RandomForestClassifier` do pacote `Scikit-learn`. O método princial a ser utilizado é o `modelo.predict()`, o qual retorna uma classificação para um dado cliente. 
> Para mais detalhes utilize:
> https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html




