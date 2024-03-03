import requests


def buscar_cep(cep):
    cep= str(cep)
    cep = cep.replace("-", "").replace(".", "").replace(" ", "")

    if len(cep) == 8:
        link = f'https://viacep.com.br/ws/{cep}/json/'

        requisicao = requests.get(link)

        dic_requisicao = requisicao.json()

        uf = dic_requisicao['uf']
        cidade = dic_requisicao['localidade']
        bairro = dic_requisicao['bairro']
    else:
        print("CEP Inválido")

    return uf,cidade,bairro

if __name__=="__main__":
    cep = 69915202
    buscar_cep(cep)