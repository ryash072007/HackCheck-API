from rest_framework_simplejwt.authentication import JWTAuthentication
from db.models import TeamMember


class TeamParticipantAuthentication(JWTAuthentication):
    """
    Custom JWT authentication that adds participant info to the request
    """

    def authenticate(self, request):
        result = super().authenticate(request)

        if result is None:
            return None

        user, validated_token = result

        # Add participant info to request if available in token
        participant_id = validated_token.get("participant_id")
        if participant_id:
            try:
                participant = TeamMember.objects.get(id=participant_id)
                # Attach participant to request for easy access in views
                request.participant = participant
            except TeamMember.DoesNotExist:
                pass

        return result
