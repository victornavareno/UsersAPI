# Flask Authentication API
This Flask, SQLAlchemy and JWT Python API provides user **authentication and profile management**. 

### User Registration
**POST /register**  
Registers a new user as either a "host" or a "subscriber". Default role is "subscriber".
- Required fields: `name`, `email`, `password`, `city`
  
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


## Author: Víctor Navareño

