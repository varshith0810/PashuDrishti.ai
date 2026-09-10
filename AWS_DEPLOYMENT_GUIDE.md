# AWS Production Deployment Guide for PashuDrishti.ai
## (Amazon ECS Express Mode / ECS Fargate)

> [!IMPORTANT]
> **AWS Notice**: Starting April 30, 2026, AWS App Runner is no longer onboarding new customers. AWS officially recommends **Amazon ECS Express Mode** and **Amazon ECS Fargate** as the modern, long-term successor for running containerized web applications.

This guide provides end-to-end instructions for deploying PashuDrishti.ai using **Amazon ECS Express Mode / Fargate** to smoothly handle **1,000+ daily prediction requests** with sub-100ms inference latency, zero server maintenance, and automated scaling.

---

## 1. Architecture Overview

```
[Users / Mobile Clients] 
          │ (HTTPS)
          ▼
   [Route 53 / Custom Domain]
          │
          ▼
   [Amazon ECS Express Mode / Fargate Service]
     ├── 1 vCPU, 2 GB RAM (Task)
     ├── Gunicorn (2 Uvicorn Worker Threads)
     ├── PyTorch INT8 Model (~80ms inference)
     ├── Reverse Geocoding Memory Cache
     └── SQLite Database (Volume / Mount)
          │
          ▼ (Optional)
    [Amazon S3 Bucket] ── (High-resolution cattle images archive)
```

### Why ECS Express Mode Easily Handles 1,000 Requests/Day:
- **Traffic Profile**: 1,000 requests/day = average **~0.012 req/sec**, peaking at **1 to 3 req/sec** during peak daylight farm hours.
- **Performance**: Each prediction takes **~80ms** on CPU.
- **Capacity**: A single Fargate task (1 vCPU, 2 GB RAM) comfortably handles **15–25 requests/second** (~1.5+ million requests/day). 1,000 requests/day uses less than **0.2%** of available capacity.
- **Cost**: ~$15–$25 / month on Fargate.

---

## 2. Option A (Recommended): Deploying to Amazon ECS Express Mode

Amazon ECS Express Mode is designed to provide the simplicity of App Runner with the power, flexibility, and long-term support of Amazon ECS.

### Step 1: Create Amazon ECR Repository

```bash
aws ecr create-repository \
    --repository-name pashudrishti-ai \
    --region us-east-1 \
    --image-scanning-configuration scanOnPush=true
```

### Step 2: Build & Push the Production Container Image

```bash
# 1. Authenticate Docker with Amazon ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com

# 2. Build the production image using our optimized Dockerfile
docker build -t pashudrishti-ai:latest .

# 3. Tag and push to your ECR registry
docker tag pashudrishti-ai:latest <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/pashudrishti-ai:latest
docker push <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/pashudrishti-ai:latest
```

### Step 3: Deploy via Amazon ECS Express Mode

1. Open the **Amazon ECS Console**:
   [https://console.aws.amazon.com/ecs/v2/express-mode?region=us-east-1](https://console.aws.amazon.com/ecs/v2/express-mode?region=us-east-1)
2. Click **Create Service**.
3. **Application name**: `pashudrishti-backend`
4. **Container image**: `<AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/pashudrishti-ai:latest`
5. **Port**: `8000`
6. **Compute configuration**:
   - **CPU**: `1 vCPU`
   - **Memory**: `2 GB`
7. **Environment variables**:
   - `MODEL_BUNDLE`: `cattle_model_low_hw.tar.gz`
   - `DEBUG_BUNDLE`: `false`
   - `SESSION_SECRET`: `generate-a-secure-random-string`
   - `AWS_S3_BUCKET`: *(Optional: your S3 bucket name)*
8. **Networking & Ingress**:
   - Select **Public endpoint / HTTPS** (ECS Express Mode provisions automatic HTTPS URL and load balancer).
9. Click **Deploy**. In 2–4 minutes, your service is live and accessible globally!

---

## 3. Option B: Deploying via Standard ECS Fargate CLI

If you prefer deploying via the AWS CLI with our included [ecs-task-def.json](file:///c:/Users/Hp/OneDrive/Desktop/reddy/Github/PashuDrishti.ai/ecs-task-def.json):

```bash
# 1. Create ECS Cluster
aws ecs create-cluster --cluster-name pashudrishti-cluster --region us-east-1

# 2. Register Task Definition (replace <AWS_ACCOUNT_ID> with your account ID)
sed -i 's/<AWS_ACCOUNT_ID>/YOUR_ACCOUNT_ID/g' ecs-task-def.json
aws ecs register-task-definition --cli-input-json file://ecs-task-def.json --region us-east-1

# 3. Create Fargate Service
aws ecs create-service \
    --cluster pashudrishti-cluster \
    --service-name pashudrishti-service \
    --task-definition pashudrishti-backend \
    --desired-count 1 \
    --launch-type FARGATE \
    --network-configuration "awsvpcConfiguration={subnets=[subnet-xxxxxx],securityGroups=[sg-xxxxxx],assignPublicIp=ENABLED}" \
    --region us-east-1
```

---

## 4. Option C (Budget): Deploying on AWS EC2 `t4g.small` ($7/month)

For absolute lowest monthly cost, an EC2 Graviton2 instance running Docker:

```bash
# 1. Launch Ubuntu 24.04 ARM64 instance (t4g.small) in EC2 console
ssh -i your-key.pem ubuntu@<EC2_PUBLIC_IP>

# 2. Install Docker
sudo apt update && sudo apt install -y docker.io git

# 3. Clone repository
git clone https://github.com/varshith0810/PashuDrishti.ai.git
cd PashuDrishti.ai

# 4. Build & run production container
sudo docker build -t pashudrishti:latest .
sudo docker run -d \
  --name pashudrishti \
  --restart always \
  -p 80:8000 \
  -v $(pwd)/data:/app/data \
  -e SESSION_SECRET="your-secure-random-secret" \
  pashudrishti:latest

# Check health
curl http://localhost/health
```

---

## 5. Automated CI/CD Setup with GitHub Actions

The repository includes [`.github/workflows/deploy-aws.yml`](.github/workflows/deploy-aws.yml) configured for Amazon ECS.

To enable automated testing and deployment on every `git push`:
1. In your GitHub repository, navigate to **Settings** &rarr; **Secrets and variables** &rarr; **Actions**.
2. Add the following secrets:
   - `AWS_ACCESS_KEY_ID`: IAM user access key with ECR and ECS permissions.
   - `AWS_SECRET_ACCESS_KEY`: IAM user secret key.
3. Every commit to `main` will:
   - Automatically execute the comprehensive test suite with 9 different cattle pictures.
   - Build the production Docker image.
   - Push to Amazon ECR.
   - Update the Amazon ECS Service with zero downtime.

---

## 6. (Optional) Amazon S3 Photo Archiving

1. Create an S3 bucket:
   ```bash
   aws s3 mb s3://pashudrishti-photos-prod --region us-east-1
   ```
2. In your ECS service configuration, add the environment variable:
   ```text
   AWS_S3_BUCKET=pashudrishti-photos-prod
   AWS_REGION=us-east-1
   ```
3. Ensure the ECS Task Role has `s3:PutObject` and `s3:GetObject` permissions. All uploaded animal photos will automatically be archived in S3 with unique timestamped keys.
