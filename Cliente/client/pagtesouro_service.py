import requests
from django.conf import settings

class PagTesouroService:
    def __init__(self):
        self.token = settings.PAGTESOURO_CLIENT["JWT_TOKEN_ACCESS"]
        self.base_url = settings.PAGTESOURO_CLIENT["API_BASE_URL"]
    
    def getBaseUrl(self):
        return self.base_url.rstrip('/')

    def get_index_request(self):
        url = self.getBaseUrl() + '/'
        headers = {
            'Authorization': f'Bearer {self.token}'
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            # Trate os erros de acordo com suas necessidades
            raise Exception(f'Erro na requisição GET: {response.status_code}')
