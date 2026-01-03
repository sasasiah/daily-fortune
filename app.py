from flask import Flask, request, render_template
from deep_translator import GoogleTranslator
import requests, math, random
from datetime import date

app = Flask(__name__)

# =======================
# Zodiac
# =======================
def get_zodiac(day, month):
    zodiacs = [
        ("capricorn", (12, 22), (1, 19)),
        ("aquarius", (1, 20), (2, 18)),
        ("pisces", (2, 19), (3, 20)),
        ("aries", (3, 21), (4, 19)),
        ("taurus", (4, 20), (5, 20)),
        ("gemini", (5, 21), (6, 20)),
        ("cancer", (6, 21), (7, 22)),
        ("leo", (7, 23), (8, 22)),
        ("virgo", (8, 23), (9, 22)),
        ("libra", (9, 23), (10, 22)),
        ("scorpio", (10, 23), (11, 21)),
        ("sagittarius", (11, 22), (12, 21)),
    ]
    for sign, start, end in zodiacs:
        if (month == start[0] and day >= start[1]) or \
           (month == end[0] and day <= end[1]):
            return sign
    return "capricorn"

# =======================
# Translate
# =======================
def translate_to_th(text):
    if not text:
        return text
    try:
        return GoogleTranslator(source="en", target="th").translate(text)
    except:
        return text

# =======================
# Horoscope
# =======================
def get_fortune(sign):
    try:
        r = requests.get(f"https://ohmanda.com/api/horoscope/{sign}", timeout=5)
        j = r.json()
        return j["horoscope"]
    except:
        return "Today is a good day to stay calm and plan your next step."

# =======================
# Numerology
# =======================
def life_path(day, month, year):
    total = sum(map(int, f"{day}{month}{year}"))
    while total > 9:
        total = sum(map(int, str(total)))
    return total

NUM_MEANING = {
    1: "Leadership and confidence",
    2: "Gentle and charming",
    3: "Creative and cheerful",
    4: "Stable and hardworking",
    5: "Freedom loving and adaptable",
    6: "Responsible and caring",
    7: "Deep thinker",
    8: "Power and success",
    9: "Kind and compassionate"
}

# =======================
# Major Arcana
# =======================
MAJOR_ARCANA = [
    ("The Fool", "New beginnings and taking risks"),
    ("The Magician", "Power, skill, and action"),
    ("The High Priestess", "Wisdom and intuition"),
    ("The Empress", "Abundance and happiness"),
    ("The Emperor", "Stability and authority"),
    ("The Hierophant", "Knowledge and guidance"),
    ("The Lovers", "Love and important choices"),
    ("The Chariot", "Determination and victory"),
    ("Strength", "Inner power and courage"),
    ("The Hermit", "Self-reflection and analysis"),
    ("Wheel of Fortune", "Change and destiny"),
    ("Justice", "Fairness and truth"),
    ("The Hanged Man", "Waiting and sacrifice"),
    ("Death", "Transformation and rebirth"),
    ("Temperance", "Balance and harmony"),
    ("The Devil", "Bondage and temptation"),
    ("The Tower", "Sudden change"),
    ("The Star", "Hope and peace"),
    ("The Moon", "Fear and illusion"),
    ("The Sun", "Joy and success"),
    ("Judgement", "Second chances"),
    ("The World", "Completion and fulfillment"),
]

def get_major_arcana():
    name, meaning = random.choice(MAJOR_ARCANA)
    return {"name": name, "meaning": meaning}

# =======================
# Biorhythm
# =======================
def biorhythm(day, month, year):
    birth = date(year, month, day)
    today = date.today()
    days = (today - birth).days
    return (
        round(math.sin(2 * math.pi * days / 23) * 100, 1),
        round(math.sin(2 * math.pi * days / 28) * 100, 1),
        round(math.sin(2 * math.pi * days / 33) * 100, 1),
    )

# =======================
# Route
# =======================
@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        name = request.form["name"]
        day = int(request.form["day"])
        month = int(request.form["month"])
        year = int(request.form["year"])
        do_translate = request.form.get("translate") == "yes"

        zodiac = get_zodiac(day, month)
        fortune = get_fortune(zodiac)

        card = get_major_arcana()
        life = life_path(day, month, year)
        phy, emo, intel = biorhythm(day, month, year)

        if do_translate:
            fortune = translate_to_th(fortune)
            card["meaning"] = translate_to_th(card["meaning"])
            life_meaning = translate_to_th(NUM_MEANING[life])
        else:
            life_meaning = NUM_MEANING[life]

        result = {
            "name": name,
            "zodiac": zodiac.capitalize(),
            "fortune": fortune,
            "card": card,
            "life_number": life,
            "life_meaning": life_meaning,
            "physical": phy,
            "emotional": emo,
            "intellectual": intel,
        }

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
