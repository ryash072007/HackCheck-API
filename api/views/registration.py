from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from db.models import Account, TeamProfile
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from django.db import transaction


class TeamRegistration(APIView):
    """
    Team registration view.
    Creates an Account and associated TeamProfile.

    Created by Yash Raj on 11/03/2025
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):

        if not request.user.is_admin:
            return Response(
                {"error": "You don't have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

        team_name = request.data.get("team_name")
        password = request.data.get("password")

        # Validate inputs
        if not team_name or not password:
            return Response(
                {"error": "Team name and password are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if team name is available
        if Account.objects.filter(username=team_name).exists():
            return Response(
                {"error": "Team name already taken"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Create account and team profile in a transaction
        try:
            with transaction.atomic():
                # Create the account
                account = Account.objects.create_user(
                    username=team_name, password=password, is_admin=False
                )

                # Create the team profile
                team = TeamProfile.objects.create(
                    account=account,
                    team_name=team_name,
                    score=0,
                    participants_registered=0,
                    team_password=password,
                )

            return Response(
                {
                    "message": f"Team {team_name} registered successfully",
                    "team_id": team.id,
                    "team_name": team.team_name,
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return Response(
                {"error": f"Registration failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
