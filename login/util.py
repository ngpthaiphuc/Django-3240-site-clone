from login.models import FriendRequest as Friend_Request

#/***************************************************************************************
#*  REFERENCES
#*  Title: Real-time Chat Messenger (only for account and friends system)
#*  Author: CodingWithMitch
#*  Date: Oct 16th, 2020
#*  URL: https://www.youtube.com/playlist?list=PLgCYzUzKIBE9KUJZJUmnDFYQfVyXYjX6r
#*
#***************************************************************************************/

def get_friend_request_or_false(sender, receiver):
    try:
        return Friend_Request.objects.get(sender= sender, receiver=receiver, is_active=True)
    except Exception as e:
        return False
