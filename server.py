from flask import Flask, request, render_template
import requests
import os
#الارسال للسحابه 
import smtplib
from email.message import EmailMessage

def send_to_email(filepath, filename):
    msg = EmailMessage()
    msg["Subject"] = f"ملف جديد: {filename}"
    msg["From"] = "your@email.com"
    msg["To"] = "target@email.com"
    msg.set_content("تم رفع الملف إلى الأرشيف")

    with open(filepath, "rb") as f:
        msg.add_attachment(f.read(), maintype="application", subtype="octet-stream", filename=filename)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login("your@email.com", "password")
        smtp.send_message(msg)
#اخر الارسال للسحابه 

app = Flask(__name__)
import os

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    files = request.files.getlist("file")
    folder = request.form.get("folder", "عام")
    os.makedirs("uploads", exist_ok=True)

    for file in files:
        filename = file.filename
        filepath = os.path.join("uploads", filename)
        file.save(filepath)

        # إرسال الملف إلى البوت
        tg_files = {"document": open(filepath, "rb")}
        data = {
            "chat_id": CHAT_ID,
            "caption": f"📁 {folder} | 📄 {filename}",
        }
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument", data=data, files=tg_files)

    return "✅ تم إرسال جميع الملفات بنجاح"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
