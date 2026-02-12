from flask import Flask, render_template, request, redirect, url_for
import smtplib
from email.message import EmailMessage
import os

app = Flask(__name__)

EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        interest = request.form.get("interest")
        message = request.form.get("message")

        if not all([first_name, last_name, email, interest, message]):
            return redirect(url_for("index"))

        # Only try sending mail if credentials exist
        if EMAIL_ADDRESS and EMAIL_PASSWORD:
            try:
                msg = EmailMessage()
                msg["Subject"] = "New SMJ Expedition Enquiry"
                msg["From"] = EMAIL_ADDRESS
                msg["To"] = EMAIL_ADDRESS

                msg.set_content(f"""
New enquiry received

First Name: {first_name}
Last Name: {last_name}
Email: {email}
Interest: {interest}

Message:
{message}
                """)

                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                    server.send_message(msg)

            except Exception as e:
                print("Email sending failed:", e)

        # Always redirect even if email fails
        return redirect(url_for("index"))

    return render_template("index.html")


if __name__ == "__main__":
    app.run()
