from tortoise import fields, models


class User(models.Model):
    id = fields.BigIntField(pk=True)
    firstname = fields.CharField(max_length=50, null=True)
    lastname = fields.CharField(max_length=20)
    username = fields.CharField(50, unique=True)
    email = fields.CharField(255, unique=True)
    phone = fields.CharField(25, null=True)
    password = fields.CharField(255, null=True)
    avatar = fields.CharField(255, null=True)
    email_confirmed_at = fields.DatetimeField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True, null=True)
    updated_at = fields.DatetimeField(auto_now=True, null=True)
    is_active = fields.BooleanField(default=True)
    roles = fields.ForeignKeyField('models.Role', related_name='user_role')

    class Meta:
        table = 'users'

    class PydanticMeta:
        computed = ["full_name"]
        exclude = ["password"]

    def full_name(self) -> str:
        return f"{self.firstname or ''} {self.lastname or ''}".strip()

    def __str__(self):
        return self.email

class Role(models.Model):
    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=25, unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = 'roles'

    def __str__(self):
        return self.name

class VerifyCode(models.Model):
    id = fields.BigIntField(pk=True)
    email = fields.CharField(max_length=255)
    code = fields.CharField(max_length=255, unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = 'verify_codes'

    def __str__(self):
        return f'{self.email}/{self.code}'