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


@app.route('/api/ports', methods=['GET'])
def get_ports():
    # 获取分页和搜索参数
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    search = request.args.get('search', '')

    ports = list_ports()

    # 搜索过滤
    if search:
        ports = [port for port in ports if search in port['port']]

    # 实现分页
    total = len(ports)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_ports = ports[start:end]

    return jsonify({
        "total": total,
        "page": page,
        "per_page": per_page,
        "ports": paginated_ports
    })


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
@app.route('/')
def index():
    return render_template('index.html')  # 返回Vue构建后的HTML

def start_flask():
    app.run(host='127.0.0.1', port=5000)


if __name__ == '__main__':
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.daemon = True
    flask_thread.start()

    webview.create_window("端口管理工具", "http://127.0.0.1:5000")
    webview.start()
