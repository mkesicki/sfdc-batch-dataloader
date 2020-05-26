#!/usr/bin/python3 -u

import argparse
import pprint
import sfdc
import os
import subprocess
import re
import datetime

def prepareProcessFile(object, username, password, instance_url, key_file, fields ):

    pwd = os.path.dirname(os.path.realpath(__file__))

    soql = "SELECT " + ",".join(fields) + " FROM " + object.title()

    date = datetime.datetime.now().strftime("_%Y_%m_%d %H_%M")

    dest_file_path = pwd + "\\data\\" + object + date + ".csv"
    log_file_path = pwd + "\\logs\\" + object + date + ".log"
    sdl_file = pwd + "\\config\\" + object + ".sdl"
    process_file = pwd + "\\config\\process-conf.xml" #pwd + "\\config\\process-" + object +".xml"

    text="""<!DOCTYPE beans PUBLIC "-//SPRING//DTD BEAN//EN" "http://www.springframework.org/dtd/spring-beans.dtd">
<beans><bean id="csv{object_name}ExtractProcess" class="com.salesforce.dataloader.process.ProcessRunner" singleton="false">
<description>csv{object_name}Extract job gets account info from salesforce and saves info into a CSV file."</description>
        <property name="name" value="csv{object_name}ExtractProcess"/>
        <property name="configOverrideMap">
            <map>
                <entry key="sfdc.debugMessages" value="false"/>
                <entry key="sfdc.debugMessagesFile" value="{log_path}"/>
                <entry key="sfdc.endpoint" value="{instance_url}"/>
                <entry key="sfdc.username" value="{username}"/>
                <entry key="sfdc.password" value="{password}"/>
                <entry key="process.encryptionKeyFile" value="{key_file}"/>
                <entry key="sfdc.timeoutSecs" value="600"/>
                <entry key="sfdc.loadBatchSize" value="200"/>
                <entry key="sfdc.entity" value="{object_name}"/>
                <entry key="sfdc.extractionRequestSize" value="500"/>
                <entry key="sfdc.extractionSOQL" value="{soql}"/>
                <entry key="process.operation" value="extract"/>
                <entry key="process.mappingFile" value="{sdl_file}"/>
                <entry key="dataAccess.type" value="csvWrite"/>
                <entry key="dataAccess.name" value="{save_path}"/>
                <entry key="process.enableExtractSuccessOutput" value="true"/>
                <entry key="process.statusOutputDirectory" value="{log_dir}"/>
                <entry key="process.outputError" value="{log_dir}\errors.csv"/>
                <entry key="process.outputSuccess" value="{log_dir}\success.csv"/>
            </map>
        </property>
    </bean>
</beans>"""

    xml = text.format(object_name=object.title(), instance_url=instance_url, password=password, key_file=key_file, soql=soql, sdl_file=sdl_file, save_path=dest_file_path, log_path=log_file_path, username=username, log_dir=os.path.dirname(log_file_path))

    print("Store process configuration file in: " + process_file)

    f = open(process_file, "w")
    f.write(xml)
    f.close()

    return process_file

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description = 'Backup salesforce data')
    parser.add_argument('login_url', metavar = 'login_url', help = 'Login url to Salesforce (production or sandbox)')
    parser.add_argument('client_id', metavar = 'client_id', help = 'Salesforce application client_id used to login')
    parser.add_argument('client_secret', metavar = 'client_secret', help = 'Salesforce application client_secret used to login')
    parser.add_argument('username', metavar = 'username', help = 'User name for login')
    parser.add_argument('password', metavar = 'password', help = 'User password for login')
    parser.add_argument('path', metavar = 'path', help = 'Absolute path to Data Loader *.uber.jar file')
    parser.add_argument('object', metavar = 'object', help = 'Salesforce object to backup')
    parser.add_argument('--fields', metavar = 'fields', help = 'Coma separated list of fields to export, all if not selected')
    args = parser.parse_args()

    instance_url = sfdc.login(args)

    if args.fields is not None:
        fields = args.fields.split(',')
    else:
        fields = sfdc.getFields(args.object)

    pwd = os.path.dirname(os.path.realpath(__file__))
    path = args.path
    key_file = pwd + "\\key\\" + "key.key"
    logs_path = pwd + "\\logs"

    print("Encrypt password...")

    subprocess.run(["java", "-cp", path, "com.salesforce.dataloader.security.EncryptionUtil", "-k", key_file], check=True)
    result = subprocess.run(["java", "-cp", path, "com.salesforce.dataloader.security.EncryptionUtil", "-e", args.password, key_file], check=True, capture_output=True)

    lines = result.stdout.decode('utf-8').split('\n')
    password = lines[1].strip()

    sdl_file_path = "config\\" + args.object + ".sdl"
    print("Generate SDL file: " + sdl_file_path)
    sdl_file = open(sdl_file_path, "w")

    for field in fields:
        sdl_file.write(field + "=" + field + "\n")
    sdl_file.close()

    print("Generate xml config file")

    process_file = prepareProcessFile(args.object, args.username, password, args.login_url, key_file, fields)

    print(process_file)

    print("Run process")
    process_name = "csv" + args.object.title() + "ExtractProcess"
    result = subprocess.run(["java", "-cp", path, "-Dsalesforce.config.dir=" + pwd + "\\config", "com.salesforce.dataloader.process.ProcessRunner", "process.name=" + process_name ], check=True)
