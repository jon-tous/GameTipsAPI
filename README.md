# GameTipsAPI

A back-end service responsible for managing the data (game tips and related entities, stored in `MongoDB`) for client apps that may request it.

Built with `FastAPI`, `Pydantic`, and `PyMongo`.

## Endpoints

`GET /experience/{experience_level_id}`

-   Get experience level details
    -   `experience_level_id` must be between 1 and 3 (inclusive)

`GET /games`

-   Get all games

`GET /games/{id}`

-   Get a game with specified id

`GET /tips`

-   Get tips, optionally filtering by game, experience, and/or spoilers
    -   optional query params: `game_id: str`, `experience: int`, `spoiler_free: bool`
        -   eg. `GET /tips?experience=1&spoiler_free=true`
    -   Note: `spoiler_free` flag defaults to false, so by default all tips are returned, but if you pass `spoiler_free=true` the tips with spoilers will be filtered out of the results.

`GET tips/{id}`

-   Get a tip with specified id

`PATCH /tips/{id}/like`

-   Add a like to a tip

`GET /reports`

-   Get all reports, optionally filtering for tip_id
    -   optional query params: `tip_id: str`
        -   eg. `GET /reports?tip_id=64c3cdfbd54e7b39dc4b1d74`

`POST /reports`

-   Report a tip with specified id
    -   Content-type: `application/json`
    -   Example request body:
        -   `{"tip_id": "64c3cdfbd54e7b39dc4b1d74","reason": "Incorrect Information","description": "string"}`

View interactive, automatically generated documentation on all endpoints in your browser at `<host_url>/docs` when the server is running, via `FastAPI`'s Swagger UI.

## Set up

To host the API on your own machine, download the code in this repo and install the necessary packages from `requirements.txt`. I recommend using a virtual environment to sandbox these dependencies.

Run `uvicorn game-tip-service:app --reload` to start the server and ^C to exit.

### Tools

Scripts are included in `/tools` to help back up and restore collections and their documents from a `MongoDB` database to a local JSON file and vice versa. 

A JSON dump of some starting data has also been included in `/tools`.

## Requesting and receiving data

HTTP requests can be sent to the above endpoints once a server is running, using a combination of the appropriate HTTP verb (e.g. `GET`) and URL path (e.g. `<host_url>/games`), passing the correct HTTP headers, query parameters, and body payload as required by the endpoint.

Example `GET` request and response:

```python
def get_request(url) -> str:
    try:
        res = requests.get(url)
        return json.dumps(res.json(), indent=4)
    except Exception as e:
        return f"Error: {e}"

# Make the request
url = "http://127.0.0.1:8000/games"
print(f"GET {url}")
test_get_games = get_request(url)
print(test_get_games)

### OUTPUT: ###
GET http://127.0.0.1:8000/games
[
    {
        "_id": "64c3c941d54e7b39dc4b1d6d",
        "title": "ASTLIBRA Revision",
        "description": "Confront time and fate in the 2D action RPG, Astlibra Revision. Explore meticulously crafted worlds, fight brutal boss battles, and upgrade your skills to take down enemies lurking around every corner."
    },
    {
        "_id": "64c3c9f9d54e7b39dc4b1d6e",
        "title": "Counter-Strike: Global Offensive",
        "description": "Counter-Strike: Global Offensive (CS: GO) expands upon the team-based action gameplay that it pioneered when it was launched 19 years ago. CS: GO features new maps, characters, weapons, and game modes, and delivers updated versions of the classic CS content (de_dust2, etc.)."
    },
    {
        "_id": "64c3ca4dd54e7b39dc4b1d6f",
        "title": "Crab Champions",
        "description": "Claw your way across exotic islands combining fluid movement with fast paced combat to become a Crab Champion in this third person shooter with roguelike elements."
    }
]
```

Example `POST` request and response:

```python
from fastapi.encoders import jsonable_encoder

report = ReportModel(  # defined in models.py
        tip_id="64c3cdfbd54e7b39dc4b1d74",
        reason=ReportModel.Reason.INCORRECT,
        description="Test report"
    )

def post_request(url, payload) -> str:
    try:
        res = requests.post(url, json=payload)
        return json.dumps(res.json(), indent=4)
    except Exception as e:
        return f"Error: {e}"

# Make the request
url = "http://127.0.0.1:8000/reports"
print(f"POST {url}")
test_post_report = post_request(url, payload=jsonable_encoder(report))
print(test_post_report)

### Output: ###
POST http://127.0.0.1:8000/reports
{
    "_id": "64c7e15fbdac21580a9a00fe",
    "tip_id": "64c3cdfbd54e7b39dc4b1d74",
    "reason": "Incorrect Information",
    "description": "Test report"
}
```

Example calls for all endpoints can be found in [`example.py`](https://github.com/jon-tous/GameTipsAPI/blob/main/example.py).

### UML Sequence Diagram

![](https://github.com/jon-tous/GameTipsAPI/blob/main/Sequence%20Diagram.png)
