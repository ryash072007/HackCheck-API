# HackCheck API
 HackCheck is a fully automated hackathon platform where participants solve a set number of coding challenges within a given time. It features real-time code evaluation, automatic scoring, and a leaderboard system. The backend is built with Python and Django, while the frontend uses Next.js. It also integrates a judge system like CodeRunner for automated code execution and grading.

 Frontend Link: https://github.com/Gopesh456/HackCheck-UI

# HackCheck Database Setup

![HackCheck Database Visualiser](<GitHub Files/Database Visualiser.png>)

# How to setup, install, and use

1. Install postgres-sql onto port 5432 and ensure that its service runs
2. Clone this repository (main branch for windows | self-host for linux)
3. On windows, run the setup_backend.bat file. On linux, just install the requirements file and makemigrations and migrate.
4. On windows, open the terminal (powershell) in the cwd of this repo and run start_backend.ps1 -> `.\start_backend.ps1`. You might have to enable script running in your execution policy. On linux, just use gunicorn.
5. To stop the server, press `ctrl + c` in the caddy pop-up window (the other terminal window that would have opened after running the backend), and wait for the server to stop.

# HackCheck API Documentation

This document provides a comprehensive guide to all available endpoints in the HackCheck-API project. For each endpoint, you'll find information about required authentication, input parameters, and expected responses.

## Table of Contents

1. Authentication
2. Team Management
3. Questions and Answers
4. Hackathon Administration
5. System Management
6. Utilities
7. Things you have to do in the django admin portal

---

## 1. Authentication

### 1.1. Team Sign In

**Endpoint:** `/team_signin/`  
**Method:** POST  
**Authentication:** None required  
**Description:** Authenticates a team member and provides a JWT token for access.

**Request Body:**
```json
{
  "team_name": "example_team",
  "password": "example_password",
  "participant_name": "John Doe"
}
```

**Response:**
```json
{
  "team_name": "example_team",
  "score": 0,
  "participant_name": "John Doe",
  "token": "jwt_token_string"
}
```

**Error Responses:**
- `400 Bad Request` - Invalid team name or password
- `400 Bad Request` - Participant name is required
- `400 Bad Request` - Hackathon has not started yet
- `400 Bad Request` - Team is full

### 1.2. Admin Sign In

**Endpoint:** `/admin_signin/`  
**Method:** POST  
**Authentication:** None required  
**Description:** Authenticates an admin user and provides a JWT token with admin privileges.

**Request Body:**
```json
{
  "username": "admin_username",
  "password": "admin_password"
}
```

**Response:**
```json
{
  "username": "admin_username",
  "token": "jwt_token_string"
}
```

**Error Responses:**
- `400 Bad Request` - Invalid username
- `400 Bad Request` - Wrong password

---

## 2. Team Management

### 2.1. Register Team

**Endpoint:** `/register/`  
**Method:** POST  
**Authentication:** Admin JWT token  
**Description:** Creates a new team.

**Request Body:**
```json
{
  "team_name": "new_team",
  "password": "team_password"
}
```

**Response:**
```json
{
  "message": "Team new_team registered successfully",
  "team_id": 1,
  "team_name": "new_team"
}
```

**Error Responses:**
- `400 Bad Request` - Team name and password are required
- `400 Bad Request` - Team name already taken
- `403 Forbidden` - Not an admin user
- `500 Internal Server Error` - Registration failed

### 2.2. Get Team Points

**Endpoint:** `/get_points/`  
**Method:** POST  
**Authentication:** Team or Admin JWT token  
**Description:** Gets points for a specific team or all teams.

**Request Body:**
```json
{
  "team_id": 1  // Optional - Omit or use "ALL" to get all teams
}
```

**Response (Single Team):**
```json
{
  "score": 100
}
```

**Response (All Teams):**
```json
{
  "teams": [
    {
      "id": 2,
      "team_name": "Team Alpha",
      "score": 150,
      "participants": ["Yash", "Gopesh"]
    },
    {
      "id": 1,
      "team_name": "Team Beta",
      "score": 100,
      "participants": ["Raj", "Jana"]
    }
  ]
}
```

**Error Responses:**
- `404 Not Found` - Team not found

### 2.3. Delete Team

**Endpoint:** `/delete_team/`  
**Method:** POST  
**Authentication:** Admin JWT token  
**Description:** Deletes a team by ID.

**Request Body:**
```json
{
  "team_id": 1
}
```

**Response:**
```json
{
  "message": "Team 1 successfully deleted."
}
```

**Error Responses:**
- `400 Bad Request` - Missing 'team_id' in request body
- `403 Forbidden` - Not an admin user
- `404 Not Found` - Team does not exist
- `500 Internal Server Error` - Error occurred while deleting team

