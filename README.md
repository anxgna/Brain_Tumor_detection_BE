# Brain Tumor Detection Backend

This is a FastAPI-based backend service designed to classify MRI brain scan images into two categories: "Tumor" or "No Tumor". It integrates a Convolutional Neural Network (CNN) model.

## Prerequisites

- Python 3.10 or higher
- `venv` (Python Virtual Environments)

## Setup Instructions

1. **Clone or Navigate to the Project Directory**
   Open your terminal and make sure you are in the project folder:
   ```bash
   cd Brain_Tumor_detection_BE
   ```

2. **Create a Virtual Environment**
   It's highly recommended to use a virtual environment to manage dependencies:
   ```bash
   python3 -m venv venv
   ```
   *Note: If `python3` doesn't work, try `python -m venv venv`.*

3. **Activate the Virtual Environment**
   - On Linux/macOS:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

4. **Install Dependencies**
   Install all the required Python packages into your active virtual environment:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Server

Once all the dependencies are successfully installed, you can start the FastAPI backend server using Uvicorn:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Testing the API

After starting the server, you can verify it's working properly.

1. **Health Check endpoint**:
   Open your browser or use curl in another terminal window:
   ```bash
   curl http://localhost:8000/health
   ```
   You should see: `{"status":"ok","message":"Brain Tumor Detection API is running"}`

2. **API Documentation**:
   FastAPI automatically provides interactive API documentation. You can view all routes, their request formats, and experiment directly in the browser by visiting:
   [http://localhost:8000/docs](http://localhost:8000/docs)

   From here, you can click on the `POST /upload` API block, browse for an MRI image to upload, and copy the returned `scan_id`. Then use the `POST /predict` block using that `scan_id` to get a prediction result.
