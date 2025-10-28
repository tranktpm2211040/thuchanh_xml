import requests
import jsonschema
from jsonschema import validate

# --- ĐỊNH NGHĨA CÁC SCHEMA ĐỂ KIỂM TRA ---

# Schema cho Bài 9.1 (Book)
schema_book = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "title": {"description": "Là chuỗi, dài tối thiểu 3 ký tự, tối đa 100 ký tự.", "type": "string", "minLength": 3, "maxLength": 100},
    "author": {"description": "Là chuỗi, không được rỗng.", "type": "string", "minLength": 1},
    "price": {"description": "Là số, phải lớn hơn 0.", "type": "number", "exclusiveMinimum": 0},
    "inStock": {"description": "Là boolean (true/false).", "type": "boolean"},
    "categories": {"description": "Là mảng chuỗi, mỗi phần tử dài ít nhất 2 ký tự.", "type": "array", "items": {"type": "string", "minLength": 2}},
    "rating": {"description": "Là số, nằm trong khoảng 0 đến 5, không bắt buộc.", "type": "number", "minimum": 0, "maximum": 5}
  },
  "required": ["title", "author", "price", "inStock"]
}

# Schema cho Bài 9.2 (User)
schema_user = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "users": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "username": {"type": "string", "minLength": 3, "maxLength": 15, "pattern": "^[a-zA-Z0-9]+$"},
          "password": {"type": "string", "minLength": 8, "pattern": "^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^a-zA-Z0-9]).*$"},
          "emails": {"type": "array", "items": {"type": "string", "format": "email"}},
          "age": {"type": "integer", "minimum": 13, "maximum": 100},
          "address": {
            "type": "object",
            "properties": {
              "city": {"type": "string", "minLength": 1},
              "street": {"type": "string"}
            },
            "required": ["city"]
          },
          "hobbies": {"type": "array", "items": {"type": "string", "minLength": 2}},
          "isVerified": {"type": "boolean", "default": False}
        },
        "required": ["username", "password", "emails", "age", "address"]
      }
    }
  },
  "required": ["users"]
}

# Schema cho Response của /api/subtract (Tự xây dựng)
schema_subtract_response = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "result": {"type": "number"}
  },
  "required": ["result"]
}


# --- HÀM TRỢ GIÚP ĐỂ KIỂM TRA VÀ IN KẾT QUẢ ---
def validate_json(data, schema, endpoint_name):
    """Hàm này nhận dữ liệu JSON và schema, sau đó in ra kết quả kiểm tra."""
    print(f"--- Đang kiểm tra endpoint: {endpoint_name} ---")
    print(f"Dữ liệu JSON nhận được:\n{data}\n")
    try:
        # Thực hiện kiểm tra
        validate(instance=data, schema=schema)
        print(f"✅ KẾT QUẢ: Dữ liệu HỢP LỆ (valid) với schema {endpoint_name}.")
    except jsonschema.exceptions.ValidationError as err:
        print(f"❌ KẾT QUẢ: Dữ liệu KHÔNG HỢP LỆ (invalid) với schema {endpoint_name}.")
        print(f"LỖI TÌM THẤY: {err.message}")
    print("-" * 40 + "\n")

# --- CHẠY KIỂM TRA CÁC API ---
BASE_URL = "http://127.0.0.1:5000"

print(f"Bắt đầu gọi API từ server: {BASE_URL}...\n")

try:
    # 1. Kiểm tra /api/book (Bài 9.1)
    r_book = requests.get(f"{BASE_URL}/api/book")
    if r_book.status_code == 200:
        validate_json(r_book.json(), schema_book, "/api/book")
    else:
        print(f"Lỗi khi gọi /api/book: {r_book.status_code}")

    # 2. Kiểm tra /api/user/<username> (Bài 9.2)
    r_user = requests.get(f"{BASE_URL}/api/user/minh123")
    if r_user.status_code == 200:
        validate_json(r_user.json(), schema_user, "/api/user")
    else:
        print(f"Lỗi khi gọi /api/user: {r_user.status_code}")

    # 3. Kiểm tra /api/subtract
    payload = {"a": 20, "b": 8.5}
    print(f"--- Đang kiểm tra endpoint: /api/subtract (POST) ---")
    print(f"Dữ liệu gửi đi: {payload}\n")
    r_subtract = requests.post(f"{BASE_URL}/api/subtract", json=payload)
    if r_subtract.status_code == 200:
        # Kiểm tra dữ liệu *nhận về* từ server
        validate_json(r_subtract.json(), schema_subtract_response, "/api/subtract (response)")
    else:
        print(f"Lỗi khi gọi /api/subtract: {r_subtract.status_code}")

    # 4. KIỂM CHỨNG LỖI (theo yêu cầu cuối bài)
    print("--- BẮT ĐẦU KIỂM CHỨNG LỖI (Yêu cầu: Thử thay đổi dữ liệu JSON) ---")
    # Gọi API /api/invalid_book mà server đã cố tình làm sai
    r_invalid_book = requests.get(f"{BASE_URL}/api/invalid_book")
    if r_invalid_book.status_code == 200:
        validate_json(r_invalid_book.json(), schema_book, "/api/invalid_book")
    else:
        print(f"Lỗi khi gọi /api/invalid_book: {r_invalid_book.status_code}")

except requests.exceptions.ConnectionError:
    print("\n******************* LỖI KẾT NỐI *******************")
    print(f"Không thể kết nối tới server tại {BASE_URL}.")
    print("Vui lòng đảm bảo bạn đã chạy file 'server.py' trong một terminal khác.")
    print("***************************************************")