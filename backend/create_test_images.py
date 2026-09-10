import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import shutil

TEST_DIR = Path(__file__).resolve().parent / "test_images"
TEST_DIR.mkdir(parents=True, exist_ok=True)

def create_gir_cow():
    img = Image.new("RGB", (320, 240), color=(165, 42, 42))
    draw = ImageDraw.Draw(img)
    draw.ellipse([40, 60, 280, 220], fill=(180, 50, 45), outline=(130, 30, 25))
    draw.ellipse([180, 30, 270, 130], fill=(150, 40, 35))
    draw.polygon([(170, 70), (160, 140), (185, 110)], fill=(120, 30, 25))
    draw.polygon([(260, 70), (275, 140), (250, 110)], fill=(120, 30, 25))
    img = img.filter(ImageFilter.GaussianBlur(1.5))
    path = TEST_DIR / "01_gir_reddish.jpg"
    img.save(path, format="JPEG", quality=90)
    return path

def create_holstein():
    img = Image.new("RGB", (300, 300), color=(245, 245, 245))
    draw = ImageDraw.Draw(img)
    draw.ellipse([30, 40, 140, 150], fill=(20, 20, 25))
    draw.ellipse([150, 80, 280, 220], fill=(15, 15, 20))
    draw.ellipse([70, 180, 170, 270], fill=(25, 25, 30))
    draw.ellipse([200, 20, 260, 80], fill=(30, 30, 35))
    img = img.filter(ImageFilter.GaussianBlur(1.0))
    path = TEST_DIR / "02_holstein_spotted.jpg"
    img.save(path, format="JPEG", quality=90)
    return path

def create_murrah_buffalo():
    img = Image.new("RGB", (256, 256), color=(25, 28, 32))
    draw = ImageDraw.Draw(img)
    draw.ellipse([50, 50, 210, 210], fill=(35, 38, 44))
    draw.arc([40, 30, 120, 110], start=120, end=330, fill=(60, 60, 65), width=8)
    draw.arc([140, 30, 220, 110], start=210, end=60, fill=(60, 60, 65), width=8)
    draw.ellipse([100, 150, 160, 190], fill=(18, 20, 22))
    img = img.filter(ImageFilter.GaussianBlur(1.2))
    path = TEST_DIR / "03_murrah_dark.jpg"
    img.save(path, format="JPEG", quality=92)
    return path

def create_sahiwal():
    img = Image.new("RGB", (400, 300), color=(205, 133, 63))
    draw = ImageDraw.Draw(img)
    draw.ellipse([80, 70, 350, 260], fill=(220, 150, 80))
    draw.ellipse([240, 40, 340, 140], fill=(190, 120, 50))
    draw.ellipse([280, 100, 320, 130], fill=(230, 200, 170))
    img = img.filter(ImageFilter.GaussianBlur(1.5))
    path = TEST_DIR / "04_sahiwal_golden.jpg"
    img.save(path, format="JPEG", quality=90)
    return path

def create_brahman():
    img = Image.new("RGB", (224, 224), color=(215, 220, 225))
    draw = ImageDraw.Draw(img)
    draw.ellipse([50, 30, 130, 120], fill=(160, 165, 175))
    draw.ellipse([30, 80, 200, 200], fill=(195, 200, 208))
    draw.ellipse([140, 90, 210, 170], fill=(175, 180, 190))
    draw.polygon([(150, 150), (170, 210), (190, 160)], fill=(155, 160, 170))
    img = img.filter(ImageFilter.GaussianBlur(1.0))
    path = TEST_DIR / "05_brahman_grey.jpg"
    img.save(path, format="JPEG", quality=90)
    return path

def create_jersey():
    img = Image.new("RGB", (280, 350), color=(210, 166, 121))
    draw = ImageDraw.Draw(img)
    draw.ellipse([40, 80, 250, 300], fill=(188, 143, 98))
    draw.ellipse([80, 30, 200, 150], fill=(160, 115, 75))
    draw.ellipse([110, 110, 170, 145], fill=(240, 230, 210))
    path = TEST_DIR / "06_jersey_fawn.png"
    img.save(path, format="PNG")
    return path

def copy_system_samples():
    sample_paths = []
    gradio_lion = Path(__file__).resolve().parent.parent / ".venv/Lib/site-packages/gradio/media_assets/images/lion.jpg"
    if gradio_lion.exists():
        dest = TEST_DIR / "07_lion_sample.jpg"
        shutil.copy(gradio_lion, dest)
        sample_paths.append(dest)
        
    sklearn_china = Path(__file__).resolve().parent.parent / ".venv/Lib/site-packages/sklearn/datasets/images/china.jpg"
    if sklearn_china.exists():
        dest = TEST_DIR / "08_scenery_china.jpg"
        shutil.copy(sklearn_china, dest)
        sample_paths.append(dest)

    sklearn_flower = Path(__file__).resolve().parent.parent / ".venv/Lib/site-packages/sklearn/datasets/images/flower.jpg"
    if sklearn_flower.exists():
        dest = TEST_DIR / "09_flower_sample.jpg"
        shutil.copy(sklearn_flower, dest)
        sample_paths.append(dest)
        
    return sample_paths

def generate_all_images():
    generated = [
        create_gir_cow(),
        create_holstein(),
        create_murrah_buffalo(),
        create_sahiwal(),
        create_brahman(),
        create_jersey(),
    ]
    generated.extend(copy_system_samples())
    print(f"Generated {len(generated)} diverse test images in {TEST_DIR}:")
    for p in generated:
        print(f"  - {p.name} ({p.stat().st_size} bytes)")
    return generated

if __name__ == "__main__":
    generate_all_images()
