from tortoise.models import Model
from tortoise import fields
from flask_security import UserMixin, RoleMixin


class TelegramUser(Model):
    id = fields.IntField(pk=True)
    telegram_id = fields.BigIntField(unique=True, index=True)
    active = fields.BooleanField(default=True)
    state = fields.CharField(16)

    @property
    def format_words(self):
        string = ''
        for word in await self.keywords.all():
            string += word.text
            string += "+"
        return string

    def __str__(self):
        return str(self.telegram_id)


class Keyword(Model):
    id = fields.IntField(pk=True)
    owner = fields.ForeignKeyField('models.TelegramUser', related_name='keywords', index=True)
    text = fields.CharField(100)


class User(Model, UserMixin):
    id = fields.IntField(pk=True)
    email = fields.CharField(254, unique=True)
    password = fields.CharField(255)
    active = fields.BooleanField()
    roles = fields.ManyToManyField(
        'models.Role', related_name='users', through='roles_users'
    )


class Role(Model, RoleMixin):
    id = fields.IntField(pk=True)
    name = fields.CharField(100, unique=True)
    description = fields.CharField(255)
