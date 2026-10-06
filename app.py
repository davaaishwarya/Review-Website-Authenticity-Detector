import streamlit as st
import pickle
import re
import pandas as pd
import requests
from urllib.parse import urlparse
from datetime import datetime


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="VeriShield | Trust & Security",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>

@import url(
'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
);

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #f8fafc;
}

.block-container {
    max-width: 1350px;
    padding-top: 1.5rem;
}


/* TOP NAVIGATION */

.topnav {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 16px 24px;
    margin-bottom: 22px;
    box-shadow: 0 3px 12px rgba(15,23,42,0.04);
}

.logo {
    font-size: 23px;
    font-weight: 800;
    color: #0f172a;
}

.logo span {
    color: #2563eb;
}

.nav-right {
    text-align: right;
    color: #64748b;
    font-size: 13px;
}


/* HERO */

.hero {
    background:
    linear-gradient(
        120deg,
        #0f172a,
        #172554,
        #1d4ed8
    );

    border-radius: 20px;
    padding: 45px;
    color: white;
    margin-bottom: 25px;

    box-shadow:
    0 15px 40px rgba(30,64,175,0.18);
}

.hero-small {
    color: #93c5fd;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1px;
    margin-bottom: 10px;
}

.hero-title {
    font-size: 39px;
    font-weight: 800;
    letter-spacing: -1.2px;
}

.hero-text {
    color: #cbd5e1;
    font-size: 15px;
    max-width: 700px;
    line-height: 1.7;
    margin-top: 10px;
}


/* CARDS */

.card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 15px;
    padding: 22px;
    box-shadow: 0 4px 15px rgba(15,23,42,0.04);
}

.card-title {
    color: #64748b;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .5px;
}

.card-number {
    color: #0f172a;
    font-size: 28px;
    font-weight: 800;
    margin-top: 7px;
}

.card-description {
    color: #94a3b8;
    font-size: 12px;
    margin-top: 4px;
}


/* SECTION */

.section-heading {
    color: #0f172a;
    font-size: 23px;
    font-weight: 800;
    margin-top: 25px;
}

.section-text {
    color: #64748b;
    font-size: 14px;
    margin-bottom: 18px;
}


/* STATUS */

.status-green {
    background: #ecfdf5;
    border: 1px solid #bbf7d0;
    color: #166534;
    padding: 18px;
    border-radius: 12px;
    font-weight: 700;
}

.status-red {
    background: #fef2f2;
    border: 1px solid #fecaca;
    color: #991b1b;
    padding: 18px;
    border-radius: 12px;
    font-weight: 700;
}

.status-yellow {
    background: #fffbeb;
    border: 1px solid #fde68a;
    color: #92400e;
    padding: 18px;
    border-radius: 12px;
    font-weight: 700;
}


/* SECURITY CHECK */

.check-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 13px;
    padding: 18px;
    text-align: center;
    min-height: 100px;
}

.check-title {
    font-size: 13px;
    font-weight: 700;
    color: #334155;
}

.check-value {
    margin-top: 8px;
    font-size: 13px;
}


/* DOMAIN */

.domain {
    background: #0f172a;
    color: #93c5fd;
    padding: 15px 18px;
    border-radius: 9px;
    font-family: monospace;
}


/* FOOTER */

.footer {
    border-top: 1px solid #e2e8f0;
    margin-top: 50px;
    padding: 25px;
    text-align: center;
    color: #64748b;
    font-size: 12px;
}


/* BUTTON */

.stButton > button {
    background: #2563eb;
    color: white;
    border: none;
    border-radius: 9px;
    min-height: 45px;
    font-weight: 700;
}

.stButton > button:hover {
    background: #1d4ed8;
}


/* INPUT */

.stTextInput input,
.stTextArea textarea {
    border-radius: 9px !important;
    border: 1px solid #cbd5e1 !important;
}


/* TABS */

