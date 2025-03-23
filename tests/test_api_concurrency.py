import requests
import concurrent.futures


def call_api(id, endpoint="login/", jwt_token=None, data=None):
    if data is None:
        data = {
            "team_name": "Bhavans 03",
            "participant_name": "Yash",
            "password": "Test1234",
        }

    headers = {}
    if jwt_token:
        headers["Authorization"] = f"Bearer {jwt_token}"

    try:
        response = requests.post(
            f"http://localhost:8000/{endpoint}", json=data, headers=headers
        )
        return id, response.status_code, response.elapsed.total_seconds()
    except requests.exceptions.ConnectionError:
        print(f"Request {id} failed: Connection error", flush=True)
        return id, 0, 0  # 0 status code indicates connection error


# Number of concurrent requests
num_requests = 50

jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQyNzQ3NzI4LCJpYXQiOjE3NDI3MzY5MjgsImp0aSI6ImQ3Y2FmMmE1NzIwOTQ0MDBiZGEyOTBlYjZlZjkzMzU4IiwidXNlcl9pZCI6NiwidGVhbV9pZCI6MywidGVhbV9uYW1lIjoiQmhhdmFucyAwMyIsInBhcnRpY2lwYW50X2lkIjo3LCJwYXJ0aWNpcGFudF9uYW1lIjoiWWFzaCJ9.2UMFLKldMl-t4jGqR5D69HbsDxVfIRMdGBVS7D2rEhE"  # Replace with your actual JWT token when needed

# Execute requests concurrently
with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    futures = [
        executor.submit(call_api, i, jwt_token=jwt_token, endpoint="login/",) for i in range(num_requests)
    ]
    results = [future.result() for future in concurrent.futures.as_completed(futures)]

# Analyze results
status_counts = {}
total_time = 0
connection_errors = 0

for req_id, status, time in results:
    if status == 0:
        connection_errors += 1
    else:
        status_counts[status] = status_counts.get(status, 0) + 1
        total_time += time

print(f"Completed {num_requests} requests")
print(f"Connection errors: {connection_errors}")
print(f"Status code counts: {status_counts}")
if num_requests > connection_errors:
    print(
        f"Average response time: {total_time/(num_requests-connection_errors):.4f} seconds"
    )
else:
    print("No successful requests to calculate average response time")
