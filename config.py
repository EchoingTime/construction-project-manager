"""
@File Name: config.py
@Description: This file contains configuration settings for the flask app. Namely, 
the email server settings for sending emails using Flask-Mail. 
"""

import os
class Config:
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'patsawicki20042@gmail.com'   #os.environ.get('EMAIL_USER')
    MAIL_PASSWORD =  'pfyo jvvu ntwd plxz'        #os.environ.get('EMAIL_PASS')
    MAIL_DEFAULT_SENDER = 'patsawicki20042@gmail.com'