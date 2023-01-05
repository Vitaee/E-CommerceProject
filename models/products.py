from unicodedata import category
from tortoise import fields, models

class Product(models.Model):
    id = fields.BigIntField(pk=True)
    title = fields.CharField(max_length=150, null=True)
    description = fields.TextField(null=True)
    price = fields.FloatField(null=True)
    images = fields.JSONField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True, null=True)
    updated_at = fields.DatetimeField(auto_now=True, null=True)
    count = fields.IntField(null=True)
    rating = fields.FloatField(null=True)
    business = fields.ManyToManyField("models.Business", related_name='product_owner', through='products_owner')
    category = fields.ManyToManyField('models.Category', related_name='products', through='product_category')

    class Meta:
        table = 'products'

    class PydanticMeta:
        computed = ["get_all_business", "get_all_categories"]



    async def get_all_business(self):
        business = await self.business.all()
        return  business[0].name

    async def get_all_categories(self):
        categories = await self.category.all()
        return  categories[0].name

    def __str__(self):
        return self.title

class Business(models.Model):
    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=100, null=True)
    country = fields.CharField(max_length=100, null=True)
    image = fields.TextField(null=True)
    business_owner = fields.ForeignKeyField('models.User', related_name='business_owner', null=True, on_delete=fields.SET_NULL)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = 'business'
    
    def __str__(self) -> str:
        return self.name

class Category(models.Model):
    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=100, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = 'category'
    
    def __str__(self) -> str:
        return self.name


