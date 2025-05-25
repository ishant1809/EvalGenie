from flask import Flask, render_template, request
from PIL import Image
import io
import easyocr
import os

app = Flask(__name__)
reader = easyocr.Reader(['en'])  # Load once at startup

@app.route("/", methods=["GET", "POST"])
def index():
    result = {}
    if request.method == "POST":
        file = request.files.get("file")
        reference = request.form.get("reference", "")
        if file:
            image_bytes = file.read()
            image = Image.open(io.BytesIO(image_bytes))

            # OCR with EasyOCR
            output = reader.readtext(image_bytes, detail=0)
            extracted = " ".join(output).strip()

            # Scoring
            if extracted.lower() == reference.strip().lower():
                score = 1
                feedback = "Perfect match!"
            else:
                score = 0
                feedback = "Mismatch. Please review the answer."

            result = {
                "extracted": extracted,
                "score": score,
                "feedback": feedback
            }
    return render_template("index.html", **result)

if __name__ == "__main__":
    app.run(debug=True)
