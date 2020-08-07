def say(request, dict):
    new_dict = dict
    # for action in new_dict["actions"]:
    #     if action.keys()[0] == 'say':
    #         action['say'] = request.POST.get("say-text")
    new_dict["actions"].append({"say":request.POST.get("say-text")})
    print(new_dict)
    print(request.POST)
    return new_dict
