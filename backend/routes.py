from fastapi import APIRouter, Path

from api import get_products

router = APIRouter(prefix="/api")


@router.get("/products")
def all_products():
    return get_products()


@router.get("/search/{text}")
def search(text: str = Path(min_length=1)):
    return [p for p in get_products() if text.lower() in p["title"].lower()]


@router.get("/price/{max_price}")
def by_price(max_price: float = Path(ge=0)):
    return [p for p in get_products() if p["price"] <= max_price]


@router.get("/rating/{min_rate}")
def by_rating(min_rate: float = Path(ge=0, le=5)):
    return [p for p in get_products() if p["rating"]["rate"] >= min_rate]