### 2.4. Get Teams

**Endpoint:** `/get_teams/`  
**Method:** POST  
**Authentication:** Admin JWT token  
**Description:** Gets all team profiles including passwords.

**Request Body:** None required

**Response:**
```json
{
  "teams": [
    {
      "id": 1,
      "name": "Team Alpha",
      "password": "password1"
    },
    {
      "id": 2,
      "name": "Team Beta",
      "password": "password2"
    }
  ]
}
```

**Error Responses:**
- `403 Forbidden` - Not an admin user

### 2.5. Get Team Participants Names

**Endpoint:** `/get_team_participants_names/`  
**Method:** POST  
**Authentication:** Team JWT token  
**Description:** Retrieves the names of all participants in the authenticated user's team.

**Response:**
```json
{
  "participants": ["Participant Name 1", "Participant Name 2", "..."]
}
```

**Error Responses:**
- `200 OK` - Successfully retrieved participants names
- `401 Unauthorized` - Authentication credentials were not provided or are invalid

---

## 3. Questions and Answers

### 3.1. Get All Questions

**Endpoint:** `/get_questions/`  
**Method:** POST  
**Authentication:** Team or Admin JWT token  
**Description:** Gets all questions. Admin view shows basic info, team view shows status.

**Request Body:** None required

**Response (Admin):**
```json
{
  "questions": [
    {
      "question": "Sort an array",
      "question_number": 1,
      "question_id": 1,
      "difficulty": "easy"
    },
    {
      "question": "Find the maximum value",
      "question_number": 2,
      "question_id": 2,
      "difficulty": "medium"
    }
  ],
  "type": "admin"
}
```

**Response (Team):**
```json
{
  "questions": [
    {
      "question": "Sort an array",
      "question_number": 1,
      "question_id": 1,
      "status": "CORRECT",
      "score": 95,
      "difficulty": "easy"
    },
    {
      "question": "Find the maximum value",
      "question_number": 2,
      "question_id": 2,
      "status": "NOT_ANSWERED",
      "score": 0,
      "difficulty": "medium"
    }
  ],
  "type": "team"
}
```

### 3.2. Get Single Question

**Endpoint:** `/get_question/`  
**Method:** POST  
**Authentication:** Team or Admin JWT token  
**Description:** Gets a single question by ID or number.

**Request Body:**
```json
{
  "question_id": 1  // OR "question_number": 1 (don't use both)
}
```

**Response (Admin):**
```json
{
  "question_id": 1,
  "title": "Sort an array",
  "question_number": 1,
  "description": "Write a function to sort an array...",
  "samples": {
    "input": ["example input data"],
    "output": ["example output data"]
  },
  "tests": {
    "input": ["test input data"],
    "output": ["test output data"]
  },
  "difficulty": "easy",
  "type": "admin"
}
```

**Response (Team):**
```json
{
  "question_number": 1,
  "status": "CORRECT", // INCORRECT | NOT_ANSWERED
  "score": 0,
  "question_id": 1,
  "title": "Sort an array",
  "description": "Write a function to sort an array...",
  "samples": {
    "input": ["example input data"],
    "output": ["example output data"]
  },
  "tests": {
    "input": ["test input data"],
    "output": ["test output data"]
  },
  "difficulty": "easy",
  "type": "team"
}
```

**Error Responses:**
- `400 Bad Request` - Missing 'question_id' or 'question_number' in request body
- `400 Bad Request` - Provide only one of 'question_id' or 'question_number'
- `404 Not Found` - Question does not exist

### 3.3. Add Question

**Endpoint:** `/add_question/`  
**Method:** POST  
**Authentication:** Admin JWT token  
**Description:** Adds a new question.

**Request Body:**
```json
{
  "title": "New Question",
  "description": "Question description...",
  "samples": {
    "input": ["sample input 1", "sample input 2", "sample input 3"],
    "output": ["sample output 1", "sample output 2", "sample output 3"]
  },
  "tests": {
    "input": ["test input 1", "test input 2", "test input 3", "test input 4"],
    "output": ["test output 1", "test output 2", "test output 3", "test output 4"]
  },
  "difficulty": "medium"
}
```

**Response:**
```json
{
  "message": "Question successfully added.",
  "question": {
    "id": 3,
    "question_number": 3,
    "title": "New Question",
    "difficulty": "medium"
  }
}
```

