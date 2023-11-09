import os
from typing import List, Dict

import pandas as pd
from pymongo import MongoClient
from flask import (
    Flask,
    request,
    render_template,
    redirect,
    url_for,
    flash,
    jsonify
)


app = Flask(__name__)
app.secret_key = "lerolero"


def parse_csv(file_path: str) -> List[Dict]:
    """
    Parses a CSV file and returns its data as a list of dictionaries.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        list: A list of dictionaries representing the data from the CSV file.
    """
    data = []
    with open(file_path, "r") as file:
        df = pd.read_csv(file)
        data = df.to_dict(orient="records")
    return data


def connect_mongodb() -> MongoClient:
    """
    Connects to a MongoDB server and returns the database instance.

    Returns:
        MongoClient: The MongoDB client instance.
    """
    client = MongoClient("mongodb://172.21.0.18:27017/")
    db = client["netflix"]
    return db


def store_in_mongodb(data: List[Dict]) -> None:
    """
    Stores data in a MongoDB collection.

    Args:
        data (list): A list of dictionaries to be stored in MongoDB.
    """
    db = connect_mongodb()
    collection = db["movies"]
    collection.insert_many(data)


def upload_chunk(uploaded_file) -> str:
    """
    Uploads a file in chunks and returns the file path.

    Args:
        uploaded_file (FileStorage): The uploaded file object.

    Returns:
        str: The path to the uploaded file on the server.
    """
    file_name = uploaded_file.filename
    file_path = os.path.join("uploads", file_name)
    chunk_size = 4096

    with open(file_path, "wb") as file:
        while True:
            chunk = uploaded_file.stream.read(chunk_size)
            if not chunk:
                break
            file.write(chunk)

    return file_path


@app.route("/upload", methods=["POST"])
def upload_file():
    uploaded_file = request.files["file"]

    if uploaded_file.filename != "":
        file_path = upload_chunk(uploaded_file)
        # uploaded_file.save('uploads/' + uploaded_file.filename)

        data = parse_csv(file_path)
        store_in_mongodb(data)

        return "File uploaded and data stored successfully in MongoDB"
    else:
        flash("Please select a file", "error")
        return redirect(url_for("index"))


@app.route("/query", methods=["POST"])
def query_mongodb():
    """
    Query MongoDB for movie records based on specified criteria.

    Request Format:
        {
            "field": "field_name",   # Field to query (e.g., "title")
            "value": "search_value", # Value to search for
            "page": 1,               # Page number (default is 1)
            "quantity": 10           # Number of results per page (default 10)
        }

    Returns:
        JSON response containing movie records that match the criteria.
        If no field and value are provided, returns all movies.

    Raises:
        400 Bad Request: Invalid JSON data in the request body.
    """
    try:
        data = request.get_json()
        field = data.get("field")
        value = data.get("value")
        page = int(data.get("page", 1))
        quantity = int(data.get("quantity", 10))
    except (KeyError, ValueError):
        return jsonify({"error": "Invalid JSON data in the request body"})

    db = connect_mongodb()
    collection = db["movies"]

    query = {}
    if field and value:
        query[field] = {"$regex": f".*{value}.*", "$options": "i"}

    skip = (page - 1) * quantity
    result = list(
        collection.find(query, {"_id": 0}).skip(skip).limit(quantity)
    )

    return jsonify(result)


@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    if request.method == "POST":
        flash("Please select a file", "error")  # Flash an error message
    return render_template("index.html", error=error)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
