## Salesforce Data Loader batch backup (windows only)

This simple script configures and executes export data from Salesforce for backup purposes.
It is calling data loader from terminal - Windows only

## Usage

```
$ py ./backup.py -h
usage: backup.py [-h] [--fields fields]
                 login_url client_id client_secret username password path object

Backup salesforce data

positional arguments:
  login_url        Login url to Salesforce (production or sandbox)
  client_id        Salesforce application client_id used to login
  client_secret    Salesforce application client_secret used to login
  username         User name for login
  password         User password for login
  path             Absolute path to Data Loader *.uber.jar file
  object           Salesforce object to backup

optional arguments:
  -h, --help       show this help message and exit
  --fields fields  Coma separated list of fields to export, all if not selected
```

```
 py ./backup.py https://test.salesforce.com client_id client_secret username password "C:\Data Loader\salesforce.com\Data Loader\bin" Account --fields=name,lastname
```