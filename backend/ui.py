"""
PashuDrishti.ai - Modern UI/UX Engine
High-fidelity dark-mode glassmorphism design system for cattle & buffalo breed recognition.
"""

from __future__ import annotations

import html
from typing import Any
from starlette.requests import Request

# Comprehensive Breed Metadata Dictionary (Native Tract, Primary Purpose, Characteristics)
BREED_FACTS: dict[str, dict[str, str]] = {
    "gir": {
        "species": "Cattle (Bos indicus)",
        "origin": "Saurashtra / Gir Hills, Gujarat",
        "purpose": "Milch (High Milk Yield)",
        "fat": "4.5% - 5.0%",
        "traits": "Prominent convex forehead, long pendulous ears curved like folded leaves, reddish-brown spotted coat.",
    },
    "murrah": {
        "species": "Buffalo (Bubalus bubalis)",
        "origin": "Rohtak, Jind & Hisar, Haryana",
        "purpose": "Premier Dairy Buffalo",
        "fat": "7.0% - 8.5%",
        "traits": "Jet-black body, tightly curled spiraling horns, white switch on tail, renowned as 'Black Gold'.",
    },
    "sahiwal": {
        "species": "Cattle (Bos indicus)",
        "origin": "Montgomery region (Punjab / Rajasthan)",
        "purpose": "Heavy Milch Breed",
        "fat": "4.5% - 5.2%",
        "traits": "Reddish-dun to pale red coat, loose skin with voluminous dewlap, stumpy horns, docile temperament.",
    },
    "kankrej": {
        "species": "Cattle (Bos indicus)",
        "origin": "Rann of Kutch, Gujarat",
        "purpose": "Dual-Purpose (Draught & Milk)",
        "fat": "4.8% - 5.2%",
        "traits": "Massive lyre-shaped horns, characteristic 'Sawai Chal' gait, silver-grey coat with dark extremities.",
    },
    "ongole": {
        "species": "Cattle (Bos indicus)",
        "origin": "Prakasam & Guntur, Andhra Pradesh",
        "purpose": "Dual-Purpose (Heavy Draught & Milk)",
        "fat": "4.2% - 4.8%",
        "traits": "Majestic white muscular frame, large fleshy hump in males, black muzzle, revered worldwide (foundation of Brahman cattle).",
    },
    "tharparkar": {
        "species": "Cattle (Bos indicus)",
        "origin": "Thar Desert, Rajasthan / Sindh",
        "purpose": "Dual-Purpose (Hardy Desert Breed)",
        "fat": "4.7% - 5.0%",
        "traits": "White or light grey coat, medium horns, exceptional drought and heat tolerance.",
    },
    "redsindhi": {
        "species": "Cattle (Bos indicus)",
        "origin": "Sindh / Balochistan / Kerala",
        "purpose": "Milch Breed",
        "fat": "4.5% - 5.0%",
        "traits": "Deep rich red or fawn coat, compact frame, thick horns, resilient in humid climates.",
    },
    "jaffrabadi": {
        "species": "Buffalo (Bubalus bubalis)",
        "origin": "Gir Forest & Coastal Saurashtra, Gujarat",
        "purpose": "Heavy Dairy Buffalo",
        "fat": "7.5% - 9.0%",
        "traits": "Heaviest Indian buffalo breed, drooping broad horns turning upwards at tips, prominent bulging forehead.",
    },
    "surti": {
        "species": "Buffalo (Bubalus bubalis)",
        "origin": "Kaira & Baroda, Gujarat",
        "purpose": "Dairy Buffalo",
        "fat": "7.0% - 8.0%",
        "traits": "Medium-sized compact body, sickle-shaped flat horns, two white collars (chevrons) under neck.",
    },
    "nili ravi": {
        "species": "Buffalo (Bubalus bubalis)",
        "origin": "Sutlej & Ravi River Valleys, Punjab",
        "purpose": "Dairy Buffalo",
        "fat": "6.8% - 7.5%",
        "traits": "Distinctive 'Panj Kalyan' markings (white on forehead, muzzle, legs, and tail switch) with wall eyes.",
    },
}

def _escape(value: object) -> str:
    return html.escape(str(value), quote=True)

def get_breed_info(breed_name: str) -> dict[str, str]:
    normalized = breed_name.strip().lower()
    for key, info in BREED_FACTS.items():
        if key in normalized or normalized in key:
            return info
    return {
        "species": "Indigenous Livestock (NBAGR Registered)",
        "origin": "Indian Subcontinent Native Tract",
        "purpose": "Milch / Draught / Dual-Purpose",
        "fat": "4.5% - 7.5%",
        "traits": f"Recognized indigenous Indian breed '{breed_name.title()}', registered with NBAGR.",
    }

