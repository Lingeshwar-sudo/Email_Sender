
import streamlit as st
import smtplib
import pandas as pd
import time
import re
import io
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# =========================
# ✅ HARD-CODED CREDENTIALS
# Change these once — never enter them again!
# =========================
SENDER_EMAIL = "sales@icebergsindia.com"        # <-- Replace with your Gmail
APP_PASSWORD  = "sosp yvol jxyj dgnm"       # <-- Replace with your App Password

# =========================
# PAGE CONFIG & STYLING
# =========================
st.set_page_config(page_title="Gmail Bulk Sender", page_icon="📧", layout="wide")

# -----------------------------------------------------------------------
# BACKGROUND IMAGE
# -----------------------------------------------------------------------
# Option A (default): pure CSS gradient — works everywhere, no file needed.
# Option B: uncomment the IMAGE_URL line and set your image URL.
#
# IMAGE_URL = "https://images.unsplash.com/photo-1557683316-973673baf926?w=1600"
# bg_css = f"background: url('{IMAGE_URL}') center/cover fixed no-repeat;"
#
# Option C: local file — put the image next to this script, then:
# import base64, pathlib
# data = base64.b64encode(pathlib.Path("your_image.jpg").read_bytes()).decode()
# bg_css = f"background: url('data:image/jpeg;base64,{data}') center/cover fixed;"
# -----------------------------------------------------------------------




st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

/* ── Sky background ── */
.stApp {
    background-image: url("data:image/jpeg;base64,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AQE/Af4OnTTOdQ0QhCE/Q1KfPV0pRPqHjSiZ853nv0eNE9UIQnKedE9s5L0UT6J+j00omXg3mJlKUuqlGx+R7il2vbSlKXU1R+H2GvI+ohc2lLth7Sc6/h761jHnSl6NjHg86XoGMeD1f//EAB4RAAICAgIDAAAAAAAAAAAAAAARAVAwQBAgYHCA/9oACAECAQE/Acc+Mz8WIXRCqkTHRVSEq5CIwuiQhCxMY6Jd1wx2T2YrY2GPUjMhC34yoVBHueK2CM//xAAZEAABBQAAAAAAAAAAAAAAAAAhAFFgoLD/2gAIAQEABj8C1vGjoRpLf//EACAQAQEBAQEBAQEBAQEBAQAAAAEAERAgMEBQMSFhUXH/2gAIAQEAAT8hIiOHCIjhEREREREREREREf3ThHSOHDhEREREcERERHCP7eQRB5OkcIiIiIjgiIiOn8bPzZZBZFkcIiOkRERERERERER/Fz9GWRZzLIIsjyREREREREREf38s5kFnxOERwiIiIjhEf3css5lnMs9ERERERERERERH5d/jZZZZZZBZBZ7IiIiIiIiIiI/Tv8PLOZZZBZZ8iIiIiIiIiLY/m5Z9ssgssssss5no4REREREREcOn0f5mWWWWWWWWWfIiIiIiIiIiI+z9Th+TfR0LIILLLLLLPmdIiIiIiIiI4eDr4ePy23h92W222233llllllln0IjhEREREREcIiOnlmfW2222222wwx9dlttttt+GQWWWWdz6ERERERERERwiI+DMzPvbbbbYbYYbfG+dlllllttttt4RHMssssss+WWdIiIiIiIiPBER8GZn3ttttvA2www22y222222yyzHhttttvSOZZZ9M+BEREREREcIiPgzPHr5222223ghwbbLbbbbLMYzZbbbbbYiI4cyz6ZZ3PBERERERERHCOHp4zxmePjbbbbeCHQbMttvCzGLLxtttvCIiP0EREREcIiI4R8meM9e7bbbbbbbEOHeWWW2Yxjw3jbbbYiIiI+D5yzuWeTpEREREfZnrMzMzMttsttvA8HDvKWWWYx4bbbbDDDEMMR9s7nyOEcIiPs9eszMzNtttttttsQmUYcLLLMXjbbbYYYhiGGGH55Z5yzueSIiIiI+z6ZmZmeLbbbbbb0JhLjThZZZZbbbYYYYYYYYbbfpnvLPJEREREflZmZmZZZbbbbbbbYh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");
    background-size: cover;
    background-position: center center;
    background-attachment: fixed;
    background-repeat: no-repeat;
}

