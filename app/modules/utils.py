from requests import Response

def extract_sp_link(link:str, verify_type: str):
    segments = link.split("/")
    return segments[-1].split("?")[0], segments[-2] == verify_type

def verify_request(req: Response, desc, default_code: int):
    print(f"{desc} results:")
    if req.status_code == 401:
        msg = "You have to authenticate (401)"
    elif req.status_code == default_code:
        msg = f"No errors. Code {req.status_code}"
    else:
        msg = f"Error: code {req.status_code}"
        print(req.json())
    print(msg + "\n")
    return msg

def group_tracks(tracks):
    total = len(tracks)
    segments = (total // 100) + 1
    final = []
    for iter in tuple(range(segments)):
        iter += 1
        iter *= 100
        segment = tracks[(iter-100):iter]
        final.append(segment)
    return final
