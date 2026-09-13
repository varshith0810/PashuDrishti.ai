import json
from pathlib import Path
import torch
from torchvision import transforms, models
import torch.nn as nn
from PIL import Image
from src.config import Paths

class Predictor:
    def __init__(self, model_path: Path, class_path: Path):
        with open(class_path, "r", encoding="utf-8") as f:
            self.classes = json.load(f)

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        if self.device.type == "cuda":
            torch.backends.cudnn.benchmark = True
        model = models.efficientnet_b0(weights=None)
        in_features = model.classifier[1].in_features
        model.classifier[1] = nn.Linear(in_features, len(self.classes))
        try:
            state = torch.load(model_path, map_location=self.device, weights_only=False)
        except TypeError:
            state = torch.load(model_path, map_location=self.device)
        if isinstance(state, dict) and "model_state_dict" in state:
            state = state["model_state_dict"]
        model.load_state_dict(state)
        self.model = model.to(self.device).eval()

        self.tfms = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ])
    def predict(self, image: Image.Image, top_k: int = 3):
        use_cuda = self.device.type == "cuda"
        x = self.tfms(image.convert("RGB")).unsqueeze(0).to(self.device, non_blocking=use_cuda)
        with torch.inference_mode():
            if use_cuda:
                with torch.amp.autocast(device_type="cuda", dtype=torch.float16):
                    logits = self.model(x)
            else:
                logits = self.model(x)
            probs = torch.softmax(logits, dim=1)[0]
            vals, idxs = torch.topk(probs, k=min(top_k, len(self.classes)))
        return [
            {"breed": self.classes[i], "confidence": float(v)}
            for v, i in zip(vals.cpu().tolist(), idxs.cpu().tolist())
        ]
def load_predictor():
    paths = Paths()
    candidate_dirs = [
        paths.model_dir,
        paths.project_root.parent / "models",
        Path("models"),
        Path("backend/ml/models"),
    ]
    for c in candidate_dirs:
        m = c / "breed_classifier.pt"
        cl = c / "class_names.json"
        if m.exists() and cl.exists():
            return Predictor(m, cl)
    return Predictor(paths.model_dir / "breed_classifier.pt", paths.model_dir / "class_names.json")