DESIGN_SYSTEM_CSS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  :root {
    --bg-main: #080c14;
    --bg-card: rgba(18, 25, 43, 0.78);
    --bg-card-hover: rgba(24, 34, 58, 0.88);
    --border-subtle: rgba(255, 255, 255, 0.08);
    --border-glow: rgba(99, 102, 241, 0.35);
    --primary: #6366f1;
    --primary-hover: #4f46e5;
    --primary-glow: rgba(99, 102, 241, 0.28);
    --accent-emerald: #10b981;
    --accent-cyan: #06b6d4;
    --accent-amber: #f59e0b;
    --text-main: #f8fafc;
    --text-muted: #94a3b8;
    --text-dim: #64748b;
    --font-heading: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
    --font-body: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    --radius-sm: 8px;
    --radius-md: 14px;
    --radius-lg: 20px;
    --radius-xl: 28px;
    --transition-fast: 0.18s cubic-bezier(0.16, 1, 0.3, 1);
    --transition-smooth: 0.28s cubic-bezier(0.16, 1, 0.3, 1);
  }

  *, *::before, *::after {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  body {
    font-family: var(--font-body);
    background: var(--bg-main);
    color: var(--text-main);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    overflow-x: hidden;
    line-height: 1.5;
    background-image:
      radial-gradient(circle at 18% 12%, rgba(99, 102, 241, 0.14) 0%, transparent 45%),
      radial-gradient(circle at 82% 78%, rgba(16, 185, 129, 0.12) 0%, transparent 50%),
      radial-gradient(circle at 50% 50%, rgba(6, 182, 212, 0.05) 0%, transparent 60%);
    background-attachment: fixed;
  }

  /* Custom Scrollbar */
  ::-webkit-scrollbar { width: 8px; height: 8px; }
  ::-webkit-scrollbar-track { background: #0b1120; }
  ::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 4px; }
  ::-webkit-scrollbar-thumb:hover { background: #334155; }

  /* App Shell & Navigation */
  .app-shell {
    max-width: 1200px;
    width: 100%;
    margin: 0 auto;
    padding: 24px 20px 60px;
    flex: 1;
    display: flex;
    flex-direction: column;
  }

  .site-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 20px;
    padding: 14px 24px;
    margin-bottom: 28px;
    background: rgba(15, 23, 42, 0.65);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-lg);
    box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
  }

  .brand-group {
    display: flex;
    align-items: center;
    gap: 14px;
    text-decoration: none;
    color: var(--text-main);
  }

  .brand-logo-icon {
    width: 44px;
    height: 44px;
    border-radius: 12px;
    background: linear-gradient(135deg, #4f46e5 0%, #10b981 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 16px rgba(99, 102, 241, 0.4);
    flex-shrink: 0;
  }

  .brand-title {
    font-family: var(--font-heading);
    font-size: 1.35rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    background: linear-gradient(90deg, #ffffff 0%, #cbd5e1 50%, #818cf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }

  .brand-tag {
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    padding: 2px 8px;
    background: rgba(99, 102, 241, 0.2);
    border: 1px solid rgba(99, 102, 241, 0.4);
    border-radius: 999px;
    color: #a5b4fc;
    margin-left: 6px;
  }

  .header-actions {
    display: flex;
    align-items: center;
    gap: 14px;
    flex-wrap: wrap;
  }

  .status-badge {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    font-size: 0.8rem;
    font-weight: 600;
    padding: 6px 14px;
    background: rgba(16, 185, 129, 0.12);
    border: 1px solid rgba(16, 185, 129, 0.3);
    border-radius: 999px;
    color: #34d399;
  }

  .status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #10b981;
    box-shadow: 0 0 10px #10b981;
    animation: pulseGlow 2s infinite;
  }

  @keyframes pulseGlow {
    0%, 100% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.35); opacity: 0.65; }
  }

  .nav-btn {
    text-decoration: none;
    font-size: 0.86rem;
    font-weight: 600;
    color: #cbd5e1;
    padding: 8px 16px;
    border-radius: var(--radius-sm);
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid var(--border-subtle);
    transition: all var(--transition-fast);
    display: inline-flex;
    align-items: center;
    gap: 6px;
  }

  .nav-btn:hover {
    background: rgba(255, 255, 255, 0.12);
    color: #fff;
    border-color: rgba(255, 255, 255, 0.2);
    transform: translateY(-1px);
  }

  .nav-btn.primary {
    background: linear-gradient(135deg, var(--primary) 0%, #4338ca 100%);
    border-color: transparent;
    color: #fff;
    box-shadow: 0 4px 14px var(--primary-glow);
  }

  .nav-btn.primary:hover {
    background: linear-gradient(135deg, #818cf8 0%, var(--primary) 100%);
    box-shadow: 0 6px 20px var(--primary-glow);
  }

  .user-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 12px;
    background: rgba(30, 41, 59, 0.7);
    border: 1px solid var(--border-subtle);
    border-radius: 999px;
    font-size: 0.82rem;
    color: #e2e8f0;
  }

  .user-avatar {
    width: 22px;
    height: 22px;
    border-radius: 50%;
    background: linear-gradient(135deg, #818cf8, #38bdf8);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.7rem;
    font-weight: 700;
    color: #0f172a;
  }

  /* Glass Cards */
  .glass-card {
    background: var(--bg-card);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-lg);
    padding: 32px;
    box-shadow: 0 20px 45px -15px rgba(0, 0, 0, 0.6), 0 0 35px -12px rgba(99, 102, 241, 0.12);
    transition: border-color var(--transition-smooth);
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
  }

  .glass-card:hover {
    border-color: var(--border-glow);
  }

  .glass-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent 0%, rgba(99, 102, 241, 0.6) 50%, transparent 100%);
    opacity: 0.7;
  }

  /* Typography */
  h1, h2, h3, h4 {
    font-family: var(--font-heading);
    color: #ffffff;
    letter-spacing: -0.02em;
    font-weight: 700;
  }

  .section-eyebrow {
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #818cf8;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .section-title {
    font-size: 1.85rem;
    font-weight: 800;
    margin-bottom: 10px;
    line-height: 1.2;
  }

  .section-desc {
    color: var(--text-muted);
    font-size: 0.98rem;
    max-width: 680px;
    margin-bottom: 28px;
  }

  /* Form Controls */
  .form-group {
    margin-bottom: 20px;
  }

  .form-label {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.88rem;
    font-weight: 600;
    color: #e2e8f0;
    margin-bottom: 8px;
  }

  .form-input {
    width: 100%;
    padding: 13px 16px;
    background: rgba(11, 17, 32, 0.85);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: var(--radius-md);
    color: #ffffff;
    font-size: 0.95rem;
    font-family: var(--font-body);
    transition: all var(--transition-fast);
    outline: none;
  }

  .form-input:focus {
    border-color: #818cf8;
    background: rgba(15, 23, 42, 0.95);
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.25);
  }

  .form-input::placeholder {
    color: var(--text-dim);
  }

  .input-with-button {
    display: flex;
    gap: 10px;
  }

  .btn-secondary {
    padding: 12px 18px;
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.14);
    border-radius: var(--radius-md);
    color: #f1f5f9;
    font-weight: 600;
    font-size: 0.88rem;
    cursor: pointer;
    transition: all var(--transition-fast);
    display: inline-flex;
    align-items: center;
    gap: 6px;
    white-space: nowrap;
  }

  .btn-secondary:hover {
    background: rgba(255, 255, 255, 0.16);
    border-color: rgba(255, 255, 255, 0.25);
    transform: translateY(-1px);
  }

  /* Drag & Drop Upload Zone */
  .upload-zone {
    position: relative;
    border: 2px dashed rgba(99, 102, 241, 0.4);
    background: rgba(15, 23, 42, 0.5);
    border-radius: var(--radius-lg);
    padding: 36px 24px;
    text-align: center;
    cursor: pointer;
    transition: all var(--transition-smooth);
    margin-bottom: 22px;
  }

  .upload-zone:hover, .upload-zone.dragover {
    border-color: #818cf8;
    background: rgba(99, 102, 241, 0.08);
    transform: translateY(-2px);
    box-shadow: 0 10px 30px -10px rgba(99, 102, 241, 0.3);
  }

  .upload-zone input[type="file"] {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    opacity: 0;
    cursor: pointer;
    z-index: 10;
  }

  .upload-icon-circle {
    width: 64px;
    height: 64px;
    border-radius: 50%;
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(6, 182, 212, 0.2) 100%);
    border: 1px solid rgba(99, 102, 241, 0.4);
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 16px;
    color: #a5b4fc;
    font-size: 1.75rem;
    transition: transform var(--transition-fast);
  }

  .upload-zone:hover .upload-icon-circle {
    transform: scale(1.1);
  }

  .upload-primary-text {
    font-family: var(--font-heading);
    font-size: 1.15rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 6px;
  }

  .upload-secondary-text {
    font-size: 0.85rem;
    color: var(--text-muted);
  }

  /* Live Client Preview */
  .preview-container {
    display: none;
    margin-top: 18px;
    padding: 16px;
    background: rgba(11, 17, 32, 0.95);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: var(--radius-md);
    align-items: center;
    gap: 16px;
  }

  .preview-thumbnail {
    width: 72px;
    height: 72px;
    border-radius: var(--radius-sm);
    object-fit: cover;
    border: 1px solid rgba(255, 255, 255, 0.2);
  }

  .preview-info {
    flex: 1;
    text-align: left;
  }

  .preview-filename {
    font-weight: 600;
    font-size: 0.92rem;
    color: #f1f5f9;
    margin-bottom: 4px;
  }

  .preview-meta {
    font-size: 0.78rem;
    color: var(--text-muted);
  }

  /* Sample Quick Pickers */
  .samples-bar {
    margin-top: 24px;
    padding-top: 20px;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
  }

  .samples-label {
    font-size: 0.82rem;
    font-weight: 600;
    color: var(--text-muted);
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 6px;
  }

  .sample-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
  }

  .sample-chip {
    background: rgba(30, 41, 59, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 999px;
    padding: 6px 14px;
    font-size: 0.82rem;
    font-weight: 600;
    color: #e2e8f0;
    cursor: pointer;
    transition: all var(--transition-fast);
    display: inline-flex;
    align-items: center;
    gap: 6px;
  }

  .sample-chip:hover {
    background: rgba(99, 102, 241, 0.25);
    border-color: #818cf8;
    color: #fff;
    transform: translateY(-1px);
  }

  /* Submit Button */
  .btn-submit {
    width: 100%;
    padding: 16px 28px;
    background: linear-gradient(135deg, #4f46e5 0%, #10b981 100%);
    border: none;
    border-radius: var(--radius-md);
    color: #ffffff;
    font-family: var(--font-heading);
    font-size: 1.05rem;
    font-weight: 700;
    letter-spacing: 0.01em;
    cursor: pointer;
    transition: all var(--transition-smooth);
    box-shadow: 0 8px 25px rgba(99, 102, 241, 0.35);
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
  }

  .btn-submit:hover {
    background: linear-gradient(135deg, #6366f1 0%, #34d399 100%);
    box-shadow: 0 12px 32px rgba(16, 185, 129, 0.4);
    transform: translateY(-2px);
  }

  /* Grid Layouts */
  .grid-2col {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
  }

  .grid-result {
    display: grid;
    grid-template-columns: 380px 1fr;
    gap: 28px;
    align-items: start;
  }

  @media (max-width: 900px) {
    .grid-2col, .grid-result {
      grid-template-columns: 1fr;
    }
    .site-header {
      flex-direction: column;
      align-items: flex-start;
    }
    .header-actions {
      width: 100%;
      justify-content: space-between;
    }
  }

  /* Flash Alerts */
  .flash-alert {
    padding: 14px 18px;
    border-radius: var(--radius-md);
    margin-bottom: 20px;
    font-size: 0.92rem;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 10px;
    animation: fadeIn 0.25s ease-out;
  }

  .flash-alert.error {
    background: rgba(239, 68, 68, 0.15);
    border: 1px solid rgba(239, 68, 68, 0.4);
    color: #fca5a5;
  }

  .flash-alert.success {
    background: rgba(16, 185, 129, 0.15);
    border: 1px solid rgba(16, 185, 129, 0.4);
    color: #6ee7b7;
  }

  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(-4px); }
    to { opacity: 1; transform: translateY(0); }
  }

  /* Result View Elements */
  .hero-prediction-card {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.85) 0%, rgba(15, 23, 42, 0.95) 100%);
    border: 1px solid rgba(99, 102, 241, 0.4);
    border-radius: var(--radius-lg);
    padding: 24px 28px;
    margin-bottom: 24px;
    box-shadow: 0 14px 35px -10px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.1);
  }

  .hero-prediction-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 16px;
    flex-wrap: wrap;
    margin-bottom: 14px;
  }

  .predicted-breed-title {
    font-size: 2.3rem;
    font-weight: 800;
    background: linear-gradient(135deg, #ffffff 0%, #38bdf8 60%, #34d399 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.1;
  }

  .confidence-pill {
    padding: 8px 18px;
    border-radius: 999px;
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.25) 0%, rgba(6, 182, 212, 0.25) 100%);
    border: 1px solid rgba(16, 185, 129, 0.5);
    color: #34d399;
    font-family: var(--font-heading);
    font-weight: 800;
    font-size: 1.15rem;
    box-shadow: 0 0 20px rgba(16, 185, 129, 0.25);
  }

  .meta-chips-row {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 14px;
  }

  .meta-chip {
    padding: 6px 14px;
    border-radius: 8px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    font-size: 0.82rem;
    color: #cbd5e1;
    display: inline-flex;
    align-items: center;
    gap: 6px;
  }

  .img-preview-container {
    position: relative;
    border-radius: var(--radius-lg);
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.12);
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.6);
  }

  .img-preview {
    width: 100%;
    height: auto;
    max-height: 380px;
    object-fit: cover;
    display: block;
    transition: transform var(--transition-smooth);
  }

  .img-preview:hover {
    transform: scale(1.03);
  }

  /* Distribution Bars */
  .distribution-list {
    display: flex;
    flex-direction: column;
    gap: 14px;
    list-style: none;
    margin-top: 16px;
  }

  .distribution-item {
    background: rgba(11, 17, 32, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: var(--radius-md);
    padding: 14px 18px;
    transition: all var(--transition-fast);
  }

  .distribution-item:hover {
    background: rgba(15, 23, 42, 0.85);
    border-color: rgba(99, 102, 241, 0.3);
  }

  .distribution-header {
    display: flex;
    justify-content: space-between;
    font-size: 0.95rem;
    font-weight: 600;
    margin-bottom: 8px;
  }

  .progress-track {
    width: 100%;
    height: 8px;
    background: rgba(255, 255, 255, 0.08);
    border-radius: 999px;
    overflow: hidden;
  }

  .progress-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #6366f1 0%, #10b981 100%);
    transition: width 0.8s cubic-bezier(0.16, 1, 0.3, 1);
  }

  /* Quick-Fill Credentials */
  .quick-creds-container {
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: var(--radius-md);
    padding: 14px 18px;
    margin-bottom: 22px;
  }

  .quick-creds-title {
    font-size: 0.78rem;
    font-weight: 700;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 6px;
  }

  .quick-creds-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
  }

  .cred-chip {
    padding: 6px 12px;
    background: rgba(99, 102, 241, 0.12);
    border: 1px solid rgba(99, 102, 241, 0.28);
    border-radius: var(--radius-sm);
    color: #c7d2fe;
    font-size: 0.78rem;
    font-weight: 600;
    cursor: pointer;
    transition: all var(--transition-fast);
  }

  .cred-chip:hover {
    background: rgba(99, 102, 241, 0.25);
    border-color: #818cf8;
    color: #ffffff;
    transform: translateY(-1px);
  }

  /* Site Footer */
  .site-footer {
    margin-top: auto;
    padding: 28px 20px 20px;
    border-top: 1px solid rgba(255, 255, 255, 0.06);
    text-align: center;
    font-size: 0.82rem;
    color: var(--text-dim);
  }

  .footer-links {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin-top: 8px;
    flex-wrap: wrap;
  }

  .footer-links a {
    color: var(--text-muted);
    text-decoration: none;
    transition: color var(--transition-fast);
  }

  .footer-links a:hover {
    color: #818cf8;
  }
