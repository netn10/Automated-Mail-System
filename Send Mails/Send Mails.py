import json
import csv
import smtplib
import sys
import time
import yagmail
from MASSAGE import MASSAGE

# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Load all the settings from the json file
try:
    with open('settings.json') as s:
        obj = s.read()
        settings = json.loads(obj)
        SENDER_EMAIL = settings["SENDER_EMAIL"]
        SENDER_PASSWORD = settings["SENDER_PASSWORD"]
except FileNotFoundError:
    print("Error: File not found. Please create settings.json in this program's folder and try again.")

# Collect all the info in separated arrays
partner_email = []
partner_name = []

try:
    with open('All_Info.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            partner_email.append(row[0])
            partner_name.append(row[1])
except FileNotFoundError:
    print("Error: File not found. Please create All_Info.csv in this program's folder and try again.")

try:
    yag = yagmail.SMTP(SENDER_EMAIL, SENDER_PASSWORD)
except Exception:
    print("Error: The email address or the password are incorrect. Please check them and try again.")
    input()
    sys.exit(0)

mails_with_errors = 0
i = -1
for email in partner_email:
    i = i + 1
    print("Sending email to: {} \n".format(partner_name[i]))
    subject = "נושא: בקשתנו לשותפות עם {}".format(partner_name[i])
    with open('All_Info.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            mail, name = row
            msg = MASSAGE.format(partner_name[i])
        time.sleep(3)
        try:
            yag.send(email, subject, msg)
        except smtplib.SMTPRecipientsRefused:
            print("Error: The recipient address is not valid.")
            mails_with_errors = mails_with_errors + 1
            continue

if mails_with_errors == 0:
    print("All emails are successfully sent.")
else:
    print("All mails are successfully sent except " + mails_with_errors)
