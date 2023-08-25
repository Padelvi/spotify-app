from requests import Response

def extract_sp_link(link:str, verify_type: str):
    segments = link.split("/")
    return segments[-1].split("?")[0], segments[-2] == verify_type


def add_content_type_to_headers(headers):
    return {
        **headers,
        "Content-Type": "application/json"
    }

def verify_request(req: Response, desc, default_code: int):
    print(f"{desc} results:")
    if req.status_code == 401:
        msg = "You have to authenticate"
    elif req.status_code == default_code:
        msg = f"No errors. Code {req.status_code}"
    else:
        msg = f"Error: code {req.status_code}"
    print(msg)
    return msg
