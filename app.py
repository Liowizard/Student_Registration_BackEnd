from flask import Flask, jsonify, render_template, request, send_from_directory, session
from flask_cors import CORS

from email_otp import sendEmailVerificationRequest

app = Flask(__name__)

cors = CORS(app)


app.secret_key = "EmailAuthentication"


@app.route("/verify", methods=["POST"])
def verify():
    rec_email = request.get_json()
    rec_email = rec_email.get("email")

    print("rec_email)", rec_email)

    current_otp = sendEmailVerificationRequest(
        receiver=rec_email
    )  # this function sends otp to the receiver and also returns the same otp for our session storage
    print("current_otp", current_otp)
    session["current_otp"] = current_otp
    return current_otp


@app.route("/GetData", methods=["POST"])
def GetData():
    json_data = request.form["json_data"]
    file = request.files["file"]
    file.save("uploads/" + file.filename)
    print("data", json_data)
    return "done"


if __name__ == "__main__":
    app.run(debug=True)
