# -*- coding: utf8 -*-
# coding : utf8

from googleapiclient import discovery
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime

###############################################################################
def print_calendar():

	# Setup the Calendar API
	SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
	store = file.Storage('credentials_cal.json')
	creds = store.get()
	if not creds or creds.invalid:
	    flow = client.flow_from_clientsecrets('client_id.json', SCOPES)
	    creds = tools.run_flow(flow, store)
	service = build('calendar', 'v3', http=creds.authorize(Http()))

	# Call the Calendar API to get 5 events
	now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
	events_result = service.events().list(calendarId='primary', timeMin=now, maxResults=5, singleEvents=True, orderBy='startTime').execute()
	events = events_result.get('items', [])

	# Reading the events
	for event in events:

		start_date = event['start'].get('dateTime', event['start'].get('date'))
		print(start_date, event['summary'])

		try :
			start_date_troncated = start_date[0:-6]
			eventdate = time.strptime(start_date_troncated, '%Y-%m-%dT%H:%M:%S')

		except Exception as e:
			#print("No hour")
			eventdate = time.strptime(start_date, '%Y-%m-%d')

		msg_to_say = u" " + str(event['summary']) + " le " + str(eventdate.tm_mday) + " " + str(eventdate.tm_mon) + " deux mille dix huit "	# + str(eventdate.tm_year)
		print(msg_to_say)

###############################################################################
def GetMessage(service, user_id, msg_id):
	"""Get a Message with given ID.

	Args:
	service: Authorized Gmail API service instance.
	user_id: User's email address. The special value "me"
	can be used to indicate the authenticated user.
	msg_id: The ID of the Message required.

	Returns:
	A Message.
	"""
	try:
		message = service.users().messages().get(userId=user_id, id=msg_id).execute()
		return message

	except Exception as e:
		print('Exception' + str(e))


###############################################################################
def ListMessagesWithLabels(service, user_id, label_ids=[]):
	"""List all Messages of the user's mailbox with label_ids applied.

	Args:
	service: Authorized Gmail API service instance.
	user_id: User's email address. The special value "me"
	can be used to indicate the authenticated user.
	label_ids: Only return Messages with these labelIds applied.

	Returns:
	List of Messages that have all required Labels applied. Note that the
	returned list contains Message IDs, you must use get with the
	appropriate id to get the details of a Message.
	"""
	try:
		response = service.users().messages().list(userId=user_id, labelIds=label_ids).execute()
		messages = []

		if 'messages' in response:
			messages.extend(response['messages'])

		msg_cmpt = 0

		for msg_id in response['messages']:
			msg_cmpt += 1
			current_msg = GetMessage(service, user_id, msg_id['id'])
			print ('Message %d : %s\n' % (msg_cmpt, current_msg['snippet']))

			# Read the message
			msg_to_say = u" " + current_msg['snippet']
			print(msg_to_say)
			
	except Exception as e:
		print('Exception' + str(e)) 


###############################################################################
def ListMessagesLabels(service, user_id, label_ids=[]):

	labels = results.get('labels', [])
	if not labels:
		print('No labels found.')
	else:
	    print('Labels:')
	    for label in labels:
	        print(label['name'])


###############################################################################
def print_email():

	# Setup the Gmail API
	SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
	store = file.Storage('credentials_email.json')
	creds = store.get()

	if not creds or creds.invalid:
	    flow = client.flow_from_clientsecrets('client_id.json', SCOPES)
	    creds = tools.run_flow(flow, store)

	# Call the Gmail API
	service = build('gmail', 'v1', http=creds.authorize(Http()))
	ListMessagesWithLabels(service, 'me', 'UNREAD')
    

############################################################################
if __name__ == "__main__":

	print_calendar()
	print_email()
