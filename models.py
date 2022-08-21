from tortoise.models import Model
from tortoise import fields


class TelegramUser(Model):
    id = fields.IntField(pk=True)
    telegram_id = fields.BigIntField(unique=True, index=True)
    active = fields.BooleanField(default=True)
    state = fields.CharField(16, default='')

    @property
    async def format_words(self):
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