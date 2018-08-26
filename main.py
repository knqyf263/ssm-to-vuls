#!/usr/bin/python
# coding:utf-8

import sys
import boto3
import json
import urllib


def list_inventory_entries(client, instanceid, next_token):
    if next_token:
        return client.list_inventory_entries(
            InstanceId=instanceid,
            TypeName="AWS:Application",
            NextToken=next_token,
            MaxResults=50,
        )
    return client.list_inventory_entries(
        InstanceId=instanceid, TypeName="AWS:Application", MaxResults=50
    )


def ssm_to_vuls(instanceid, host):
    body = {"family": "redhat", "release": "7.5", "packages": {}, "runningKernel": {}}
    client = boto3.client("ssm")
    next_token = None
    while True:
        response = list_inventory_entries(client, instanceid, next_token)

        for entry in response["Entries"]:
            name = entry["Name"]
            epoch = entry.get("Epoch", 0)
            version = entry["Version"]
            release = entry["Release"]
            arch = entry["Architecture"]

            body["packages"][name] = {
                "name": name,
                "version": f"{epoch}:{version}",
                "release": release,
                "arch": arch,
            }
            if name == "kernel":
                body["runningKernel"]["release"] = f"{version}-{release}.{arch}"
        next_token = response.get("NextToken", None)
        if not next_token:
            break

    url = f"http://{host}/vuls"
    method = "POST"
    headers = {"Content-Type": "application/json"}

    json_data = json.dumps(body).encode("utf-8")
    request = urllib.request.Request(
        url, data=json_data, method=method, headers=headers
    )
    with urllib.request.urlopen(request) as response:
        response_body = response.read().decode("utf-8")
        print(response_body)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("Usage: %s <instance-id> <vuls host:port>" % sys.argv[0])

    ssm_to_vuls(sys.argv[1], sys.argv[2])
