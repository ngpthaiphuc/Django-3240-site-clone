from enum import Enum

#/***************************************************************************************
#*  REFERENCES
#*  Title: Real-time Chat Messenger (only for account and friends system)
#*  Author: CodingWithMitch
#*  Date: Oct 16th, 2020
#*  URL: https://www.youtube.com/playlist?list=PLgCYzUzKIBE9KUJZJUmnDFYQfVyXYjX6r
#*
#***************************************************************************************/

class FriendRequestStatus(Enum):
	NO_REQUEST_SENT = -1
	THEM_SENT_TO_YOU = 0
	YOU_SENT_TO_THEM = 1


