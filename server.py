from flask import Flask
from flask import render_template
app = Flask(__name__)
from twilio.rest import Client
import json
import os
import settings
import functions
from datetime import datetime
import pytz
import time

# Multiple request variables
client = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)

@app.route("/")
def friday():
  # Global and Misc Variables
  records = ['example']
  request = ""
  prefix = 0
  parsedInput = []

  # Opens JSON
  data = json.load(open('commands.json'))

  # Creates list of messages
  messages = client.messages.list(limit=5)

  # Searches through messages
  for record in messages:
    for x in range(0, len(records)):
      if record.sid != records[x] and record.from_ == settings.ARYANFROM:
          body = record.body.lower()
          cleanedInput = functions.cleanInput(body)
          parsedInput = functions.parseInput(cleanedInput)
          for x in data:
              if request == "":
                  for i in range(0, len(data[x])):
                      command = data[x][i].split()
                      for e in range(0, len(command)):
                          if len(command) == e + 1 and command[e] == parsedInput[e]:
                              request = x
                              prefix = len(command)
                              break
                          elif len(command) is not e and command[e] == parsedInput[e]:
                              print("Parsing...")
                          else:
                              break
  # Processes requests
  if request == 'stock':
      functions.sendMessage(client, functions.readStockPrice(parsedInput[prefix]))
      functions.wipeMessages(client)
      request = ""
      prefix = 0
  elif request == 'hello':
      functions.sendMessage(client, "Hello Mr. Kini" + '\n' + "How can I help you?")
      functions.wipeMessages(client)
      request = ""
      prefix = 0
  elif request == 'weather':
    functions.sendMessage(client, functions.weatherCheck())
    functions.wipeMessages(client)
    request = ""
    prefix = 0
    
  # Regulatory Processes
  for x in range(0, 4):
    if datetime.now(pytz.timezone('America/New_York')).strftime("%H:%M:%S") == "07:00:0" + str(x):
        functions.sendMessage(client, functions.dailyUpdate())
        functions.wipeMessages(client)
        time.sleep(1)
        break
    
  return render_template("index.html")

@app.route("/emailRead")
def fridayEmail():
  nl = '\n'
  section = "---------------------------"
  
  emailCompiled = functions.readEmail()
  if emailCompiled != "You have mail!" + nl + section + nl:
    functions.sendMessage(client, emailCompiled)
    functions.wipeMessages(client)
    
  return render_template("index.html")

if __name__ == "__main__":
  app.run()
