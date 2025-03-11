# HackCheck API
 HackCheck is a fully automated hackathon platform where participants solve a set number of coding challenges within a given time. It features real-time code evaluation, automatic scoring, and a leaderboard system. The backend is built with Python and Django, while the frontend uses Next.js. It also integrates a judge system like CodeRunner for automated code execution and grading.

# Softwares being used: Django PostgreSQL

# Extra details
1. At any time, only one hackathon will be active.
2. The entire team will have the same login. Before the hackathon begins, they will be allowed to login and enter what name they will be using.

## To-Do Items:
1. User and Admin accounts with JWT authentication using a {length of hackathon} lifetime. [DONE]
NOTE: the user account is just the team account. The jwt token sent to the user will contain the TeamMember instance of the participant which will be used for storage of information.
2. Admin should have the functionality to edit/add/remove questions.
3. Admin show have the ability to add/edit/remove sample input and output similar to hackerrank.
4. Admin should be able to reset the database to a clean state for the next hackathon.
5. Ability for the user to test their code with 3 test input and output (Backend part is to just store these?)
6. Each participant is part of a team, and the score is tabulated for the whole team. The score is based on the time spent till submission of the code.
7. Store all the data sent by any user to keep accurate data tracking (and data saving for redundancy)

## Useful tools:
1. [SQL Browser](https://sqlitebrowser.org/dl/)