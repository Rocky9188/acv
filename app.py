from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__, template_folder="web")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/result")
def result():
    passport = request.args.get("passport_number", "").strip()
    occupation = request.args.get("occupation_key", "").strip()
    nationality = request.args.get("nationality_id", "").strip()
    locale = request.args.get("locale", "en")

    if not passport or not occupation or not nationality:
        return jsonify({"error": "Missing params"}), 400

    url = (
        "https://svp-international-api.pacc.sa/api/v1/visitor_space/labors"
        f"?passport_number={passport}&occupation_key={occupation}"
        f"&nationality_id={nationality}&locale={locale}"
    )

    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        return jsonify({"error": f"Upstream error: {str(e)}"}), 502

    # নিরাপত্তার জন্য প্রত্যাশিত কী না থাকলে ডিফল্ট দিয়ে দিচ্ছি
    return jsonify({
        "exam_result": data.get("exam_result"),
        "exam_date": data.get("exam_date"),
        "test_center_name": data.get("test_center_name"),
    })

if __name__ == "__main__":
    # 5000 ব্যস্ত থাকলে 5001 ব্যবহার করতে পারেন
    app.run(host="0.0.0.0", port=5000)
