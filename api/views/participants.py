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


        answer = Answer.objects.create(
            question=question,
            answer_code=code,
            is_correct_answer=is_correct_answer,
            team_member=team_member,
        )

        if is_correct_answer:
            time_submitted = answer.time_submitted
            
            time_started = hackathon_settings.time_started
            if time_started.tzinfo is not None:
                time_started = time_started.replace(tzinfo=None)
                
            if time_submitted.tzinfo is not None:
                time_submitted = time_submitted.replace(tzinfo=None)
                
            if hackathon_settings.is_paused:
                time_submitted = hackathon_settings.time_paused
                if time_submitted.tzinfo is not None:
                    time_submitted = time_submitted.replace(tzinfo=None)
            time_left = hackathon_settings.duration - (time_submitted - time_started - hackathon_settings.time_spent_paused)

            hackathon_time_spent = hackathon_settings.duration - time_left
            intervals_done = hackathon_time_spent // hackathon_settings.score_decrement_interval
            score_decrement = hackathon_settings.score_decrement_per_interval * intervals_done
            score = hackathon_settings.max_score - score_decrement

            answer.score = score
            answer.save()

            team_member.team.score += score
            team_member.team.save()

        return Response(
            {"message": "Answer submitted successfully."},
            status=status.HTTP_200_OK,
        )
