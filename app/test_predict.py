import sys
sys.path.append(".")

from app.model_loader import model, predict_image, class_names
from PIL import Image
import torch

print("=" * 50)
print("Class names loaded:", class_names)
print("=" * 50)

# Model ke kuch weights check karo (confirm karne ke liye ke trained weights load hue ya random)
print("Sample weight value (fc layer):", model.fc.weight[0][:5])
print("=" * 50)

# Apne test dataset se ek image ka EXACT path yahan daalo
# jaise: "C:/Users/YourName/Downloads/HealthyLeaf_5.jpg"
test_image_path = test_folder = r"D:\DataSets\Disease Dataset of Wheat Original, Augmented, and Balanced for Deep Learning\Wheat Disease\Wheat Disease\Split Dataset\Test\FusariumFootRot\augmented_pil_540_b1.01_c1.07_col0.90.jpg"

image = Image.open(test_image_path)
predicted_class, confidence = predict_image(image)

print(f"Image: {test_image_path}")
print(f"Predicted: {predicted_class}")
print(f"Confidence: {confidence}%")