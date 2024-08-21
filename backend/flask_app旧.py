from flask import Flask, jsonify, request, render_template
import subprocess
import webview
import threading

app = Flask(__name__, static_folder='static', template_folder='templates')

def list_ports():
    result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True)
    lines = result.stdout.splitlines()

    ports = []
    for line in lines:
        if "LISTENING" in line or "ESTABLISHED" in line:
            parts = line.split()
            if len(parts) >= 5:
                local_address = parts[1]
                pid = parts[4]
                state = parts[3]
                port = local_address.split(':')[-1]
                ports.append({"pid": pid, "port": port, "state": state})
    return ports

@app.route('/')
def index():
    return render_template('index.html')  # 返回Vue构建后的HTML

@app.route('/api/ports', methods=['GET'])
def get_ports():
    ports = list_ports()
    return jsonify(ports)

@app.route('/api/kill', methods=['POST'])
def kill_process():
    data = request.json
    pid = data.get("pid")
    try:
        result = subprocess.run(['taskkill', '/F', '/PID', str(pid)], capture_output=True, text=True)
        if "成功" in result.stdout:
            return jsonify({"status": "success", "message": f"成功终止PID为 {pid} 的进程。"})
        else:
            return jsonify({"status": "error", "message": result.stdout})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

def start_flask():
    app.run(host='127.0.0.1', port=5000)

if __name__ == '__main__':
    # 在后台线程启动 Flask
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # 启动 WebView
    webview.create_window("端口管理工具", "http://127.0.0.1:5000")
    webview.start()
