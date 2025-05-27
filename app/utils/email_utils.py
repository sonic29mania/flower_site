import smtplib

def send_code_to_email(receiver_email, code):
    sender_email = "sophioxi@gmail.com"
    sender_password = "aogy oruc kbkr atex"
    subject = "Flower Tale"
    message = f"Ваш код для входу: {code}"
    full_message = f"Subject: {subject}\nContent-Type: text/plain; charset=utf-8\n\n{message}"

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, full_message.encode("utf-8"))
    except Exception as e:
        print("Email sending error:", e)
