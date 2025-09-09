# trustscripture
Fake Website Detector App
🛡️ Fake Website Detector App

Ứng dụng AI + rule-based giúp phát hiện website giả mạo, xuyên tạc hoặc lừa đảo liên quan đến Kinh Thánh & Kitô giáo.
Được xây dựng bằng Python + Streamlit + Hugging Face.

🚀 1. Chạy trên local
Cài đặt môi trường
git clone https://github.com/<your-repo>/fake-website-detector.git
cd fake-website-detector
pip install -r requirements.txt

Chạy ứng dụng
streamlit run app.py


Ứng dụng sẽ chạy tại: http://localhost:8501

🌐 2. Deploy trên Streamlit Community Cloud (Miễn phí)

Đẩy toàn bộ code lên GitHub.

Repo cần có:

app.py

requirements.txt

README.md (file này)

Vào Streamlit Community Cloud
 → Sign in bằng GitHub.

Chọn New App → kết nối repo → chọn branch & file app.py.

Streamlit sẽ tự động build dựa trên requirements.txt.

Sau khi deploy, bạn sẽ có URL dạng:

https://your-app-name.streamlit.app


(Tuỳ chọn) Muốn gắn domain riêng → thêm CNAME record tại DNS domain trỏ về app.

☁️ 3. Deploy trên Render (Free Tier + Push-to-Deploy)
Chuẩn bị

Tài khoản Render

Repo GitHub chứa code (tương tự như trên)

Các bước

Vào Render Dashboard → New + Web Service.

Kết nối GitHub → chọn repo.

Chọn Environment: Python 3.x

Thêm requirements.txt để Render tự build.

Trong phần Start Command, nhập:

streamlit run app.py --server.port $PORT --server.address 0.0.0.0


Lưu ý: Render yêu cầu bind tới $PORT và 0.0.0.0 để app hoạt động.

Deploy → Render sẽ build và cung cấp URL dạng:

https://your-app-name.onrender.com

Push-to-deploy

Mỗi lần push code mới lên GitHub → Render tự build & deploy lại app.

📝 4. File requirements.txt mẫu
streamlit
requests
beautifulsoup4
tldextract
python-whois
transformers
torch

🔒 5. Bảo mật & lưu ý

Với app public: nên dùng Cloudflare (miễn phí) để quản lý domain & SSL.

Nếu app lớn, Render free tier có thể “sleep” → cần nâng cấp (tính phí theo usage).

Nếu cần uptime 24/7, có thể chuyển sang Oracle Cloud Free Tier hoặc VPS rẻ (Hetzner).

📄 License

MIT License — dùng tự do cho nghiên cứu & phi thương mại.