.block-container { padding: 2rem 2.5rem; max-width: 1300px; }

/* Headings — dark navy so they pop on sky */
h1 {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1.9rem !important;
    color: #0f172a !important;
    letter-spacing: -0.5px;
    text-shadow: 0 1px 3px rgba(255,255,255,0.6);
}
h2, h3 {
    font-family: 'DM Sans', sans-serif !important;
    color: #0f172a !important;
    font-weight: 600 !important;
}
p, label { color: #1e293b !important; }
small, .subtitle { color: #334155 !important; }

/* ── Panels — solid white so text is always readable ── */
.panel {
    background: rgba(255,255,255,0.92);
    border: 1px solid rgba(255,255,255,0.7);
    border-radius: 14px;
    padding: 1.5rem 1.8rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}
.panel-title {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 1.8px;
    text-transform: uppercase;
    color: #64748b;
    margin-bottom: 1rem;
    display: block;
}

/* Stat cards */
.stat-row { display: flex; gap: 12px; margin: 1rem 0; }
.stat-card {
    flex: 1;
    background: rgba(255,255,255,0.92);
    border: 1px solid rgba(255,255,255,0.7);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    text-align: center;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07);
}
.stat-num { font-size: 1.8rem; font-weight: 700; display: block; color: #0f172a; }
.stat-lbl { font-size: 0.72rem; letter-spacing: 1px; text-transform: uppercase; color: #64748b; }
.s-total .stat-num { color: #4361ee; }
.s-sent  .stat-num { color: #16a34a; }
.s-fail  .stat-num { color: #dc2626; }
.s-skip  .stat-num { color: #d97706; }

/* Inputs */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    border: 1.5px solid #cbd5e1 !important;
    border-radius: 10px !important;
    background: #ffffff !important;
    color: #0f172a !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.92rem !important;
}
.stTextArea > div > div > textarea {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.85rem !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #4361ee !important;
    box-shadow: 0 0 0 3px rgba(67,97,238,0.15) !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #4361ee, #6d4aff) !important;
    color: #fff !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.65rem 1.8rem !important;
    font-size: 0.92rem !important;
    transition: all 0.18s;
    width: 100%;
    box-shadow: 0 4px 14px rgba(67,97,238,0.35);
}
.stButton > button:hover { opacity: 0.88 !important; transform: translateY(-1px); }

/* File uploader */
.stFileUploader > div {
    border: 1.5px dashed #94a3b8 !important;
    border-radius: 12px !important;
    background: rgba(255,255,255,0.85) !important;
}

/* Progress */
.stProgress > div > div > div { background: #4361ee !important; }

/* Preview box */
.email-preview {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.9rem;
    color: #0f172a;
    line-height: 1.7;
    white-space: pre-wrap;
}
.preview-field { color: #64748b; font-size: 0.8rem; margin-bottom: 0.2rem; }
.preview-value { color: #0f172a; font-size: 0.92rem; margin-bottom: 0.8rem; }
.tag-chip {
    display: inline-block;
    background: #eff6ff;
    color: #2563eb;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
    padding: 3px 10px;
    margin: 2px;
    font-family: 'DM Mono', monospace;
}

/* Credential banner */
.cred-banner {
    background: rgba(220,252,231,0.95);
    border: 1px solid #86efac;
    border-radius: 10px;
    padding: 0.7rem 1.2rem;
    color: #15803d !important;
    font-size: 0.88rem;
    margin-bottom: 1rem;
}

/* Expander */
div[data-testid="stExpander"] {
    background: rgba(255,255,255,0.92);
    border: 1px solid rgba(255,255,255,0.7);
    border-radius: 12px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07);
}

/* Page subtitle */
.subtitle { color: #334155; margin-top: -0.5rem; font-size: 0.95rem; }
hr { border-color: rgba(0,0,0,0.08) !important; }

/* Streamlit default label text */
.stTextInput label, .stTextArea label, .stSlider label,
.stCheckbox label, .stRadio label, .stFileUploader label {
    color: #1e293b !important;
    font-weight: 500 !important;
}

/* Slider track */
.stSlider > div { background: transparent !important; }

/* Info / success / error boxes */
.stInfo, .stSuccess, .stError, .stWarning {
    background: rgba(255,255,255,0.92) !important;
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HELPERS
# =========================
def fill_template(template_subject, template_body, row_data):
    subject = template_subject
    body = template_body
    for col, val in row_data.items():
        placeholder = "{{" + str(col) + "}}"
        subject = subject.replace(placeholder, str(val))
        body = body.replace(placeholder, str(val))
    return subject, body

def extract_placeholders(text):
    return re.findall(r"\{\{(\w+)\}\}", text)

def send_email_gmail(sender_email, app_password, recipient_email, subject, body, is_html=False):
    msg = MIMEMultipart("alternative")
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject
    mime_type = "html" if is_html else "plain"
    msg.attach(MIMEText(body, mime_type, "utf-8"))
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, app_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())

def validate_email(email):
    return bool(re.match(r"^[\w.\-+]+@[\w.\-]+\.\w{2,}$", str(email).strip()))

# =========================
# HEADER
# =========================
st.markdown("## 📧 Gmail Bulk Sender")
st.markdown("<p class='subtitle'>Send personalized outreach emails to all your clients in one go — via Gmail SMTP</p>", unsafe_allow_html=True)
st.markdown("---")

# =========================
# CREDENTIAL STATUS BANNER
# =========================
creds_ok = SENDER_EMAIL != "youremail@gmail.com" and APP_PASSWORD != "xxxx xxxx xxxx xxxx"

if creds_ok:
    st.markdown(f"""
    <div class="cred-banner">
        ✅ &nbsp;Sending as <strong>{SENDER_EMAIL}</strong> &nbsp;·&nbsp; App password loaded from code
    </div>
    """, unsafe_allow_html=True)
else:
    st.warning("⚠️ Please open this script and set your **SENDER_EMAIL** and **APP_PASSWORD** at the top of the file (lines 14–15).")

# =========================
# LAYOUT: 2 COLUMNS
# =========================
col_left, col_right = st.columns([1, 1.1], gap="large")

# ============================================================
# LEFT COLUMN — CONFIGURATION
# ============================================================
with col_left:

    # --- RECIPIENT LIST ---
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<span class="panel-title">Recipient List</span>', unsafe_allow_html=True)

    upload_mode = st.radio(
        "How to provide recipients?",
        ["Upload CSV file", "Paste emails manually"],
        horizontal=True,
        label_visibility="collapsed"
    )

    df_recipients = None
    manual_emails = []

    if upload_mode == "Upload CSV file":
        st.markdown("""
<small style='color:#7878a8;'>CSV must have an <code>email</code> column. Extra columns (e.g. <code>name</code>, <code>company</code>) become template variables.</small>
        """, unsafe_allow_html=True)
        uploaded = st.file_uploader("Upload recipient CSV", type=["csv"], label_visibility="collapsed")
        if uploaded:
            try:
                df_recipients = pd.read_csv(uploaded)
                df_recipients.columns = [c.strip().lower().replace(" ", "_") for c in df_recipients.columns]
                if "email" not in df_recipients.columns:
                    st.error("CSV must have an 'email' column.")
                    df_recipients = None
                else:
                    st.success(f"Loaded **{len(df_recipients)}** rows. Columns: `{'`, `'.join(df_recipients.columns)}`")
            except Exception as e:
                st.error(f"Could not read CSV: {e}")

    else:
        raw_emails = st.text_area(
            "Paste emails (one per line or comma-separated)",
            placeholder="client1@company.com\nclient2@firm.com\nceo@startup.io",
            height=140,
            label_visibility="collapsed"
        )
        if raw_emails.strip():
            parts = re.split(r"[\n,;]+", raw_emails)
            manual_emails = [e.strip() for e in parts if e.strip()]
            df_recipients = pd.DataFrame({"email": manual_emails})
            st.info(f"{len(manual_emails)} emails detected.")

    st.markdown('</div>', unsafe_allow_html=True)

    # --- SEND SETTINGS ---
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<span class="panel-title">Send Settings</span>', unsafe_allow_html=True)

    delay_sec = st.slider(
        "Delay between emails (seconds)",
        min_value=1, max_value=15, value=3,
        help="Adding a small delay avoids Gmail spam throttling."
    )
    is_html_body = st.checkbox("Send as HTML email", value=False, help="If checked, HTML tags in your body will render. If unchecked, plain text.")
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# RIGHT COLUMN — EMAIL TEMPLATE
# ============================================================
with col_right:

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<span class="panel-title">Email Template</span>', unsafe_allow_html=True)

    st.markdown("<small style='color:#7878a8;'>Use <code>{{column_name}}</code> for personalization. E.g. <code>{{name}}</code>, <code>{{company}}</code></small>", unsafe_allow_html=True)

    subject_template = st.text_input(
        "Subject Line",
        placeholder="Partnering with {{company}} — Technical Development Services",
    )

    body_template = st.text_area(
        "Email Body",
        placeholder="""Hi {{name}},

I came across {{company}} and was impressed by what you're building.

We're a technical startup specializing in [your service]. We'd love to help you with [specific need].

Here's what we offer:
- Service 1
- Service 2
- Service 3

Would you be open to a quick 15-minute call this week?

Best regards,
[Your Name]
[Your Company]""",
        height=320,
        label_visibility="visible"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # --- PLACEHOLDER DETECTION ---
    if subject_template or body_template:
        all_placeholders = list(set(
            extract_placeholders(subject_template) +
            extract_placeholders(body_template)
        ))
        if all_placeholders:
            chips = " ".join([f'<span class="tag-chip">{{{{{p}}}}}</span>' for p in all_placeholders])
            st.markdown(f"<div style='margin-bottom:0.8rem;'><small style='color:#7878a8;'>Placeholders detected:</small><br>{chips}</div>", unsafe_allow_html=True)

    # --- PREVIEW ---
    if df_recipients is not None and len(df_recipients) > 0 and (subject_template or body_template):
        with st.expander("👁️ Preview first email"):
            first_row = df_recipients.iloc[0].to_dict()
            prev_subject, prev_body = fill_template(subject_template, body_template, first_row)
            st.markdown(f"<p class='preview-field'>TO</p><p class='preview-value'>{first_row.get('email','')}</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='preview-field'>SUBJECT</p><p class='preview-value'>{prev_subject}</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='preview-field'>BODY</p>", unsafe_allow_html=True)
            st.markdown(f"<div class='email-preview'>{prev_body}</div>", unsafe_allow_html=True)

# =========================
# SEND SECTION
# =========================
st.markdown("---")

# Summary before send
if df_recipients is not None and len(df_recipients) > 0:
    valid_count = sum(1 for e in df_recipients["email"].astype(str) if validate_email(e))
    invalid_count = len(df_recipients) - valid_count

    st.markdown(f"""
    <div class="stat-row">
        <div class="stat-card s-total"><span class="stat-num">{len(df_recipients)}</span><span class="stat-lbl">Total</span></div>
        <div class="stat-card s-sent"><span class="stat-num">{valid_count}</span><span class="stat-lbl">Valid emails</span></div>
        <div class="stat-card s-fail"><span class="stat-num">{invalid_count}</span><span class="stat-lbl">Invalid / skipped</span></div>
        <div class="stat-card s-skip"><span class="stat-num">~{valid_count * delay_sec}s</span><span class="stat-lbl">Est. total time</span></div>
    </div>
    """, unsafe_allow_html=True)

send_col1, send_col2, send_col3 = st.columns([1, 1, 1])

with send_col2:
    send_btn = st.button("🚀 Send Emails to All Recipients")

# =========================
# SEND LOGIC
# =========================
if send_btn:
    errors = []
    if not creds_ok:
        errors.append("Set your SENDER_EMAIL and APP_PASSWORD in the script first.")
    if df_recipients is None or len(df_recipients) == 0:
        errors.append("No recipients loaded.")
    if not subject_template.strip():
        errors.append("Subject line cannot be empty.")
    if not body_template.strip():
        errors.append("Email body cannot be empty.")

    if errors:
        for e in errors:
            st.error(f"⚠️ {e}")
        st.stop()

    # Test SMTP connection first
    st.markdown("**Connecting to Gmail...**")
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, APP_PASSWORD.replace(" ", ""))
        st.success("✅ Gmail connected successfully!")
    except smtplib.SMTPAuthenticationError:
        st.error("❌ Authentication failed. Check your Gmail address and App Password. Make sure 2-Step Verification is ON.")
        st.stop()
    except Exception as ex:
        st.error(f"❌ Connection error: {ex}")
        st.stop()

    # Send loop
    results = []
    total = len(df_recipients)
    progress_bar = st.progress(0)
    status_container = st.empty()
    log_lines = []

    for i, (_, row) in enumerate(df_recipients.iterrows()):
        recipient = str(row.get("email", "")).strip()
        row_dict = row.to_dict()

        if not validate_email(recipient):
            results.append({"Email": recipient, "Status": "Skipped", "Reason": "Invalid email format"})
            log_lines.append(f"⚠️  [{i+1}/{total}] SKIP  {recipient} — invalid format")
            status_container.markdown("\n".join(log_lines[-6:]))
            continue

        try:
            subject_filled, body_filled = fill_template(subject_template, body_template, row_dict)
            send_email_gmail(
                SENDER_EMAIL,
                APP_PASSWORD.replace(" ", ""),
                recipient,
                subject_filled,
                body_filled,
                is_html=is_html_body
            )
            results.append({"Email": recipient, "Status": "Sent", "Reason": "—"})
            log_lines.append(f"✅  [{i+1}/{total}] SENT  {recipient}")

        except smtplib.SMTPRecipientsRefused:
            results.append({"Email": recipient, "Status": "Failed", "Reason": "Recipient refused by server"})
            log_lines.append(f"❌  [{i+1}/{total}] FAIL  {recipient} — refused")

        except smtplib.SMTPException as smtp_err:
            results.append({"Email": recipient, "Status": "Failed", "Reason": str(smtp_err)[:80]})
            log_lines.append(f"❌  [{i+1}/{total}] FAIL  {recipient} — {smtp_err}")

        except Exception as ex:
            results.append({"Email": recipient, "Status": "Failed", "Reason": str(ex)[:80]})
            log_lines.append(f"❌  [{i+1}/{total}] FAIL  {recipient} — {ex}")

        progress_bar.progress((i + 1) / total)
        status_container.code("\n".join(log_lines[-8:]), language=None)

        if i < total - 1:
            time.sleep(delay_sec)

    status_container.empty()
    progress_bar.progress(1.0)

    # Final summary
    df_results = pd.DataFrame(results)
    sent_count = (df_results["Status"] == "Sent").sum()
    fail_count = (df_results["Status"] == "Failed").sum()
    skip_count = (df_results["Status"] == "Skipped").sum()

    st.markdown("---")
    st.markdown("### ✅ Campaign Complete")

    st.markdown(f"""
    <div class="stat-row">
        <div class="stat-card s-total"><span class="stat-num">{total}</span><span class="stat-lbl">Total</span></div>
        <div class="stat-card s-sent"><span class="stat-num">{sent_count}</span><span class="stat-lbl">Sent</span></div>
        <div class="stat-card s-fail"><span class="stat-num">{fail_count}</span><span class="stat-lbl">Failed</span></div>
        <div class="stat-card s-skip"><span class="stat-num">{skip_count}</span><span class="stat-lbl">Skipped</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### Delivery Report")
    st.dataframe(df_results, use_container_width=True, height=300)

    csv_report = df_results.to_csv(index=False)
    st.download_button(
        "⬇️ Download Delivery Report (CSV)",
        data=csv_report,
        file_name="email_delivery_report.csv",
        mime="text/csv"
    )
