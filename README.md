# 🔐 ChainSentinel API

This is the core backend service for **ChainSentinel**, a blockchain fraud detection system. The API is built with FastAPI and integrates with Firebase, a machine learning microservice, and Firestore for secure and intelligent transaction analysis.

---

## 🚀 Key Features

- 🔐 **JWT Authentication** via Firebase
- 🔍 **Real-time fraud analysis** with external ML service
- 📡 **Etherscan API** integration for blockchain transaction data
- ⚠️ **User-defined alerts** on suspicious activities
- 🧠 **Retrainable ML model** through secure endpoints
- 🧾 **Labeling and feedback** for model improvement
- 📁 Modular, scalable Python project architecture

---

## 📁 Project Structure

```
chain-sentinel-api/
├── app/
│   ├── api/v1/routers/    # All versioned route logic
│   ├── auth/              # Firebase auth and JWT
│   ├── core/              # App configuration
│   ├── firebase/          # Firestore client & initialization
│   ├── models/            # Firestore document models
│   ├── schemas/           # Request/response validation
│   ├── services/          # Business logic: alerts, ML, blockchain
│   └── main.py            # FastAPI app definition
├── credentials/           # Firebase credentials
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 🔄 API Endpoints

### Transactions

| Method | Endpoint                              | Description                  |
| ------ | ------------------------------------- | ---------------------------- |
| GET    | `/api/v1/transactions/{address}`      | List transactions by address |
| POST   | `/api/v1/transactions`                | Create new transaction       |
| PATCH  | `/api/v1/transactions/{doc_id}/label` | Update real label            |

### Alerts

| Method | Endpoint                    | Description           |
| ------ | --------------------------- | --------------------- |
| GET    | `/api/v1/alerts`            | Get alerts by user    |
| POST   | `/api/v1/alerts`            | Create a new alert    |
| GET    | `/api/v1/alerts/by-address` | Get alerts by address |
| DELETE | `/api/v1/alerts/{alert_id}` | Delete an alert       |

### Analysis

| Method | Endpoint          | Description         |
| ------ | ----------------- | ------------------- |
| POST   | `/api/v1/analyze` | Analyze transaction |

### Risk Reports

| Method | Endpoint        | Description                 |
| ------ | --------------- | --------------------------- |
| GET    | `/api/v1/risks` | Get suspicious transactions |

### ML Model

| Method | Endpoint                  | Description               |
| ------ | ------------------------- | ------------------------- |
| POST   | `/api/v1/ml/train`        | Train ML model            |
| GET    | `/api/v1/ml/train/status` | Get model training status |

### Admin

| Method | Endpoint                      | Description       |
| ------ | ----------------------------- | ----------------- |
| POST   | `/api/v1/auth/register-admin` | Register an admin |

### Health Check

| Method | Endpoint         | Description         |
| ------ | ---------------- | ------------------- |
| GET    | `/api/v1/health` | Health check status |

---

## 🔐 Authentication

All secured endpoints require a **Firebase JWT token** in the `Authorization` header:

```
Authorization: Bearer <your_token>
```

---

## 💻 Running Locally

```bash
# Clone the repository
git clone https://github.com/your_username/chain-sentinel-api.git
cd chain-sentinel-api

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the API
uvicorn app.main:app --reload
```

---

## ☁️ Deployment on Google Cloud Run

```bash
gcloud builds submit --tag gcr.io/YOUR_PROJECT/chain-sentinel-api

gcloud run deploy chain-sentinel-api \
  --image gcr.io/YOUR_PROJECT/chain-sentinel-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

## 🧪 Tests

This project is structured to support Pytest and modular testing (tests folder to be implemented).

---

## 📚 References

- [Firebase Admin SDK](https://firebase.google.com/docs/admin/setup)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Firestore](https://firebase.google.com/docs/firestore)
- [Etherscan API](https://docs.etherscan.io/)
- Part of the broader [ChainSentinel Ecosystem](https://github.com/your_username/ChainSentinel)
