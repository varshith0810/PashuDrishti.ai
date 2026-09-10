# PashuDrishti.ai (पशु दृष्टि)
### AI-Powered Indian Cattle & Buffalo Breed Recognition Platform

[![Deploy to Amazon ECS](https://github.com/varshith0810/PashuDrishti.ai/actions/workflows/deploy-aws.yml/badge.svg)](https://github.com/varshith0810/PashuDrishti.ai/actions/workflows/deploy-aws.yml)
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.2%2B_CPU-EE4C2C.svg?logo=pytorch)](https://pytorch.org/)
[![AWS ECS Fargate](https://img.shields.io/badge/AWS-ECS_Fargate-FF9900.svg?logo=amazonaws)](https://aws.amazon.com/ecs/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**PashuDrishti.ai** is an enterprise-ready, deep-learning livestock diagnostic platform specifically engineered to classify **41 indigenous and commercial Indian cattle and buffalo breeds** from uploaded photos. Powered by a CPU-optimized, dynamically quantized (INT8) **EfficientNet-B0** convolutional neural network, PashuDrishti.ai delivers sub-100ms inference without requiring expensive GPU infrastructure.

---

## 🌐 Live Cloud Deployment

PashuDrishti.ai is deployed 24/7 on **AWS ECS Fargate** behind an **AWS Application Load Balancer (ALB)** in the Mumbai (`ap-south-1`) region:

- **Official Web Application**: **[http://pashudrishti-alb-1806113337.ap-south-1.elb.amazonaws.com](http://pashudrishti-alb-1806113337.ap-south-1.elb.amazonaws.com)**
- **Sign In Portal**: **[http://pashudrishti-alb-1806113337.ap-south-1.elb.amazonaws.com/signin](http://pashudrishti-alb-1806113337.ap-south-1.elb.amazonaws.com/signin)**
- **System Health Check**: **[http://pashudrishti-alb-1806113337.ap-south-1.elb.amazonaws.com/health](http://pashudrishti-alb-1806113337.ap-south-1.elb.amazonaws.com/health)** `(HTTP 200 OK)`
- **Interactive Swagger Docs**: **[http://pashudrishti-alb-1806113337.ap-south-1.elb.amazonaws.com/docs](http://pashudrishti-alb-1806113337.ap-south-1.elb.amazonaws.com/docs)**

### Pre-Seeded Demonstration Accounts
You can immediately sign in and test the platform using any of these accounts:

| Username | Password | Role | Description |
| :--- | :--- | :--- | :--- |
| **`testuser`** | `password123` | User | General farmer / user testing account |
| **`farmer`** | `farmer123` | User | Field worker / cattle owner account |
| **`admin`** | `admin123` | Admin | Administrative account |
| **`demo`** | `demo123` | User | Rapid presentation account |

---

## ✨ Key Capabilities

- **41-Breed Recognition**: High-precision multi-class classification covering Gir, Murrah, Sahiwal, Red Sindhi, Jaffrabadi, Kankrej, Tharparkar, and 34 other breeds.
- **Sub-100ms Low-Hardware Inference**: Pre-warmed INT8 dynamic quantization runs in ~80ms on commodity CPUs, allowing a single 1 vCPU container to handle over **1.5 million requests/month**.
- **Dual Interface (Web UI + REST API)**: Server-rendered modern web UI for browser users and JSON REST endpoints (`/api/predict`, `/api/predictions`) for mobile apps and IoT collars.
- **Geolocation & Reverse-Geocoding**: Accepts optional GPS coordinates (`lat,long`), maps the animal to a geographic district/state using cached OpenStreetMap Nominatim queries.
- **Persistent Storage**: Integrated SQLite relational store with foreign key enforcement for user profiles, password hashing (SHA-256), and historical prediction logs.
- **Cloud-Native & Production-Hardened**: Containerized via Docker (multi-stage CPU PyTorch, <700MB image), monitored with CloudWatch logs, and orchestrated through zero-downtime rolling deploys via GitHub Actions.

---

## 🐄 Supported Indian Breeds (41 Classes)

PashuDrishti.ai identifies 41 distinct breeds of Indian cattle (*Bos indicus*) and river buffaloes (*Bubalus bubalis*):

```
Alambadi        Amritmahal      Ayrshire        Banni           Bargur
Bhadawari       Brown Swiss     Dangi           Deoni           Gir
Guernsey        Hallikar        Hariana         Holstein Fr.    Jaffrabadi
Jersey          Kangayam        Kankrej         Kasargod        Kenkatha
Kherigarh       Khillari        Krishna Valley  Malnad Gidda    Mehsana
Murrah          Nagori          Nagpuri         Nili Ravi       Nimari
Ongole          Pulikulam       Rathi           Red Dane        Red Sindhi
Sahiwal         Surti           Tharparkar      Toda            Umblachery
Vechur
```

---

## 🏛️ System Architecture

```
                                  [ Farmers & External Clients ]
                                                │
                                                ▼ (HTTP Port 80 / HTTPS Port 443)
                            ┌─────────────────────────────────────────┐
                            │    AWS Application Load Balancer (ALB)  │
                            │           (pashudrishti-alb)            │
                            └───────────────────┬─────────────────────┘
                                                │
                                                ▼ (Port 8000 Forwarding)
                            ┌─────────────────────────────────────────┐
                            │        Target Group (pashudrishti-tg)   │
                            └───────────────────┬─────────────────────┘
                                                │
                                                ▼
                            ┌─────────────────────────────────────────┐
                            │         Amazon ECS Fargate Task         │
                            │   ├── 1 vCPU, 2 GB RAM                  │
                            │   ├── Gunicorn / Uvicorn Workers        │
                            │   ├── Pre-warmed INT8 EfficientNet-B0   │
                            │   ├── In-Memory Geocoding Cache         │
                            │   └── SQLite Persistent Store (/data)   │
                            └───────────────────┬─────────────────────┘
                                                │
                                                ▼ (Optional Archive)
                                    [ Amazon S3 Bucket (Images) ]
```

---

## 🚀 Quickstart Guide

### Prerequisites
- **Python 3.10+** (Python 3.11 recommended)
- **Git**
- **Virtual Environment tool** (`venv`)

### 1. Clone & Set Up Local Environment
```bash
# Clone the repository
git clone https://github.com/varshith0810/PashuDrishti.ai.git
cd PashuDrishti.ai

# Create and activate virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

# Install CPU-optimized PyTorch and requirements
pip install --upgrade pip
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
```

### 2. Run the Application
```bash
# Launch the FastAPI production server
uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload
```
Open **[http://localhost:8000](http://localhost:8000)** in your browser. Default users are auto-seeded on first boot (`testuser:password123`, `farmer:farmer123`, `admin:admin123`).

### 3. Run Automated Integration & Prediction Tests
The test suite executes 10 test phases verifying all endpoints and performing live breed predictions across 9 diverse test images:
```bash
# In a separate terminal while the server is running:
python backend/test_api.py
```

---

## 🐳 Docker Deployment

Run the containerized production build locally:

```bash
# Build the lightweight Docker image
docker build -t pashudrishti-ai:latest .

# Run container on Port 8000 with persistent data mount
docker run -d \
  -p 8000:8000 \
  -e SESSION_SECRET="production-secure-random-key" \
  -v $(pwd)/data:/app/data \
  --name pashudrishti \
  pashudrishti-ai:latest

# Check health
curl http://localhost:8000/health
```

---

## 📡 API Reference

Interactive OpenAPI documentation is generated automatically by FastAPI at `/docs` (Swagger UI) and `/redoc`.

### Key Endpoints

| Endpoint | Method | Auth Required | Description |
| :--- | :--- | :--- | :--- |
| **`/health`** | `GET` | No | Returns system status and loaded model details (`status: ok`, `model_loaded: true`). |
| **`/signin`** | `GET, POST` | No | HTML sign-in form / session authentication. |
| **`/create-account`** | `GET, POST` | No | User registration with validation and duplicate checking. |
| **`/logout`** | `GET` | Yes | Terminates current user session and cookies. |
| **`/predict`** | `POST` | Yes | Multipart form upload. Dual-mode: returns HTML result page for browsers or JSON when `Accept: application/json` is sent. |
| **`/api/predict`** | `POST` | Yes | Direct REST API endpoint returning structured prediction JSON, confidence, and reverse-geocoded location. |
| **`/api/predictions`** | `GET` | Yes | Fetches paginated prediction history for the authenticated user from SQLite. |

### Sample Prediction Request (REST API)

```bash
curl -X POST "http://localhost:8000/api/predict" \
  -H "Cookie: session=<SESSION_COOKIE>" \
  -F "file=@cow_photo.jpg" \
  -F "animal_id=COW-KA-2026-0042" \
  -F "gps_coordinates=12.9716,77.5946"
```

**JSON Response (`200 OK`)**:
```json
{
  "animal_id": "COW-KA-2026-0042",
  "predicted_breed": "Gir",
  "confidence": 91.42,
  "location": "Bengaluru, Karnataka, India",
  "gps_coordinates": "12.9716,77.5946",
  "top_scores": [
    {"breed": "Gir", "confidence": 91.42},
    {"breed": "Red_Sindhi", "confidence": 4.18},
    {"breed": "Sahiwal", "confidence": 2.15},
    {"breed": "Bhadawari", "confidence": 1.10},
    {"breed": "Tharparkar", "confidence": 0.65}
  ]
}
```

---

## ⚙️ Environment Variables

| Variable | Default | Description |
| :--- | :--- | :--- |
| `PORT` | `8000` | Port on which the application listens. |
| `SESSION_SECRET` | `change-me` | Secret key used to encrypt and sign user cookies. |
| `MODEL_BUNDLE` | `cattle_model_low_hw.tar.gz` | Path to the compressed model bundle. |
| `DEBUG_BUNDLE` | `false` | When set to `true`, exposes `/debug/bundle` to inspect archive metadata (disabled in prod). |
| `DB_PATH` | `/app/data/app.db` | Absolute path to the SQLite persistence database. |
| `WEB_CONCURRENCY` | `2` | Number of parallel Uvicorn worker processes in container. |
| `AWS_S3_BUCKET` | *(Optional)* | S3 bucket name for archiving incoming cattle photos. |
| `AWS_REGION` | `ap-south-1` | AWS region for S3 uploads and AWS services. |

---

## 🔄 CI/CD & Automated Deployment

The repository is equipped with a GitHub Actions workflow: [`.github/workflows/deploy-aws.yml`](.github/workflows/deploy-aws.yml).

### Automated Pipeline Workflow:
1. **Automated Testing**: On every push to `main`, an Ubuntu runner boots up, generates test pictures via PIL, boots a background server, and runs `backend/test_api.py` across all endpoints.
2. **Container Build**: Builds the CPU-optimized Docker container.
3. **ECR Registry Push**: Authenticates with Amazon ECR (`239830941290.dkr.ecr.ap-south-1.amazonaws.com/pashudrishti-ai`) and pushes `latest` and commit-SHA-tagged images.
4. **Zero-Downtime Rollout**: Updates the ECS Task Definition and triggers a rolling update on `pashudrishti-web-service`. Traffic shifts only after target health checks pass.

> For complete manual provisioning steps, AWS CLI commands, operational runbooks, and cost breakdowns, consult the **[AWS Production Deployment Guide](AWS_DEPLOYMENT_GUIDE.md)**.

---

## 📂 Repository Structure

```text
PashuDrishti.ai/
├── .github/
│   └── workflows/
│       └── deploy-aws.yml         # GitHub Actions CI/CD automated pipeline
├── backend/
│   ├── app.py                     # Primary FastAPI application (UI + REST APIs + Lifespan)
│   ├── db.py                      # SQLite database connection & migrations
│   ├── schema.sql                 # Relational schema (users, predictions tables)
│   ├── seed_users.py              # Pre-seeded test accounts
│   ├── s3_utils.py                # Optional AWS S3 image archive integration
│   ├── create_test_images.py      # Standalone PIL image generator for testing
│   ├── test_api.py                # End-to-end integration test runner
│   ├── README.md                  # Detailed backend documentation
│   └── ml/
│       ├── colab_breed_recognition.py # Single-file Colab training script
│       ├── export_low_hardware.py     # INT8 & TorchScript quantization exporter
│       └── src/
│           ├── infer.py           # Core ML inference engine & preprocessing
│           ├── train.py           # EfficientNet training loop
│           ├── preprocess.py      # Dataset normalization & transformations
│           ├── config.py          # ML hyperparameters & path constants
│           └── web_app.py         # Entrypoint compatibility layer
├── .dockerignore                  # Docker build exclusions
├── .gitignore                     # Git tracking exclusions
├── AWS_DEPLOYMENT_GUIDE.md        # Comprehensive enterprise deployment runbook
├── Dockerfile                     # Multi-stage CPU PyTorch production Dockerfile
├── LICENSE                        # MIT License
├── README.md                      # Primary project overview and documentation
├── app.py                         # Standalone demo entry point
├── cattle_model_low_hw.tar.gz     # Quantized 41-breed INT8 model bundle (15.1 MB)
├── ecs-task-def.json              # Amazon ECS Fargate task definition
└── requirements.txt               # Locked Python dependencies
```

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
