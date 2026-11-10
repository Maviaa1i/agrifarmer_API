# Wheat Disease Detection API

An AI-powered system for detecting wheat leaf diseases from images using deep learning (transfer learning), served through a REST API built with FastAPI. This is the core module (MVP) of a larger **Agriculture AI Software** project aimed at helping Pakistani farmers with crop monitoring and disease diagnosis.

## Project Overview

Farmers can upload a photo of a wheat leaf, and the system will:
1. Classify the leaf as **Healthy** or identify the specific **disease**
2. Return a **confidence score** for the prediction
3. Provide a **severity level** and **treatment recommendation**

This is the foundational piece of a larger vision that will eventually include satellite-based farm monitoring (NDVI/NDWI), weather/soil integration, and proactive risk alerts.

## Problem Statement

Wheat crops in Pakistan are affected by several fungal diseases that reduce yield and grain quality. Early and accurate identification of these diseases is often difficult for farmers without expert knowledge, leading to delayed or incorrect treatment. This project aims to make disease diagnosis accessible via a simple photo upload from a mobile device.

## Dataset

- **Source:** [Disease Dataset of Wheat – Original, Augmented, and Balanced for Deep Learning](https://data.mendeley.com/datasets/5gc7hwydwg/1) (Mendeley Data)
- **Classes (5):** Healthy Leaf, Black Point, Fusarium Foot Rot, Leaf Blight, Wheat Blast
- **Split used:** Pre-divided by the dataset authors
  - Train: 3,500 images (700 per class)
  - Validation: 1,000 images (200 per class)
  - Test: 500 images (100 per class)
- Balanced across all classes to avoid bias during training.

## Model & Approach

- **Technique:** Transfer Learning
- **Base architecture:** ResNet18 (pretrained on ImageNet)
- **Framework:** PyTorch
- **Approach:**
  1. Loaded ResNet18 with pretrained ImageNet weights
  2. Froze all convolutional layers (feature extractor)
  3. Replaced the final fully-connected layer to output 5 classes
  4. Trained only the new classification head for 10 epochs
  5. Evaluated on a held-out, unseen test set

### Why Transfer Learning?
Training a CNN from scratch requires large datasets and significant compute. Transfer learning leverages features already learned from millions of ImageNet images (edges, textures, shapes), allowing strong performance with a comparatively small, domain-specific dataset.

## Results

| Metric | Score |
|---|---|
| Train Accuracy | 98.34% |
| Validation Accuracy | 98.40% |
| **Test Accuracy (unseen data)** | **99.20%** |

**Per-class performance (Test Set):**

| Class | Precision | Recall | F1-score |
|---|---|---|---|
| Black Point | 0.97 | 1.00 | 0.99 |
| Fusarium Foot Rot | 1.00 | 0.99 | 0.99 |
| Healthy Leaf | 0.99 | 0.97 | 0.98 |
| Leaf Blight | 1.00 | 1.00 | 1.00 |
| Wheat Blast | 1.00 | 1.00 | 1.00 |

The close gap between training and test accuracy indicates the model generalizes well and is not overfitting.

## Tech Stack

| Layer | Technology |
|---|---|
| Model Training | Python, PyTorch, Torchvision, Google Colab (GPU) |
| Backend API | FastAPI, Uvicorn |
| Image Processing | Pillow (PIL) |
| Planned Frontend | Flutter |

## Project Structure

```
wheat-disease-api/
│
├── models/
│   ├── wheat_classifier_resnet18.pth   # Trained model weights
│   └── class_names.json                 # Class label mapping
│
├── app/
│   ├── __init__.py
│   ├── model_loader.py       # Loads model, runs inference
│   ├── suggestions.py        # Disease -> treatment recommendation mapping
│   └── main.py                # FastAPI application & endpoints
│
├── requirements.txt
└── README.md
```

## Setup & Installation

```bash
# Create and activate a virtual environment
python -m venv venv

# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies and start the API
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://127.0.0.1:8000`, with interactive documentation at `http://127.0.0.1:8000/docs`.

## Railway Deployment

Deploy from the repository root so Railway uses the root `Procfile`, `requirements.txt`, `app/`, and `models/`. Set a strong `SECRET_KEY` in Railway's Variables and attach a PostgreSQL service so `DATABASE_URL` is provided. The Procfile starts Uvicorn on Railway's assigned port. The model weights and `models/class_names.json` must remain in the deployed repository.

## API Endpoints

### `GET /`
Health check — confirms the API is running.

### `POST /predict`
Accepts an image file and returns the disease prediction.

**Request:** `multipart/form-data` with a `file` field (image)

**Response example:**
```json
{
  "predicted_class": "HealthyLeaf",
  "confidence": 99.84,
  "disease_name": "Healthy",
  "severity": "None",
  "description": "Wheat plant is healthy, no disease detected.",
  "recommendation": "Continue regular monitoring and standard crop care practices."
}
```

## Future Work (Planned Roadmap)

- [ ] Flutter mobile app integration (camera capture → API → result display)
- [ ] Deployment to a cloud server for public/mobile access
- [ ] Farm boundary mapping via GPS
- [ ] Satellite-based monitoring (Sentinel-2, NDVI/NDWI) for early anomaly detection
- [ ] Weather and soil moisture integration for context-aware risk scoring
- [ ] Support for additional crops beyond wheat

## Author

[Aapka naam yahan likhein]
Final Year Project — [University/Program ka naam]