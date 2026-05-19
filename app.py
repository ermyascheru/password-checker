from flask import Flask, request, render_template_string
import re
import random
import string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Password Checker</title>
    <style>
        body {
            font-family: Arial;
            background: #0f172a;
            color: white;
            text-align: center;
            padding-top: 80px;
        }

        input {
            padding: 10px;
            width: 300px;
            margin: 10px;
        }

        button {
            padding: 10px 15px;
            margin: 5px;
            cursor: pointer;
        }

        .generated {
            color: #00ff99;
            font-size: 20px;
        }

        .weak { color: red; }
        .medium { color: orange; }
        .strong { color: lime; }
    </style>
</head>
<body>

    <h1>🔐 Password Strength Checker</h1>

    <form method="POST">
        <input type="text" name="password" placeholder="Enter password">
        <br>
        <button name="check">Check Strength</button>
        <button name="generate">Generate Password</button>
    </form>

    {% if strength %}
        <h2 class="{{ strength.lower() }}">Strength: {{ strength }}</h2>
    {% endif %}

    {% if feedback %}
        <ul style="list-style:none;">
            {% for item in feedback %}
                <li>{{ item }}</li>
            {% endfor %}
        </ul>
    {% endif %}

    {% if generated %}
        <h2>Generated Password</h2>
        <p class="generated">{{ generated }}</p>
    {% endif %}

</body>
</html>
"""


def check_strength(password):
    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Use at least 8 characters")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Add uppercase letters")

    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Add lowercase letters")

    if re.search(r"[0-9]", password):
        score += 1
    else:
        feedback.append("Add numbers")

    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("Add special characters")

    if score <= 2:
        return "Weak", feedback
    elif score <= 4:
        return "Medium", feedback
    else:
        return "Strong", feedback


def generate_password(length=12):
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(chars) for _ in range(length))


@app.route("/", methods=["GET", "POST"])
def home():
    strength = None
    feedback = []
    generated = None

    if request.method == "POST":
        if "check" in request.form:
            password = request.form["password"]
            strength, feedback = check_strength(password)

        if "generate" in request.form:
            generated = generate_password()

    return render_template_string(
        HTML,
        strength=strength,
        feedback=feedback,
        generated=generated
    )


if __name__ == "__main__":
    app.run(debug=True)
