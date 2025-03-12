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
                status=status.HTTP_403_FORBIDDEN
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
                
                return Response({
                    "message": "Database successfully reset for new hackathon",
                    "deleted": {
                        "accounts": account_count,
                        "teams": team_count,
                        "members": member_count,
                        "questions": question_count,
                        "answers": answer_count
                    }
                }, status=status.HTTP_200_OK)
                
        except Exception as e:
            return Response({
                "error": f"An error occurred while resetting the database: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)