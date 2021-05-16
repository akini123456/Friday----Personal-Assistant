import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

ACCOUNT_SID = os.environ.get("ACCOUNT_SID")
AUTH_TOKEN = os.environ.get("AUTH_TOKEN")
FRIDAY = os.environ.get("FRIDAY")
ARYANFROM = os.environ.get("ARYANFROM")
ARYANSEND = os.environ.get("ARYANSEND")
IMAP = os.environ.get("IMAP")
PASSWORD = os.environ.get("PASSWORD")
EMAIL = os.environ.get("EMAIL")
ACCOUNT_SID = os.environ.get("ACCOUNT_SID")
AUTH_TOKEN = os.environ.get("AUTH_TOKEN")