import requests

# Function to run the code with the given input data and capture the output
def run_code_with_input(source_code, language_id, input_data):
    # Upload the source code using Judge0 API
    endpoint = "https://api.judge0.com/submissions"
    data = {
        "source_code": source_code,
        "language_id": language_id,
        "stdin": input_data
    }
    response = requests.post(endpoint, json=data)

    # Get the submission token
    submission_token = response.json().get("token")

    # Check the status of the submission and wait until it is completed
    status_endpoint = f"{endpoint}/{submission_token}"
    while True:
        response = requests.get(status_endpoint)
        status_data = response.json()
        status = status_data.get("status", {}).get("id")

        if status == 3:  # Completed status
            break
        elif status == 6:  # Compilation error
            raise RuntimeError("Compilation error")
        elif status == 7:  # Runtime error
            raise RuntimeError("Runtime error")

    # Get the output of the code
    output = status_data.get("stdout", "")
    return output
