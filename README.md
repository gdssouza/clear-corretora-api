# API da Corretora Clear
![License](https://img.shields.io/github/license/gdssouza/clear-corretora-api)

O projeto tem como objetivo desenvolver uma API pública extra-oficial para automatizar negociações na BOVESPA. 

### Dependências

* requests
* BeautifulSoup

### Exemplo de uso

```python
import API

# login
corretora = API.clear("nnnnnnnnnn", "dd/mm/yyyy", "xxxxx")
sessao = corretora.login()

print("Lendo token")
dados_sessao_atual = corretora.getDataAccess()
print(dados_sessao_atual)

print("Atualizando token")
dados_sessao_atual = corretora.token()
print(dados_sessao_atual)
```

### Contribuições

Apenas abra um PR. Nossos commits seguem a nomeclatura Conventional Commits:

`<type>[optional scope]: <description>`

#### Do List

Algumas sugestões do que fazer::

* Função para ler a carteira
* Função para comprar ativos
* Função para vender ativos

### Créditos

* @gdssouza
