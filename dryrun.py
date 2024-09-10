from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def launch_ec2_instance(instance_name):
    return "i-1234567890abcdef0"

def wait_for_instance(instance_id):
    pass

def get_instance_public_ip(instance_id):
    return "203.0.113.0"

@app.route('/launch_instance', methods=['POST'])
def launch_instance():
    try:
        instance_name = request.form['instance_name']
        instance_id = launch_ec2_instance(instance_name)
        wait_for_instance(instance_id)
        public_ip = get_instance_public_ip(instance_id)
        return jsonify({'instance_id': instance_id, 'public_ip': public_ip, 'instance_name': instance_name})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
