# We Watch

## What is it?
The idea is simple: watch videos together over the internet.

We Watch is a way for people, regardless of distance, to do things like watch movies together. Or listen to the same playlist. Or follow a TV series together. The way it works is that any number of people can watch the same video, and if one of them pauses it, then it pauses for everyone. Same goes for fast-forwarding or rewinding. And it keeps the time signature at sync, so that not one person is ahead of any other.

There will also be a chat, for people to communicate while they watch. And the ability to function as a library where you can save videos you like, or want to watch in the future. Also, you can create and maintain playlists.

Currently, the application is limited to videos sourced from Youtube, and there is no chat or playlist functionality. Further development is required for these features.

## Technologies Used
The application is built on Python's Tornado framework for the HTTP framework and Websocket handling, as well as using its template engine for the frontend website. For ease of frontend design, the Bootstrap framework is being used. Data is being stored using Redis, an in-memory key-value store. There is no database requirement.

Further requirements needed for development include pipenv, to manage proper Python imports, bpython and ipdb for debugging and so on.

All requirements except for pipenv and Redis are installed automatically within the Makefile.

## Technical Notes

### Usage Flow:
When a user accesses the website by visiting the URL for the first time,
- A unique user is created in Redis, identified by a unique auth token.
- The token is saved client-side in the form of a signed cookie.
- This cookie is used to identify the user in subsequent website accesses, without the user creating a username and password.
- The auth token is "consumed" and regenerated upon every website access to prevent spoofing.

When a user adds a Youtube video,
- The video is stored in Redis, linked to the user, and will remain there until deleted.
- The video is identified by a unique auto-incrementing ID.
- A unique "invite key" is generated and stored along with the video.
- The video can be accessed by the ID, but only by the user that added it.
- It can also be accessed by the invite key by anyone.

When watching a video,
- A websocket connection is opened between the user's frontend and the Tornado server.
- The server maintains a list of all the websocket connections watching the same video.
    - Note that there might be duplicates of a video -- multiple IDs of the same video added by different people. These will not be kept in sync.
- Through the websocket, the server enforces that the video be in the same state across all clients.

### Technical Details:
The file structure is divided like so:
- `/`
    - `server_options.conf`
        - Contains the "settings" of the application. Which port to listen to, etc.
    - `redis_db_options.conf`
        - Contains Redis settings-- how often to back up, etc.
    - `README.md`
    - `Makefile`
        - Rules:
            - `init` - Initializes the environment and installs prereqs.
            - `redis` - Runs the Redis key-value store
            - `run` - Runs the server
            - `clean` - Destroys the virtual environment
    - `logs/`
    - `dependencies/`
        - Contains the Redis source, from where it can be installed.
    - `storage/`
        - Where Redis stores backups
    - `src/`
        - `server.py`
            - **Execution begins here.**
            - Initializes the application, as well as the Redis connection. Maintains routing.
        - `controllers/`
            - All handlers reside here, as well as the 'BaseHandler', from which they all derive.
            - The main logic of the application occurs as part of the handlers.
        - `frontend/`
            - `static/`
                - Contains images, static CSS, JS, etc.
            - `templates/`
                - Contains the HTML templates for the Tornado display engine.
            - `uimodules/`
                - The frontend is broken down into reusable components called modules, which reside here, along with the Python file to manage them.
        - `managers/`
            - All interaction with Redis happens within the managers stored here. They are inherited by the handlers to access and modify the key-value store in an organized and black-box fashion.
    - ...and various editor and git related files.
