DISEASE_INFO = {
    "HealthyLeaf": {
        "disease_name": "Healthy",
        "severity": "None",
        "description": "Wheat plant is healthy, no disease detected.",
        "recommendation": "Continue regular monitoring and standard crop care practices."
    },
    "BlackPoint": {
        "disease_name": "Black Point",
        "severity": "Moderate",
        "description": "A fungal disease that discolors the wheat kernel embryo end, affecting grain quality.",
        "recommendation": "Improve field drainage, avoid excess nitrogen, and consider fungicide application during grain filling stage. Consult local agricultural officer for approved fungicides."
    },
    "FusariumFootRot": {
        "disease_name": "Fusarium Foot Rot",
        "severity": "High",
        "description": "A soil-borne fungal disease attacking the base of the stem, causing lodging and yield loss.",
        "recommendation": "Practice crop rotation, avoid wheat-after-wheat planting, ensure proper field drainage, and use certified disease-free seeds."
    },
    "LeafBlight": {
        "disease_name": "Leaf Blight",
        "severity": "High",
        "description": "A fungal infection causing lesions and yellowing on leaves, reducing photosynthesis.",
        "recommendation": "Apply appropriate fungicide as per local agricultural guidelines, remove and destroy infected plant debris, avoid overhead irrigation."
    },
    "WheatBlast": {
        "disease_name": "Wheat Blast",
        "severity": "Critical",
        "description": "A severe fungal disease that can cause complete crop loss if untreated, affects spikes and leaves.",
        "recommendation": "Immediate consultation with agricultural extension officer required. Consider resistant varieties for future planting. Isolate and monitor affected zones closely."
    }
}

def get_suggestion(predicted_class: str):
    return DISEASE_INFO.get(predicted_class, {
        "disease_name": "Unknown",
        "severity": "Unknown",
        "description": "Could not match disease information.",
        "recommendation": "Please consult a local agricultural expert."
    })