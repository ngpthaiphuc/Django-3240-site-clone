# CS 3240 - S21 / Django Campus Map
## By group B-30

In this repo...

[Manage.py - explanation](cs3240-B30-project/manage.py)

[wsgi.py: An entry-point for WSGI-compatible web servers to serve this project ](cs3240-B30-project/wsgi.py)

AppConfig: instance where metadata is stored about each of the apps installed in this project
This instance references the subclass INSTALED_APPS on [settings.py](cs3240-B30-project/settings.py)


Guidance:
Users can login through google account or register using their email address.
On the main page, user can select a location, then the map will display a route between the current location to the destination. User can also select different routes. Most popular on campus locations are included in the main page, but the user can also go to the search page to find any location that is not listed. 
In the “Choose your location” page the application is presented with a non dynamic origin and destination. Once the user types in the location they want to go to, the origin is set to the user’s current location and the destination is set to the string that was submitted by the user in the form bar. This function is useful because it allows the user to have a multitude of travel destinations not supported in the main page as well as the ability to find the quickest route to one’s friend as their latitudes and longitudes should be known to the user in the friend’s tab.
On the HoosAroundMe page, user can click on the recommended user’s account page. On that page, you can send friend request to that user and see the user’s friend list.
The Hoos around me page allows the user to add friends to be accessed by their friend page. It also implements a search feature that will let the user know how many people are inside of a circle radius that the user specifies. In its current state a set of 3 random users will pop up for the user to be able to select from in terms of adding friends. The user upon searching a location in the search box will be given a visual of a circle radius around the specified area as well as the number of hoosaroundme users within that radius.
On the My profile page, you can see your profile. You can change username or update your status on the page. You can also see friend request sent to you and choose to accept or decline the request. 
In the navbar, the friends tab shows all your friends, their email address, and their status. You can click on the user to go to his/her account profile page. 