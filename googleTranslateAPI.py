from twilio.rest import TwilioRestClient
import httplib2, urllib
import json

#Google credentials
GOOGLE_API_KEY = "AIzaSyAwXsNlDV9bkbn7_z2ghK8bEV_w9Qw9Ofs"
BASE_URL = 'https://www.googleapis.com'
PATH = '/language/translate/v2'
http = httplib2.Http()

#Twilio Credentials
account_sid = "ACab39f4aed328c466f18ba9f003c65f94"
auth_token = "5bdbe609ed7bcc9f053281b6ecff441d"
client = TwilioRestClient(account_sid, auth_token)





#https://www.googleapis.com/language/translate/v2?key=YOUR_API_KEY&q=hello%20world&source=en&target=de

# TRANSLATE_URL = ""
#
# text = ""
# text_encoded = urlib.quote_plus(text)
# # url = TRANSLATE_URL + text


# response, body = http.request(url, method, header, body)
#response, body = http.request(TRANSLATE_URL,"GET")

# print 'resppnse:', response
# print "\n", "\n"
# print 'body:' body

#parsed_body = json.loads(body)
# print 'parsed tyoe:', type(parsed_body)

# data = parsed_body['data']
# translation = data['translations']
# firstTranslation = translations[0]
# translatedText = firstTranslation['translatedText']

#translatedText2 = parsed_body['data']['translations'][0]['translatedText']




translatedArray = []

def translateText(text, language):
    encoded_text = urllib.quote(text)
    encoded_language = urllib.quote(language)

    url = BASE_URL + PATH + "?key=" + GOOGLE_API_KEY + "&q=" + encoded_text + "&source=" + "en" #+ "&target=" + encoded_language


    response, body = http.request(url,"GET")
    print type(body)
    print type(response)

    try:
        parsed_body = json.loads(body)
        print(parsed_body)
        translation = parsed_body['data']['translations'][0]['translatedText']
        return translation

    except ValueError:
        print("Your request was improperly formatted")





def translateArray(array, language):
    for i in range (0,len(array)):
        translatedArray.append(translateText(array[i],language))

    print translatedArray
    return translatedArray


itemsToTranslate = ["I love apples", "People here smell a lot!", "Dude, where's my car?"]
translateText("I like to eat cheese", "de")

# newMessage = translateText("I like to eat cheese", "de")
# message = client.messages.create(
# 	to = "+14157028892",
# 	from_= "+16508259655",
# 	body = newMessage)


# translateArray(itemsToTranslate, "fr")








# Notes
##  body only exists in POST requests, refers to the document being updated
## don't need body or header in our request
## Order doesn't matter in query parameters
