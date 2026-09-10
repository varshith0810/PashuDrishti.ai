# PashuDrishti.ai
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
- **Interactive Swagger API Docs**: **[http://pashudrishti-alb-1806113337.ap-south-1.elb.amazonaws.com/docs](http://pashudrishti-alb-1806113337.ap-south-1.elb.amazonaws.com/docs)**

---

## ✨ Production Capabilities

- **41-Breed Recognition**: High-precision multi-class classification covering Gir, Murrah, Sahiwal, Red Sindhi, Jaffrabadi, Kankrej, Tharparkar, and 34 other breeds.
- **Sub-100ms Low-Hardware Inference**: Pre-warmed INT8 dynamic quantization runs in ~80ms on commodity CPUs, allowing a single 1 vCPU container to handle over **1.5 million requests/month**.
- **Dual Interface (Web UI + REST API)**: Server-rendered web UI for browser users and JSON REST endpoints (`/api/predict`, `/api/predictions`) for mobile apps and IoT integrations.
- **Geolocation & Reverse-Geocoding**: Accepts GPS coordinates (`lat,long`), maps the animal to a geographic district/state using an in-memory cached reverse-geocoding engine.
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
                                  [ Web & Mobile Clients ]
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

## 🐳 Container Deployment

Deploy using the production multi-stage Docker container:

```bash
# Build the optimized production container
docker build -t pashudrishti-ai:latest .

# Run container on Port 8000 with volume persistence
docker run -d \
  -p 8000:8000 \
  -e SESSION_SECRET="your-secure-production-secret" \
  -v $(pwd)/data:/app/data \
  --name pashudrishti \
  pashudrishti-ai:latest

# Verify health status
curl http://localhost:8000/health
```

---

## 📡 API Reference

Interactive OpenAPI documentation is available in production at `/docs` (Swagger UI) and `/redoc`.

### Key Endpoints

| Endpoint | Method | Auth Required | Description |
| :--- | :--- | :--- | :--- |
| **`/health`** | `GET` | No | Returns system health and model readiness status (`status: ok`, `model_loaded: true`). |
| **`/signin`** | `GET, POST` | No | Authentication gateway and session management. |
| **`/create-account`** | `GET, POST` | No | Account registration with validation and unique constraint enforcement. |
| **`/logout`** | `GET` | Yes | Clears session credentials. |
| **`/predict`** | `POST` | Yes | Multipart image upload. Dual-mode: returns HTML result page or JSON when `Accept: application/json` is supplied. |
| **`/api/predict`** | `POST` | Yes | Direct REST API endpoint returning structured prediction JSON, confidence score, and reverse-geocoded location. |
| **`/api/predictions`** | `GET` | Yes | Retrieves paginated historical records from persistent storage. |

### Sample Prediction Request (REST API)

```bash
curl -X POST "http://pashudrishti-alb-1806113337.ap-south-1.elb.amazonaws.com/api/predict" \
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

## ⚙️ Production Environment Variables

| Variable | Default | Description |
| :--- | :--- | :--- |
| `PORT` | `8000` | Port on which the container listens. |
| `SESSION_SECRET` | `change-me` | Secret key used for cryptographic session cookie signing. |
| `MODEL_BUNDLE` | `cattle_model_low_hw.tar.gz` | Path to the INT8-quantized model bundle. |
| `DEBUG_BUNDLE` | `false` | When `true`, exposes `/debug/bundle` (must remain `false` in production). |
| `DB_PATH` | `/app/data/app.db` | Path to the persistent SQLite database file. |
| `WEB_CONCURRENCY` | `2` | Number of concurrent worker processes running inside the container. |
| `AWS_S3_BUCKET` | *(Optional)* | S3 bucket name for archiving incoming cattle photos. |
| `AWS_REGION` | `ap-south-1` | AWS region for cloud service communication. |

---

## 🔄 CI/CD & Automated Cloud Deployment

The platform implements automated continuous delivery via [`.github/workflows/deploy-aws.yml`](.github/workflows/deploy-aws.yml):

1. **Automated Verification**: Generates dynamic test fixtures and runs integration tests across all API routes on every commit to `main`.
2. **Container Build**: Compiles the CPU-optimized, multi-stage Docker image.
3. **ECR Registry Push**: Pushes verified images tagged with the Git commit SHA and `latest` to Amazon ECR (`239830941290.dkr.ecr.ap-south-1.amazonaws.com/pashudrishti-ai`).
4. **Zero-Downtime Deployment**: Updates the Amazon ECS Fargate task definition and shifts live traffic via the Application Load Balancer only after target health checks pass.

> For complete provisioning steps, AWS CLI commands, operational runbooks, and cost breakdowns, refer to the **[AWS Production Deployment Guide](AWS_DEPLOYMENT_GUIDE.md)**.

---

## 📂 Production Repository Structure

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
│   ├── README.md                  # Backend documentation
│   └── ml/
│       ├── colab_breed_recognition.py # Training pipeline script
│       ├── export_low_hardware.py     # INT8 & TorchScript quantization exporter
│       └── src/
│           ├── infer.py           # Core ML inference engine & preprocessing
│           ├── train.py           # EfficientNet training loop
│           ├── preprocess.py      # Dataset normalization & transformations
│           ├── config.py          # ML hyperparameters & path constants
│           └── web_app.py         # Entrypoint compatibility layer
├── .dockerignore                  # Docker build exclusions
├── .gitignore                     # Git tracking exclusions
├── AWS_DEPLOYMENT_GUIDE.md        # Enterprise deployment runbook
├── Dockerfile                     # Multi-stage CPU PyTorch production Dockerfile
├── LICENSE                        # MIT License
├── README.md                      # Primary production documentation
├── app.py                         # Standalone demo entry point
├── cattle_model_low_hw.tar.gz     # Quantized 41-breed INT8 model bundle (15.1 MB)
├── ecs-task-def.json              # Amazon ECS Fargate task definition
└── requirements.txt               # Locked dependencies
```

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
