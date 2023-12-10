# CENG445 Room Reservation System

## Phase 2 Tasks
### 1. TCP Server
- **x** It should be runnabe by 
```
python3 yourapp.py --port 1424
```
- **x** For each connection, the server should spawn a new thread to handle the connection.
- Each agent has two jobs
1. **x** Read text requests from client and make corresponding library calls and returns results for the client
2. **x** When there is a notification in the system that client should be informed, write a message to the client
- **x** Client and server speaks in a textual protocol such as JSON. First byte of the message is the length of the message, followed by the message itself.
### 2. Authentication
- **x** Username and password will be enough for authentication. Passwords will be stored as SHA256 hashes. Passwords will be stored in the database as hashes. Passwords will be sent to the server as plain text. Server will hash the password and compare it with the stored hash.
### 3. Persistent Storage
- **x** SQLite will be used as the database. Database will be stored in a file.
### 4. Server-Sent Notifications
- **x** Server should be able to send notifications to clients according to their view when there is a change in the any object inside the view.
- **x** There is only one View object per user. 
- **x** User will be notified for all events in the matching query definitions for the View. 
- **x** Note that permissions changes may also trigger notifications.
### 5. Organization Permissions
- **x** Organization objects will have a dictionary of permissions. Permissions will be in the form of
    ```
    {
    "user1": ["LIST", "ADD", "ACCESS", "DELETE"],
    ...
    }
    ```
- **✓ LIST**: user can list the Room objects in the organization.
- **✓ ADD**: user can add new rooms to the organization.
- **x ACCESS**: user can access the rooms and events in the organization. Note that this can be done without LIST permission.
- **✓ DELETE**: user can delete a Room in the organization if s/he also has WRITE permission on it. Owner of the Organization can delete the Room without WRITE permission. All Events in the Room are automatically deleted regardless of Event permissions.
### 6. Room have their own permissions
    ```
    {
        "LIST": ["user1", "user2"], // user can list and view the Event reservations for the
room.
        "RESERVE": ["user1"], // user can reserve the room
        "PERRESERVE": ["user1"], // user can reserve the room for periodic events. Implies RESERVE permission
        "DELETE": ["user1"], // user can delete the reservations for the room. It requires write permission on the Event. Owner of the room can delete the reservations without WRITE permission on the Event.
        "WRITE": ["user1"],
    }
    ```
### 7. Event have their own permissions
    ```
    {
        "READ": ["user1", "user2"], // user can see the title and details of the events. If
not granted room will be displayed as BUSY without any other detail.
        "WRITE": ["user1"], // User can update and delete (if Room has DELETE too) the Event
    }
    ```
### 8. View
- **x** roomView and dayView commands result on a list of tables, a table per matching Room and a table per matching Day respectively.