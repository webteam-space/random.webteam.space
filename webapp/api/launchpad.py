from webapp import api


api_session = api.requests.CachedSession(expire_after=3600)


def process_response(response):
    if not response.ok:
        raise Exception("Response not ok")
    try:
        body = response.json()
    except ValueError as decode_error:
        api_error_exception = ApiResponseDecodeError(
            "JSON decoding failed: {}".format(decode_error)
        )
        raise Exception("Response not ok")

    return body


def get_canonical_webmonkeys():
    response = api_session.get(
        url="https://api.launchpad.net/1.0/~canonical-webmonkeys/members_details"
    )

    return process_response(response)


def get_member_link(url):
    response = api_session.get(url=url)

    return process_response(response)