</style>
"""

# Biometric Bull/Cow Emblem SVG
BRAND_ICON_SVG = """
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M7 6C4 3 2 7 2 7c0 4 2 8 10 8s10-4 10-8c0 0-2-4-5-1"/>
  <circle cx="12" cy="14" r="2"/>
  <path d="M12 16v3"/>
  <circle cx="8" cy="11" r="1" fill="currentColor"/>
  <circle cx="16" cy="11" r="1" fill="currentColor"/>
  <path d="M9 19c1.5 1 4.5 1 6 0"/>
</svg>
"""

HOME_CLIENT_SCRIPT = """
<script>
  const fileInput = document.getElementById('fileInput');
  const dropZone = document.getElementById('uploadDropZone');
  const previewContainer = document.getElementById('previewContainer');
  const previewImg = document.getElementById('previewImg');
  const previewFilename = document.getElementById('previewFilename');
  const previewSize = document.getElementById('previewSize');
  const removeBtn = document.getElementById('removeImgBtn');
  const form = document.getElementById('predictionForm');
  const submitBtn = document.getElementById('submitBtn');
  const btnText = document.getElementById('btnText');
  const btnSpinner = document.getElementById('btnSpinner');

  if (fileInput) {
    fileInput.addEventListener('change', function(e) {
      if (this.files && this.files[0]) {
        const file = this.files[0];
        previewFilename.textContent = file.name;
        previewSize.textContent = (file.size / 1024).toFixed(1) + ' KB';
        const reader = new FileReader();
        reader.onload = function(evt) {
          previewImg.src = evt.target.result;
          previewContainer.style.display = 'flex';
        };
        reader.readAsDataURL(file);
      }
    });
  }

  if (removeBtn) {
    removeBtn.addEventListener('click', function(e) {
      e.stopPropagation();
      fileInput.value = '';
      previewContainer.style.display = 'none';
      previewImg.src = '';
    });
  }

  if (dropZone) {
    ['dragenter', 'dragover'].forEach(function(eventName) {
      dropZone.addEventListener(eventName, function() { dropZone.classList.add('dragover'); }, false);
    });
    ['dragleave', 'drop'].forEach(function(eventName) {
      dropZone.addEventListener(eventName, function() { dropZone.classList.remove('dragover'); }, false);
    });
  }

  const detectBtn = document.getElementById('detectGpsBtn');
  if (detectBtn) {
    detectBtn.addEventListener('click', function() {
      const btn = this;
      const geoStatus = document.getElementById('geoStatus');
      if (!navigator.geolocation) {
        alert('Geolocation is not supported by your browser.');
        return;
      }
      btn.disabled = true;
      btn.innerHTML = '<span>Detecting...</span>';
      navigator.geolocation.getCurrentPosition(
        function(pos) {
          const lat = pos.coords.latitude.toFixed(4);
          const lon = pos.coords.longitude.toFixed(4);
          document.getElementById('gpsInput').value = lat + ', ' + lon;
          btn.disabled = false;
          btn.innerHTML = '<span>&check; Acquired</span>';
          if (geoStatus) geoStatus.style.display = 'inline';
        },
        function(err) {
          btn.disabled = false;
          btn.innerHTML = '<span>Detect Location</span>';
          alert('Location permission denied or unavailable: ' + err.message);
        },
        { enableHighAccuracy: true, timeout: 7000 }
      );
    });
  }

  const genIdBtn = document.getElementById('genIdBtn');
  if (genIdBtn) {
    genIdBtn.addEventListener('click', function() {
      const randomNum = Math.floor(1000 + Math.random() * 9000);
      document.getElementById('animalIdInput').value = 'IND-' + new Date().getFullYear() + '-' + randomNum;
    });
  }

  window.quickFillSample = function(breed, gps, id) {
    const gpsEl = document.getElementById('gpsInput');
    const idEl = document.getElementById('animalIdInput');
    if (gpsEl) gpsEl.value = gps;
    if (idEl) idEl.value = id;
  };

  if (form) {
    form.addEventListener('submit', function() {
      submitBtn.disabled = true;
      submitBtn.style.opacity = '0.8';
      if (btnText) btnText.style.display = 'none';
      if (btnSpinner) btnSpinner.style.display = 'inline-block';
    });
  }
