# HackCheck UI
 HackCheck is a fully automated hackathon platform where participants solve a set number of coding challenges within a given time. It features real-time code evaluation, automatic scoring, and a leaderboard system. The backend is built with Python and Django, while the frontend uses Next.js. It also integrates a judge system like CodeRunner for automated code execution and grading.

# Softwares being used: Django PostgreSQL

## To-Do Items:
1. User and Admin accounts with JWT authentication using a {length of hackathon} lifetime.
2. Admin should have the functionality to edit/add/remove questions.
3. Admin show have the ability to add/edit/remove sample input and output similar to hackerrank.
4. Admin should be able to reset the database to a clean state for the next hackathon.
5. Ability for the user to test their code with 3 test input and output (Backend part is to just store these?)
6. Store all the data sent by any user to keep accurate data tracking (and data saving for redundancy)