from flask import Flask, render_template, request, jsonify
import boto3

app = Flask(__name__)

def initialize_boto3_session(profile_name="default", region_name='us-east-1'):
    session = boto3.Session(profile_name=profile_name)
    return session.client('ec2', region_name=region_name)

ec2 = initialize_boto3_session()

@app.route('/')
def index():
    return render_template('index.html')

def launch_ec2_instance(instance_name):
    response = ec2.run_instances(
        ImageId='ami-04b70fa74e45c3917',
        InstanceType='t2.micro',
        MaxCount=1,
        MinCount=1,
        KeyName="oko_keypair1",
        SecurityGroupIds=['sg-0cc308eedbf74ac98'],
        TagSpecifications=[{'ResourceType': 'instance', 'Tags': [{'Key': 'Name', 'Value': instance_name}]}]
    )
    return response['Instances'][0]['InstanceId']

def wait_for_instance(instance_id):
    waiter = ec2.get_waiter('instance_running')
    waiter.wait(InstanceIds=[instance_id])

def get_instance_public_ip(instance_id):
    response = ec2.describe_instances(InstanceIds=[instance_id])
    return response['Reservations'][0]['Instances'][0].get('PublicIpAddress', 'N/A')

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
