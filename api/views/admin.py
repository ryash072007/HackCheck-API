from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db import transaction
from db.models import (
    TeamProfile,
    TeamMember,
    Question,
    Answer,
    Account,
    HackathonSettings,
)


class ResetHackathonDatabase(APIView):
    """
    Admin endpoint to reset all hackathon data.
    This clears all team profiles, members, questions, answers, and non-admin accounts.
    Admin accounts are preserved.

    Requires admin authentication.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        # First check if the user is an admin
        if not request.user.is_admin:
            return Response(
                {"error": "You don't have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            with transaction.atomic():
                # Delete all answers first (to respect foreign key constraints)
                answer_count = Answer.objects.all().count()
                Answer.objects.all().delete()

                # Delete all questions
                question_count = Question.objects.all().count()
                Question.objects.all().delete()

                # Delete all team members
                member_count = TeamMember.objects.all().count()
                TeamMember.objects.all().delete()

                # Get team profiles for counting
                team_count = TeamProfile.objects.all().count()

                # Get non-admin accounts for deletion
                non_admin_accounts = Account.objects.filter(is_admin=False)
                account_count = non_admin_accounts.count()

                # Delete all team profiles (will cascade delete the related accounts)
                TeamProfile.objects.all().delete()

                # Delete any remaining non-admin accounts
                non_admin_accounts.delete()

                return Response(
                    {
                        "message": "Database successfully reset for new hackathon",
                        "deleted": {
                            "accounts": account_count,
                            "teams": team_count,
                            "members": member_count,
                            "questions": question_count,
                            "answers": answer_count,
                        },
                    },
                    status=status.HTTP_200_OK,
                )

        except Exception as e:
            return Response(
                {"error": f"An error occurred while resetting the database: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class DeleteTeam(APIView):
    """
    Admin endpoint to delete a team by its ID.

    Requires admin authentication.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_admin:
            return Response(
                {"error": "You don't have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

        team_id = request.data.get("team_id")
        if not team_id:
            return Response(
                {"error": "Missing 'team_id' in request body."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            with transaction.atomic():
                team = TeamProfile.objects.get(id=team_id)
                account = team.account
                team.delete()
                account.delete()

                return Response(
                    {"message": f"Team {team_id} successfully deleted."},
                    status=status.HTTP_200_OK,
                )

        except TeamProfile.DoesNotExist:
            return Response(
                {"error": f"Team {team_id} does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            return Response(
                {"error": f"An error occurred while deleting team {team_id}: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class AddQuestion(APIView):
    """
    Admin endpoint to add a new question.

    Requires admin authentication.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_admin:
            return Response(
                {"error": "You don't have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

        title = request.data.get("title")
        description = request.data.get("description")
        samples = request.data.get("samples")
        tests = request.data.get("tests")
        difficulty = request.data.get("difficulty")

        # Check each required field and provide specific error messages
        missing_fields = []
        if not title:
            missing_fields.append("title")
        if not description:
            missing_fields.append("description")
        if not samples:
            missing_fields.append("samples")
        if not tests:
            missing_fields.append("tests")

        if missing_fields:
            return Response(
                {
                    "error": f"Missing required fields: {', '.join(missing_fields)}",
                    "missing_fields": missing_fields,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not isinstance(samples, dict) or not isinstance(tests, dict):
            return Response(
                {"error": "Samples and tests must be dictionaries."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        if not ("input" in samples and "output" in samples):
            return Response(
                {"error": "Samples must have 'input' and 'output' keys."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        if not ("input" in tests and "output" in tests):
            return Response(
                {"error": "Tests must have 'input' and 'output' keys."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if difficulty not in ["easy", "medium", "hard"]:
            return Response(
                {"error": "Difficulty must be 'easy', 'medium', or 'hard'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        question_number = Question.objects.count() + 1

        try:
            question = Question.objects.create(
                title=title,
                description=description,
                samples=samples,
                tests=tests,
                number=question_number,
                difficulty=difficulty,
            )
            return Response(
                {
                    "message": "Question successfully added.",
                    "question": {
                        "id": question.id,
                        "question_number": question.number,
                        "title": question.title,
                        "difficulty": question.difficulty,
                    },
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return Response(
                {"error": f"An error occurred while adding the question: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class RemoveQuestion(APIView):
    """
    Admin endpoint to remove a question by its ID.

    Requires admin authentication.
    """

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
                {"error": "Cannot remove questions after the hackathon has started."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if hackathon_settings.has_ended:
            return Response(
                {"error": "Cannot remove questions after the hackathon has ended."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        question_id = request.data.get("question_id")
        question_number = request.data.get("question_number")

        if question_id and question_number:
            return Response(
                {"error": "Provide only one of 'question_id' or 'question_number'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not question_id and not question_number:
            return Response(
                {
                    "error": "Missing 'question_id' or 'question_number' in request body."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if question_number:
            question_id = (
                Question.objects.filter(number=question_number)
                .values_list("id", flat=True)
                .first()
            )

        try:
            question = Question.objects.get(id=question_id)
            question.delete()

            with transaction.atomic():
                remaining_questions = Question.objects.all().order_by('number')
                for i, q in enumerate(remaining_questions, 1):
                    if q.number != i:
                        q.number = i
                        q.save()

            return Response(
                {"message": f"Question id {question_id} successfully removed."},
                status=status.HTTP_200_OK,
            )

        except Question.DoesNotExist:
            return Response(
                {"error": f"Question {question_id} does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            return Response(
                {
                    "error": f"An error occurred while removing question {question_id}: {str(e)}"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class UpdateQuestion(APIView):
    """
    Admin endpoint to update a question by its ID or number.

    Requires admin authentication.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_admin:
            return Response(
                {"error": "You don't have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

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

        title = request.data.get("title")
        description = request.data.get("description")
        samples = request.data.get("samples")
        tests = request.data.get("tests")
        difficulty = request.data.get("difficulty")

        if title is not None:
            question.title = title

        if description is not None:
            question.description = description

        if samples is not None:
            if not isinstance(samples, dict):
                return Response(
                    {"error": "Samples must be a dictionary."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            question.samples = samples

        if tests is not None:
            if not isinstance(tests, dict):
                return Response(
                    {"error": "Tests must be a dictionary."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            question.tests = tests
        
        if difficulty is not None:
            if difficulty not in ["easy", "medium", "hard"]:
                return Response(
                    {"error": "Difficulty must be 'easy', 'medium', or 'hard'."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            question.difficulty = difficulty

        try:
            question.save()
            return Response(
                {
                    "message": "Question successfully updated.",
                    "question": {
                        "id": question.id,
                        "question_number": question.number,
                        "title": question.title,
                        "difficulty": question.difficulty,
                    },
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": f"An error occurred while updating the question: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class GetTeams(APIView):
    """
    Admin endpoint to get all team profiles.

    Requires admin authentication.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_admin:
            return Response(
                {"error": "You don't have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

        teams = TeamProfile.objects.all()
        team_data = [
            {"id": team.id, "name": team.team_name, "password": team.team_password}
            for team in teams
        ]

        return Response({"teams": team_data}, status=status.HTTP_200_OK)


class AdminDashboard(APIView):
    """
    Admin endpoint to get all team profiles, questions, and answers.

    Requires admin authentication.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_admin:
            return Response(
                {"error": "You don't have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

        hackathon_settings = HackathonSettings.get_instance()
        hackathon_status = hackathon_settings.has_started

        num_teams = TeamProfile.objects.count()
        num_questions = Question.objects.count()
        total_answers = Answer.objects.count()

        # Get current time for calculating time remaining
        current_time = datetime.now()
        time_started = hackathon_settings.time_started
        
        # Normalize timezone if present to prevent timezone-related calculation issues
        if time_started.tzinfo is not None:
            time_started = time_started.replace(tzinfo=None)
            
        # If hackathon is paused, use the pause time instead of current time
        if hackathon_settings.is_paused:
            current_time = hackathon_settings.time_paused
            if current_time.tzinfo is not None:
                current_time = current_time.replace(tzinfo=None)
            
        # Calculate time left: hackathon duration minus elapsed time (excluding paused periods)
        time_left = hackathon_settings.duration - (
            current_time - time_started - hackathon_settings.time_spent_paused
        )
        # Convert to seconds for client-side use
        time_left_seconds = time_left.total_seconds()

        return Response(
            {
                "hackathon_status": hackathon_status,
                "num_teams": num_teams,
                "num_questions": num_questions,
                "total_answers": total_answers,
                "time_left_seconds": time_left_seconds,
            },
            status=status.HTTP_200_OK,
        )


class GetScoreSettings(APIView):
    """
    Admin endpoint to get the score settings for the hackathon.

    Requires admin authentication.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_admin:
            return Response(
                {"error": "You don't have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

        hackathon_settings = HackathonSettings.get_instance()
        score_settings = {
            "max_score": hackathon_settings.max_score,
            "score_decrement_interval_seconds": hackathon_settings.score_decrement_interval.total_seconds(),
            "score_decrement_per_interval": hackathon_settings.score_decrement_per_interval,
        }

        return Response(score_settings, status=status.HTTP_200_OK)


class UpdateScoreSettings(APIView):
    """
    Admin endpoint to update the score settings for the hackathon.

    Requires admin authentication.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_admin:
            return Response(
                {"error": "You don't have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

        max_score = request.data.get("max_score")
        score_decrement_interval_seconds = request.data.get(
            "score_decrement_interval_seconds"
        )
        score_decrement_per_interval = request.data.get("score_decrement_per_interval")

        if (
            not max_score
            and not score_decrement_interval_seconds
            and not score_decrement_per_interval
        ):
            return Response(
                {
                    "error": "Provide at least one of 'max_score', 'score_decrement_interval_seconds', or 'score_decrement_per_interval'."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        hackathon_settings = HackathonSettings.get_instance()

        if max_score:
            hackathon_settings.max_score = max_score

        if score_decrement_interval_seconds:
            hackathon_settings.score_decrement_interval = timedelta(
                seconds=score_decrement_interval_seconds
            )

        if score_decrement_per_interval:
            hackathon_settings.score_decrement_per_interval = (
                score_decrement_per_interval
            )

        hackathon_settings.save()

        return Response(
            {"message": "Score settings successfully updated."},
            status=status.HTTP_200_OK,
        )


class ExportLeaderboard(APIView):
    """
    Admin endpoint to export the leaderboard as a CSV file.

    Requires admin authentication.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_admin:
            return Response(
                {"error": "You don't have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

        hackathon_settings = HackathonSettings.get_instance()
        if not hackathon_settings.has_started:
            return Response(
                {"error": "The hackathon has not started yet."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        teams = TeamProfile.objects.all().order_by("-score")
        team_data = [
            {
                "Team Name": team.team_name,
                "Score": team.score,
            }
            for team in teams
        ]

        response = Response(team_data, status=status.HTTP_200_OK)

        with open("leaderboard.csv", "w") as f:
            f.write("Team Name,Score\n")
            for team in team_data:
                f.write(f"{team['Team Name']},{team['Score']}\n")

        return response


class ResetCurrentHackathon(APIView):
    """
    Admin endpoint to reset the current hackathon.

    Requires admin authentication.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_admin:
            return Response(
                {"error": "You don't have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

        hacathon_settings = HackathonSettings.get_instance()
        hacathon_settings.has_started = False
        hacathon_settings.has_ended = False
        hacathon_settings.time_started = None
        hacathon_settings.time_paused = None
        hacathon_settings.is_paused = False
        hacathon_settings.time_spent_paused = timedelta(seconds=0)
        hacathon_settings.save()

        Answer.objects.all().delete()
        TeamProfile.objects.all().update(score=0, participants_registered=0)

        return Response(
            {"message": "Current hackathon successfully reset."},
            status=status.HTTP_200_OK,
        )
