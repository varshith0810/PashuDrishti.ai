import asyncio
from io import BytesIO
from pathlib import Path
import time
import httpx
from PIL import Image

BASE_URL = "http://localhost:8000"
TEST_IMAGES_DIR = Path(__file__).resolve().parent / "test_images"

async def run_all_tests():
    print("=" * 70)
    print(" PashuDrishti.ai - Comprehensive API & Prediction Test Suite")
    print(f" Target: {BASE_URL}")
    print("=" * 70)

    # 1. Health Check
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=15.0) as client:
        print("\n--- [1] Testing /health ---")
        r = await client.get("/health")
        assert r.status_code == 200, f"Health check failed with {r.status_code}: {r.text}"
        data = r.json()
        print(f"Status: {r.status_code}, Response: {data}")
        assert data.get("status") == "ok", "Expected status == ok"
        assert data.get("model_loaded") is True, "Expected model_loaded == True"
        print("  -> /health PASSED")

    # 2. Diagnostic bundle endpoint (default disabled)
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=10.0) as client:
        print("\n--- [2] Testing /debug/bundle (default security check) ---")
        r = await client.get("/debug/bundle")
        print(f"Status: {r.status_code} (Expected 403 when DEBUG_BUNDLE is disabled)")
        assert r.status_code == 403, f"Expected 403, got {r.status_code}"
        print("  -> /debug/bundle security check PASSED")

    # 3. Unauthenticated Home redirect
    async with httpx.AsyncClient(base_url=BASE_URL, follow_redirects=False, timeout=10.0) as client:
        print("\n--- [3] Testing Unauthenticated / Access ---")
        r = await client.get("/")
        print(f"Status: {r.status_code} (Expected 303 Redirect to /signin)")
        assert r.status_code == 303, f"Expected 303, got {r.status_code}"
        assert r.headers.get("location") == "/signin"
        print("  -> Unauthenticated home redirect PASSED")

    # 4. Auth Pages (GET /signin, GET /create-account)
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=10.0) as client:
        print("\n--- [4] Testing Auth Pages Rendering ---")
        r_signin = await client.get("/signin")
        assert r_signin.status_code == 200 and "Sign In" in r_signin.text
        print("  -> GET /signin: 200 OK")

        r_create = await client.get("/create-account")
        assert r_create.status_code == 200 and "Create Account" in r_create.text
        print("  -> GET /create-account: 200 OK")

    # 5. Account Registration Tests (Validation, Success, Duplicate)
    test_username = f"farmer_{int(time.time())}"
    test_password = "SecurePassword456"
    test_email = f"{test_username}@example.com"

    async with httpx.AsyncClient(base_url=BASE_URL, timeout=10.0) as client:
        print("\n--- [5] Testing /create-account ---")
        # Empty fields
        r_empty = await client.post(
            "/create-account",
            data={"email": "", "username": "", "password": ""},
            headers={"Accept": "application/json"},
        )
        assert r_empty.status_code == 400, f"Expected 400 for empty fields, got {r_empty.status_code}"
        print(f"  -> Empty input validation: {r_empty.status_code} (Properly Rejected)")

        # Valid registration
        r_create = await client.post(
            "/create-account",
            data={"email": test_email, "username": test_username, "password": test_password},
            headers={"Accept": "application/json"},
        )
        assert r_create.status_code == 201, f"Expected 201, got {r_create.status_code}: {r_create.text}"
        print(f"  -> Valid registration for '{test_username}': {r_create.status_code} Created")

        # Duplicate registration
        r_dup = await client.post(
            "/create-account",
            data={"email": test_email, "username": test_username, "password": test_password},
            headers={"Accept": "application/json"},
        )
        assert r_dup.status_code == 400, f"Expected 400 for duplicate user, got {r_dup.status_code}"
        print(f"  -> Duplicate registration handling: {r_dup.status_code} (Properly Prevented)")

    # 6. Sign In & Session Tests
    client_session = httpx.AsyncClient(base_url=BASE_URL, follow_redirects=True, timeout=30.0)
    print("\n--- [6] Testing /signin ---")
    # Invalid credentials
    r_bad_auth = await client_session.post(
        "/signin",
        data={"identity": test_username, "password": "wrongpassword"},
        headers={"Accept": "application/json"},
    )
    assert r_bad_auth.status_code == 401
    print(f"  -> Invalid credentials rejection: {r_bad_auth.status_code} (Properly Rejected)")

    # Valid credentials
    r_good_auth = await client_session.post(
        "/signin",
        data={"identity": test_username, "password": test_password},
        headers={"Accept": "application/json"},
    )
    assert r_good_auth.status_code == 200, f"Expected 200, got {r_good_auth.status_code}"
    print(f"  -> Valid sign in: {r_good_auth.status_code} Success for '{test_username}'")

    # Access authenticated Home page
    r_auth_home = await client_session.get("/")
    assert r_auth_home.status_code == 200
    assert "Indian Cattle & Buffalo Breed Classifier" in r_auth_home.text
    assert f"Signed in as {test_username}" in r_auth_home.text
    print(f"  -> Authenticated Home View: 200 OK (User identified as {test_username})")

    # 7. Predictions with Different Pictures
    image_files = sorted(list(TEST_IMAGES_DIR.glob("*.*")))
    if not image_files:
        print("Test images not found, generating on the fly...")
        try:
            from create_test_images import generate_all_images
        except ImportError:
            from backend.create_test_images import generate_all_images
        generate_all_images()
        image_files = sorted(list(TEST_IMAGES_DIR.glob("*.*")))

    assert len(image_files) > 0, "No test images found in test_images directory!"
    print(f"Found {len(image_files)} different test images to evaluate:")

    gps_samples = [
        ("30.9010,75.8573", "Punjab"),
        ("22.3039,70.8022", "Gujarat"),
        ("12.9716,77.5946", "Karnataka"),
        ("26.9124,75.7873", "Rajasthan"),
        ("28.7041,77.1025", "Delhi"),
        ("19.0760,72.8777", "Maharashtra"),
        ("25.3176,82.9739", "Varanasi"),
        ("13.0827,80.2707", "Tamil Nadu"),
        ("17.3850,78.4867", "Telangana"),
    ]

    prediction_results = []
    for idx, img_path in enumerate(image_files, start=1):
        gps_coord, region_hint = gps_samples[(idx - 1) % len(gps_samples)]
        animal_id = f"ANIMAL-{idx:03d}-{img_path.stem[:8].upper()}"

        with open(img_path, "rb") as f:
            file_bytes = f.read()

        # Alternate between JSON accept and direct /api/predict to test both endpoints
        if idx % 2 == 1:
            endpoint = "/predict"
            headers = {"Accept": "application/json"}
        else:
            endpoint = "/api/predict"
            headers = {}

        files = {"file": (img_path.name, file_bytes, "image/jpeg" if img_path.suffix != ".png" else "image/png")}
        data = {"animal_id": animal_id, "gps_coordinates": gps_coord}

        t0 = time.perf_counter()
        resp = await client_session.post(endpoint, files=files, data=data, headers=headers)
        elapsed_ms = (time.perf_counter() - t0) * 1000

        assert resp.status_code == 200, f"Prediction failed for {img_path.name}: {resp.status_code} - {resp.text}"
        res_json = resp.json()
        breed = res_json.get("predicted_breed")
        confidence = res_json.get("confidence")
        location = res_json.get("location")
        top_scores = res_json.get("top_scores", [])

        prediction_results.append({
            "image": img_path.name,
            "breed": breed,
            "confidence": confidence,
            "location": location,
            "endpoint": endpoint,
            "latency_ms": elapsed_ms,
        })

        print(f"  [{idx:02d}] {img_path.name:24} -> Predicted: {breed:<15} ({confidence:5.2f}%) | Loc: {location[:30]} | {elapsed_ms:4.0f}ms")

    # Also test HTML form rendering for /predict
    print("\n--- [8] Testing /predict Browser HTML Output ---")
    first_img = image_files[0]
    with open(first_img, "rb") as f:
        file_bytes = f.read()
    files = {"file": (first_img.name, file_bytes, "image/jpeg")}
    data = {"animal_id": "HTML-TEST-001", "gps_coordinates": "22.30,70.80"}
    r_html = await client_session.post("/predict", files=files, data=data, headers={"Accept": "text/html"})
    assert r_html.status_code == 200
    assert "Prediction Result" in r_html.text
    assert "Predicted Breed:" in r_html.text
    print("  -> Browser HTML format response: 200 OK")

    # 9. Test Prediction History persistence
    print("\n--- [9] Testing /api/predictions Persistence in Database ---")
    r_history = await client_session.get("/api/predictions")
    assert r_history.status_code == 200
    history_data = r_history.json()
    predictions_in_db = history_data.get("predictions", [])
    print(f"  -> Retrieved {len(predictions_in_db)} persisted predictions from SQLite database for {test_username}")
    assert len(predictions_in_db) >= len(image_files), "Expected all predictions to be recorded in the database!"

    # 10. Logout Test
    print("\n--- [10] Testing /logout ---")
    r_logout = await client_session.get("/logout", headers={"Accept": "application/json"})
    assert r_logout.status_code == 200
    # Confirm user is logged out
    r_post_logout = await client_session.get("/", follow_redirects=False)
    assert r_post_logout.status_code == 303, f"Expected 303 after logout, got {r_post_logout.status_code}"
    print("  -> Logout: Successfully cleared session")

    await client_session.aclose()

    # Summary Report
    print("\n" + "=" * 70)
    print(" ALL API ENDPOINTS & PREDICTION TESTS PASSED SUCCESSFULLY! ")
    print("=" * 70)
    print(f"Total Different Pictures Evaluated: {len(prediction_results)}")
    for p in prediction_results:
        print(f"  * {p['image']} -> {p['breed']} ({p['confidence']}%) via {p['endpoint']}")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(run_all_tests())
