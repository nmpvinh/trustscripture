import streamlit as st
import requests
import tldextract
import whois
from bs4 import BeautifulSoup
from transformers import pipeline

# ========== 1. Load model Hugging Face ==========
@st.cache_resource
def load_model():
    return pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

nlp_model = load_model()

# ========== 2. Rule-based checks ==========
def rule_based_check(url: str):
    issues = []
    score = 0

    # Extract domain
    domain_info = tldextract.extract(url)
    domain = f"{domain_info.domain}.{domain_info.suffix}"

    # Rule 1: URL quá dài
    if len(url) > 75:
        issues.append("URL quá dài, có thể là dấu hiệu giả mạo.")
        score += 1

    # Rule 2: WHOIS ẩn
    try:
        w = whois.whois(domain)
        if not w.organization:
            issues.append("WHOIS bị ẩn hoặc thiếu thông tin.")
            score += 1
    except Exception:
        issues.append("Không truy xuất được WHOIS.")
        score += 1

    # Rule 3: Domain miễn phí hoặc bất thường
    if domain_info.suffix in ["tk", "ml", "ga", "cf", "gq"]:
        issues.append(f"Domain sử dụng TLD miễn phí: {domain_info.suffix}")
        score += 1

    return score, issues

# ========== 3. AI-based checks ==========
def ai_based_check(url: str):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        text_content = " ".join(soup.stripped_strings)[:500]  # lấy 500 ký tự đầu
        result = nlp_model(text_content)[0]
        return result
    except Exception as e:
        return {"label": "ERROR", "score": 0.0, "error": str(e)}

# ========== 4. Streamlit UI ==========
st.set_page_config(page_title="Fake Website Detector", page_icon="🛡️", layout="wide")

st.title("🛡️ Fake Website Detector")
st.markdown("Công cụ phát hiện website giả mạo / lừa đảo về Kitô giáo & Kinh Thánh.")

url = st.text_input("🔗 Nhập URL để kiểm tra:", "https://example.com")

if st.button("Kiểm tra"):
    if not url.startswith("http"):
        st.warning("⚠️ Hãy nhập URL đầy đủ (bao gồm http:// hoặc https://)")
    else:
        with st.spinner("Đang phân tích..."):
            # Rule-based
            rule_score, rule_issues = rule_based_check(url)

            # AI-based
            ai_result = ai_based_check(url)

        # ========== Hiển thị kết quả ==========
        st.subheader("📊 Kết quả kiểm tra")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Rule-based check")
            if rule_issues:
                for issue in rule_issues:
                    st.error(f"- {issue}")
            else:
                st.success("Không phát hiện dấu hiệu đáng ngờ.")

        with col2:
            st.markdown("### AI-based check")
            if ai_result.get("label") == "ERROR":
                st.error(f"Lỗi khi phân tích nội dung: {ai_result.get('error')}")
            else:
                label = ai_result["label"]
                score = round(ai_result["score"] * 100, 2)
                if label == "NEGATIVE":
                    st.error(f"AI đánh giá nội dung KHẢ NGHI ({score}%)")
                else:
                    st.success(f"AI đánh giá nội dung AN TOÀN ({score}%)")

        # ========== Tổng kết ==========
        risk_level = rule_score
        if ai_result.get("label") == "NEGATIVE":
            risk_level += 1

        st.subheader("🧾 Kết luận")
        if risk_level >= 2:
            st.error("⚠️ Website có khả năng GIẢ MẠO hoặc LỪA ĐẢO.")
        else:
            st.success("✅ Website có vẻ an toàn.")
