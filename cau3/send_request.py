import requests
import json

def send_create_session():
    
    url = "https://crypto-assignment.dangduongminhnhat2003.workers.dev/session/create?userId=group-1"

    headers = {
        "X-User-Id": "group-1",
        "User-Agent": "okhttp/4.11.0"
    }

    # payload = {
    #     "algorithm": "ecdh",
    #     "curveParameters": {
    #         "p": "6277101735386680763835789423207666416083908700390324961279",
    #         "a": "-3",
    #         "b": "2455155546008943817740293915197451784769108058161191238065",
    #         "Gx": "3289624317623424368845348028842487418520868978772050262753",
    #         "Gy": "5673242899673324591834582889556471730778853907191064256384",
    #         "order": "6277101735386680763835789423176059013767194773182842284081"
    #     }
    # }
    payload = {
        "algorithm": "ecdh",
        "curveParameters": {
            "p": "6277101735386680763835789423207666416083908700390324961279",
            "a": "-5",
            "b": "0",
            "Gx": "5",
            "Gy": "10",
            "order": "78463771692333509547947367790095830201048858754879062016"
            # order = 2*3*233*1423*542371*1247019193105105253*4665277676011395028667308207
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        print(f"✅ Gửi request thành công!")
        print(f"Status Code: {response.status_code}\n")

        print("--- Headers Phản hồi ---")
        for key, value in response.headers.items():
            print(f"{key}: {value}")
        
        print("\n--- Body Phản hồi (Nội dung) ---")

        try:
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        except requests.exceptions.JSONDecodeError:

            print(response.text)

    except requests.exceptions.RequestException as e:
        print(f"❌ Gửi request thất bại: {e}")

# Chạy hàm
if __name__ == "__main__":
    send_create_session()
    
# ✅ Gửi request thành công!
# Status Code: 200

# --- Headers Phản hồi ---
# Date: Fri, 05 Dec 2025 02:54:02 GMT
# Content-Type: application/json
# Transfer-Encoding: chunked
# Connection: keep-alive
# Access-Control-Allow-Origin: *
# Access-Control-Allow-Headers: Content-Type, X-Session-Token
# Access-Control-Allow-Methods: GET, POST, OPTIONS
# Vary: accept-encoding
# Report-To: {"group":"cf-nel","max_age":604800,"endpoints":[{"url":"https://a.nel.cloudflare.com/report/v4?s=0dy%2FQLwPsORM2%2F8imlKx1BSKZtOV58Yazi3fQmvFq1lCDYAZqXOUCDABpuKaWxDHOxwKe70CeoNM%2Bv7PT%2FoBGwPLRHclh81RtJxlqTPjVrX5GJ0iYId5d3FhFdtB3yXv2spaQJIOB%2F55IvmxaIA1lUPc7Q%3D%3D"}]}
# Nel: {"report_to":"cf-nel","success_fraction":0.0,"max_age":604800}
# Content-Encoding: gzip
# Server: cloudflare
# CF-RAY: 9a9041aea8a69fc2-SIN
# alt-svc: h3=":443"; ma=86400

# --- Body Phản hồi (Nội dung) ---
# {
#   "success": true,
#   "sessionToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJTZWN1cmVDaGF0IiwiaWF0IjoxNzY0OTAzMjQyLCJleHAiOjE3NjQ5MDM1NDIsInN1YiI6Imdyb3VwLTEiLCJzaWQiOiJlYTNkOGJlZDlhNWVkNzQwYjczNWY0ZWM2Y2MxZGI0MTkwN2Y2OGNhMDIxOWYyOWZkMTMyN2M1MWM2YTNiMDk1IiwiYWxnb3JpdGhtIjoiZWNkaCIsInB1YmxpY0tleSI6eyJ4IjoiNTIzMzE5NzI5NDMxMjc2NTM1NjU4OTM3NjA3NTkxMTcyNTk5MjI4OTQ0ODg2OTc2MjQwNzcxMjc3NiIsInkiOiIzNjQzMDg0NjM0MjUwMjIwMzAxMDkxNDcyMjk0MDc2MjAyODM4MzQ0NTUxMjk1MjM5NTUxNzU0MjE2In0sImVuY3J5cHRlZERhdGEiOiJqZVVPd0dBR0Zwa1B1Wkl5Zlh1cWJHM0xoc2R2bVRsU21TYUF3S2Q0YWtrcGhDa0M5SmszNy1PN1U3UG9nSjFOQmlySF9RNmxWajFYSjBQSS1KTnlOaHBpUHk2VUpQX0tINkhJSDBUdnRQRV9CRW9Yc1UwOU44eHJHbzJrSE50YUl0NVZWaWpLR0d0Q3BIYXJkUU5yVk4xTW9XZjNkWnppdVdVTXpQUldBZXBvempudDJyZG4wNGhNaHkzeDQ1Vjk2c28yZ0lWeWstMnhRbDg2ekxqc0FZb2xXREtWNktMbmw0cnpoUjNPN3Q1Zjl3OWRJU2ZUdzJMZERGdzh2SXZWa0VIMXFjeU84N0RVQjVwMXpGNHBWY2FnbEg4LVRieGZWTUJsTURURVV3bDFGUWRrVDc5RHg2MXktNWxRb05hZ1FHY0h5YWRGQ0NodU81Zzk0Rjh5VngtQVlTLU0yV2l3YkswLXVsZU5pQ1lXSUZFM0FFSHNKdDdMUHdLR1hsMEFnUDF1VGdVUHdzWDllN3VnT0hJQjgyZXNIVURKcXpFIiwiY3JlYXRlZEF0IjoxNzY0OTAzMjQyMDM2LCJsYXN0QWN0aXZpdHkiOjE3NjQ5MDMyNDIwMzZ9.wB11O9-NxDv8GJLY4EY-v-6Reh9iw_2oXgkgX8ltqNQ",
#   "algorithm": "ecdh",
#   "serverPublicKey": {
#     "x": "5233197294312765356589376075911725992289448869762407712776",
#     "y": "3643084634250220301091472294076202838344551295239551754216"
#   },
#   "signatureSupported": true,
#   "serverSignaturePublicKey": {
#     "x": "585136333299365181715457862858146444887560916302476619132",
#     "y": "4888877295848971362306018578958649139131207302246344381334"
#   },
#   "sessionSignature": {
#     "r": "22967202110519565804759367334393447210825896872986227205",
#     "s": "14010520034876759527878858733825872359392165123758879768",
#     "messageHash": "11403540358899906849003707375682185709375304588481108024",
#     "algorithm": "ECDSA-P192"
#   },
#   "signatureAlgorithm": "ECDSA-P192"
# }