import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "wheat_classifier_resnet18.pth")
CLASSES_PATH = os.path.join(BASE_DIR, "models", "class_names.json")

device = torch.device("cpu")   # local machine pe CPU hi use hoga

with open(CLASSES_PATH, "r") as f:
    class_names = json.load(f)

def load_model():
    model = models.resnet18(weights=None)
    num_features = model.fc.in_features
    model.fc = nn.Linear(num_features, len(class_names))

    print("Model file size (bytes):", os.path.getsize(MODEL_PATH))
    
    checkpoint = torch.load(MODEL_PATH, map_location=device)
    result = model.load_state_dict(checkpoint, strict=True)
    print("Missing keys:", result.missing_keys)
    print("Unexpected keys:", result.unexpected_keys)

    model.to(device)
    model.eval()
    return model

model = load_model()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                          std=[0.229, 0.224, 0.225])
])

def predict_image(image: Image.Image):
    image = image.convert("RGB")
    img_tensor = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(img_tensor)
        probabilities = torch.nn.functional.softmax(outputs, dim=1)
        confidence, predicted_idx = torch.max(probabilities, 1)

    predicted_class = class_names[predicted_idx.item()]
    confidence_score = round(confidence.item() * 100, 2)

    return predicted_class, confidence_score