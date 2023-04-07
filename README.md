# Boto Script to Create/Update IAM Role in AWS Account

## Introduction

This document outlines the steps required to create or update an IAM role in an AWS Account with a role trust for a different account ID.

## Prerequisites

1. AWS Command Line Interface (CLI) installed on your local machine.
2. IAM permissions to create or update IAM roles in the AWS Account.

## Procedure

### Using AWS CLI

You can use the AWS CLI to create or update an IAM role with a role trust for a different account ID. Follow the steps below:

1. Open a terminal window and run the following command to create a new IAM role:

```
aws iam create-role --role-name {RoleName} --assume-role-policy-document file://{PolicyFilePath}

```

Replace `{RoleName}` with the name of the IAM role you want to create and `{PolicyFilePath}` with the path to the policy document file. The policy document file should contain the role trust policy with the account ID of the trusted account.

For example, the contents of the policy document file may look like this:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::{trusted-account-id}:root"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}

```

Replace `{trusted-account-id}` with the ID of the trusted AWS account.

1. To update an existing IAM role, use the following command:

```
aws iam update-assume-role-policy --role-name {RoleName} --policy-document file://{PolicyFilePath}

```

Replace `{RoleName}` with the name of the IAM role you want to update and `{PolicyFilePath}` with the path to the policy document file.

### Using Boto3 Python Script

You can also use the Boto3 Python library to create or update an IAM role with a role trust for a different account ID. See the example script below:

```
import boto3
import json

iam = boto3.client('iam')

def create_or_update_role(role_name, policy_file_path, trusted_account_id):
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

    with open(policy_file_path, 'w') as policy_file:
        json.dump(trust_policy, policy_file)

    try:
        iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(trust_policy)
        )
        print("IAM role {role_name} created successfully.".format(role_name=role_name))
    except iam.exceptions.EntityAlreadyExistsException:
        iam.update_assume_role_policy(
            RoleName=role_name,
            PolicyDocument=json.dumps(trust_policy)
        )
        print("IAM role {role_name} updated successfully.".format(role_name=role_name))

```

Replace `{RoleName}` with the name of the IAM role you want to create or update, `{PolicyFilePath}` with the path to the policy document file, and `{trusted-account-id}` with the ID of the trusted AWS account.

To create or update an IAM role, run the `create_or_update_role()` function with the appropriate parameters:

```
create_or_update_role('my-role', '/path/to/policy.json', '123456789012')

```

## Conclusion

In this document, we have seen the steps required to create or update an IAM role in an AWS Account with a role trust for a different account ID. This script can be used to automate the process of creating or updating IAM roles with specific role trust policies.