**Error Responses:**
- `400 Bad Request` - Missing required fields
- `400 Bad Request` - Samples and tests must be dictionaries
- `400 Bad Request` - Samples must have 'input' and 'output' keys
- `400 Bad Request` - Tests must have 'input' and 'output' keys
- `400 Bad Request` - Difficulty must be 'easy', 'medium', or 'hard'
- `403 Forbidden` - Not an admin user
- `500 Internal Server Error` - Error occurred while adding the question

### 3.4. Remove Question

**Endpoint:** `/remove_question/`  
**Method:** POST  
**Authentication:** Admin JWT token  
**Description:** Removes a question by ID or number.

**Request Body:**
```json
{
  "question_id": 1  // OR "question_number": 1 (don't use both)
}
```

**Response:**
```json
{
  "message": "Question id 1 successfully removed."
}
```

**Error Responses:**
- `400 Bad Request` - Missing 'question_id' or 'question_number' in request body
- `400 Bad Request` - Provide only one of 'question_id' or 'question_number'
- `403 Forbidden` - Not an admin user
- `404 Not Found` - Question does not exist
- `500 Internal Server Error` - Error occurred while removing question

### 3.5. Update Question

**Endpoint:** `/update_question/`  
**Method:** POST  
**Authentication:** Admin JWT token  
**Description:** Updates an existing question.

**Request Body:**
```json
{
  "question_id": 1,  // OR "question_number": 1 (don't use both)
  "title": "Updated Title",  // Optional
  "description": "Updated description...",  // Optional
  "samples": {  // Optional
    "input": ["sample input 1", "sample input 2", "sample input 3"],
    "output": ["sample output 1", "sample output 2", "sample output 3"]
  },
  "tests": {  // Optional
    "input": ["test input 1", "test input 2", "test input 3", "test input 4"],
    "output": ["test output 1", "test output 2", "test output 3", "test output 4"]
  },
  "difficulty": "hard"  // Optional
}
```

**Response:**
```json
{
  "message": "Question successfully updated.",
  "question": {
    "id": 1,
    "question_number": 1,
    "title": "Updated Title",
    "difficulty": "hard"
  }
}
```

**Error Responses:**
- `400 Bad Request` - Missing 'question_id' or 'question_number' in request body
- `400 Bad Request` - Provide only one of 'question_id' or 'question_number'
- `400 Bad Request` - Samples must be a dictionary
- `400 Bad Request` - Tests must be a dictionary
- `400 Bad Request` - Difficulty must be 'easy', 'medium', or 'hard'
- `403 Forbidden` - Not an admin user
- `404 Not Found` - Question does not exist
- `500 Internal Server Error` - Error occurred while updating the question

### 3.6. Submit Answer

**Endpoint:** `/submit/`  
**Method:** POST  
**Authentication:** Team JWT token  
**Description:** Submits an answer for a question.

**Request Body:**
```json
{
  "question_number": 1,
  "code": "code string here",
  "is_correct_answer": false,
  "tests": {
    "input": ["test input data"],
    "output": ["test output data"]
  }
}
```

**Response:**
```json
{
  "message": "Answer submitted successfully."
}
```

**Error Responses:**
- `400 Bad Request` - Code is required to submit answer
- `400 Bad Request` - Question number is required to submit answer
- `400 Bad Request` - Tests are required to submit answer
- `400 Bad Request` - Hackathon has not started yet
- `400 Bad Request` - Hackathon has ended
- `400 Bad Request` - This question has already been answered correctly
- `404 Not Found` - Question does not exist

### 3.7. Save Shared Code

**Endpoint:** `/save_shared_code/`  
**Method:** POST  
**Authentication:** Team JWT token  
**Description:** Saves shared code for a team's question to enable collaboration between team members.

**Request Body:**
```json
{
  "question_number": 1,
  "shared_code": "function solution(input) {\n  // Code implementation here\n  return result;\n}"
}
```

**Response:**
```json
{
  "message": "Shared code saved successfully.",
  "static_file": "http://192.168.1.100:8000/saved_codes/UUID.py"
}
```

**Error Responses:**
- `400 Bad Request` - Missing 'shared_code' in request body
- `400 Bad Request` - Missing 'question_number' in request body
- `403 Forbidden` - Not authorized
- `404 Not Found` - Question does not exist

### 3.8. Get Shared Code

**Endpoint:** `/saved_codes/<str:uuid>/`  
**Method:** GET  
**Authentication:** None required  
**Description:** Retrieves a previously saved Python code file for sharing between team members.

**URL Parameters:**
- The UUID and filename are generated automatically when shared code is saved

**Response:**
- The Python file content with appropriate mime-type
- Or a 404 page if the file doesn't exist

**Notes:**
- A steaming response is created mimicking as if the file is saved in the filesystem while its actually stored in the database.

