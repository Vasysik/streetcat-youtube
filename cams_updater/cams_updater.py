import urllib.request
import json 
import cam_viewer

def github_list(cams_json):
    data = json.load(urllib.request.urlopen("https://raw.githubusercontent.com/Vasysik/streetcat-viewer/main/cams_list.json"))
    with open(cams_json, "r") as json_file:
        cams_list = json.load(json_file)
    for group in data:
        if group not in cams_list:
            cams_list[group] = {
                "title": data[group]["title"],
                "cameras": data[group]["cameras"],
                "included": True,
                "statuses": []
            }
        with open(cams_json, "w") as json_file:
            json.dump(cams_list, json_file, indent=4)

def get_statuses(group):
    statuses = []
    title = group["title"]
    print(f"Check {title}...")
    for camera in group["cameras"]:
        status = cam_viewer.url_available(camera)
        print(status)
        statuses.append(status)
    return(statuses)

def statuses_list(cams_json):
    with open(cams_json, "r") as json_file:
        cams_list = json.load(json_file)
    for group in cams_list:
        cams_list[group] = {
            "title": cams_list[group]["title"],
            "cameras": cams_list[group]["cameras"],
            "included": cams_list[group]["included"],
            "statuses": get_statuses(cams_list[group])
        }
        with open(cams_json, "w") as json_file:
            json.dump(cams_list, json_file, indent=4)

github_list("cams_list.json")
statuses_list("cams_list.json")
