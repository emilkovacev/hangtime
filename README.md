# Hangtime 🗓️
An event-sharing application :)

## Requirements
* User Accounts with Secure Authentication (user accounts for personal calendars)
* Users to see all users who are currently logged in (users can see other users + calendars)
* Users can send direct messages (DM) to other users with notifications when a DM is received (Messaging App)
* Users can share some form of multimedia content which is stored and hosted on your server (Users share calendars)
* Live interactions between users via WebSockets (Cannot be text, Calendar changes are updated live 

## Apps
* Schedule Builder
* Messaging App
* Login Screen

## Models

### Schedule Builder

#### User
* username: str
* password: str

#### Event
* start_datetime: datetime str (tbd)
* end_datetime: datetime str (tbd)
* duration: calculated from start-time and end-time