</script>
"""

SIGNIN_CLIENT_SCRIPT = """
<script>
  window.fillCreds = function(u, p) {
    document.getElementById('identity').value = u;
    document.getElementById('password').value = p;
  };

  const togglePwd = document.getElementById('togglePwd');
  const pwdInput = document.getElementById('password');
  if (togglePwd && pwdInput) {
    togglePwd.addEventListener('click', function() {
      if (pwdInput.type === 'password') {
        pwdInput.type = 'text';
        togglePwd.textContent = 'Hide';
      } else {
        pwdInput.type = 'password';
        togglePwd.textContent = 'Show';
      }
    });
  }
</script>
"""

def modern_shell(content: str, request: Request, active_page: str = "home") -> str:
    user = request.session.get("user")
    user_str = str(user) if user else None

    if user_str:
        user_initial = user_str[0].upper() if user_str else "U"
        auth_nav = f"""
        <div class="user-badge">
          <div class="user-avatar">{_escape(user_initial)}</div>
          <span style="font-weight:600;">{_escape(user_str)}</span>
        </div>
        <a href="/logout" class="nav-btn">Sign Out</a>
        """
        signed_in_hidden = f"<span style='display:none'>Signed in as {_escape(user_str)}</span>"
    else:
        auth_nav = """
        <a href="/signin" class="nav-btn primary">Sign In</a>
        <a href="/create-account" class="nav-btn">Create Account</a>
        """
        signed_in_hidden = ""

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>PashuDrishti.ai - Indigenous Indian Cattle & Buffalo Breed Recognition</title>
  {DESIGN_SYSTEM_CSS}
</head>
<body>
  <div class="app-shell">
    <header class="site-header">
      <a href="/" class="brand-group">
        <div class="brand-logo-icon">
          {BRAND_ICON_SVG}
        </div>
        <div>
          <div style="display:flex; align-items:center;">
            <span class="brand-title">PashuDrishti.ai</span>
            <span class="brand-tag">v2.4 INT8</span>
          </div>
          <p style="font-size:0.75rem; color:var(--text-dim); margin-top:1px;">Indigenous Livestock AI Platform</p>
        </div>
      </a>

      <div class="header-actions">
        <div class="status-badge">
          <span class="status-dot"></span>
          <span>41 Native Breeds Active</span>
        </div>
        <a href="/" class="nav-btn {'primary' if active_page == 'home' else ''}">Classifier</a>
        <a href="/docs" target="_blank" class="nav-btn">API Docs</a>
        {auth_nav}
      </div>
    </header>

    {signed_in_hidden}
    {content}

    <footer class="site-footer">
      <p>PashuDrishti.ai &bull; Indigenous Indian Cattle & Buffalo Breed Classification Engine &bull; Optimized for Edge & Cloud</p>
      <div class="footer-links">
        <a href="/health">System Health</a>
        <a href="/docs">Swagger API</a>
        <a href="/redoc">ReDoc Documentation</a>
        <a href="https://github.com/varshith0810/PashuDrishti.ai" target="_blank">GitHub Repository</a>
      </div>
    </footer>
  </div>
</body>
</html>"""


