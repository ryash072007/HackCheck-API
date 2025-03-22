from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from db.models import Question
from db.models.question import Answer, SharedCode
from db.models.user import TeamProfile, TeamMember
from rest_framework.permissions import IsAuthenticated
from api.helper import extract_info_from_jwt, get_uuid_path


class GetTeamPoints(APIView):
    """ "
    Get points of a team or all teams.
    """

    def post(self, request):
        team_id = request.data.get("team_id", None)
        if team_id is None or team_id == "ALL":
            teams = TeamProfile.objects.all().order_by("-score")
            data = [
                {
                    "id": team.id,
                    "team_name": team.team_name,
                    "score": team.score,
                    "participants": TeamMember.objects.filter(team=team).values_list(
                        "name", flat=True
                    ),
                }
                for team in teams
            ]
            return Response({"teams": data}, status=status.HTTP_200_OK)
        else:
            try:
                team = TeamProfile.objects.get(id=team_id)
                return Response({"score": team.score}, status=status.HTTP_200_OK)
            except TeamProfile.DoesNotExist:
                return Response(
                    {"error": "Team not found"}, status=status.HTTP_404_NOT_FOUND
                )


class GetAllQuestions(APIView):
    """
    Get the status of all questions for the authenticated user's team.
    This endpoint returns the status of all questions for the team that the authenticated user belongs to.
    The status can be one of the following:
    - 'NOT_ANSWERED': The team has not submitted any answers for the question.
    - 'CORRECT': The team has submitted a correct answer for the question.
    - 'INCORRECT': The team has submitted answers for the question, but none are correct.
    Returns:
        Response: A JSON object with a 'questions' array containing objects with the following fields:
            - question (str): The title of the question.
            - question_name (str): The number/identifier of the question.
            - status (str): The status of the question ('NOT_ANSWERED', 'CORRECT', or 'INCORRECT').

    Get questions status.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):

        if request.user.is_admin:
            questions = Question.objects.all().order_by("number")
            data = []
            for question in questions:
                data.append(
                    {
                        "question": question.title,
                        "question_number": question.number,
                        "question_id": question.id,
                        "difficulty": question.difficulty,
                    }
                )
            return Response(
                {"questions": data, "type": "admin"}, status=status.HTTP_200_OK
            )

        participant_data = extract_info_from_jwt(request)
        team_id = participant_data["participant"]["team_id"]
        team = TeamProfile.objects.get(id=team_id)

        questions = Question.objects.all().order_by("number")

        data = []
        for question in questions:
            q_status = None
            score = 0
            answers = Answer.objects.filter(question=question, team=team)
            if not answers:
                q_status = "NOT_ANSWERED"
            else:
                correct_answers = answers.filter(is_correct_answer=True).exists()
                if correct_answers:
                    q_status = "CORRECT"
                    score = answers.filter(is_correct_answer=True).first().score
                else:
                    q_status = "INCORRECT"

            data.append(
                {
                    "question": question.title,
                    "question_number": question.number,
                    "question_id": question.id,
                    "status": q_status,
                    "score": score,
                    "difficulty": question.difficulty,
                }
            )

        return Response({"questions": data, "type": "team"}, status=status.HTTP_200_OK)


class GetSingleQuestion(APIView):
    """
    Get the status of a single question for the authenticated user's team.
    This endpoint returns the status of a single question for the team that the authenticated user belongs to.
    The status can be one of the following:
    - 'NOT_ANSWERED': The team has not submitted any answers for the question.
    - 'CORRECT': The team has submitted a correct answer for the question.
    - 'INCORRECT': The team has submitted answers for the question, but none are correct.
    Returns:
        Response: A JSON object with a 'question' object containing the following fields:
            - question (str): The title of the question.
            - question_name (str): The number/identifier of the question.
            - status (str): The status of the question ('NOT_ANSWERED', 'CORRECT', or 'INCORRECT').

    Get questions status.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        question_id = request.data.get("question_id")
        question_number = request.data.get("question_number")

        if not question_id and not question_number:
            return Response(
                {
                    "error": "Missing 'question_id' or 'question_number' in request body."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if question_id and question_number:
            return Response(
                {"error": "Provide only one of 'question_id' or 'question_number'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            if question_number:
                question = Question.objects.get(number=question_number)
            else:
                question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return Response(
                {"error": f"Question does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if request.user.is_admin:
            return Response(
                {
                    "question_id": question.id,
                    "title": question.title,
                    "question_number": question.number,
                    "description": question.description,
                    "samples": question.samples,
                    "tests": question.tests,
                    "difficulty": question.difficulty,
                    "type": "admin",
                },
                status=status.HTTP_200_OK,
            )

        participant_data = extract_info_from_jwt(request)
        team_id = participant_data["participant"]["team_id"]
        team = TeamProfile.objects.get(id=team_id)

        q_status = None
        score = 0
        answers = Answer.objects.filter(question=question, team=team)
        if not answers:
            q_status = "NOT_ANSWERED"
        else:
            correct_answers = answers.filter(is_correct_answer=True).exists()
            if correct_answers:
                q_status = "CORRECT"
                score = answers.filter(is_correct_answer=True).first().score
            else:
                q_status = "INCORRECT"

        return Response(
            {
                "question_number": question.number,
                "status": q_status,
                "score": score,
                "question_id": question.id,
                "title": question.title,
                "description": question.description,
                "samples": question.samples,
                "tests": question.tests,
                "difficulty": question.difficulty,
                "type": "team",
            },
            status=status.HTTP_200_OK,
        )


class GetTeamParticipantsNames(APIView):
    """
    Get the names of all participants in a team.
    This endpoint returns the names of all participants in a team.
    Returns:
        Response: A JSON object with a 'participants' array containing the names of the participants.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        participant_data = extract_info_from_jwt(request)
        team_id = participant_data["participant"]["team_id"]
        team = TeamProfile.objects.get(id=team_id)

        participants = TeamMember.objects.filter(team=team).values_list(
            "name", flat=True
        )

        return Response({"participants": list(participants)}, status=status.HTTP_200_OK)


class SaveSharedCode(APIView):
    """
    API endpoint for saving shared code for a team's question.
    This view allows authenticated team members to save shared code related to a specific question.
    The team ID and participant information are extracted from the JWT token in the request.
    Request body must include:
        - shared_code: The code to be shared
        - question_id: The ID of the question the code relates to
        Response: A JSON object with a 'message' indicating success, or an 'error' message
                  with appropriate HTTP status code if the request is invalid.
    Status codes:
        - 200 OK: Code successfully saved
        - 400 BAD REQUEST: Missing required fields in request body
        - 404 NOT FOUND: Specified question does not exist
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        participant_data = extract_info_from_jwt(request)
        team_id = participant_data["participant"]["team_id"]
        team = TeamProfile.objects.get(id=team_id)
        partipant = TeamMember.objects.get(
            id=participant_data["participant"]["id"], team=team
        )

        shared_code = request.data.get("shared_code", None)
        if not shared_code:
            return Response(
                {"error": "Missing 'shared_code' in request body."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        question_number = request.data.get("question_number", None)
        if not question_number:
            return Response(
                {"error": "Missing 'question_id' in request body."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            question = Question.objects.get(number=question_number)
        except Question.DoesNotExist:
            return Response(
                {"error": f"Question does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        SharedCode.objects.create(
            team=team,
            code=shared_code,
            question=question,
            time_shared=datetime.now(),
            team_member=partipant,
        )

        return Response(
            {"message": "Shared code saved successfully."}, status=status.HTTP_200_OK
        )


class GetSharedCode(APIView):
    """
    Retrieve shared code entries for the authenticated user's team.
    This view allows team members to fetch all code that has been shared within their team.
    The shared code entries are ordered by time shared (most recent first).
    Methods:
        post: Retrieve all shared code entries for the authenticated user's team.
    Authentication:
        Requires a valid JWT token from an authenticated user.
    Response:
        200 OK: Returns a list of shared code entries with the following information for each:
            - code: The shared code content
            - question_number: The question number the code is associated with
            - time_shared: The time when the code was shared (HH:MM:SS format)
            - team_member_name: Name of the team member who shared the code
            - static_file: Path to any associated static file
        404 NOT FOUND: If no shared code entries exist for the team
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        participant_data = extract_info_from_jwt(request)
        team_id = participant_data["participant"]["team_id"]
        team = TeamProfile.objects.get(id=team_id)

        shared_code = SharedCode.objects.filter(team=team)
        if shared_code:
            shared_codes_data = []
            for sc in SharedCode.objects.filter(team=team).order_by('-time_shared'):
                shared_codes_data.append({
                    "code": sc.code,
                    "question_number": sc.question.number,
                    "time_shared": sc.time_shared.strftime("%H:%M:%S"),
                    "team_member_name": sc.team_member.name,
                    "static_file": get_uuid_path(sc.file_uuid),
                })
            
            return Response(
                {"shared_codes": shared_codes_data},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"message": "No shared code found for this question."},
                status=status.HTTP_404_NOT_FOUND,
            )