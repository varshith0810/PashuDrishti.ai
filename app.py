import sys
from pathlib import Path

ML_DIR = Path(__file__).resolve().parent / "backend" / "ml"
if str(ML_DIR) not in sys.path:
    sys.path.insert(0, str(ML_DIR))

import gradio as gr
from PIL import Image
from src.infer import load_predictor
predictor = None
def classify(image: Image.Image | None):
    if image is None:
        return "⚠️ Please upload an animal image before clicking Recognize Breed."
    global predictor
    try:
        if predictor is None:
            predictor = load_predictor()
        preds = predictor.predict(image, top_k=5)
        top = preds[0]
        lines = [f"Predicted Breed: {top['breed']}", "", "Top-5 confidence scores:"]
        for item in preds:
            lines.append(f"- {item['breed']}: {item['confidence']*100:.2f}%")
        return "\n".join(lines)
    except Exception as exc:
        return f"⚠️ Prediction Error: {exc}\nPlease ensure the model weights are available in the models/ directory."
with gr.Blocks(title="Indian Cattle & Buffalo Breed Recognition") as demo:
    gr.Markdown("## AI-Assisted Breed Recognition for Indian Cattle and Buffaloes")
    gr.Markdown("Upload an animal image to identify its breed (software-only model; no hardware dependencies).")
    with gr.Row():
        image = gr.Image(type="pil", label="Upload Animal Image")
        output = gr.Textbox(label="Recognition Output", lines=10)
    button = gr.Button("Recognize Breed")
    button.click(classify, inputs=image, outputs=output)
if __name__ == "__main__":
    demo.launch()
