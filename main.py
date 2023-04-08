import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://intranet.policiamilitar.mg.gov.br/lite/recursos-humanos/web/?p=1&nome=&nr_pol=&postograd=&genero=T&ativo=A&unidade=2560&municipio=&bairro=&endereco='

url_login = 'https://intranet.policiamilitar.mg.gov.br/'
url_dados = 'https://intranet.policiamilitar.mg.gov.br/lite/recursos-humanos/web/?p=1&nome=&nr_pol=&postograd=&genero=T&ativo=A&unidade=2560&municipio=&bairro=&endereco='

# Credenciais de autenticação
username = '1400688'
password = 'p4ss1ntr4'

# Dados para enviar na requisição POST de login
data = {
    'username': username,
    'password': password
}

# Realiza o login
session = requests.session()
session.post(url_login, data=data)

# Acessa a página que contém os dados desejados
response = session.get(url_dados)

# Verifica se a autenticação foi realizada com sucesso
if "Erro" in response.text:
    raise Exception("Erro na autenticação.")
else:
    print("Autenticação realizada com sucesso.")

# Acessa a página desejada após o login
response = session.get(url_dados)

html = response.content

print(html)

# Cria o objeto BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Procura as divs com a classe 'item busca-pessoal'
divs = soup.find_all('div', {'class': 'item busca-pessoal'})

# print('divs', divs)

# Lista para armazenar os registros
registros = []

print('registros', registros)

# Percorre as divs encontradas
for div in divs:
    # Extrai os elementos dl
    dl_elements = div.find_all('dl')
    # Extrai os dados dos subelementos do dl
    npol = dl_elements[0].find('dt').text
    nome = dl_elements[0].find('dd').text
    lotacao = dl_elements[0].find_all('dd')[1].text
    # Adiciona o registro na lista
    registros.append([npol, nome, lotacao])

# Cria o DataFrame com os registros
df = pd.DataFrame(registros, columns=['NPol', 'Nome', 'Lotação'])

# Salva o DataFrame em um arquivo xlsx
df.to_excel('registros.xlsx', index=False)
