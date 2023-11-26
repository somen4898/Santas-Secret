from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from rest_framework import viewsets, serializers
from .models import Participant, EventDetails
from .serializers import ParticipantSerializer, EventDetailsSerializer
from .utils import assign_secret_santas, generate_pairings_response
import json
from django.shortcuts import redirect
import uuid

# Start the user interaction and generate a session_id
def start_user_interaction(request):
    # Generate and set session_id if it's not already set
    if 'session_id' not in request.session:
        request.session['session_id'] = str(uuid.uuid4())

    # Redirect to the next step, e.g., a form for creating an event
    return redirect('create_event_form')

# View for handling the submission of participants
@csrf_exempt
@require_http_methods(["POST"])
def submit_participants(request):
    try:
        session_id = request.session.get('session_id')
        if not session_id:
            return JsonResponse({'error': 'Session ID is missing'}, status=400)

        data = json.loads(request.body)
        participant_data = data.get('participants')
        participants = [Participant(session_id=session_id, **pdata) for pdata in participant_data]

        Participant.objects.bulk_create(participants)

        return JsonResponse({'message': 'Participants submitted successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


# ViewSet for Participant model
class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer

    def perform_create(self, serializer):
        session_id = self.request.session.get('session_id')
        if not session_id:
            # Handle the case where session_id is not set
            raise serializers.ValidationError("Session ID is missing")

        serializer.save(session_id=session_id)


# ViewSet for EventDetails model
class EventDetailsViewSet(viewsets.ModelViewSet):
    queryset = EventDetails.objects.all()
    serializer_class = EventDetailsSerializer

    def perform_create(self, serializer):
        session_id = self.request.session.get('session_id')
        if not session_id:
            raise serializers.ValidationError("Session ID is missing")

        event_details = serializer.save(session_id=session_id)
        participants = Participant.objects.filter(session_id=session_id)
        pairings = assign_secret_santas(participants, event_details)
        pairing_response = generate_pairings_response(participants, pairings)

        # Return this response
        return JsonResponse({'event_details': serializer.data, 'pairings': pairing_response})