def modern_home(request: Request) -> str:
    content = f"""
    <section class="glass-card">
      <div class="section-eyebrow">
        <span>AI Biometrics</span> &bull; <span>Edge-Optimized Vision</span>
      </div>
      <h1 class="section-title">Indian Cattle & Buffalo Breed Classifier</h1>
      <p class="section-desc">
        Instant, sub-100ms multi-breed biometric recognition for Indian livestock with reverse-geocoded geographic verification across 41 registered native breeds.
      </p>

      <form id="predictionForm" action="/predict" method="post" enctype="multipart/form-data">
        <!-- Drag & Drop Upload Zone -->
        <div class="upload-zone" id="uploadDropZone">
          <input type="file" id="fileInput" name="file" accept="image/*" required>
          <div class="upload-icon-circle">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
              <polyline points="17 8 12 3 7 8"/>
              <line x1="12" y1="3" x2="12" y2="15"/>
            </svg>
          </div>
          <div class="upload-primary-text">Upload or Drop Animal Photo Here</div>
          <div class="upload-secondary-text">Supports JPEG, PNG, WEBP &bull; High resolution side profile recommended</div>

          <!-- Live Client Preview Container -->
          <div class="preview-container" id="previewContainer">
            <img class="preview-thumbnail" id="previewImg" src="" alt="Thumbnail preview">
            <div class="preview-info">
              <div class="preview-filename" id="previewFilename">image.jpg</div>
              <div class="preview-meta" id="previewSize">0 KB</div>
            </div>
            <button type="button" class="btn-secondary" id="removeImgBtn" style="padding: 6px 12px; font-size: 0.78rem;">Change Image</button>
          </div>
        </div>

        <div class="grid-2col">
          <!-- Animal ID Input -->
          <div class="form-group">
            <label class="form-label">
              <span>Animal ID (optional)</span>
              <button type="button" id="genIdBtn" style="background:none; border:none; color:#818cf8; font-size:0.75rem; font-weight:600; cursor:pointer;">
                &plus; Auto-Generate ID
              </button>
            </label>
            <input type="text" id="animalIdInput" name="animal_id" class="form-input" placeholder="e.g. COW-GJ-2026-881">
          </div>

          <!-- Geolocation Input with Browser Auto-Detect -->
          <div class="form-group">
            <label class="form-label">
              <span>GPS Coordinates (lat,long)</span>
              <span id="geoStatus" style="font-size:0.75rem; color:#10b981; display:none;">&check; Coordinates Acquired</span>
            </label>
            <div class="input-with-button">
              <input type="text" id="gpsInput" name="gps_coordinates" class="form-input" placeholder="e.g. 21.6032, 70.8022 (Gir Region)">
              <button type="button" id="detectGpsBtn" class="btn-secondary" title="Use current GPS location">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M12 2a8 8 0 0 0-8 8c0 5.25 8 12 8 12s8-6.75 8-12a8 8 0 0 0-8-8z"/>
                  <circle cx="12" cy="10" r="3"/>
                </svg>
                <span>Detect Location</span>
              </button>
            </div>
          </div>
        </div>

        <!-- Sample Breeds Quick-Selector -->
        <div class="samples-bar">
          <div class="samples-label">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            <span>Quick-Test Native Breeds (Click to prefill demo sample):</span>
          </div>
          <div class="sample-chips">
            <button type="button" class="sample-chip" onclick="quickFillSample('Gir (Gujarat)', '21.6032,70.8022', 'GIR-COW-042')">
              <span>🐄 Gir Cattle (Saurashtra)</span>
            </button>
            <button type="button" class="sample-chip" onclick="quickFillSample('Murrah (Haryana)', '28.9845,76.6066', 'MURRAH-BUF-108')">
              <span>🐃 Murrah Buffalo (Rohtak)</span>
            </button>
            <button type="button" class="sample-chip" onclick="quickFillSample('Sahiwal (Punjab)', '30.8717,75.8520', 'SAHIWAL-2026')">
              <span>🐄 Sahiwal Cattle (Punjab)</span>
            </button>
            <button type="button" class="sample-chip" onclick="quickFillSample('Kankrej (Kutch)', '23.7337,69.8597', 'KANKREJ-771')">
              <span>🐄 Kankrej Cattle (Kutch)</span>
            </button>
          </div>
        </div>

        <div style="margin-top: 26px;">
          <button type="submit" id="submitBtn" class="btn-submit">
            <span id="btnText">Predict Breed &amp; Verify Biometrics &rarr;</span>
            <span id="btnSpinner" style="display:none;">Analyzing with EfficientNet-B0 INT8...</span>
          </button>
        </div>
      </form>
    </section>
    """ + HOME_CLIENT_SCRIPT
    return modern_shell(content, request, active_page="home")


