from flask import Flask, render_template, request, jsonify
from tuneai_integration import analyze_github_profile

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    tuneAI_response = analyze_github_profile(user_input)
    # tuneAI_response = "okay broooo"
    # For simplicity, echoing user input (replace this with any processing logic you need)
    bot_response = f"{tuneAI_response}"
    return jsonify({"response": bot_response})

if __name__ == "__main__":
    # app.run(debug=True)
    app.run(port=7788)
