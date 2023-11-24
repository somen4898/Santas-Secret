# utils.py

import random
from django.core.mail import send_mail
from django.conf import settings


def assign_secret_santas(participants):
    shuffled = participants[:]
    random.shuffle(shuffled)
    pairings = {}
    for i in range(len(shuffled)):
        gifter = shuffled[i]
        giftee = shuffled[(i + 1) % len(shuffled)]
        pairings[gifter] = giftee
    return pairings


def send_secret_santa_emails(participants, pairings, event_details):
    for participant in participants:
        giftee = pairings[participant]
        subject = "Your Secret Santa Assignment"
        message = f"Hello {participant.name}, you are Secret Santa for {giftee.name}! " \
                  f"The event is on {event_details.date} with a budget of {event_details.budget}."
        send_mail(subject, message, settings.EMAIL_HOST_USER, [participant.email])
