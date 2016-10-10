import TwilioRestClient
from twilio.rest import TwilioRestClient

account_sid = "ACab39f4aed328c466f18ba9f003c65f94"
auth_token = "5bdbe609ed7bcc9f053281b6ecff441d"

client = TwilioRestClient(account_sid, auth_token)


message = client.messages.create(
	to = "+650825-9655",
	from_= "+14157028892",
	body = "Is this going to work?")


BASE_URL = "https://api.twilio.com"
PATH = "/2010-04-01/Accounts/"
QUERY = "/ACab39f4aed328c466f18ba9f003c65f94/Messages.json"

url = BASE_URL + PATH + QUERY

response, body = http.request(url,"GET")

print(response)
print(body)





# https://api.twilio.com/2010-04-01/Accounts/AC87769992cf0edbd7bfbd177e6c15a760/Messages.json
