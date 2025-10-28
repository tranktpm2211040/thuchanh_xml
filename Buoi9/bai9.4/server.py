from flask import Flask, jsonify, request

app = Flask(__name__)

# --- Định nghĩa các route ---

@app.route('/')
def home():
    """Route cơ bản."""
    return "Xin chào từ Flask trên mọi địa chỉ IP!"

# 1. API cho Bài 9.1 (Sách)
@app.route('/api/book', methods=['GET'])
def get_book():
    """Trả về dữ liệu sách hợp lệ (theo schema 9.1)."""
    book_data = {
        "title": "Học Python cơ bản",
        "author": "Nguyễn Minh",
        "price": 120000,
        "inStock": True,
        "categories": ["Lập trình", "Python", "Cơ bản"],
        "rating": 4.5
    }
    return jsonify(book_data)

# 2. API cho Bài 9.2 (User)
@app.route('/api/user/<username>', methods=['GET'])
def get_user(username):
    """
    Trả về danh sách user hợp lệ (theo schema 9.2).
    Chúng ta bỏ qua 'username' và trả về toàn bộ dữ liệu mẫu.
    Lưu ý: Dữ liệu của 'lan456' thiếu 'street' và 'isVerified' 
    nhưng vẫn HỢP LỆ vì schema 9.2 không bắt buộc 2 trường này.
    """
    user_data = {
      "users": [
        {
          "username": "minh123",
          "password": "Abc@1234", # Hợp lệ với regex
          "emails": ["minh123@example.com", "backup@gmail.com"],
          "age": 16,
          "address": {
            "city": "Cần Thơ",
            "street": "45 Nguyễn Trãi"
          },
          "hobbies": ["đọc sách", "chơi game"],
          "isVerified": False
        },
        {
          "username": "lan456",
          "password": "Xyz@5678!", # Hợp lệ với regex
          "emails": ["lan456@example.com"],
          "age": 18,
          "address": {
            "city": "Hà Nội" # Thiếu 'street' -> vẫn hợp lệ
          },
          "hobbies": ["vẽ", "nghe nhạc"],
          # Thiếu 'isVerified' -> vẫn hợp lệ (có default: false)
        }
      ]
    }
    return jsonify(user_data)

# 3. API cho phép trừ (POST)
@app.route('/api/subtract', methods=['POST'])
def subtract():
    """Nhận 2 số a, b và trả về kết quả a - b."""
    data = request.json
    a = data.get('a')
    b = data.get('b')
    
    if a is None or b is None:
        return jsonify({"error": "Thiếu giá trị 'a' hoặc 'b'"}), 400
        
    try:
        result = float(a) - float(b)
        # Trả về kết quả theo schema tự định nghĩa
        response_data = {"result": result}
        return jsonify(response_data)
    except ValueError:
        return jsonify({"error": "Giá trị 'a' hoặc 'b' không phải là số"}), 400

# 4. API DÙNG ĐỂ KIỂM CHỨNG (trả về dữ liệu sai)
@app.route('/api/invalid_book', methods=['GET'])
def get_invalid_book():
    """
    Trả về dữ liệu sách KHÔNG HỢP LỆ (dùng cho phần Kiểm chứng).
    Lỗi: 'title' quá ngắn (yêu cầu min 3) và thiếu 'author' (bắt buộc).
    """
    invalid_book_data = {
        "title": "Py", # Lỗi: Quá ngắn
        # "author": "Nguyễn Minh", # Lỗi: Thiếu trường bắt buộc
        "price": 120000,
        "inStock": True
    }
    return jsonify(invalid_book_data)

# --- Chạy server ---
if __name__ == '__main__':
    # Chạy trên mọi IP (0.0.0.0) ở cổng 5000
    app.run(host='0.0.0.0', port=5000, debug=True)