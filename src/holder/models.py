from tortoise import fields, models


class Holder(models.Model):
    id = fields.BigIntField(pk=True)
    address = fields.CharField(max_length=500, unique=True)