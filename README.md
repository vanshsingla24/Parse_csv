# CSV to Nested JSON Converter

This is a Flask web application that allows you to upload a CSV file, preview its contents, and convert it to a nested JSON structure. You can also preview and download the resulting JSON.

## Features
- Upload any CSV file via the web interface
- Preview the first 5 rows of your CSV
- View the converted JSON in a collapsible/expandable viewer
- Download the resulting JSON file

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/vanshsingla24/Parse_csv.git
   cd Parse_csv
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the App

1. **Start the Flask server:**
   ```bash
   python3 csv_to_json.py
   ```

2. **Open your browser and go to:**
   ```
   http://127.0.0.1:5000/
   ```

3. **Upload your CSV file, preview the data, and download the JSON!**

## Notes
- Do not commit your `venv` or large data files to the repository.
- For production use, consider deploying with a production WSGI server (e.g., Gunicorn).

## License
MIT 