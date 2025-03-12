from datetime import datetime
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

class StartHackathon(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_admin:
            return Response(
                {"error": "You don't have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )
        
        hackathon_settings = HackathonSettings.get_instance()
        if hackathon_settings.has_started:
            return Response(
                {"error": "Hackathon has already started."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        hackathon_settings.has_started = True
        hackathon_settings.has_ended = False
        hackathon_settings.time_started = datetime.now()
        hackathon_settings.save()

        return Response(
            {"message": "Hackathon started successfully."},
            status=status.HTTP_200_OK,
        )

class EndHackathon(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_admin:
            return Response(
                {"error": "You don't have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )
        
        hackathon_settings = HackathonSettings.get_instance()
        if hackathon_settings.has_ended:
            return Response(
                {"error": "Hackathon has already ended."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        hackathon_settings.has_started = False
        hackathon_settings.has_ended = True
        hackathon_settings.time_ended = datetime.now()
        hackathon_settings.save()

        return Response(
            {"message": "Hackathon ended successfully."},
            status=status.HTTP_200_OK,
        )

class PauseHackathon(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_admin:
            return Response(
                {"error": "You don't have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )
        
        hackathon_settings = HackathonSettings.get_instance()
        if hackathon_settings.is_paused:
            return Response(
                {"error": "Hackathon is already paused."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        hackathon_settings.is_paused = True
        hackathon_settings.time_paused = datetime.now()
        hackathon_settings.save()

        return Response(
            {"message": "Hackathon paused successfully."},
            status=status.HTTP_200_OK,
        )

class ResumeHackathon(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_admin:
            return Response(
                {"error": "You don't have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )
        
        hackathon_settings = HackathonSettings.get_instance()
        if not hackathon_settings.is_paused:
            return Response(
                {"error": "Hackathon is not paused."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        hackathon_settings.is_paused = False
        current_time = datetime.now()
        pause_time = hackathon_settings.time_paused
        if pause_time.tzinfo is not None:
            pause_time = pause_time.replace(tzinfo=None)
        hackathon_settings.time_spent_paused += current_time - pause_time
        hackathon_settings.save()

        return Response(
            {"message": "Hackathon resumed successfully."},
            status=status.HTTP_200_OK,
        )

class GetTimeLeft(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        hackathon_settings = HackathonSettings.get_instance()
        if not hackathon_settings.has_started:
            return Response(
                {"error": "Hackathon has not started yet."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if hackathon_settings.has_ended:
            return Response(
                {"error": "Hackathon has ended."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        current_time = datetime.now()
        time_started = hackathon_settings.time_started
        if time_started.tzinfo is not None:
            time_started = time_started.replace(tzinfo=None)
        if hackathon_settings.is_paused:
            current_time = hackathon_settings.time_paused
            if current_time.tzinfo is not None:
                current_time = current_time.replace(tzinfo=None)
        time_left = hackathon_settings.duration - (current_time - time_started - hackathon_settings.time_spent_paused)
        return Response(
            {"time_left": time_left.total_seconds()},
            status=status.HTTP_200_OK,
        )

