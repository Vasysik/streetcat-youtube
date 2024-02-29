import urllib.request
import json 
import cam_viewer
from time import sleep

cams_json = "cams_list.json"
tasks_json = "./cams_updater/tasks.json"

def add_group(cams_json, group, title = "", cameras = []):
    with open(cams_json, "r") as json_file:
        cams_list = json.load(json_file)
    if group not in cams_list:
        cams_list[group] = {
            "title": title,
            "cameras": cameras,
            "statuses": [],
            "included": True
        }
        with open(cams_json, "w") as json_file:
            json.dump(cams_list, json_file, indent=4)
        return(True)
    else: return(False)

def add_camera(cams_json, group, camera):
    with open(cams_json, "r") as json_file:
        cams_list = json.load(json_file)
    if group in cams_list and camera not in cams_list[group]["cameras"]:
        cameras = cams_list[group]["cameras"]
        cameras.append(camera)
        cams_list[group] = {
            "title": cams_list[group]["title"],
            "cameras": cameras,
            "statuses": [],
            "included": cams_list[group]["included"]
        }
        with open(cams_json, "w") as json_file:
            json.dump(cams_list, json_file, indent=4)
        return(True)
    else: return(False)

def remove_group(cams_json, group):
    with open(cams_json, "r") as json_file:
        cams_list = json.load(json_file)
    if group in cams_list:
        del cams_list[group]
        with open(cams_json, "w") as json_file:
            json.dump(cams_list, json_file, indent=4)
        return(True)
    else: return(False)

def remove_camera(cams_json, group, camera):
    with open(cams_json, "r") as json_file:
        cams_list = json.load(json_file)
    if group in cams_list and camera in cams_list[group]["cameras"]:
        cameras = cams_list[group]["cameras"]
        cameras.remove(camera)
        cams_list[group] = {
            "title": cams_list[group]["title"],
            "cameras": cameras,
            "statuses": [],
            "included": cams_list[group]["included"]
        }
        with open(cams_json, "w") as json_file:
            json.dump(cams_list, json_file, indent=4)
        return(True)
    else: return(False)

def update_statuses(cams_json, group):
    with open(cams_json, "r") as json_file:
        cams_list = json.load(json_file)
    if group in cams_list:
        statuses = []
        for camera in cams_list[group]["cameras"]:
            statuses.append(cam_viewer.url_available(camera))
        cams_list[group] = {
            "title": cams_list[group]["title"],
            "cameras": cams_list[group]["cameras"],
            "statuses": statuses,
            "included": cams_list[group]["included"]
        }
        with open(cams_json, "w") as json_file:
            json.dump(cams_list, json_file, indent=4)
        return(True)
    else: return(False)

def add_from_json_url(cams_json, url):
    data = json.load(urllib.request.urlopen(url))
    with open(cams_json, "r") as json_file:
        cams_list = json.load(json_file)
    for group in data:
        add_group(cams_json = cams_json,
                  group = group,
                  title = data[group]["title"], 
                  cameras = data[group]["cameras"])
    return(True)

while True:
    with open(tasks_json, "r") as json_file:
        tasks = json.load(json_file)
    for add_group_task in list(tasks["add_group"]):
        add_group(cams_json = cams_json,
                group = tasks["add_group"][add_group_task]["group"],
                title = tasks["add_group"][add_group_task]["title"],
                cameras = tasks["add_group"][add_group_task]["cameras"])
        del tasks["add_group"][add_group_task]
    for add_camera_task in list(tasks["add_camera"]):
        add_camera(cams_json = cams_json,
                group = tasks["add_camera"][add_camera_task]["group"],
                camera = tasks["add_camera"][add_camera_task]["camera"])
        del tasks["add_camera"][add_camera_task]
    for remove_group_task in list(tasks["remove_group"]):
        remove_group(cams_json = cams_json,
                    group = tasks["remove_group"][remove_group_task]["group"])
        del tasks["remove_group"][remove_group_task]
    for remove_camera_task in list(tasks["remove_camera"]):
        remove_camera(cams_json = cams_json,
                    group = tasks["remove_camera"][remove_camera_task]["group"],
                    camera = tasks["remove_camera"][remove_camera_task]["camera"])
        del tasks["remove_camera"][remove_camera_task]
    for update_statuses_task in list(tasks["update_statuses"]):
        update_statuses(cams_json = cams_json,
                        group = tasks["update_statuses"][update_statuses_task]["group"])
        del tasks["update_statuses"][update_statuses_task]
    for add_from_json_url_task in list(tasks["add_from_json_url"]):
        add_from_json_url(cams_json = cams_json,
                        url = tasks["add_from_json_url"][add_from_json_url_task]["url"])
        del tasks["add_from_json_url"][add_from_json_url_task]
    with open(tasks_json, "w") as json_file:
        json.dump(tasks, json_file, indent=4)