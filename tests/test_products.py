import pytest
from models.products import Product, Business, Category
from database.base import get_test_database
import pytest_asyncio

product_data = {

    "title": "Fjallraven - Foldsack No. 1 Backpack, Fits 15 Laptops",
    "price": 109.95,
    "description": "Your perfect pack for everyday use and walks in the forest. Stash your laptop (up to 15 inches) in the padded sleeve, your everyday",
    "images": ["https://fakestoreapi.com/img/81fPKd-2AYL._AC_SL1500_.jpg"],
    "rating": 3.9,
    "count": 120,
}

business_data = {
    "name":"TestCompany",
    "image": "https://media.istockphoto.com/id/696570136/tr/foto%C4%9Fraf/ku%C5%9F-g%C3%B6z-g%C3%B6r%C3%BC%C5%9F-i%C5%9F.jpg?s=612x612&w=0&k=20&c=u-1pVLDu1JrEBpICNpXfmEUl8RciLLq4T7CXURQEfMA=",
    "country": "Turkey"
}

category_data = {
    "name": "Clothes"
}


@pytest.mark.anyio
async def test_create_product():

    await Product.all().delete()
    await Business.all().delete()
    await Category.all().delete()

    business = await Business.create(**business_data)
    category = await Category.create(**category_data)


    product = await Product.create(**product_data)
    await product.business.add(business)
    await product.category.add(category)

    product = await Product.filter(rating=3.9).first()

    product_business = await product.business.all().first()

    assert product_business.name == business_data["name"]

    assert product.title == product_data['title']

    assert await product.filter(title=product.title).count() == 1