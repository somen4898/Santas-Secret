from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import submit_participants, ParticipantViewSet, EventDetailsViewSet

router = DefaultRouter()
router.register(r'participants', ParticipantViewSet)
router.register(r'event-details', EventDetailsViewSet)

urlpatterns = [
    path('api/submit-participants/', submit_participants, name='submit-participants'),
    path('api/', include(router.urls)),
]
