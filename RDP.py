import boto3
from botocore.exceptions import ClientError
import os

def fetch_rdp_file(instance_id, region_name):
    # Create a Boto3 EC2 client
    ec2_client = boto3.client('ec2', region_name=region_name)

    try:
        # Get the instance details
        response = ec2_client.describe_instances(InstanceIds=[instance_id])
        instance = response['Reservations'][0]['Instances'][0]

        # Extract public IP address or public DNS name
        if 'PublicIpAddress' in instance:
            public_ip = instance['PublicIpAddress']
        elif 'PublicDnsName' in instance:
            public_ip = instance['PublicDnsName']
        else:
            print(f"No Public IP address or DNS name found for instance {instance_id}.")
            return

        # Construct RDP file content
        rdp_content = f"""\
full address:s:{public_ip}
username:s:test
password 51:s:Oko@123
"""

        # Write RDP content to a file
        rdp_filename = f"{instance_id}.rdp"
        with open(rdp_filename, 'w') as rdp_file:
            rdp_file.write(rdp_content)

        print(f"RDP file '{rdp_filename}' created successfully.")

        # Open the RDP file
        os.system(f"mstsc {rdp_filename}")

    except ClientError as e:
        print(f"Error fetching RDP file: {e}")

# Example usage
if __name__ == '__main__':
    instance_id = input("Enter your instance ID: ").strip()
    region_name = 'us-east-1'  # Mumbai region
    fetch_rdp_file(instance_id, region_name)