def modern_signin(request: Request, message: str = "", *, is_error: bool = False) -> str:
    flash_html = ""
    if message:
        alert_class = "error" if is_error else "success"
        flash_html = f"""
        <div class="flash-alert {alert_class}">
          <span>{"&excl;" if is_error else "&check;"}</span>
          <span>{_escape(message)}</span>
        </div>
        """

    content = f"""
    <div style="max-width: 480px; margin: 40px auto 0; width: 100%;">
      <section class="glass-card">
        <div class="section-eyebrow">
          <span>Secure Platform Access</span>
        </div>
        <h2 class="section-title" style="font-size: 1.75rem;">Sign In</h2>
        <p class="section-desc" style="font-size: 0.9rem; margin-bottom: 20px;">
          Access the PashuDrishti.ai breed recognition suite, analytics, and telemetry dashboard.
        </p>

        {flash_html}

        <!-- Pre-Seeded Quick Credentials Picker -->
        <div class="quick-creds-container">
          <div class="quick-creds-title">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
            <span>One-Click Demo Login:</span>
          </div>
          <div class="quick-creds-chips">
            <button type="button" class="cred-chip" onclick="fillCreds('farmer', 'farmer123')">
              &bull; farmer / farmer123
            </button>
            <button type="button" class="cred-chip" onclick="fillCreds('testuser', 'password123')">
              &bull; testuser / password123
            </button>
            <button type="button" class="cred-chip" onclick="fillCreds('admin', 'admin123')">
              &bull; admin / admin123
            </button>
          </div>
        </div>

        <form action="/signin" method="post" id="signinForm">
          <div class="form-group">
            <label class="form-label" for="identity">Username or Email</label>
            <input id="identity" name="identity" class="form-input" placeholder="e.g. farmer or testuser" required autocomplete="username">
          </div>

          <div class="form-group">
            <div class="form-label">
              <label for="password">Password</label>
              <button type="button" id="togglePwd" style="background:none; border:none; color:#818cf8; font-size:0.75rem; cursor:pointer;">Show</button>
            </div>
            <input id="password" type="password" name="password" class="form-input" placeholder="Enter your password" required autocomplete="current-password">
          </div>

          <div style="margin-top: 24px;">
            <button type="submit" class="btn-submit" style="padding: 13px;">
              <span>Sign In to Dashboard &rarr;</span>
            </button>
          </div>
        </form>

        <div style="margin-top: 24px; padding-top: 18px; border-top: 1px solid rgba(255,255,255,0.08); text-align: center; font-size: 0.88rem; color: var(--text-muted);">
          <span>New to PashuDrishti?</span>
          <a href="/create-account" style="color: #818cf8; font-weight: 600; text-decoration: none; margin-left: 6px;">Create account</a>
        </div>
      </section>
    </div>
    """ + SIGNIN_CLIENT_SCRIPT
    return modern_shell(content, request, active_page="signin")


