from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from db.models import HackathonSettings

class ChangeMaxParticipants(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_admin:
            return Response(
                {"error": "You don't have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )
        
        max_participants = request.data.get('max_participants')
        if not max_participants:
            return Response(
                {"error": "max_participants is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        hackathon_settings = HackathonSettings.get_instance()
        hackathon_settings.max_team_size = max_participants
        hackathon_settings.save()

        return Response(
            {"message": f"Max participants changed successfully to {hackathon_settings.max_team_size}"},
            status=status.HTTP_200_OK,
        )