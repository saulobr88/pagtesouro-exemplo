# PagTesouro Exemplo - Cliente

Aplicação Cliente da API do PagTesouro

# Como usar

1. clonar o repositório
2. Criar o virtual enviroment (`python -m venv venv`)
3. usar o pip para instalar as dependências (`pip install -r requirements.txt`)
4. Se o arquivo `db.sqlite3` não existir, devem ser executadas as migrations (`python manage.py migrate`)
5. Executar a aplicação (`python manage.py runserver`), preferencialmente em uma porta diferente da porta padrão.

# Usuários

| Nome  | Senha        | Descrição                                 |
| ----- | ------------ | ----------------------------------------- |
| admin | admin        | Superuser. Possui acesso ao painel /admin |
| user1 | User1@123456 | Usuário comum da aplicação                |
| user2 | User2@123456 | Usuário comum da aplicação                |
