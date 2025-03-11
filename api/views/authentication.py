from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from db.models import Account, TeamProfile, TeamMember

class TeamSignIn(APIView):
    """
    Team login view.
    """
    def post(self, request):
        team_name = request.data.get('team_name')
        password = request.data.get('password')
        
        try:
            account = Account.objects.get(username=team_name)
        except Account.DoesNotExist:
            return Response({'error': 'Invalid team name or password'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not account.check_password(password):
            return Response({'error': 'Invalid team name or password'}, status=status.HTTP_400_BAD_REQUEST)
        
        team = TeamProfile.objects.get(account=account)
        token = RefreshToken.for_user(account)
        
        return Response({
            'team_name': team.team_name,
            'score': team.score,
            'token': str(token.access_token),
        })