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
    budget = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return f"Event on {self.date} with budget {self.budget}"

class Pairing(models.Model):
    gifter = models.ForeignKey(Participant, related_name='gifts_given', on_delete=models.CASCADE)
    giftee = models.ForeignKey(Participant, related_name='gifts_received', on_delete=models.CASCADE)
    event = models.ForeignKey(EventDetails, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.gifter.name} -> {self.giftee.name}"