### 3.9. Clear All Shared Code

**Endpoint:** `/clear_all_shared_code/`  
**Method:** POST  
**Authentication:** Team JWT token  
**Description:** Clears all shared code entries for the authenticated user's team.

**Request Body:** None required

**Response:**
```json
{
  "message": "Shared code cleared successfully."
}
```

**Error Responses:**
- `401 Unauthorized` - Not authenticated or invalid token

### 3.10 Log Activity

**Endpoint:** `/log_activity/`  
**Method:** POST  
**Authentication:** Team JWT token  
**Description:** Logs malicious activity of a participant.

**Request Body:**
```json
{
  "question_number": 1,
  "activity_type": "Tab Switch",
  "details": "Participant switched to another tab despite lockdown."
}
```

**Response:**
```json
{
  "message": "Activity logged successfully."
}
```

**Error Responses:**
- `400 Bad Request` - Question number is required to log activity
- `400 Bad Request` - Activity type is required to log activity
- `400 Bad Request` - Details are required to log activity
- `401 Unauthorized` - Not authenticated or invalid token

---

## 4. Hackathon Administration

### 4.1. Start Hackathon

**Endpoint:** `/start_hackathon/`  
**Method:** POST  
**Authentication:** Admin JWT token  
**Description:** Starts the hackathon.

**Request Body:** None required

**Response:**
```json
{
  "message": "Hackathon started successfully."
}
```

**Error Responses:**
- `400 Bad Request` - Hackathon has already started
- `403 Forbidden` - Not an admin user

### 4.2. End Hackathon

**Endpoint:** `/end_hackathon/`  
**Method:** POST  
**Authentication:** Admin JWT token  
**Description:** Ends the hackathon.

**Request Body:** None required

**Response:**
```json
{
  "message": "Hackathon ended successfully."
}
```

**Error Responses:**
- `400 Bad Request` - Hackathon has already ended
- `403 Forbidden` - Not an admin user

### 4.3. Pause Hackathon

**Endpoint:** `/pause_hackathon/`  
**Method:** POST  
**Authentication:** Admin JWT token  
**Description:** Pauses the hackathon timer.

**Request Body:** None required

**Response:**
```json
{
  "message": "Hackathon paused successfully."
}
```

**Error Responses:**
- `400 Bad Request` - Hackathon is already paused
- `403 Forbidden` - Not an admin user

### 4.4. Resume Hackathon

**Endpoint:** `/resume_hackathon/`  
**Method:** POST  
**Authentication:** Admin JWT token  
**Description:** Resumes a paused hackathon.

**Request Body:** None required

**Response:**
```json
{
  "message": "Hackathon resumed successfully."
}
```

**Error Responses:**
- `400 Bad Request` - Hackathon is not paused
- `403 Forbidden` - Not an admin user

### 4.5. Get Time Left

**Endpoint:** `/get_time_left/`  
**Method:** POST  
**Authentication:** Team or Admin JWT token  
**Description:** Gets the time remaining in the hackathon.

**Request Body:** None required

**Response:**
```json
{
  "time_left": 3600.0  // Time left in seconds
}
```

**Error Responses:**
- `400 Bad Request` - Hackathon has not started yet
- `400 Bad Request` - Hackathon has ended

### 4.6. Change Time Left

**Endpoint:** `/change_time_left/`  
**Method:** POST  
**Authentication:** Admin JWT token  
**Description:** Changes the time remaining in the hackathon.

**Request Body:**
```json
{
  "time_left_seconds": 3600  // New time in seconds
}
```

**Response:**
```json
{
  "message": "Time left updated successfully."
}
```

**Error Responses:**
- `400 Bad Request` - Missing 'time_left_seconds' in request body
- `403 Forbidden` - Not an admin user

### 4.7. Change Max Participants

**Endpoint:** `/change_max_participants/`  
**Method:** POST  
**Authentication:** Admin JWT token  
**Description:** Changes the maximum allowed team size.

**Request Body:**
```json
{
  "max_participants": 5
}
```

**Response:**
```json
{
  "message": "Max participants changed successfully to 5"
}
```

**Error Responses:**
- `400 Bad Request` - max_participants is required
- `403 Forbidden` - Not an admin user

### 4.8. Check Hackathon Status

**Endpoint:** `/check_hackathon_status/`  
**Method:** POST  
**Authentication:** Team or Admin JWT token  
**Description:** Checks the current status of the hackathon.

**Request Body:** None required

**Response:**
```json
{
  "has_started": true,
  "has_ended": false,
  "is_paused": false
}
```

**Error Responses:**
- `403 Forbidden` - Invalid or missing authentication token

