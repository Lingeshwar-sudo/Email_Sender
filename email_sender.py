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

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

/* ── Sky background ── */
.stApp {
    background-image: url("data:image/jpeg;base64,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");
    background-size: cover;
    background-position: center center;
    background-attachment: fixed;
    background-repeat: no-repeat;
}

.block-container { padding: 2rem 2.5rem; max-width: 1300px; }

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

/* ── FIX: Visible cursor in all inputs ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    border: 1.5px solid #cbd5e1 !important;
    border-radius: 10px !important;
    background: #ffffff !important;
    color: #0f172a !important;
    caret-color: #4361ee !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.92rem !important;
}
.stTextArea > div > div > textarea {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.85rem !important;
    caret-color: #4361ee !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #4361ee !important;
    box-shadow: 0 0 0 3px rgba(67,97,238,0.15) !important;
    outline: none !important;
    caret-color: #4361ee !important;
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

.stFileUploader > div {
    border: 1.5px dashed #94a3b8 !important;
    border-radius: 12px !important;
    background: rgba(255,255,255,0.85) !important;
}

.stProgress > div > div > div { background: #4361ee !important; }

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

.cred-banner {
    background: rgba(220,252,231,0.95);
    border: 1px solid #86efac;
    border-radius: 10px;
    padding: 0.7rem 1.2rem;
    color: #15803d !important;
    font-size: 0.88rem;
    margin-bottom: 1rem;
}

div[data-testid="stExpander"] {
    background: rgba(255,255,255,0.92);
    border: 1px solid rgba(255,255,255,0.7);
    border-radius: 12px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07);
}

.subtitle { color: #334155; margin-top: -0.5rem; font-size: 0.95rem; }
hr { border-color: rgba(0,0,0,0.08) !important; }

.stTextInput label, .stTextArea label, .stSlider label,
.stCheckbox label, .stRadio label, .stFileUploader label {
    color: #1e293b !important;
    font-weight: 500 !important;
}

.stSlider > div { background: transparent !important; }

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

def send_email_gmail(sender_email, app_password, recipient_email, subject, body, cc_list=None, is_html=False):
    msg = MIMEMultipart("alternative")
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject
    if cc_list:
        msg["Cc"] = ", ".join(cc_list)
    mime_type = "html" if is_html else "plain"
    msg.attach(MIMEText(body, mime_type, "utf-8"))
    all_recipients = [recipient_email] + (cc_list if cc_list else [])
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, app_password)
        server.sendmail(sender_email, all_recipients, msg.as_string())

def validate_email(email):
    return bool(re.match(r"^[\w.\-+]+@[\w.\-]+\.\w{2,}$", str(email).strip()))

def parse_cc_emails(raw_cc):
    """Parse and validate CC emails from a comma/newline-separated string."""
    if not raw_cc or not raw_cc.strip():
        return [], []
    parts = re.split(r"[\n,;]+", raw_cc)
    valid, invalid = [], []
    for e in parts:
        e = e.strip()
        if not e:
            continue
        if validate_email(e):
            valid.append(e)
        else:
            invalid.append(e)
    return valid, invalid

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

    # --- CC FIELD ---
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<span class="panel-title">CC (Carbon Copy)</span>', unsafe_allow_html=True)
    st.markdown("<small style='color:#7878a8;'>These addresses will be CC'd on <strong>every</strong> email sent. Separate multiple addresses with commas.</small>", unsafe_allow_html=True)

    raw_cc = st.text_area(
        "CC addresses",
        placeholder="manager@company.com, colleague@company.com",
        height=80,
        label_visibility="collapsed"
    )
    cc_valid, cc_invalid = parse_cc_emails(raw_cc)
    if cc_valid:
        st.success(f"CC: {', '.join(cc_valid)}")
    if cc_invalid:
        st.warning(f"Invalid CC emails (will be ignored): {', '.join(cc_invalid)}")

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
            if cc_valid:
                st.markdown(f"<p class='preview-field'>CC</p><p class='preview-value'>{', '.join(cc_valid)}</p>", unsafe_allow_html=True)
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
            results.append({"Email": recipient, "CC": ", ".join(cc_valid) if cc_valid else "—", "Status": "Skipped", "Reason": "Invalid email format"})
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
                cc_list=cc_valid if cc_valid else None,
                is_html=is_html_body
            )
            results.append({"Email": recipient, "CC": ", ".join(cc_valid) if cc_valid else "—", "Status": "Sent", "Reason": "—"})
            cc_note = f" (CC: {', '.join(cc_valid)})" if cc_valid else ""
            log_lines.append(f"✅  [{i+1}/{total}] SENT  {recipient}{cc_note}")

        except smtplib.SMTPRecipientsRefused:
            results.append({"Email": recipient, "CC": ", ".join(cc_valid) if cc_valid else "—", "Status": "Failed", "Reason": "Recipient refused by server"})
            log_lines.append(f"❌  [{i+1}/{total}] FAIL  {recipient} — refused")

        except smtplib.SMTPException as smtp_err:
            results.append({"Email": recipient, "CC": ", ".join(cc_valid) if cc_valid else "—", "Status": "Failed", "Reason": str(smtp_err)[:80]})
            log_lines.append(f"❌  [{i+1}/{total}] FAIL  {recipient} — {smtp_err}")

        except Exception as ex:
            results.append({"Email": recipient, "CC": ", ".join(cc_valid) if cc_valid else "—", "Status": "Failed", "Reason": str(ex)[:80]})
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