button[data-baseweb="tab"] {
    font-weight: 700;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD MODEL
# ============================================================

try:

    with open("model.pkl", "rb") as f:
        model = pickle.load(f)

    with open("vectorizer.pkl", "rb") as f:
        vectorizer = pickle.load(f)

except FileNotFoundError:

    st.error(
        "model.pkl or vectorizer.pkl is missing."
    )

    st.stop()


# ============================================================
# SESSION HISTORY
# ============================================================

if "history" not in st.session_state:
    st.session_state.history = []


# ============================================================
# OFFICIAL DOMAINS
# ============================================================

OFFICIAL_DOMAINS = {

    "google": ["google.com"],
    "youtube": ["youtube.com"],
    "facebook": ["facebook.com"],
    "instagram": ["instagram.com"],
    "whatsapp": ["whatsapp.com"],

    "amazon": [
        "amazon.com",
        "amazon.in"
    ],

    "flipkart": ["flipkart.com"],
    "microsoft": ["microsoft.com"],
    "apple": ["apple.com"],
    "openai": ["openai.com"],

    "chatgpt": [
        "chatgpt.com",
        "openai.com"
    ],

    "github": ["github.com"],
    "linkedin": ["linkedin.com"],
    "netflix": ["netflix.com"],
    "spotify": ["spotify.com"],
    "telegram": ["telegram.org"],
    "twitter": ["twitter.com"],
    "x": ["x.com"],
    "canva": ["canva.com"],
    "zoom": ["zoom.us"],
    "discord": ["discord.com"],
    "snapchat": ["snapchat.com"],
    "pinterest": ["pinterest.com"],
    "adobe": ["adobe.com"],
    "oracle": ["oracle.com"],
    "cisco": ["cisco.com"],
    "ibm": ["ibm.com"],
    "deloitte": ["deloitte.com"],
    "tcs": ["tcs.com"],
    "infosys": ["infosys.com"],
    "wipro": ["wipro.com"],
    "accenture": ["accenture.com"],
    "cognizant": ["cognizant.com"],
    "capgemini": ["capgemini.com"],
    "hcl": ["hcltech.com"],
    "tech mahindra": ["techmahindra.com"],
    "walmart": ["walmart.com"],
    "paypal": ["paypal.com"],
    "ebay": ["ebay.com"],
    "samsung": ["samsung.com"],
    "intel": ["intel.com"],
    "nvidia": ["nvidia.com"]
}


# ============================================================
# REVIEW CLEANING
# ============================================================

def clean_text(text):

    text = text.lower()

    text = re.sub(
        r"http\S+|www\S+",
        " ",
        text
    )

    text = re.sub(
        r"[^a-zA-Z\s]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# REVIEW MODEL
# ============================================================

def get_result(review):

    cleaned = clean_text(review)

    vector = vectorizer.transform(
        [cleaned]
    )

    probabilities = model.predict_proba(
        vector
    )[0]

    classes = model.classes_

    fake = None
    original = None

    for label, probability in zip(
        classes,
        probabilities
    ):

        label = str(label).lower().strip()

        if label in [
            "fake",
            "false",
            "fraud",
            "0"
        ]:

            fake = probability * 100

        elif label in [
            "original",
            "genuine",
            "real",
            "true",
            "1"
        ]:

            original = probability * 100

    if fake is None or original is None:

        prediction = str(
            model.predict(vector)[0]
        )

        confidence = max(
            probabilities
        ) * 100

        return (
            prediction,
            confidence,
            None,
            None
        )

    prediction = (
        "Fake"
        if fake > original
        else "Original"
    )

    confidence = max(
        fake,
        original
    )

    return (
        prediction,
        confidence,
        fake,
        original
    )


# ============================================================
# REVIEW ANALYSIS
# ============================================================

def analyze_review(review):

    words = review.split()

    word_count = len(words)

    unique_words = len(
        set(
            word.lower()
            for word in words
        )
    )

    characters = len(review)

    exclamations = review.count("!")

    questions = review.count("?")

    uppercase = sum(
        1
        for c in review
        if c.isupper()
    )

    word_list = re.findall(
        r"[a-zA-Z]+",
        review.lower()
    )

    frequency = {}

    for word in word_list:

        frequency[word] = (
            frequency.get(word, 0) + 1
        )

    repeated = []

    for word, count in frequency.items():

        if count >= 3 and len(word) > 2:

            repeated.append(
                f"{word} ({count})"
            )

    suspicious_phrases = [

        "best product ever",
        "buy now",
        "100% amazing",
        "must buy",
        "everyone should buy",
        "best ever",
        "perfect product",
        "worst product ever"
    ]

    found = []

    lower = review.lower()

    for phrase in suspicious_phrases:

        if phrase in lower:
            found.append(phrase)

    quality = 100

    if exclamations >= 5:
        quality -= 15

    if uppercase > 20:
        quality -= 10

    if repeated:
        quality -= 15

    if found:
        quality -= 20

    quality = max(
        quality,
        0
    )

    return {

        "words": word_count,

        "unique": unique_words,

        "characters": characters,

        "exclamations": exclamations,

        "questions": questions,

        "uppercase": uppercase,

        "repeated": repeated,

        "phrases": found,

        "quality": quality
    }


# ============================================================
# DOMAIN CLEAN
# ============================================================

def clean_domain(domain):

    domain = domain.lower().strip()

    if domain.startswith("www."):
        domain = domain[4:]

    return domain


# ============================================================
# OFFICIAL DOMAIN
# ============================================================

def is_official(domain, company):

    company = company.lower().strip()

    domain = clean_domain(domain)

    if company not in OFFICIAL_DOMAINS:
        return None

    for official in OFFICIAL_DOMAINS[company]:

        official = clean_domain(
            official
        )

        if (
            domain == official
            or domain.endswith(
                "." + official
            )
        ):

            return True

    return False


# ============================================================
# URL ANALYSIS
# ============================================================

def analyze_url(
    website,
    domain
):

    warnings = []

    deductions = 0

    parsed = urlparse(website)

    # HTTPS
    if parsed.scheme != "https":

        warnings.append(
            "HTTPS is not enabled."
        )

        deductions += 20

    # IP address
    if re.match(
        r"^\d{1,3}(\.\d{1,3}){3}$",
        domain
    ):

        warnings.append(
            "IP address used instead of domain."
        )

        deductions += 30

    # @
    if "@" in website:

        warnings.append(
            "URL contains @ symbol."
        )

        deductions += 25

    # Long URL
    if len(website) > 100:

        warnings.append(
            "URL is unusually long."
        )

        deductions += 10

    # Hyphen
    if domain.count("-") >= 3:

        warnings.append(
            "Domain contains multiple hyphens."
        )

        deductions += 10

    # Subdomains
    if domain.count(".") >= 3:

        warnings.append(
            "Large number of subdomains detected."
        )

        deductions += 10

    suspicious = [

        "login",
        "verify",
        "verification",
        "secure",
        "account",
        "update",
        "password",
        "claim",
        "gift",
        "bonus"
    ]

    found = []

    for word in suspicious:

        if word in website.lower():
            found.append(word)

    if found:

        warnings.append(
            "Sensitive keywords detected: "
            + ", ".join(found)
        )

        deductions += 10

    return warnings, deductions


# ============================================================
# WEBSITE CHECK
# ============================================================

def check_website(
    website,
    company
):

    if not website.startswith(
        ("http://", "https://")
    ):

        website = (
            "https://" +
            website
        )

    parsed = urlparse(website)

    domain = clean_domain(
        parsed.netloc
    )

    if not domain:

        return {
            "valid": False,
            "message": "Invalid URL."
        }

    https = (
        parsed.scheme.lower()
        == "https"
    )

    official = is_official(
        domain,
        company
    )

    reachable = False

    status_code = None

    final_domain = domain

    redirect = False

    try:

        response = requests.get(
            website,
            timeout=8,
            allow_redirects=True,
            headers={
                "User-Agent":
                "Mozilla/5.0"
            }
        )

        status_code = response.status_code

        reachable = (
            status_code < 400
        )

        if response.url:

            final_domain = clean_domain(
                urlparse(
                    response.url
                ).netloc
            )

            redirect = (
                final_domain != domain
            )

    except requests.RequestException:

        reachable = False

    warnings, deductions = analyze_url(
        website,
        domain
    )

    score = 0

    if official is True:
        score += 60

    if https:
        score += 20

    if reachable:
        score += 20

    score -= deductions

    score = max(
        0,
        min(score, 100)
    )

    if official is True:

        status = "OFFICIAL"

    elif official is False:

        status = "NOT OFFICIAL"

    elif warnings:

        status = "SUSPICIOUS"

    else:

        status = "UNABLE TO VERIFY"

    return {

        "valid": True,

        "domain": final_domain,

        "original_domain": domain,

        "official": official,

        "https": https,

        "reachable": reachable,

        "status_code": status_code,

        "redirect": redirect,

        "warnings": warnings,

        "score": score,

        "status": status
    }


# ============================================================
# TOP NAV
# ============================================================

st.markdown("""
<div class="topnav">

<div style="display:flex;justify-content:space-between;align-items:center;">

<div class="logo">
🔐 Veri<span>Shield</span>
</div>

<div class="nav-right">
AI Trust & Security Platform<br>
<span style="color:#22c55e;">● System Operational</span>
</div>

</div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# HERO
# ============================================================

st.markdown("""
<div class="hero">

<div class="hero-small">
VERISHIELD SECURITY PLATFORM
</div>

<div class="hero-title">
Trust what you read.<br>
Verify where you connect.
</div>

<div class="hero-text">
An AI-powered platform for analyzing online reviews
and verifying websites using machine-learning predictions,
domain intelligence and URL security analysis.
</div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# DASHBOARD
# ============================================================

total = len(
    st.session_state.history
)

reviews = len([
    x for x in st.session_state.history
    if x["Type"] == "Review"
])

websites = len([
    x for x in st.session_state.history
    if x["Type"] == "Website"
])


a, b, c, d = st.columns(4)

with a:

    st.markdown(
        f"""
        <div class="card">

        <div class="card-title">
        Total Analyses
        </div>

        <div class="card-number">
        {total}
        </div>

        <div class="card-description">
        Security activities
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )

with b:

    st.markdown(
        f"""
        <div class="card">

        <div class="card-title">
        Review Checks
        </div>

        <div class="card-number">
        {reviews}
        </div>

        <div class="card-description">
        AI review analysis
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )

with c:

    st.markdown(
        f"""
        <div class="card">

        <div class="card-title">
        Website Checks
        </div>

        <div class="card-number">
        {websites}
        </div>

        <div class="card-description">
        Domain verification
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )

with d:

    st.markdown(
        """
        <div class="card">

        <div class="card-title">
        Platform Status
        </div>

        <div class="card-number"
        style="font-size:22px;color:#16a34a;">
        OPERATIONAL
        </div>

        <div class="card-description">
        Analysis engine available
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# TABS
# ============================================================

st.write("")

review_tab, website_tab, history_tab = st.tabs(
    [
        "📝 Review Verification",
        "🌐 Website Verification",
        "📊 Activity"
    ]
)


# ============================================================
# REVIEW TAB
# ============================================================

with review_tab:

    st.markdown(
        '<div class="section-heading">Review Verification</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-text">
        Use the AI model to classify a review and inspect
        linguistic patterns that may indicate suspicious content.
        </div>
        """,
        unsafe_allow_html=True
    )

    samples = [

        "Write my own review",

        "I bought this phone last month. "
        "The battery lasts all day and "
        "the camera quality is good.",

        "Amazing amazing amazing!!! "
        "Best product ever!!! Everyone "
        "should buy this!!!",

        "The product arrived late. "
        "The package was damaged and "
        "the quality was poor."
    ]

    selected = st.selectbox(
        "Review template",
        samples
    )

    if selected == "Write my own review":

        default = ""

    else:

        default = selected

    review = st.text_area(
        "Review",
        value=default,
        height=170,
        placeholder="Enter review text..."
    )

    if st.button(
        "RUN AI REVIEW CHECK",
        use_container_width=True
    ):

        if not review.strip():

            st.warning(
                "Enter a review first."
            )

        else:

            prediction, confidence, fake, original = (
                get_result(review)
            )

            analysis = analyze_review(
                review
            )

            st.divider()

            if prediction.lower() == "fake":

                st.markdown(
                    """
                    <div class="status-red">
                    ⚠ POTENTIALLY FAKE REVIEW
                    <br>
                    <small>
                    AI analysis detected patterns associated
                    with potentially artificial review content.
                    </small>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    """
                    <div class="status-green">
                    ✓ POTENTIALLY ORIGINAL REVIEW
                    <br>
                    <small>
                    The model did not identify strong
                    fake-review indicators.
                    </small>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.write("")

            x1, x2, x3 = st.columns(3)

            with x1:

                st.metric(
                    "AI Confidence",
                    f"{confidence:.1f}%"
                )

            with x2:

                st.metric(
                    "Quality Score",
                    f'{analysis["quality"]}/100'
                )

            with x3:

                st.metric(
                    "Words",
                    analysis["words"]
                )

            if (
                fake is not None
                and original is not None
            ):

                st.divider()

                st.subheader(
                    "AI Classification"
                )

                p1, p2 = st.columns(2)

                with p1:

                    st.metric(
                        "Fake Probability",
                        f"{fake:.1f}%"
                    )

                    st.progress(
                        min(fake / 100, 1)
                    )

                with p2:

                    st.metric(
                        "Original Probability",
                        f"{original:.1f}%"
                    )

                    st.progress(
                        min(original / 100, 1)
                    )

                chart = pd.DataFrame({

                    "Result": [
                        "Fake",
                        "Original"
                    ],

                    "Probability": [
                        fake,
                        original
                    ]

                })

                st.bar_chart(
                    chart.set_index(
                        "Result"
                    )
                )

            st.divider()

            st.subheader(
                "Content Profile"
            )

            c1, c2, c3, c4, c5 = st.columns(5)

            with c1:
                st.metric(
                    "Characters",
                    analysis["characters"]
                )

            with c2:
                st.metric(
                    "Unique Words",
                    analysis["unique"]
                )

            with c3:
                st.metric(
                    "Exclamations",
                    analysis["exclamations"]
                )

            with c4:
                st.metric(
                    "Questions",
                    analysis["questions"]
                )

            with c5:
                st.metric(
                    "Uppercase",
                    analysis["uppercase"]
                )

            st.divider()

            st.subheader(
                "Writing Pattern Analysis"
            )

            if analysis["repeated"]:

                st.warning(
                    "Repeated words: "
                    + ", ".join(
                        analysis["repeated"]
                    )
                )

            if analysis["phrases"]:

                st.warning(
                    "Promotional phrases: "
                    + ", ".join(
                        analysis["phrases"]
                    )
                )

            if (
                not analysis["repeated"]
                and not analysis["phrases"]
                and analysis["exclamations"] < 5
            ):

                st.success(
                    "✓ No major suspicious writing patterns detected."
                )

            st.session_state.history.append({

                "Time":
                    datetime.now().strftime(
                        "%H:%M:%S"
                    ),

                "Type":
                    "Review",

                "Input":
                    review[:60],

                "Result":
                    prediction

            })


# ============================================================
# WEBSITE TAB
# ============================================================

with website_tab:

    st.markdown(
        '<div class="section-heading">Website Verification</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-text">
        Verify whether a submitted website matches a known
        official domain and inspect basic URL security indicators.
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        company = st.text_input(
            "Company / Service",
            placeholder="Example: TCS"
        )

    with col2:

        website = st.text_input(
            "Website URL",
            placeholder="Example: https://www.tcs.com"
        )

    if st.button(
        "VERIFY WEBSITE",
        use_container_width=True
    ):

        if not company.strip():

            st.warning(
                "Enter the company name."
            )

        elif not website.strip():

            st.warning(
                "Enter the website URL."
            )

        else:

            result = check_website(
                website,
                company
            )

            if not result["valid"]:

                st.error(
                    result["message"]
                )

            else:

                st.divider()

                status = result["status"]

                if status == "OFFICIAL":

                    st.markdown(
                        """
                        <div class="status-green">
                        ✓ OFFICIAL DOMAIN VERIFIED
                        <br>
                        <small>
                        The submitted domain matches
                        the known official domain.
                        </small>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                elif status == "NOT OFFICIAL":

                    st.markdown(
                        """
                        <div class="status-red">
                        ✕ DOMAIN NOT VERIFIED
                        <br>
                        <small>
                        The submitted domain does not match
                        the known official domain.
                        </small>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                elif status == "SUSPICIOUS":

                    st.markdown(
                        """
                        <div class="status-yellow">
                        ⚠ SUSPICIOUS URL
                        <br>
                        <small>
                        One or more URL characteristics
                        require additional caution.
                        </small>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                else:

                    st.info(
                        "Official identity could not be confirmed."
                    )

                st.write("")

                score = result["score"]

                if score >= 80:
                    risk = "LOW"

                elif score >= 50:
                    risk = "MEDIUM"

                else:
                    risk = "HIGH"

                m1, m2, m3, m4 = st.columns(4)

                with m1:

                    st.metric(
                        "Trust Score",
                        f"{score}/100"
                    )

                with m2:

                    st.metric(
                        "Risk",
                        risk
                    )

                with m3:

                    st.metric(
                        "HTTPS",
                        "YES"
                        if result["https"]
                        else "NO"
                    )

                with m4:

                    st.metric(
                        "Reachable",
                        "YES"
                        if result["reachable"]
                        else "NO"
                    )

                st.progress(
                    min(score / 100, 1)
                )

                st.divider()

                st.subheader(
                    "Security Checks"
                )

                q1, q2, q3 = st.columns(3)

                with q1:

                    st.markdown(
                        f"""
                        <div class="check-card">

                        <div class="check-title">
                        Domain Identity
                        </div>

                        <div class="check-value">
                        {"✓ MATCHED" if result["official"] is True
                        else "✕ NOT MATCHED" if result["official"] is False
                        else "ℹ UNKNOWN"}
                        </div>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with q2:

                    st.markdown(
                        f"""
                        <div class="check-card">

                        <div class="check-title">
                        Connection
                        </div>

                        <div class="check-value">
                        {"🔒 HTTPS ENABLED" if result["https"]
                        else "⚠ HTTP CONNECTION"}
                        </div>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with q3:

                    st.markdown(
                        f"""
                        <div class="check-card">

                        <div class="check-title">
                        Availability
                        </div>

                        <div class="check-value">
                        {"✓ ONLINE" if result["reachable"]
                        else "✕ UNAVAILABLE"}
                        </div>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                st.divider()

                st.subheader(
                    "Domain Information"
                )

                st.markdown(
                    f"""
                    <div class="card">

                    <b>Company</b><br>
                    {company}

                    <br><br>

                    <b>Detected Domain</b>

                    <div class="domain">
                    {result["domain"]}
                    </div>

                    <br>

                    <b>HTTP Status:</b>
                    {result["status_code"] if result["status_code"] else "N/A"}

                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.divider()

                st.subheader(
                    "URL Security Analysis"
                )

                if result["warnings"]:

                    for warning in result["warnings"]:

                        st.warning(
                            "⚠ " + warning
                        )

                else:

                    st.success(
                        "✓ No major suspicious URL patterns detected."
                    )

                st.divider()

                st.subheader(
                    "Redirect Analysis"
                )

                if result["redirect"]:

                    st.warning(
                        "The URL redirected to another domain."
                    )

                    st.write(
                        "Original:",
                        result["original_domain"]
                    )

                    st.write(
                        "Final:",
                        result["domain"]
                    )

                else:

                    st.success(
                        "✓ No different-domain redirect detected."
                    )

                st.divider()

                if risk == "LOW":

                    st.success(
                        "🛡️ Recommendation: The website "
                        "passed the available automated checks."
                    )

                elif risk == "MEDIUM":

                    st.warning(
                        "⚠️ Recommendation: Verify the "
                        "domain independently before entering "
                        "sensitive information."
                    )

                else:

                    st.error(
                        "🚨 Recommendation: Exercise extreme "
                        "caution and avoid entering sensitive "
                        "information until the website is verified."
                    )

                st.session_state.history.append({

                    "Time":
                        datetime.now().strftime(
                            "%H:%M:%S"
                        ),

                    "Type":
                        "Website",

                    "Input":
                        website[:60],

                    "Result":
                        status

                })

                st.info(
                    "HTTPS indicates an encrypted connection. "
                    "It does not by itself prove that a website "
                    "is official."
                )


# ============================================================
# HISTORY
# ============================================================

with history_tab:

    st.markdown(
        '<div class="section-heading">Security Activity</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-text">
        Recent review and website verification activity
        for the current application session.
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.session_state.history:

        df = pd.DataFrame(
            st.session_state.history
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        if st.button(
            "Clear Activity"
        ):

            st.session_state.history = []

            st.rerun()

    else:

        st.info(
            "No security activity yet."
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">

<b>🔐 VeriShield</b><br>

AI Trust & Security Platform

<br><br>

Review Intelligence • Website Verification •
URL Security Analysis

<br><br>

This application provides automated,
assistive analysis for educational purposes.
Results should be independently verified.

</div>
""", unsafe_allow_html=True)