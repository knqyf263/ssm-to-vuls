# ssm-to-vuls
Collect package list from System Manager and Send them to Vuls server

## Usage

```
$ pipenv install
```

Specify your AWS instance id and Vuls server domain name or IP address

```
$ pipenv run python main.py
Usage: main.py <instance-id> <vuls host:port>

$ pipenv run python main.py i-XXXXXXXXXXXXXX localhost:5515
```
