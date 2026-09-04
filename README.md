# PashuDrishti.ai

An AI-assisted web application for identifying Indian cattle and buffalo breeds from an uploaded image. PashuDrishti.ai runs a PyTorch EfficientNet-B0 model behind a FastAPI interface and presents the most likely breed alongside its confidence score and top predictions.

## Overview

PashuDrishti.ai is designed to make breed recognition straightforward for livestock-related workflows. After creating an account and signing in, users can upload an image, optionally record an animal ID and GPS coordinates, and review the prediction result in the browser.

### Key capabilities

- **Image-based breed recognition** using a trained EfficientNet-B0 classifier.
- **Top-five predictions** with confidence scores.
- **Optional animal ID and GPS metadata** included with each prediction result.
- **Simple browser interface** with account creation and sign-in.
- **Health and model-bundle diagnostics** for deployment checks.
- **Model bundle support** for TorchScript or dynamically quantized INT8 model artifacts.

> **Note:** Predictions are model estimates and should be reviewed by a qualified livestock professional when they inform important decisions.

## Technology Stack

**Application and machine learning**

- **FastAPI** provides the web application and HTTP endpoints.
- **PyTorch** and **Torchvision** run the EfficientNet-B0 classifier and image preprocessing.
- **Pillow** loads uploaded images.
- **Uvicorn** serves the ASGI application.

**Supporting tools**

- **Gradio** provides an optional local demo (`app.py`).
- **Pandas**, **scikit-learn**, and related utilities support training workflows.
- **SQLite helpers** and a schema are included for future persistence work.

## Getting Started

### Prerequisites

- Python 3.10 or later.
- A compatible model bundle. The repository includes `cattle_model_low_hw.tar.gz` by default.
- `pip` for installing Python dependencies.

### Installation

1. Clone the repository and enter it:

   ```bash
   git clone https://github.com/varshith0810/PashuDrishti.ai.git
   cd PashuDrishti.ai
   ```

2. Create and activate a virtual environment (recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set a strong session secret before starting the application:

   ```bash
   export SESSION_SECRET="replace-with-a-long-random-value"
   ```

5. Start the FastAPI application from the repository root:

   ```bash
   PYTHONPATH=backend/ml uvicorn backend.app:app --host 0.0.0.0 --port 8000
   ```

6. Open [http://localhost:8000](http://localhost:8000), create an account, sign in, and upload an animal image.

### Optional: use a different model bundle

Set `MODEL_BUNDLE` to the path of a compatible `.tar.gz` bundle before starting the server:

```bash
export MODEL_BUNDLE=/path/to/model-bundle.tar.gz
PYTHONPATH=backend/ml uvicorn backend.app:app --host 0.0.0.0 --port 8000
```

The bundle must contain `class_names.json` and either `breed_classifier_int8.pt` or `breed_classifier_ts.pt`.

## Using the Application

1. Visit `/create-account` to create an account.
2. Sign in at `/signin`.
3. On the home page, select an animal image.
4. Optionally enter an animal ID and GPS coordinates in `latitude,longitude` format.
5. Submit the form to view the predicted breed, confidence score, top-five results, and uploaded image.

GPS coordinates are reverse-geocoded when the lookup service is available. If it is unavailable, the submitted coordinates remain visible in the result.

## API Endpoints

| Endpoint | Method | Description |
| --- | --- | --- |
| `/` | GET | Authenticated image-upload page. |
| `/health` | GET | Service status and loaded-model information. |
| `/create-account` | GET, POST | Account registration page and submission. |
| `/signin` | GET, POST | Sign-in page and submission. |
| `/logout` | GET | Clears the current session. |
| `/predict` | POST | Processes an uploaded image and renders the prediction result. |
| `/debug/bundle` | GET | Lists model-bundle files when diagnostics are enabled. |

To enable the diagnostic endpoint, set `DEBUG_BUNDLE=true` before starting the server. Do not enable it in public production environments unless revealing bundle metadata is acceptable.

## Configuration

| Variable | Default | Description |
| --- | --- | --- |
| `MODEL_BUNDLE` | `cattle_model_low_hw.tar.gz` | Path to the model-bundle archive. |
| `SESSION_SECRET` | `change-me` | Secret used to sign browser sessions. Set a strong, unique value for every deployment. |
| `DEBUG_BUNDLE` | `false` | Enables the `/debug/bundle` diagnostic endpoint when set to `true`. |

## Project Structure

```text
PashuDrishti.ai/
├── backend/
│   ├── app.py                  # Deployment-compatible FastAPI entry point
│   ├── db.py                   # SQLite connection and initialization helpers
│   ├── schema.sql              # Database schema
│   └── ml/
│       ├── src/                # Inference, training, preprocessing, and FastAPI code
│       └── export_low_hardware.py
├── scripts/                    # Training-pipeline and model-export scripts
├── app.py                      # Optional Gradio demo
├── cattle_model_low_hw.tar.gz  # Default model bundle
├── requirements.txt            # Python dependencies
└── Docker                      # Render deployment configuration
```

## Development Notes

- The primary FastAPI implementation is `backend/ml/src/app.py`; `backend/app.py` exposes it as `backend.app:app` for deployment compatibility.
- The application keeps account data in memory. Accounts are reset when the process restarts.
- The included `backend/db.py` and `backend/schema.sql` provide a starting point for adding persistent storage.
- Training and preprocessing utilities are located in `backend/ml/src/` and `scripts/`.

## Troubleshooting

### The server cannot find `src.app`

Start the server with `PYTHONPATH=backend/ml`, as shown in the installation instructions. This makes the machine-learning source directory importable.

### The model bundle cannot be loaded

Confirm that the `MODEL_BUNDLE` path exists and that the archive contains `class_names.json` plus a supported model file. You can inspect the archive with:

```bash
tar -tzf cattle_model_low_hw.tar.gz
```

### The prediction page reports an invalid image

Upload a readable image file. The server converts valid uploads to RGB before inference.

## License

This project is distributed under the [MIT License](LICENSE).
