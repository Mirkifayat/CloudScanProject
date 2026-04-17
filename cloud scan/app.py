from flask import Flask, render_template, request, jsonify
import subprocess
import re
import os
import shutil

app = Flask(__name__)

# Helper to find Nmap path (Works on Windows and Linux/Docker)
def get_nmap_path():
    path = shutil.which("nmap")
    if path:
        return path
    # Fallback for Docker environment
    return "/usr/bin/nmap"

# Security: Only allow valid IP addresses or domain names
def is_safe_input(target):
    pattern = r"^[a-zA-Z0-9.-]+$"
    return re.match(pattern, target)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    data = request.json
    target = data.get('target')

    if not target or not is_safe_input(target):
        return jsonify({"error": "Invalid or unsafe target input"}), 400

    try:
        nmap_path = get_nmap_path()
        
        # Using -F (Fast), -Pn (No Ping), and --script=vuln for Cyber depth
       # Added -T4 for speed and -max-retries to stop Nmap from trying too hard on blocked ports
        command = [nmap_path, "-F", "-Pn", "-sV", "-T4", "--max-retries", "1", "--script=vuln", target]
        
        # Timeout set to 150 seconds because 'vuln' scripts take time
        result = subprocess.run(command, capture_output=True, text=True, timeout=150)
        
        if result.returncode == 0:
            return jsonify({"results": result.stdout})
        else:
            return jsonify({"error": "Nmap Error", "details": result.stderr}), 500
            
    except subprocess.TimeoutExpired:
        return jsonify({"error": "The scan timed out. Vulnerability scripts require more time or the target is blocking us."}), 408
    except Exception as e:
        return jsonify({"error": f"System Error: {str(e)}"}), 500

if __name__ == '__main__':
    # Render uses the PORT environment variable
    port = int(os.environ.get("PORT", 10000))
    # host='0.0.0.0' is REQUIRED for cloud deployment
    app.run(host='0.0.0.0', port=port)