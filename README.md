## Salesforce Data Loader batch backup (windows only)

This simple script configure and execute export data for backup purposes from Salesforce.
It is using possibilty to call data loader in terminal but works only in windows

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
  path             Path to Data Loader
  object           Salesforce object to backup

optional arguments:
  -h, --help       show this help message and exit
  --fields fields  Coma separated list of fields to export, all if not selected
```

```
 py ./backup.py https://test.salesforce.com client_id client_secret username password "C:\Data Loader\salesforce.com\Data Loader\bin" Account --fields=name,lastname
```