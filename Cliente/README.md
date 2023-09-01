# PagTesouro Exemplo - Cliente

Aplicação Cliente da API do PagTesouro

# Como usar

1. clonar o repositório
2. Criar o virtual enviroment (`python -m venv venv`)
3. usar o pip para instalar as dependências (`pip install -r requirements.txt`)
4. Se o arquivo `db.sqlite3` não existir, devem ser executadas as migrations (`python manage.py migrate`)
5. Definir os valores de `API_BASE_URL` e `JWT_TOKEN_ACCESS` em `Main/settings.py`
6. Executar a aplicação (`python manage.py runserver`), preferencialmente em uma porta diferente da porta padrão.
