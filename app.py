from flask import Flask, render_template, request, redirect, send_file
import sqlite3
import os

from werkzeug.utils import secure_filename
from reportlab.pdfgen import canvas

from translator import translate_text
from grammar import correct_text
from ocr import image_to_text

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ---------------- HOME ----------------

@app.route("/", methods=["GET", "POST"])
def home():

    translated = ""
    source = ""
    corrected = ""

    if request.method == "POST":

        text = request.form["text"]

        target = request.form["target"]

        corrected = correct_text(text)

        source, translated = translate_text(corrected, target)

        conn = sqlite3.connect("database.db")

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO history
            (source_language,target_language,original_text,translated_text)
            VALUES(?,?,?,?)
            """,
            (source, target, corrected, translated)
        )

        conn.commit()
        conn.close()

    return render_template(
        "index.html",
        translated=translated,
        source=source,
        corrected=corrected
    )


# ---------------- IMAGE OCR ----------------

@app.route("/image", methods=["POST"])
def image():

    file = request.files["image"]

    filename = secure_filename(file.filename)

    path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    file.save(path)

    text = image_to_text(path)

    source, translated = translate_text(text, "te")

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO history
        (source_language,target_language,original_text,translated_text)
        VALUES(?,?,?,?)
        """,
        (source, "te", text, translated)
    )

    conn.commit()

    conn.close()

    return render_template(
        "index.html",
        translated=translated,
        source=source,
        corrected=text
    )


# ---------------- HISTORY ----------------

@app.route("/history")
def history():

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM history ORDER BY id DESC"
    )

    rows = cursor.fetchall()

    conn.close()

    return render_template(
        "history.html",
        rows=rows
    )


# ---------------- FAVORITES ----------------

@app.route("/favorite", methods=["POST"])
def favorite():

    original = request.form["original"]

    translated = request.form["translated"]

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS favorites(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        original TEXT,
        translated TEXT
        )
        """
    )

    cursor.execute(
        """
        INSERT INTO favorites(original,translated)
        VALUES(?,?)
        """,
        (original, translated)
    )

    conn.commit()

    conn.close()

    return redirect("/")


# ---------------- FAVORITES PAGE ----------------

@app.route("/favorites")
def favorites():

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM favorites ORDER BY id DESC"
    )

    rows = cursor.fetchall()

    conn.close()

    return render_template(
        "favorites.html",
        rows=rows
    )


# ---------------- DASHBOARD ----------------

@app.route("/dashboard")
def dashboard():

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM history"
    )

    total = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT target_language,
        COUNT(*)
        FROM history
        GROUP BY target_language
        """
    )

    languages = cursor.fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        total=total,
        languages=languages
    )


# ---------------- DOWNLOAD PDF ----------------

@app.route("/download")
def download():

    text = request.args.get("text")

    filename = "translation.pdf"

    c = canvas.Canvas(filename)

    c.setFont("Helvetica-Bold", 18)

    c.drawString(
        150,
        800,
        "AI Language Translator"
    )

    c.setFont("Helvetica", 14)

    c.drawString(
        50,
        750,
        "Translated Text:"
    )

    c.drawString(
        50,
        720,
        text
    )

    c.save()

    return send_file(
        filename,
        as_attachment=True
    )


# ---------------- RUN ----------------

if __name__ == "__main__":

    app.run(debug=True)
    