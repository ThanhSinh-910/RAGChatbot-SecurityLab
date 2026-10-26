import os

import requests


api_key = os.getenv("GOOGLE_API_KEY", "").strip()
if not api_key:
    raise SystemExit(
        "Chưa cấu hình GOOGLE_API_KEY. Hãy đặt biến môi trường rồi chạy lại check.py."
    )

url = "https://generativelanguage.googleapis.com/v1beta/models"
print("Đang kết nối tới Google AI Studio...")
response = requests.get(url, params={"key": api_key}, timeout=30)

if response.ok:
    print("\nKết nối thành công. Các model hỗ trợ generateContent:")
    for model in response.json().get("models", []):
        if "generateContent" in model.get("supportedGenerationMethods", []):
            print(f"- {model['name'].removeprefix('models/')}")
else:
    print(f"\nKhông truy cập được API ({response.status_code}): {response.text}")
