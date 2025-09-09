import requests
from bs4 import BeautifulSoup
import tldextract
import whois
from transformers import pipeline
import streamlit as st
from datetime import datetime

# -----------------------
# Load AI model
# -----------------------
@st.cache_resource
def load_model():
    return pipeline("zero-shot-classification",
                    model="joeddav/xlm-roberta-large-xnli")

classifier = load_model()

# -----------------------
# Crawl nội dung website
# -----------------------
def crawl_page(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        text = " ".join([p.get_text() for p in soup.find_all("p")])
        return text[:2000]
    except Exception as e:
        return f"Lỗi khi crawl: {e}"

# -----------------------
# Phân tích domain
# -----------------------
def analyze_domain(url):
    ext = tldextract.extract(url)
    domain = f"{ext.domain}.{ext.suffix}"
    suspicious_score = 0

    if ext.suffix not in ["org", "com", "net", "vn"]:
        suspicious_score += 20
    if any(word in ext.domain.lower() for word in ["jesus", "bible", "vatican", "church"]):
        suspicious_score += 10
    try:
        domain_info = whois.whois(domain)
        if domain_info.creation_date:
            creation_date = domain_info.creation_date[0] if isinstance(domain_info.creation_date, list) else domain_info.creation_date
            if (datetime.now() - creation_date).days < 365:
                suspicious_score += 30
    except:
        suspicious_score += 20

    return domain, suspicious_score

# -----------------------
# Phân tích nội dung bằng AI
# -----------------------
def analyze_content(text):
    if "Lỗi khi crawl" in text:
        return 0, "unknown"

    labels = ["legit", "fake", "scam"]
    result = classifier(text, labels)
    label = result["labels"][0]
    score = result["scores"][0]

    suspicious_score = 0
    if label == "fake":
        suspicious_score += 40
    elif label == "scam":
        suspicious_score += 70

    return suspicious_score, f"{label} ({round(score*100,2)}%)"

# -----------------------
# Dashboard Streamlit
# -----------------------
st.set_page_config(page_title="Fake Website Detector", layout="centered")
st.title("🛡️ Fake Website Detector (Kinh Thánh & Kitô giáo)")

url = st.text_input("🔗 Nhập URL website cần kiểm tra:")

if st.button("Kiểm tra"):
    if url:
        st.write(f"Đang kiểm tra: **{url}**")

        # Crawl + phân tích
        text = crawl_page(url)
        domain, score_domain = analyze_domain(url)
        score_content, label_ai = analyze_content(text)

        # Tổng điểm
        total_score = score_domain + score_content
        risk_level = "✅ An toàn"
        color = "green"
        if total_score >= 70:
            risk_level = "🚨 Nguy hiểm"
            color = "red"
        elif total_score >= 40:
            risk_level = "⚠️ Đáng ngờ"
            color = "orange"

        # Hiển thị kết quả
        st.subheader("Kết quả phân tích")
        st.markdown(f"- **Domain**: {domain}")
        st.markdown(f"- **Điểm domain**: {score_domain}")
        st.markdown(f"- **AI phân loại**: {label_ai}")
        st.markdown(f"- **Điểm nội dung (AI)**: {score_content}")
        st.markdown(f"- **➡️ Tổng điểm rủi ro**: {total_score} | <span style='color:{color}'>{risk_level}</span>", unsafe_allow_html=True)

        # Xem trước nội dung crawl
        with st.expander("📄 Xem nội dung crawl được"):
            st.write(text)
    else:
        st.warning("Vui lòng nhập URL trước khi kiểm tra.")
