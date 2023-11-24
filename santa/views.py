# views.py
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from rest_framework import viewsets
from .models import Participant, EventDetails
from .serializers import ParticipantSerializer, EventDetailsSerializer
from .utils import assign_secret_santas, send_secret_santa_emails, \
    generate_pairings_response  # Assuming you have a function to send emails
import json


# View for handling the submission of participants
@csrf_exempt
@require_http_methods(["POST"])
def submit_participants(request):
    try:
        data = json.loads(request.body)
        participant_data = data.get('participants')
        participants = [Participant(**pdata) for pdata in participant_data]

        # Save participants to the database
        Participant.objects.bulk_create(participants)

        return JsonResponse({'message': 'Participants submitted successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


# ViewSet for Participant model
class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer


# ViewSet for EventDetails model
class EventDetailsViewSet(viewsets.ModelViewSet):
    queryset = EventDetails.objects.all()
    serializer_class = EventDetailsSerializer

    def perform_create(self, serializer):
        event_details = serializer.save()  # Save event details
        participants = list(Participant.objects.all())
        pairings = assign_secret_santas(participants, event_details)
        pairing_response = generate_pairings_response(participants, pairings)

        # Include this response in the JSON output
        self.response = {'event_details': serializer.data, 'pairings': pairing_response}
