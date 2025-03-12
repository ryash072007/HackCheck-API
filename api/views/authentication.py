from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from db.models import Account, TeamProfile, TeamMember
from os import environ

class TeamSignIn(APIView):
    """
    Team login view for participant authentication.
    
    Validates team credentials, manages participant registration within team size limits,
    and issues JWT tokens with team and participant information.
    
    Request format:
    - team_name: Team's username
    - password: Team's password
    - participant_name: Name of the participant logging in
    
    Returns:
    - team_name: Name of the team
    - score: Current team score
    - participant_name: Name of the authenticated participant
    - token: JWT access token containing team and participant details
    
    Created by Yash Raj at 8:24PM on 11/03/2025
    """
    def post(self, request):
        team_name = request.data.get('team_name')
        password = request.data.get('password')
        participant_name = request.data.get('participant_name')
        
        try:
            account = Account.objects.get(username=team_name)
        except Account.DoesNotExist:
            return Response({'error': 'Invalid team name or password'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not participant_name:
            return Response({'error': 'Participant name is required'}, status=status.HTTP_400_BAD_REQUEST)

        if not account.check_password(password):
            return Response({'error': 'Invalid team name or password'}, status=status.HTTP_400_BAD_REQUEST)
        
        team = TeamProfile.objects.get(account=account)

        # Check if the participant name already exists in this team
        existing = TeamMember.objects.filter(team=team, name=participant_name).exists()
        
        # Check team size limit if this is a new participant
        if not existing and team.participants_registered >= int(environ.get('MAX_TEAM_SIZE', 4)):
            return Response({'error': 'Team is full'}, status=status.HTTP_400_BAD_REQUEST)

        # Create or get TeamMember
        team_member, created = TeamMember.objects.get_or_create(
            team=team,
            name=participant_name
        )

        # If this is a new team member, increase the count
        if created:
            team.participants_registered += 1
            team.save()

        # Generate token with participant info
        token = RefreshToken.for_user(account)
        
        # Add custom claims directly to the token
        token['team_id'] = team.id
        token['team_name'] = team.team_name
        token['participant_id'] = team_member.id
        token['participant_name'] = team_member.name
        
        return Response({
            'team_name': team.team_name,
            'score': team.score,
            'participant_name': team_member.name,
            'token': str(token.access_token),
        })

class AdminSignIn(APIView):
    """
    Admin login view for admin authentication.
    
    Validates admin credentials and issues JWT tokens with admin information.
    
    Request format:
    - username: Admin username
    - password: Admin password
    
    Returns:
    - username: Username of the admin
    - token: JWT access token containing admin details
    
    Created by Yash Raj on 12/03/2025
    """
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        try:
            account = Account.objects.get(username=username, is_admin=True)
        except Account.DoesNotExist:
            return Response({'error': 'Invalid username'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not account.check_password(password):
            return Response({'error': 'wrong password'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate token with admin info
        token = RefreshToken.for_user(account)
        
        return Response({
            'username': account.username,
            'token': str(token.access_token),
        })