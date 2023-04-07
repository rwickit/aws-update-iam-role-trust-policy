import boto3
import json
import os

iam = boto3.client('iam')

def create_or_update_role(role_name, policy_file_path, trusted_account_id):
    # Define the trust policy
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "AWS": "arn:aws:iam::{trusted_account_id}:root".format(trusted_account_id=trusted_account_id)
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }

    # Write the policy to a file
    with open(policy_file_path, 'w') as policy_file:
        json.dump(trust_policy, policy_file)

    # Try to create the role
    try:
        iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(trust_policy)
        )
        print("IAM role {role_name} created successfully.".format(role_name=role_name))
    # If the role already exists, update it
    except iam.exceptions.EntityAlreadyExistsException:
        iam.update_assume_role_policy(
            RoleName=role_name,
            PolicyDocument=json.dumps(trust_policy)
        )
        print("IAM role {role_name} updated successfully.".format(role_name=role_name))
    # If the role already exists but the trust policy is different, raise an error
    except iam.exceptions.MalformedPolicyDocumentException:
        print("The role {role_name} already exists and the trust policy is different.".format(role_name=role_name))
        raise

# Create or update the role
create_or_update_role('my-role', 'policy.json', '123456789012')
