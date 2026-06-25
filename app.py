from flask import Flask, render_template_string, request, send_file
from fpdf import FPDF
import io

app = Flask(__name__)

# The Modern Claymorphism UI Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ResuMake | Claymorphism</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {
            background: linear-gradient(135deg, #fbc2eb 0%, #a6c1ee 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .clay-container {
            border-radius: 40px;
            background: rgba(255, 255, 255, 0.7);
            backdrop-filter: blur(15px);
            box-shadow: 20px 20px 60px rgba(0,0,0,0.1), 
                        -20px -20px 60px rgba(255,255,255,0.5);
            padding: 40px;
            width: 100%;
            max-width: 700px;
        }
        .clay-input {
            border-radius: 15px;
            background: #f0f0f0;
            box-shadow: inset 5px 5px 10px #c7c7c7, 
                        inset -5px -5px 10px #ffffff;
            border: none;
            padding: 15px;
            width: 100%;
            margin-bottom: 15px;
        }
        .clay-button {
            border-radius: 20px;
            background: #86efac;
            box-shadow: 8px 8px 16px #71cb92, -8px -8px 16px #9bffc6;
            color: #ffffff;
            font-weight: bold;
            font-size: 1.2rem;
            padding: 20px;
            width: 100%;
            cursor: pointer;
            transition: transform 0.1s;
        }
        .clay-button:active { transform: scale(0.98); }
    </style>
</head>
<body>
    <div class="clay-container">
        <h1 class="text-4xl font-bold text-blue-700 mb-6 text-center">🚀 ResuMake</h1>
        <form action="/generate" method="post">
            <div class="grid grid-cols-2 gap-4">
                <input type="text" name="name" placeholder="Full Name" required class="clay-input">
                <input type="text" name="phone" placeholder="Phone Number" required class="clay-input">
            </div>
            <input type="email" name="email" placeholder="Email Address" required class="clay-input">
            <input type="text" name="education" placeholder="Education (Degree, University)" required class="clay-input">
            <textarea name="experience" placeholder="Experience (Role, Company, Achievements)" class="clay-input h-24"></textarea>
            <input type="text" name="skills" placeholder="Skills (e.g., Python, SQL, React)" class="clay-input">
            <textarea name="project" placeholder="Top Project (Name, Tech Stack, Impact)" required class="clay-input h-24"></textarea>
            <button type="submit" class="clay-button">Download PDF Resume</button>
        </form>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/generate', methods=['POST'])
def generate():
    data = {k: request.form.get(k) for k in ['name', 'phone', 'email', 'education', 'experience', 'skills', 'project']}
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 22)
    pdf.cell(0, 15, txt=data['name'], ln=True, align='C')
    pdf.set_font("Arial", size=11)
    pdf.cell(0, 5, txt=f"{data['email']} | {data['phone']}", ln=True, align='C')
    pdf.ln(10)
    
    for title, content in [("Education", data['education']), ("Experience", data['experience']), 
                           ("Skills", data['skills']), ("Projects", data['project'])]:
        if content:
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(0, 10, txt=title, ln=True)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(2)
            pdf.set_font("Arial", size=11)
            pdf.multi_cell(0, 7, txt=content)
            pdf.ln(5)

    buffer = io.BytesIO(pdf.output(dest='S'))
    return send_file(buffer, mimetype='application/pdf', as_attachment=True, download_name="Resume.pdf")

if __name__ == '__main__':
    app.run(debug=True)