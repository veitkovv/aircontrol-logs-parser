from django.db import models


class Roll(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя ролла', db_index=True)
    description = models.CharField(max_length=255, verbose_name='Опциональное описание ролла', blank=True,
                                   db_index=True)
    uuid = models.CharField(max_length=64, verbose_name='Cinegy UUID', db_index=True)
    category = models.CharField(max_length=64, verbose_name='Категория ролла')
    start = models.DateTimeField(verbose_name='Время и дата начала')
    end = models.DateTimeField(verbose_name='Время и дата окончания', null=True)

    class Meta:
        unique_together = ('start', 'end', 'name', 'uuid', 'description')

    def __str__(self):
        if self.description:
            return f'{self.name} "{self.description}": {self.uuid}'
        return f'{self.name}: {self.uuid}'

    @property
    def duration(self):
        return self.end - self.start
