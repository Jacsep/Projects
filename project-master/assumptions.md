**Assumptions for auth.py**


Auth_login:  
- 
- Assume user can be logged in multiple times, no check to see if user is logged in already  
- User is logged in when registered  
- Token is same for every user and not changed dynamically for re-logins 

Auth_register:  
-  
- None

Auth_logout:  
- 
- Token are invalidated by setting as None

Auth_password_reset:
-
- Assume reset code expires every 15minutes
- 
# Assumptions for channel.py 

## Channel_invite:
 -
 - can invite to both public and private channels
 - data being stored in the channel the person is invited to is id, fname and lname

## Channel_details:
 -
 - Doesn't matter if its private or public

## Channel_messages:
 -
 - functionality for adding messages will exist soon
 - no error if the enter 0 as a start and the list has nothing

## Channel_addowner:
 - 
 - If a user is not within the channel, they can not be added as owner
 - User 0 (owner of flockr) is able to add and remove owners without directly being an owner of the channel

## Channel_removeowner:
 -  
 - An owner can remove themselves as owner
 - A channel can have no owners, it will not be deleted.

# Assumptions for channels.py

## Channels_list:

- Lists all the channels the user is in regardless of whether the channel is public or private


## Channels_listall:

- List all channels regardless of whether it is public or private


## Channels_create:

- The user that creates the channel automatically becomes the owner
- Multiple channels can have the same name
- Messages within a channel will initally be empty
- Creator of channel is automatically the first member of the channel

## user/profile/setemail:
- Assume user can set email to his previous same email.



## user/profile/sethandle
- Assume user can change handle to the same handle as he previously had