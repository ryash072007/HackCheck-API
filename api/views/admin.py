from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db import transaction
from db.models import TeamProfile, TeamMember, Question, Answer, Account


class ResetHackathon(APIView):
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
                team.delete()

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


class AddQueston(APIView):
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
                "missing_fields": missing_fields
            },
            status=status.HTTP_400_BAD_REQUEST,
            )

        
        if not isinstance(samples, dict) or not isinstance(tests, dict):
            return Response(
                {"error": "Samples and tests must be dictionaries."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if len(samples) != 3 or len(tests) != 4:
            return Response(
                {"error": "Samples must have 3 inputs and tests must have 4 inputs."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        print(samples)
        print(tests)

        question_number = Question.objects.count() + 1

        try:
            question = Question.objects.create(
                title=title,
                description=description,
                samples=samples,
                tests=tests,
                number=question_number,
            )
            return Response(
                {
                    "message": "Question successfully added.",
                    "question": {"id": question.id, "title": question.title},
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return Response(
                {"error": f"An error occurred while adding the question: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
