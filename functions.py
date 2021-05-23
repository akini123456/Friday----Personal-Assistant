import yfinance as yf
import requests
from bs4 import BeautifulSoup
import settings
import time
import imaplib
import email
from datetime import datetime, date
import pytz
from pushbullet import Pushbullet

# Dates for months
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# Variables for message formatting
nl = '\n'
section = "---------------------------"
qu = '\"'

# Scraping URLs
weatherURL = "https://weather.com/weather/today/l/d09a05ad08a76e98925aa15e3bdcab867c9ee8c0b8c3c8c11f99efadfce43c30"
quoteOfTheDayURL = "https://www.brainyquote.com/quote_of_the_day"
techCrunchURL = "https://techcrunch.com/"
commandsFridayLink = "https://friday-pa.glitch.me/#commands"

# Assistant Functions
def readStockPrice(companySymbol):
    message = ""
    try:
        companyInfo = yf.Ticker(companySymbol)
        message += companyInfo.info['shortName'] + nl + section + nl
        message += "Sym: " + companyInfo.info['symbol'] + nl + "Web: " + companyInfo.info['website'] + nl + section + nl
        message += "Ask: $" + str(companyInfo.info['ask']) + nl + "Low: $" + str(companyInfo.info['regularMarketDayLow']) + nl + "High: $" + str(companyInfo.info['regularMarketDayHigh']) + nl + section
    except:
        message = "Mr. Kini, the symbol is either invalid or has no data"
    return message
  
def getLatestNews():
    message = ""
    message += "Hi Mr. Kini, here is the latest tech news available..." + nl + section + nl

    techCrunchData = BeautifulSoup(requests.get(techCrunchURL).content, 'html.parser')
    articles = techCrunchData.findAll('a', class_='post-block__title__link')
    for x in range(0, 3):
        message += str(articles[x]['href'])
        if x != 2:
            message += '\n' + '\n'

    message += nl + section
    return message

def emergency(originalMessage):
  message = ""
  message += "Mr. Kini has gotten into an emergency! This was his message..." + nl + section + nl + originalMessage
  return message
  
def dailyUpdate():
    message = ""
    message += "Good Morning Mr. Kini, " + nl + section + nl + "Weather:" + nl + "East Brunswick, NJ" + nl
    weatherData = BeautifulSoup(requests.get(weatherURL).content, 'html.parser')
    currentTemperature = weatherData.find('span', class_='CurrentConditions--tempValue--3KcTQ').text
    highLowTemperature = weatherData.find_all('span')
    message += "Current: " + currentTemperature + nl + "Low: " + highLowTemperature[33].text + nl + "High: " + \
               highLowTemperature[32].text + nl + section + nl
    techCrunchData = BeautifulSoup(requests.get(techCrunchURL).content, 'html.parser')
    articles = techCrunchData.findAll('a', class_='post-block__title__link')
    for x in range(0, 3):
        message += str(articles[x]['href'])
        if x != 2:
            message += '\n' + '\n'
    message += nl + section + nl
    quoteData = BeautifulSoup(requests.get(quoteOfTheDayURL).content, 'html.parser')
    quote = quoteData.findAll('a', title='view quote')[1].text
    quoteAuthor = quoteData.find('a', title='view author').text
    message += '"' + quote + '"' + " --" + quoteAuthor
    return message
  
def weatherCheck():
    message = ""
    message += nl + section + nl + "Weather:" + nl + "East Brunswick, NJ" + nl
    weatherData = BeautifulSoup(requests.get(weatherURL).content, 'html.parser')
    currentTemperature = weatherData.find('span', class_='CurrentConditions--tempValue--3KcTQ').text
    highLowTemperature = weatherData.find_all('span')
    message += "Current: " + currentTemperature + nl + "Low: " + highLowTemperature[33].text + nl + "High: " + highLowTemperature[32].text + nl + section
    return message
  
