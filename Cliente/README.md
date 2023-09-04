# PagTesouro Exemplo - Cliente

Aplicação Cliente da API do PagTesouro

## Como usar

1. Clonar o repositório
2. Criar o virtual enviroment (`python -m venv venv`) e ativa-lo (`source ./venv/bin/activate`)
3. usar o pip para instalar as dependências (`pip install -r requirements.txt`)
4. Se o arquivo `db.sqlite3` não existir, devem ser executadas as migrations (`python manage.py migrate`)
5. Se não existir o arquivo `.env`, deve ser criado baseado no conteúdo do arquivo `.env.example`
6. Definir os valores de `API_BASE_URL` e `JWT_TOKEN_ACCESS` em `.env`
7. Executar a aplicação (`python manage.py runserver`), preferencialmente em uma porta diferente da porta padrão.
