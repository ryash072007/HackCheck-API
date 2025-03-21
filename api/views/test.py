from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


class TestAuthenticationView(APIView):
    """
    Simple test view to verify JWT authentication and check token claims.
    This endpoint requires a valid JWT token and returns the claims in the token.

    Created by Yash Raj on 11/03/2025
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Returns JWT token claims and attached participant information.
        """
        # Get basic information
        response_data = {
            "is_authenticated": request.user.is_authenticated,
            "user_id": request.user.id,
            "username": request.user.username,
        }

        # Check if participant info is attached to request
        if hasattr(request, "participant"):
            response_data["participant"] = {
                "id": request.participant.id,
                "name": request.participant.name,
                "team_id": request.participant.team_id,
            }
        else:
            response_data["participant"] = (
                "No participant information attached to request"
            )

        return Response(response_data, status=status.HTTP_200_OK)

def custom_404_view(request, exception=None):
    return render(request, "404.html", status=404)