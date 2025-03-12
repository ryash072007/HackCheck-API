from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from db.models import Question
from db.models.user import TeamProfile
from rest_framework.permissions import IsAuthenticated


class GetTeamPoints(APIView):
    """"
    Get points of a team or all teams.
    """
    
    def post(self, request):
        team_id = request.data.get('team_id', None)
        if team_id is None or team_id == "ALL":
            teams = TeamProfile.objects.all().order_by('-score')
            data = [{'id': team.id, 'team_name': team.team_name, 'score': team.score} for team in teams]
            return Response({'teams': data}, status=status.HTTP_200_OK)
        else:
            try:
                team = TeamProfile.objects.get(id=team_id)
                return Response({'score': team.score}, status=status.HTTP_200_OK)
            except TeamProfile.DoesNotExist:
                return Response({'error': 'Team not found'}, status=status.HTTP_404_NOT_FOUND)

class GetAllQuestions(APIView):
    """
    Get all questions.
    """
    
    permission_classes = [IsAuthenticated]

    def post(self, request):
        questions = Question.objects.all()
        data = [{'id': question.id, 'question': question.title, 'question_name': question.number} for question in questions]
        return Response({'questions': data}, status=status.HTTP_200_OK)