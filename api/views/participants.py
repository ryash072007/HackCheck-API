from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from api.helper import extract_info_from_jwt
from db.models.question import Answer, Question
from db.models.user import TeamMember
from db.models import HackathonSettings


class SubmitAnswer(APIView):
    """
    Submit answer for a question in a quiz.
    This endpoint requires a valid JWT token and returns the response.

    Created by Yash Raj on 12/03/2025
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Submit answer for a question in a quiz.
        """

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

        is_correct_answer = request.data.get("is_correct_answer", False)
        code = request.data.get("code", None)
        question_num = request.data.get("question_number", None)

        request_data = extract_info_from_jwt(request)

        if not code:
            return Response(
                {"error": "Code is required to submit answer."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not question_num:
            return Response(
                {"error": "Question number is required to submit answer."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        question = Question.objects.get(number=question_num)
        team_member = TeamMember.objects.get(id=request_data["participant"]["id"])

        print("[IMPLEMENTATION WARNING] SCORE FUNCTION TO BE IMPLEMENTED")
        score = 0
        team_member.team.score += score
        team_member.team.save()

        Answer.objects.create(
            question=question,
            answer_code=code,
            is_correct_answer=is_correct_answer,
            score=score,
            team_member=team_member,
        )

        return Response(
            {"message": "Answer submitted successfully."},
            status=status.HTTP_200_OK,
        )