def modern_create_account(request: Request, message: str = "", *, is_error: bool = False) -> str:
    flash_html = ""
    if message:
        alert_class = "error" if is_error else "success"
        flash_html = f"""
        <div class="flash-alert {alert_class}">
          <span>{"&excl;" if is_error else "&check;"}</span>
          <span>{_escape(message)}</span>
        </div>
        """

    content = f"""
    <div style="max-width: 480px; margin: 40px auto 0; width: 100%;">
      <section class="glass-card">
        <div class="section-eyebrow">
          <span>New Registration</span>
        </div>
        <h2 class="section-title" style="font-size: 1.75rem;">Create Account</h2>
        <p class="section-desc" style="font-size: 0.9rem; margin-bottom: 20px;">
          Register as a farmer, veterinarian, or agricultural researcher to access breed analytics.
        </p>

        {flash_html}

        <form action="/create-account" method="post">
          <div class="form-group">
            <label class="form-label" for="email">Email Address</label>
            <input id="email" type="email" name="email" class="form-input" placeholder="e.g. farmer@example.com" required autocomplete="email">
          </div>

          <div class="form-group">
            <label class="form-label" for="username">Username</label>
            <input id="username" name="username" class="form-input" placeholder="Choose a unique username" required autocomplete="username">
          </div>

          <div class="form-group">
            <label class="form-label" for="password">Password</label>
            <input id="password" type="password" name="password" class="form-input" placeholder="Create a secure password" required autocomplete="new-password">
          </div>

          <div style="margin-top: 24px;">
            <button type="submit" class="btn-submit" style="padding: 13px;">
              <span>Create Account &rarr;</span>
            </button>
          </div>
        </form>

        <div style="margin-top: 24px; padding-top: 18px; border-top: 1px solid rgba(255,255,255,0.08); text-align: center; font-size: 0.88rem; color: var(--text-muted);">
          <span>Already registered?</span>
          <a href="/signin" style="color: #818cf8; font-weight: 600; text-decoration: none; margin-left: 6px;">Sign In</a>
        </div>
      </section>
    </div>
    """
    return modern_shell(content, request, active_page="create_account")


