from django.db import models
from django.core.exceptions import ValidationError


def validate_positive(value):
    if value < 0:
        raise ValidationError('Value must be positive')


class Participant(models.Model):
    name = models.CharField(max_length=50, )
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class EventDetails(models.Model):
    budget = models.IntegerField(validators=[validate_positive])
    date = models.DateField()