---

## 5. System Management

### 5.1. Reset Hackathon Database

**Endpoint:** `/reset_database/`  
**Method:** POST  
**Authentication:** Admin JWT token  
**Description:** Resets all hackathon data (teams, questions, answers).

**Request Body:** None required

**Response:**
```json
{
  "message": "Database successfully reset for new hackathon",
  "deleted": {
    "accounts": 10,
    "teams": 10,
    "members": 25,
    "questions": 5,
    "answers": 50
  }
}
```

**Error Responses:**
- `403 Forbidden` - Not an admin user
- `500 Internal Server Error` - Error occurred while resetting the database

### 5.2. Reset Current Hackathon

**Endpoint:** `/reset_hackathon/`  
**Method:** POST  
**Authentication:** Admin JWT token  
**Description:** Resets the current hackathon state (timer, answers, scores) without deleting teams or questions.

**Request Body:** None required

**Response:**
```json
{
  "message": "Current hackathon successfully reset."
}
```

**Error Responses:**
- `403 Forbidden` - Not an admin user

### 5.3. Admin Dashboard

**Endpoint:** `/dashboard/`  
**Method:** POST  
**Authentication:** Admin JWT token  
**Description:** Gets overview information about the hackathon.

**Request Body:** None required

**Response:**
```json
{
  "hackathon_status": true,
  "num_teams": 10,
  "num_questions": 5,
  "total_answers": 50,
  "time_left_seconds": 3600.0
}
```

**Error Responses:**
- `403 Forbidden` - Not an admin user

### 5.4. Get Score Settings

**Endpoint:** `/get_score_settings/`  
**Method:** POST  
**Authentication:** Admin JWT token  
**Description:** Gets the current scoring settings for the hackathon.

**Request Body:** None required

**Response:**
```json
{
  "max_score": 100,
  "score_decrement_interval_seconds": 60,
  "score_decrement_per_interval": 1
}
```

**Error Responses:**
- `403 Forbidden` - Not an admin user

### 5.5. Update Score Settings

**Endpoint:** `/update_score_settings/`  
**Method:** POST  
**Authentication:** Admin JWT token  
**Description:** Updates the scoring settings for the hackathon.

**Request Body:**
```json
{
  "max_score": 100,  // Optional
  "score_decrement_interval_seconds": 60,  // Optional
  "score_decrement_per_interval": 1  // Optional
}
```

**Response:**
```json
{
  "message": "Score settings successfully updated."
}
```

**Error Responses:**
- `400 Bad Request` - Provide at least one setting to update
- `403 Forbidden` - Not an admin user

### 5.6. Export Leaderboard

**Endpoint:** `/export_leaderboard/`  
**Method:** GET  
**Authentication:** None 
**Description:** Exports the leaderboard data as CSV.

**Request Body:** None required

**Response:** CSV file data

**Error Responses:**
- `403 Forbidden` - Not an admin user

---

## 6. Utilities

### 6.1. Test Authentication

**Endpoint:** `/test_auth/`  
**Method:** POST  
**Authentication:** Any valid JWT token  
**Description:** Tests if authentication is working correctly.

**Request Body:** None required

**Response:** Depends on implementation

**Error Responses:**
- Authentication related errors

---

## Notes

- All endpoints require a valid JWT token in the Authorization header except for sign-in endpoints
- Team JWT tokens are obtained through the `/team_signin/` endpoint
- Admin JWT tokens are obtained through the `/admin_signin/` endpoint
- JWT tokens should be included in the request headers as: `Authorization: Bearer <token>`
- All dates are in ISO format
- All times are in seconds
- The API follows RESTful principles but uses POST for all endpoints for consistency

## 7. Things you have to do in the django admin portal

### 7.1 Creating a Superuser

Before you can access the Django admin portal, you need to create a superuser account. Run the following command in your terminal:

```bash
python manage.py createsuperuser
```

Then, follow the step below and sign into the admin portal. Then go to accounts -> open your own account -> set yourself as admin by checking is_admin to true and saving.

### 7.2 Open the django admin portal: http://localhost:8000/admin

When running the project during the actual hackathon (or when the frontend and backend are ran on different devices), you will have to replace the localhost part with the ipv4 address of that device on that network

### 7.3 Things you have to use the django portal for

After you start a hackathon, you can not delete any question. I suggest you familiarise yourself with the django admin portal for finetunned control (and specifically, the hackathon settings or removing participants).

If you start and end the hackathon as well, the questions can not be deleted. Either reset the current hackathon (DO NOT ON THE ACTUAL HACKATHON DAY) or uncheck the has_ended field in the hackathon settings in the django admin portal.