import requests

PRODUCTS_URL = "https://fakestoreapi.com/products"


def get_products():
    response = requests.get(PRODUCTS_URL, timeout=10)
    response.raise_for_status()
    return response.json()
