import requests 
import pandas as pd


# lista de dicionario de usuarios
def fetch_usuarios() -> list[dict]:

    url = "https://jsonplaceholder.typicode.com/users"

    try:
        response = requests.get(url, timeout=30) # desiste se a API nao responder em 30s
        response.raise_for_status() #validação do HTTP
        usuarios = response.json()

        if not isinstance(usuarios, list):
            raise ValueError("Resposta inesperada da API")

        return usuarios

    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        raise # repassa o erro para o Airflow marcar a task como falha

    except ValueError as e:
        print(f"Erro de validação: {e}")
        raise
pass
# lista de dicionario de posts
def fetch_posts() -> list[dict]:
   
    url = "https://jsonplaceholder.typicode.com/posts"

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        posts = response.json()

        if not isinstance(posts, list):
            raise ValueError("Resposta inesperada da API")

        return posts

    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        raise
    except ValueError as e:
        print(f"Erro de validação: {e}")
        raise
pass

def flatte_usuario(usuario: dict) -> dict:
    return{
        "id": usuario.get("id"),
        "name": usuario.get("name"),
        "username": usuario.get("username"),
        "email": usuario.get("email"),
        "address_street": usuario.get("address", {}).get("street"),
        "address_city": usuario.get("address", {}).get("city"),
        "address_zipcode": usuario.get("address", {}).get("zipcode"),
        "phone": usuario.get("phone"),
        "website": usuario.get("website"),
        "company_name": usuario.get("company", {}).get("name")
    }
pass

def extract_usuarios() -> pd.DataFrame:
    usuarios = fetch_usuarios()
    ususarios_flet = [flatte_usuario(u) for u in usuarios]

    df = pd.DataFrame(ususarios_flet) # Converte o JSON para um DF
    df["dl_load_timestamp"] = pd.Timestamp.now() # inserir a coluna de datetime no df

    return df
pass

def extract_posts() -> pd.DataFrame:
    posts = fetch_posts()

    df = pd.DataFrame(posts)
    df = df.rename(columns={"userId": "user_id"}) # correcao para o padrão da tabela raw_posts
    df["dl_load_timestamp"] = pd.Timestamp.now()

    return df
pass
