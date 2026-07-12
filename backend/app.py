from flask import Flask, request, jsonify
from flask_cors import CORS
import db
import hashlib

app = Flask(__name__)
CORS(app)

@app.route("/register", methods=["POST"])
def register():
    data     = request.json
    name     = data.get("name", "").strip()
    email    = data.get("email", "").strip()
    password = data.get("password", "")
    if not name or not email or not password:
        return jsonify({"message": "All fields are required"}), 400
    conn = db.get_conn()
    cur  = conn.cursor()
    cur.execute("SELECT id FROM users WHERE email=%s", (email,))
    if cur.fetchone():
        cur.close(); conn.close()
        return jsonify({"message": "Email already registered"}), 409
    hashed = hashlib.sha256(password.encode()).hexdigest()
    cur.execute("INSERT INTO users (name, email, password) VALUES (%s,%s,%s)", (name, email, hashed))
    conn.commit()
    cur.close(); conn.close()
    return jsonify({"message": "Registered successfully"}), 201

@app.route("/login", methods=["POST"])
def login():
    data     = request.json
    email    = data.get("email", "").strip()
    password = data.get("password", "")
    hashed   = hashlib.sha256(password.encode()).hexdigest()
    conn = db.get_conn()
    cur  = conn.cursor(dictionary=True)
    cur.execute("SELECT id, name FROM users WHERE email=%s AND password=%s", (email, hashed))
    user = cur.fetchone()
    cur.close(); conn.close()
    if not user:
        return jsonify({"message": "Invalid email or password"}), 401
    # Check if profile exists
    conn2 = db.get_conn()
    cur2  = conn2.cursor()
    cur2.execute("SELECT id FROM profiles WHERE user_id=%s", (user["id"],))
    has_profile = cur2.fetchone() is not None
    cur2.close(); conn2.close()
    return jsonify({"user_id": user["id"], "name": user["name"], "has_profile": has_profile}), 200

@app.route("/profile", methods=["POST"])
def save_profile():
    data       = request.json
    user_id    = data.get("user_id")
    education  = data.get("education", "")
    department = data.get("department", "")
    language   = data.get("language", "English")
    interests  = data.get("interests", "")
    skills     = ",".join(data.get("skills", []))
    conn = db.get_conn()
    cur  = conn.cursor()
    cur.execute("""
        INSERT INTO profiles (user_id, education, department, skills, interests, language)
        VALUES (%s,%s,%s,%s,%s,%s)
        ON DUPLICATE KEY UPDATE
          education=%s, department=%s, skills=%s, interests=%s, language=%s
    """, (user_id, education, department, skills, interests, language,
          education, department, skills, interests, language))
    conn.commit()
    cur.close(); conn.close()
    return jsonify({"message": "Profile saved"}), 200

@app.route("/assessment", methods=["POST"])
def save_assessment():
    data          = request.json
    user_id       = data.get("user_id")
    answers       = data.get("answers", {})
    technical     = answers.get("technical", 0)
    communication = answers.get("communication", 0)
    aptitude      = answers.get("aptitude", 0)
    logical       = answers.get("logical", 0)
    domain        = answers.get("domain", 0)
    overall       = round((technical + communication + aptitude + logical + domain) / 5)
    level         = "Beginner" if overall < 40 else "Intermediate" if overall < 71 else "Advanced"
    conn = db.get_conn()
    cur  = conn.cursor()
    cur.execute("""
        INSERT INTO assessments (user_id, technical, communication, aptitude, logical, domain, overall, level)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        ON DUPLICATE KEY UPDATE
          technical=%s, communication=%s, aptitude=%s, logical=%s, domain=%s, overall=%s, level=%s
    """, (user_id, technical, communication, aptitude, logical, domain, overall, level,
          technical, communication, aptitude, logical, domain, overall, level))
    conn.commit()
    cur.close(); conn.close()
    return jsonify({"level": level, "overall": overall}), 200

