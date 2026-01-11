import json
import httpx
import re
from config import config

def mask_sensitive(text: str, key: str) -> str:
    if not key:
        return text
    return text.replace(key, "***")

def test_api():
    print("=== Gemini API Connectivity Test ===")
    
    api_key = config.GEMINI_API_KEY
    base_url = config.BASE_URL.rstrip('/')
    api_version = config.GEMINI_API_VERSION
    model_name = config.MODEL_NAME
    
    if not api_key:
        print("Error: GEMINI_API_KEY is not set.")
        return

    # 模拟 doc_gen.py 中的 URL 构建逻辑
    if re.search(r'/v1(beta)?$', base_url):
        url_prefix = base_url
    elif "/v1" in base_url or "/v1beta" in base_url:
        url_prefix = base_url
    else:
        url_prefix = f"{base_url}/{api_version}"
        
    url = f"{url_prefix}/models/{model_name}:generateContent?key={api_key}"
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "AstrBot/ApiTest",
        "x-goog-api-key": api_key,
    }
    
    if "googleapis.com" not in base_url:
        headers["Authorization"] = f"Bearer {api_key}"

    payload = {
        "contents": [
            {
                "parts": [{"text": "Hello, this is a connectivity test. Please reply with 'OK'."}]
            }
        ],
        "generationConfig": {
            "temperature": 0.1,
            "maxOutputTokens": 10,
        }
    }

    # 脱敏打印请求信息
    masked_url = mask_sensitive(url, api_key)
    masked_headers = {k: (mask_sensitive(v, api_key) if k.lower() in ["x-goog-api-key", "authorization"] else v) for k, v in headers.items()}
    
    print(f"\n[Request Information]")
    print(f"URL: {masked_url}")
    print(f"Headers: {json.dumps(masked_headers, indent=2)}")
    print(f"Body: {json.dumps(payload, indent=2)}")

    print(f"\n[Sending Request...]")
    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.post(url, json=payload, headers=headers)
            
            print(f"Status Code: {response.status_code}")
            
            # HTML 拦截检查
            content_type = response.headers.get("Content-Type", "")
            if "text/html" in content_type or response.text.strip().startswith("<!DOCTYPE html>"):
                print("\n[ALERT] Received HTML response instead of JSON!")
                print("This usually means the request was intercepted by a WAF, portal, or the API endpoint is incorrect.")
                if len(response.text) > 500:
                    print(f"HTML Preview (first 500 chars): {response.text[:500]}...")
                else:
                    print(f"HTML Response: {response.text}")
                return

            # 脱敏打印响应
            try:
                data = response.json()
                masked_response = mask_sensitive(json.dumps(data, indent=2), api_key)
                print(f"\n[Response JSON]\n{masked_response}")
                
                if response.status_code == 200:
                    print("\n✅ Connectivity test PASSED!")
                else:
                    print("\n❌ Connectivity test FAILED with status code.")
            except json.JSONDecodeError:
                masked_body = mask_sensitive(response.text, api_key)
                print(f"\n[Response Raw Content]\n{masked_body}")
                print("\n❌ Failed to decode JSON response.")
                
    except Exception as e:
        print(f"\n❌ Request Exception: {mask_sensitive(str(e), api_key)}")

if __name__ == "__main__":
    test_api()
