"""
Evaluate trained cattle & buffalo breed recognition model on unseen data.
Computes Top-1 Accuracy, Top-5 Accuracy, average latency per image, and per-breed performance.
"""

import argparse
import json
import time
from pathlib import Path
import sys
from collections import defaultdict

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, models, transforms
from tqdm import tqdm

_ML_DIR = Path(__file__).resolve().parents[1]
if str(_ML_DIR) not in sys.path:
    sys.path.insert(0, str(_ML_DIR))

try:
    from src.config import Paths
except ImportError:
    from backend.ml.src.config import Paths


def get_eval_dataloader(data_path: Path, image_size: int = 224, batch_size: int = 32):
    # Resolve if given root containing 'test' or direct test folder
    if (data_path / "test").exists():
        eval_dir = data_path / "test"
    else:
        eval_dir = data_path

    eval_tfms = transforms.Compose([
        transforms.Resize((image_size, image_size)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])

    dataset = datasets.ImageFolder(eval_dir, transform=eval_tfms)
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=False, num_workers=2, pin_memory=torch.cuda.is_available())
    return loader, dataset.classes


def load_model_for_eval(model_path: Path, num_classes: int, device: torch.device):
    if model_path.suffix == ".pt" and "ts" in model_path.stem:
        model = torch.jit.load(str(model_path), map_location=device)
        return model.eval()

    model = models.efficientnet_b0(weights=None)
    model.classifier[1] = nn.Linear(model.classifier[1].in_features, num_classes)
    state = torch.load(model_path, map_location=device)
    model.load_state_dict(state)
    return model.to(device).eval()


def evaluate_unseen(data_path: Path, model_path: Path, class_path: Path, batch_size: int = 32):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"\n=======================================================")
    print(f"   EVALUATING MODEL PERFORMANCE ON UNSEEN DATA")
    print(f"=======================================================")
    print(f"Device: {device} ({torch.cuda.get_device_name(0) if device.type == 'cuda' else 'CPU'})")
    print(f"Model Path: {model_path}")
    print(f"Dataset Path: {data_path}")

    with open(class_path, "r", encoding="utf-8") as f:
        classes = json.load(f)

    loader, dataset_classes = get_eval_dataloader(data_path, batch_size=batch_size)
    model = load_model_for_eval(model_path, len(classes), device)

    # Class mapping index between dataset folders and model classes
    class_to_model_idx = {c: classes.index(c) for c in dataset_classes if c in classes}

    correct_top1 = 0
    correct_top5 = 0
    total_samples = 0
    latencies = []

    per_class_total = defaultdict(int)
    per_class_correct = defaultdict(int)

    print(f"Evaluating {len(loader.dataset)} unseen images across {len(dataset_classes)} classes...\n")

    with torch.inference_mode():
        for x, y in tqdm(loader, desc="Testing"):
            x = x.to(device, non_blocking=(device.type == "cuda"))

            t0 = time.perf_counter()
            if device.type == "cuda":
                with torch.amp.autocast(device_type="cuda", dtype=torch.float16):
                    logits = model(x)
            else:
                logits = model(x)
            t1 = time.perf_counter()
            latencies.append((t1 - t0) * 1000.0 / x.size(0))

            # Top-1
            pred_top1 = logits.argmax(dim=1).cpu()

            # Top-5
            k = min(5, logits.size(1))
            topk_preds = torch.topk(logits, k=k, dim=1).indices.cpu()

            # Map dataset targets to model label indices
            for i in range(len(y)):
                true_label_name = dataset_classes[y[i]]
                if true_label_name in class_to_model_idx:
                    model_target = class_to_model_idx[true_label_name]
                    is_correct_top1 = (pred_top1[i].item() == model_target)
                    is_correct_top5 = (model_target in topk_preds[i].tolist())

                    if is_correct_top1:
                        correct_top1 += 1
                        per_class_correct[true_label_name] += 1
                    if is_correct_top5:
                        correct_top5 += 1

                    per_class_total[true_label_name] += 1
                    total_samples += 1

    top1_acc = (correct_top1 / max(total_samples, 1)) * 100.0
    top5_acc = (correct_top5 / max(total_samples, 1)) * 100.0
    avg_latency = sum(latencies) / max(len(latencies), 1)

    print("\n------------------ EVALUATION RESULTS ------------------")
    print(f"Total Unseen Samples Evaluated : {total_samples}")
    print(f"Top-1 Accuracy                 : {top1_acc:.2f}%")
    print(f"Top-5 Accuracy                 : {top5_acc:.2f}%")
    print(f"Average Latency per Image      : {avg_latency:.2f} ms")
    print(f"Throughput                     : {1000.0 / avg_latency:.1f} images/sec")
    print("--------------------------------------------------------")

    # Show lowest & highest performing breeds
    class_accuracies = [
        (name, (per_class_correct[name] / per_class_total[name]) * 100.0, per_class_total[name])
        for name in per_class_total
    ]
    class_accuracies.sort(key=lambda x: x[1])

    print("\nBreeds with Lowest Accuracy (Hardest to distinguish):")
    for name, acc, count in class_accuracies[:5]:
        print(f"  - {name:<20}: {acc:5.1f}% ({count} samples)")

    print("\nBreeds with Highest Accuracy (Easiest to distinguish):")
    for name, acc, count in class_accuracies[-5:][::-1]:
        print(f"  - {name:<20}: {acc:5.1f}% ({count} samples)")
    print("========================================================\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate cattle & buffalo breed recognition model on unseen data")
    default_test = Paths().extracted_data / "test"
    parser.add_argument("--dataset_dir", type=str, default=str(default_test) if default_test.exists() else "archive/IndianCattleBuffaloeBreeds-Dataset/breeds/test")
    parser.add_argument("--model_path", type=str, default="models/breed_classifier.pt")
    parser.add_argument("--classes_path", type=str, default="models/class_names.json")
    parser.add_argument("--batch_size", type=int, default=32)
    args = parser.parse_args()

    evaluate_unseen(Path(args.dataset_dir), Path(args.model_path), Path(args.classes_path), batch_size=args.batch_size)
