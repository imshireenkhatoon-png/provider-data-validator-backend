🩺 Provider Data Validator — Backend (Flask)

A lightweight backend API built with Flask for validating healthcare provider data such as name, phone, address, and specialty.
It’s designed for the Provider Data Validator project — a hackathon-ready MVP connected to a Lovable frontend dashboard.

🚀 Features

✅ Upload and validate healthcare provider data via CSV
✅ Simulate AI-based validation with random confidence scores
✅ Generate a downloadable PDF summary report
✅ View validation statistics and health status
✅ CORS-enabled for seamless frontend connection

🧠 Tech Stack

Python 3.10+

Flask (Backend Framework)

Pandas (CSV handling)

ReportLab / FPDF (PDF generation)

Random, Time (for mock AI simulation)

Flask-CORS (Frontend integration)

⚙️ Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/imshireenkhatoon-png/provider-data-validator-backend.git
cd provider-data-validator-backend

2️⃣ Create a virtual environment
python -m venv venv


Activate it:

Windows PowerShell

venv\Scripts\activate


macOS / Linux

source venv/bin/activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Set Flask app variable
$env:FLASK_APP = "app/app.py"

5️⃣ Run the server
python -m flask run


✅ Flask will start at:
http://127.0.0.1:5000

🧩 API Endpoints
🔹 /upload (POST)

Uploads and validates a CSV file.

Request (form-data)
Key: file → Upload your CSV
CSV format:

Name,Phone,Address,Specialty
Dr. John Smith,555-1234,123 Main St,Cardiology
Dr. Emily Jones,555-5678,456 Oak Ave,Neurology


Response (JSON):

{
  "providers": [
    {
      "name": "Dr. John Smith",
      "phone": "555-1234",
      "address": "123 Main St",
      "confidence": 89,
      "status": "✅ Valid",
      "timestamp": "2025-10-28 19:30:00"
    }
  ]
}

🔹 /report (POST)

Generates a PDF report summarizing validation results.

Request (JSON):

{
  "providers": [
    {"name": "Dr. John Smith", "confidence": 89, "status": "✅ Valid"}
  ]
}


Response:
📄 Returns a downloadable PDF file with:

Total Providers

Count of Valid / Review / Invalid

Average Confidence

Timestamp of Generation

🔹 /summary (GET)

Returns aggregate statistics.

Response:

{
  "total_validated": 10,
  "average_confidence": 82.5,
  "valid_count": 7,
  "review_count": 2,
  "invalid_count": 1
}

🔹 /health (GET)

Quick health check for your API.

Response:

{"status": "API running ✅", "timestamp": "2025-10-28T19:40:00"}

🧾 Environment Variables

Create a .env file (see .env.example):

FLASK_ENV=development
SECRET_KEY=dummysecret123

🧑‍💻 Frontend Connection

If your Lovable dashboard is hosted separately:

Set API base URL in your frontend (JavaScript):

const API_BASE_URL = "http://127.0.0.1:5000";


Then fetch data like:

fetch(`${API_BASE_URL}/upload`, {
  method: "POST",
  body: formData,
});

🏁 Deployment (Optional)

You can easily deploy this backend for free on:

Render.com

Railway.app

Deta Space

🧡 Author

Shireen Khatoon
🚀 GitHub
 | 💻 Backend Developer | 🌸 Hackathon Innovator