def readEmail():
    message = ""
    message += "You have mail!" + nl + section + nl
    msg = []
    try:
      mail = imaplib.IMAP4_SSL(settings.IMAP)
      mail.login(settings.EMAIL,settings.PASSWORD)
      mail.select('inbox')
      data = mail.search(None, 'ALL')
      mail_ids = data[1]
      id_list = mail_ids[0].split()
      latest_email_id = int(id_list[-1])
      for i in range(latest_email_id, latest_email_id-10, -1):
          data = mail.fetch(str(i), '(RFC822)' )
          for response_part in data:
              arr = response_part[0]
              if isinstance(arr, tuple):
                  msg = email.message_from_string(str(arr[1]))
                  if msg['Date'].split()[4][0:5]  == datetime.now(pytz.timezone('America/New_York')).strftime("%H:%M") and textToDate(msg['Date'].split()[2] + " " + msg['Date'].split()[1] + " " + msg['Date'].split()[3]) == date.today():
                      message += msg['from'].split()[0] + " " + msg['from'].split()[1] + " has sent you an email!" + nl + section
    except Exception as e:
        message = "Cannot reach email"
    return message
  
def helpUser():
  message = ""
  message += "I am not sure if I understand Mr. Kini. Try looking at my commands sections here... "
  message += commandsFridayLink
  return message

# Text Processing for Dates
def textToDate(text):
  dateGen = ""
  for x in range(0, 12):
    if months[x] == text.split()[0]:
      if(x < 10):
        dateGen = text.split()[2] + "-0" + str(x + 1) + "-" + str(int(text.split()[1]) + 1) 
      else: 
        dateGen = text.split()[2] + "-" + str(x + 1) + "-" + str(int(text.split()[1]) + 1)
      break
  return dateGen

# Activates all message processing functions

# Clean input
def cleanInput(message):
    message = message.lower()
    message = message.replace("!", "")
    message = message.replace("@", "")
    message = message.replace("#", "")
    message = message.replace("$", "")
    message = message.replace("%", "")
    message = message.replace("^", "")
    message = message.replace("&", "")
    message = message.replace("*", "")
    message = message.replace("(", "")
    message = message.replace(")", "")
    message = message.replace("~", "")
    message = message.replace("`", "")
    message = message.replace("-", "")
    message = message.replace("_", "")
    message = message.replace("+", "")
    message = message.replace("=", "")
    message = message.replace("{", "")
    message = message.replace("}", "")
    message = message.replace("[", "")
    message = message.replace("]", "")
    message = message.replace("|", "")
    message = message.replace("\\", "")
    message = message.replace(":", "")
    message = message.replace(";", "")
    message = message.replace("\"", "")
    message = message.replace("\'", "")
    message = message.replace("<", "")
    message = message.replace(">", "")
    message = message.replace(",", "")
    message = message.replace(".", "")
    message = message.replace("?", "")
    message = message.replace("/", "")
    return message

# Parse Input
def parseInput(message):
    return (message.split())

# Wipes Messages
def wipeMessages(twilioClient):
    # Creates list of messages
    messages = twilioClient.messages.list(limit=5)
    for record in messages:
        try:
            twilioClient.messages(record.sid).delete()
        except:
            print("Delete message")

# Sends Message
def sendMessage(twilioClient, messageBody):
    # Creates list of messages
    messages = twilioClient.messages.list(limit=5)
    message = twilioClient.messages.create(
        body=messageBody,
        from_=settings.FRIDAY,
        to=settings.ARYANSEND
    )

# Sends Pushbullet
def sendPushbullet(title,message):
  pushbullet = Pushbullet(settings.PUSHBULLET_API_KEY)
  pushbullet.push_note(title,message)
  
# Sends Message on Emergency Channel
def sendPushbulletEmergencyChannel(message):
  pushbullet = Pushbullet(settings.PUSHBULLET_API_KEY)
  title = "An Emergency Has Occured!!!"
  pushbullet.channels[0].push_note(title, message)