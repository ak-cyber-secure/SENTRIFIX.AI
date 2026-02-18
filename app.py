from flask import Flask, render_template, request, redirect, url_for, send_file
import ollama
import csv
import os
from datetime import datetime
from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern

app = Flask(__name__)

# --- Custom Student ID Detector ---
id_pattern = Pattern(name="student_id_pattern", regex=r"\b\d{7}\b", score=0.5)
student_id_recognizer = PatternRecognizer(supported_entity="STUDENT_ID", patterns=[id_pattern])

analyzer = AnalyzerEngine()
analyzer.registry.add_recognizer(student_id_recognizer)

@app.route('/')
def home():
    # UI is now clean - no history sent to the template
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    raw_notes = request.form['notes']
    results = analyzer.analyze(text=raw_notes, entities=["PERSON", "EMAIL_ADDRESS", "STUDENT_ID"], language='en')
    
    local_map = {}
    for i, res in enumerate(results):
        placeholder = f"<{res.entity_type}_{i}>"
        real_value = raw_notes[res.start : res.end]
        local_map[placeholder] = real_value

    masked_text = raw_notes
    for placeholder, real_value in local_map.items():
        masked_text = masked_text.replace(real_value, placeholder)

    # Updated strict prompt for better Governance
    prompt = (
    f"Act as an Academic Advisor. Rewrite the following rough meeting notes into a "
    f"formal, professional summary for a student's permanent record. "
    f"Use a supportive yet professional tone. "
    f"IMPORTANT: You must include the placeholders {list(local_map.keys())} "
    f"naturally in your sentences. Do not mention that you are an AI. "
    f"Notes to summarize: {masked_text}"
)

    
    try:
        response = ollama.chat(model='llama3.2', messages=[{'role': 'user', 'content': prompt}])
        ai_summary = response['message']['content']
    except Exception as e:
        ai_summary = f"Error: {str(e)}"

    final_summary = ai_summary
    for placeholder, real_value in local_map.items():
        final_summary = final_summary.replace(placeholder, real_value)

    return render_template('index.html', masked=masked_text, summary=final_summary)

@app.route('/approve', methods=['POST'])
def approve():
    summary_to_save = request.form['summary_text']
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # Save to Local CSV behind the scenes
    with open("student_records.csv", "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, summary_to_save, "VERIFIED"])
    
    return redirect(url_for('home'))

# NEW: One-click download route
@app.route('/download')
def download():
    if os.path.exists("student_records.csv"):
        return send_file("student_records.csv", as_attachment=True)
    return "No records found yet."

if __name__ == '__main__':
    app.run(debug=True, port=5000)