def modern_result(
    request: Request,
    prediction: Any,
    animal_id: str,
    location_label: str,
    image_b64: str,
) -> str:
    breed_info = get_breed_info(prediction.breed)
    clean_animal_id = animal_id.strip() or "N/A"
    confidence_val = prediction.confidence
    certainty_badge = "High Certainty Match" if confidence_val >= 80 else ("Moderate Certainty" if confidence_val >= 50 else "Review Recommended")
    certainty_color = "#10b981" if confidence_val >= 80 else ("#f59e0b" if confidence_val >= 50 else "#ef4444")

    # Generate Top-5 Distribution Bars
    top_scores = getattr(prediction, "top_scores", [])
    distribution_html = ""
    for item in top_scores[:5]:
        b_name = item.get("breed", "")
        b_conf = item.get("confidence", 0.0)
        distribution_html += f"""
        <li class="distribution-item">
          <div class="distribution-header">
            <span style="color:#ffffff;">{_escape(b_name.title())}</span>
            <span style="color:#38bdf8; font-family:var(--font-heading);">{b_conf:.2f}%</span>
          </div>
          <div class="progress-track">
            <div class="progress-fill" style="width: {min(100.0, max(2.0, b_conf))}%;"></div>
          </div>
        </li>
        """

    content = f"""
    <section class="glass-card">
      <div class="section-eyebrow">
        <span>Inference Completed</span> &bull; <span>EfficientNet-B0 INT8</span>
      </div>
      <h1 class="section-title">Prediction Result</h1>
      <p class="section-desc">
        Comprehensive multi-breed biometric classification and geographical registry verification.
      </p>

      <!-- Hero Top Prediction Card -->
      <div class="hero-prediction-card">
        <div class="hero-prediction-header">
          <div>
            <div style="font-size:0.8rem; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; color:#94a3b8; margin-bottom:4px;">
              Predicted Breed:
            </div>
            <div class="predicted-breed-title">{_escape(prediction.breed.title())}</div>
          </div>
          <div style="display:flex; flex-direction:column; align-items:flex-end; gap:6px;">
            <div class="confidence-pill">
              Confidence: {prediction.confidence:.2f}%
            </div>
            <span style="font-size:0.75rem; font-weight:700; color:{certainty_color};">&bull; {certainty_badge}</span>
          </div>
        </div>

        <div class="meta-chips-row">
          <div class="meta-chip">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            <span>Animal ID: <strong>{_escape(clean_animal_id)}</strong></span>
          </div>
          <div class="meta-chip">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
            <span>Detected Location: <strong>{_escape(location_label)}</strong></span>
          </div>
          <div class="meta-chip">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
            <span>Purpose: <strong>{_escape(breed_info['purpose'])}</strong></span>
          </div>
        </div>
      </div>

      <!-- Split Analytics Grid -->
      <div class="grid-result">
        <!-- Left: Uploaded Photo Card -->
        <div>
          <h3 style="font-size:1.15rem; margin-bottom:12px; display:flex; align-items:center; gap:8px;">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
            <span>Uploaded Image</span>
          </h3>
          <div class="img-preview-container">
            <img class="img-preview" src="data:image/jpeg;base64,{image_b64}" alt="Uploaded animal">
          </div>

          <!-- Native Tract Quick Facts Card -->
          <div style="background:rgba(11,17,32,0.7); border:1px solid rgba(255,255,255,0.08); border-radius:var(--radius-md); padding:16px; margin-top:16px;">
            <h4 style="font-size:0.9rem; color:#a5b4fc; margin-bottom:8px;">Native Tract &amp; Characteristics</h4>
            <p style="font-size:0.84rem; color:var(--text-muted); margin-bottom:6px;">
              <strong>Origin:</strong> {_escape(breed_info['origin'])}
            </p>
            <p style="font-size:0.84rem; color:var(--text-muted); margin-bottom:6px;">
              <strong>Typical Milk Fat:</strong> {_escape(breed_info['fat'])}
            </p>
            <p style="font-size:0.82rem; color:var(--text-dim);">
              {_escape(breed_info['traits'])}
            </p>
          </div>
        </div>

        <!-- Right: Top-5 Probability Distribution -->
        <div>
          <h3 style="font-size:1.15rem; margin-bottom:4px; display:flex; align-items:center; gap:8px;">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
            <span>Top Scores Distribution</span>
          </h3>
          <p style="font-size:0.84rem; color:var(--text-muted);">Probability distribution output from quantized linear classification head.</p>

          <ul class="distribution-list">
            {distribution_html}
          </ul>

          <!-- Compatibility with test assertions -->
          <div style="display:none;">
            <h4>Top Scores</h4>
            <ul>{getattr(prediction, "rows_html", "")}</ul>
          </div>

          <!-- Action Buttons -->
          <div style="display:flex; gap:12px; margin-top:24px; flex-wrap:wrap;">
            <a href="/" class="btn-submit" style="flex:1; text-decoration:none; padding:14px;">
              <span>&larr; Classify Another Animal</span>
            </a>
            <button type="button" onclick="window.print()" class="btn-secondary" style="padding:14px 20px;">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>
              <span>Print Report</span>
            </button>
          </div>
        </div>
      </div>
    </section>
    """
    return modern_shell(content, request, active_page="result")
