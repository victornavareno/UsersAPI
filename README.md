# Flask Authentication API
This Flask-based API provides user **authentication and profile management**. The API differentiates between two types of users: Hosts and Subscribers. I added the **blueprint /auth/ as a HTTP request prefix.**

---
### User Registration
**POST /register**  
Registers a new user as either a "host" or a "subscriber". Default role is "subscriber".
- Required fields: `name`, `email`, `password`, `city`
- Role must be either "host" or "subscriber"
- Returns a success message and user ID upon successful registration
---

### Host Address Register
**POST /host/address**  
Allows hosts to add their address (separate step after registration).
- Requires authentication
- Only accessible to users with the "host" role
---

### User Login
**POST /login**  
Authenticates users and generates a JWT access token.
- Required fields: `email`, `password`
- Returns an access token and the user role upon successful authentication
---

### User Profile Retrieval
**GET /profile**  
Retrieves the profile details of the authenticated user.
- Requires authenticatio
- Returns user details including hosted or subscribed events based on role
---

### User Deletion
**DELETE /delete**  
Deletes the authenticated user's account.
- Requires authentication
- Deletes associated profiles for hosts and subscribers

## Author: Víctor Navareño

