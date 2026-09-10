import json
import tarfile
import torch
import torch.nn as nn
from torchvision import models

def create_dummy_model():
    classes = ["Angus", "Brahman", "Hereford"]
    
    with open("class_names.json", "w") as f:
        json.dump(classes, f)
        
    model = models.efficientnet_b0(weights=None)
    model.classifier[1] = nn.Linear(model.classifier[1].in_features, len(classes))
    model.eval()
    
    example = torch.randn(1, 3, 224, 224)
    traced = torch.jit.trace(model, example)
    traced.save("breed_classifier_ts.pt")
    
    with tarfile.open("cattle_model_low_hw.tar.gz", "w:gz") as tar:
        tar.add("class_names.json")
        tar.add("breed_classifier_ts.pt")
        
    print("Created dummy model bundle cattle_model_low_hw.tar.gz")

if __name__ == "__main__":
    create_dummy_model()
