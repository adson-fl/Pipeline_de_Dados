import requests 
import pandas as pd

# lista de dicionario de usuarios
def fetch_usuarios() -> list[dict]:

    url = "https://jsonplaceholder.typicode.com/users"

    try:
        response = requests.get(url)
        response.raise_for_status() #validação do HTTP
        usuarios = response.json()

        if not isinstance(usuarios, list):
            raise ValueError("Resposta inesperada da API")
        
        return usuarios
    
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return []
    
    except ValueError as e:
        print(f"Erro de validação: {e}")
        return []
    pass
# lista de dicionario de posts
def fetch_posts() -> list[dict]:
   
    url = "https://jsonplaceholder.typicode.com/posts"

    try:
        response = requests.get(url)
        response.raise_for_status()
        posts = response.json()

        if not isinstance(posts, list):
            raise ValueError("Resposta inesperada da API")
        
        return posts
    
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return []
    except ValueError as e:
        print(f"Erro de validação: {e}")
        return []
    pass
