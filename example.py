import json
import requests

from fastapi.encoders import jsonable_encoder
from models import ReportModel

HOST = "http://127.0.0.1:8000"


def get_request(url) -> str:
    try:
        res = requests.get(url)

        return json.dumps(res.json(), indent=4)
    except Exception as e:
        return f"Error: {e}"


def post_request(url, payload) -> str:
    try:
        res = requests.post(url, json=payload)

        return json.dumps(res.json(), indent=4)
    except Exception as e:
        return f"Error: {e}"


def patch_request_no_payload(url) -> str:
    try:
        res = requests.patch(url)

        return json.dumps(res.json(), indent=4)
    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":

    print("#########################")
    print("### TESTING ENDPOINTS ###")
    print("#########################")
    print()

    # Testing variables
    experience_level_id = 1
    game_id = "64c3c941d54e7b39dc4b1d6d"
    tip_id = "64c3cdfbd54e7b39dc4b1d74"
    report = ReportModel(
        tip_id=tip_id,
        reason=ReportModel.Reason.INCORRECT,
        description="Test report"
    )

    url = f"{HOST}/experience/{experience_level_id}"
    print(f"GET {url}")
    test_get_experience = get_request(url)
    print(test_get_experience)

    url = f"{HOST}/games"
    print(f"GET {url}")
    test_get_games = get_request(url)
    print(test_get_games)

    url = f"{HOST}/games/{game_id}"
    print(f"GET {url}")
    test_get_game = get_request(url)
    print(test_get_game)

    url = f"{HOST}/tips?game_id={game_id}&experience={experience_level_id}"
    print(f"GET {url}")
    test_get_tips = get_request(url)
    print(test_get_tips)

    url = f"{HOST}/tips/{tip_id}"
    print(f"GET {url}")
    test_get_tip_with_id = get_request(url)
    print(test_get_tip_with_id)

    url = f"{HOST}/tips/{tip_id}/like"
    print(f"PATCH {url}")
    test_like_tip = patch_request_no_payload(url)
    print(test_like_tip)

    url = f"{HOST}/reports?tip_id={tip_id}"
    print(f"GET {url}")
    test_get_reports = get_request(url)
    print(test_get_reports)

    url = f"{HOST}/reports"
    print(f"POST {url}")
    test_post_report = post_request(url, payload=jsonable_encoder(report))
    print(test_post_report)
