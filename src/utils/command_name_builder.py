def get_true_command_name(command_name: str, vehicle_type: str) -> str:
    if command_name == "lock":
        return "LOCK"
    if command_name == "unlock":
        return "UNLOCK"
    if command_name == "beep":
        return "SOUND"
    if command_name == "set_tracking_interval_30":
        return "SET_TRACKING_INTERVAL_30"
    if command_name == "set_tracking_interval_60":
        return "SET_TRACKING_INTERVAL_60"
    if command_name == "update_vehicle_location":
        if vehicle_type == "OMNI_IOT":
            return "LOCATION"
        else:
            return "GET_LOCATION"
    
    return command_name
