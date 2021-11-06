import random
from flask import jsonify,make_response
import smtplib
from cachetools import cached, TTLCache

from random import randint
from models import *

code_cache=TTLCache(maxsize=1024, ttl=1800)

# @cached(cache=code_cache)
def cache_code(email_id):
    range_start = 10**(4-1)
    range_end = (10**4)-1
    code_cache[email_id] = randint(range_start, range_end)
    return code_cache[email_id]

def send_otp(name, _email_list, otp):
    host = 'smtp.gmail.com'
    port = 587
    email = "smashx2018@gmail.com"
    password = "tedaaststewbwlhk"
    subject = "Verification"
    mail_to = _email_list
    mail_from = email
    body = f"Hi {name}, \n\n Your Verification Code is : {otp}\n\n "
    # return u_id
    message = """From: %s\nTo:
    %s\nSubject:
    %s\n\n%s""" % (mail_from, mail_to, subject, body)
    try:
        server = smtplib.SMTP(host, port)
        server.ehlo()
        server.starttls()
        server.login(email, password)
        server.sendmail(mail_from, mail_to, message)
        server.close()
        return 1
    except Exception as e:
        print(e)
        return make_response(jsonify({'msg': 'Bad request'}))

def auto_pass():
    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890@#$%&?*"
    character_list = [random.choice(characters) for i in range(6)]
    password = "".join(character_list)
    return password

def send_user_email(name, email, _email_list, psw):
    host = 'smtp.gmail.com'
    port = 587
    email = "smashx2018@gmail.com"
    password = "tedaaststewbwlhk"
    subject = "Christian Chair Profile"
    mail_to = _email_list
    body = f"Hi {name}, \n\n You Profile is Successfully Created .\n\n Your Username : {email}\n\nYour Password : {psw}\n\nYou may please change your password \n\nTHIS IS A SYSTEM GENERATED EMAIL - PLEASE DO NOT REPLY DIRECTLY TO THIS EMAIL "
    # return u_id
    message = """From: %s\nTo:
    %s\nSubject:
    %s\n\n%s""" % (email, mail_to, subject, body)
    try:
        server = smtplib.SMTP(host, port)
        server.ehlo()
        server.starttls()
        server.login(email, password)
        server.sendmail(email, mail_to, message)
        server.close()
        return 1
    except Exception as e:
        print(e)
        return make_response(jsonify({'msg': 'Bad request'}))
    
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS