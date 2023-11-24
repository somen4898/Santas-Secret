# utils.py

import random
from django.core.mail import send_mail
from django.conf import settings

from .models import Pairing


def assign_secret_santas(participants, event_details):
    shuffled = participants[:]
    random.shuffle(shuffled)
    pairings = []
    for i in range(len(shuffled)):
        gifter = shuffled[i]
        giftee = shuffled[(i + 1) % len(shuffled)]
        pairing = Pairing(gifter=gifter, giftee=giftee, event=event_details)
        pairings.append(pairing)

    Pairing.objects.bulk_create(pairings)  # Save pairings to the database
    return pairings


def send_secret_santa_emails(participants, pairings, event_details):
    for participant in participants:
        giftee = pairings[participant]
        subject = "Your Secret Santa Assignment"
        message = f"Hello {participant.name}, you are Secret Santa for {giftee.name}! " \
                  f"The event is on {event_details.date} with a budget of {event_details.budget}."
        send_mail(subject, message, settings.EMAIL_HOST_USER, [participant.email])


def generate_pairings_response(participants, pairings):
    pairing_response = []
    for participant in participants:
        giftee = pairings[participant]
        pairing_info = {'gifter': participant.name, 'giftee': giftee.name}
        pairing_response.append(pairing_info)
    return pairing_response