@app.route("/dashboard/<int:user_id>", methods=["GET"])
def get_dashboard(user_id):
    conn = db.get_conn()
    cur  = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM profiles WHERE user_id=%s", (user_id,))
    profile = cur.fetchone() or {}
    cur.execute("SELECT * FROM assessments WHERE user_id=%s", (user_id,))
    assessment = cur.fetchone() or {}
    cur.close(); conn.close()
    filled = sum([bool(profile.get("education")), bool(profile.get("department")), bool(profile.get("skills")), bool(profile.get("interests")), bool(profile.get("language")), bool(assessment)])
    profile_completion = round((filled / 6) * 100)
    overall_score = assessment.get("overall", 0)
    level = assessment.get("level", "Beginner")
    skill_categories = {"programming": assessment.get("technical", 0), "problem_solving": assessment.get("logical", 0), "data_structures": assessment.get("aptitude", 0), "web_dev": assessment.get("technical", 0), "database": assessment.get("domain", 0), "communication": assessment.get("communication", 0)}
    career_map = {
        "Beginner":     [{"career":"Junior Web Developer","match":80},{"career":"Data Entry Analyst","match":72},{"career":"IT Support","match":65},{"career":"Junior Python Dev","match":60},{"career":"QA Tester","match":55}],
        "Intermediate": [{"career":"Full Stack Developer","match":85},{"career":"Data Analyst","match":80},{"career":"Backend Developer","match":75},{"career":"ML Engineer","match":70},{"career":"Software Engineer","match":65}],
        "Advanced":     [{"career":"Data Scientist","match":92},{"career":"AI/ML Engineer","match":88},{"career":"Full Stack Developer","match":82},{"career":"Software Architect","match":78},{"career":"Cloud Engineer","match":72}],
    }
    focus_map = {
        "Beginner":     [{"name":"Python Basics","priority":"High"},{"name":"HTML & CSS","priority":"High"},{"name":"Git Basics","priority":"Medium"},{"name":"SQL Fundamentals","priority":"Medium"},{"name":"Problem Solving","priority":"Low"}],
        "Intermediate": [{"name":"Machine Learning","priority":"High"},{"name":"Data Structures","priority":"High"},{"name":"REST APIs","priority":"Medium"},{"name":"System Design","priority":"Medium"},{"name":"Cloud Basics","priority":"Low"}],
        "Advanced":     [{"name":"Deep Learning","priority":"High"},{"name":"MLOps","priority":"High"},{"name":"Distributed Systems","priority":"Medium"},{"name":"Research Papers","priority":"Medium"},{"name":"Open Source","priority":"Low"}],
    }
    return jsonify({
        "profile_completion": profile_completion, "overall_score": overall_score,
        "skills_identified": len(profile.get("skills","").split(",")) if profile.get("skills") else 0,
        "career_matches": len(career_map.get(level, [])), "courses_recommended": max(overall_score // 8, 5),
        "skill_categories": skill_categories,
        "assessment": {"technical": assessment.get("technical",0), "aptitude": assessment.get("aptitude",0), "logical": assessment.get("logical",0), "communication": assessment.get("communication",0), "domain": assessment.get("domain",0), "overall": overall_score},
        "recommendations": career_map.get(level, career_map["Beginner"]),
        "focus_skills": focus_map.get(level, focus_map["Beginner"]),
        "level": level,
    }), 200

@app.route("/learning-path/<int:user_id>", methods=["GET"])
def learning_path(user_id):
    conn = db.get_conn()
    cur  = conn.cursor(dictionary=True)
    cur.execute("SELECT level FROM assessments WHERE user_id=%s", (user_id,))
    row = cur.fetchone()
    cur.close(); conn.close()
    level = row["level"] if row else "Beginner"
    paths = {
        "Beginner":     [{"step":1,"title":"Python Fundamentals","provider":"freeCodeCamp","duration":"4 weeks","type":"Course"},{"step":2,"title":"HTML, CSS & JavaScript","provider":"The Odin Project","duration":"3 weeks","type":"Course"},{"step":3,"title":"Git & GitHub","provider":"GitHub Lab","duration":"1 week","type":"Course"},{"step":4,"title":"SQL Basics","provider":"SQLZoo","duration":"2 weeks","type":"Course"},{"step":5,"title":"Build Portfolio Project","provider":"Self","duration":"2 weeks","type":"Project"}],
        "Intermediate": [{"step":1,"title":"Data Structures & Algorithms","provider":"LeetCode","duration":"6 weeks","type":"Practice"},{"step":2,"title":"REST API with Flask","provider":"Coursera","duration":"3 weeks","type":"Course"},{"step":3,"title":"Machine Learning","provider":"Andrew Ng","duration":"8 weeks","type":"Course"},{"step":4,"title":"SQL Advanced","provider":"Mode Analytics","duration":"2 weeks","type":"Course"},{"step":5,"title":"ML Mini Project","provider":"Kaggle","duration":"3 weeks","type":"Project"}],
        "Advanced":     [{"step":1,"title":"Deep Learning","provider":"deeplearning.ai","duration":"10 weeks","type":"Course"},{"step":2,"title":"MLOps","provider":"Google Cloud","duration":"4 weeks","type":"Certification"},{"step":3,"title":"System Design","provider":"Educative.io","duration":"4 weeks","type":"Course"},{"step":4,"title":"Open Source","provider":"GitHub","duration":"Ongoing","type":"Project"},{"step":5,"title":"AI Research","provider":"ArXiv","duration":"Ongoing","type":"Research"}],
    }
    return jsonify({"level": level, "path": paths.get(level, paths["Beginner"])}), 200

if __name__ == "__main__":
    app.run(debug=True)