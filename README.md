# HackCheck API
 HackCheck is a fully automated hackathon platform where participants solve a set number of coding challenges within a given time. It features real-time code evaluation, automatic scoring, and a leaderboard system. The backend is built with Python and Django, while the frontend uses Next.js. It also integrates a judge system like CodeRunner for automated code execution and grading.

# Softwares being used: Django PostgreSQL

# Extra details
1. At any time, only one hackathon will be active.
2. The entire team will have the same login. Before the hackathon begins, they will be allowed to login and enter what name they will be using.

## To-Do Items:
1. User and Admin accounts with JWT authentication using a {length of hackathon} lifetime. [DONE]
NOTE: the user account is just the team account. The jwt token sent to the user will contain the TeamMember instance of the participant which will be used for storage of information.
2. Admin should have the functionality to edit/add/remove questions. [DONE]
3. Admin show have the ability to add/edit/remove sample input and output similar to hackerrank. [DONE] [Just edit the question]
4. Admin should be able to reset the database to a clean state for the next hackathon. [DONE]
5. Ability for the user to test their code with 3 test input and output (Backend part is to just store these?) [IF backend end part is to store, then done]
6. Each participant is part of a team, and the score is tabulated for the whole team. The score is based on the time spent till submission of the code. [DONE]
7. Store all the data sent by any user to keep accurate data tracking (and data saving for redundancy) [DONE]
8. API to send the participant's code to the database. [DONE]

9. Make a bool that tells if hackathon has started or not -> and then allow participant interaction [DONE]
10. Make a request to get points of a particular team / all the teams. [DONE] [if all returns a sorted by point version]
11. Server-side timing of hackathon [DONE]
12. Request to get time left in the hackathon [DONE]
13. Endpoint to get all questions / edit questions [DONE]
14. Endpoint to get leaderboard - Just team name and points in decreasing order [DONE] [with through point 10]
15. Ability to pause/[DONE] edit the time left [DONE]
16. Delete teams [DONE]
17. 4 Test input and output add to the question [DONE]
18. Verify only 4 test in/out are saved for Question and 3 sample in/out when creating the question [DONE]
19. Save which tests the user's answer failed
20. View logs to filter through all the data and see bs (this gonna be ehhh)
21. Export results
22. Question status for each team profile: CORRECT/INCORRECT/NOT_ANSWERED [DONE] [updated the get_questions endpoint]
23. Endpoint to get all the teams and password [DONE]

## Useful tools:
1. [SQL Browser](https://sqlitebrowser.org/dl/)