import requests
import json

# Define the path to the csv file
CSV_FILE = "netflix.csv"

BASE_URL = "http://127.0.0.1:5001"
UPLOAD_ENDPOINT = BASE_URL + "/upload"
QUERY_ENDPOINT = BASE_URL + "/query"

file_data = {"file": (CSV_FILE, open(CSV_FILE, "rb"))}

upload_response = requests.post(UPLOAD_ENDPOINT, files=file_data)

if upload_response.status_code == 200:
    print("File uploaded successfully")
else:
    print("File upload failed")

query_data = {
    "field": "title",  # Replace with desired field
    "value": "sample",  # Replace with desired value
    "page": 1,
    "quantity": 10,
}

query_response = requests.post(QUERY_ENDPOINT, json=query_data)

if query_response.status_code == 200:
    result = json.loads(query_response.text)
    print("Query results:")
    for record in result:
        print(record)
else:
    print("Query failed")
