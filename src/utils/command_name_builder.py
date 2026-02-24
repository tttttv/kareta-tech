def get_true_command_name(
    command_name: str, 
    vehicle_type: str
) -> str:
    """
    Метод для преобразования названий команд
    из коллбеков в имена команд на бэкенде.
    
    :param command_name: Название команды из коллбека
    :type command_name: str
    :param vehicle_type: Тип кареты
    :type vehicle_type: str
    
    :return: Имя команды на бэкенде
    :rtype: str
    """
    
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
    
    return command_name.upper()

def get_command_name_for_handlers(
    command_name: str
):
    """
    Метод для преобразования названий команд
    из бэкенда в названия команд для коллбэков.
    
    :param command_name: Название команды на бэкенде
    :type command_name: str
    :param vehicle_type: Тип кареты
    :type vehicle_type: str
    
    :return: Имя команды в коллбеке
    :rtype: str
    """
    
    if command_name == "LOCK":
        return "lock"
    if command_name == "UNLOCK":
        return "unlock"
    if command_name == "SOUND":
        return "beep"
    if command_name == "SET_TRACKING_INTERVAL_30":
        return "set_tracking_interval_30"
    if command_name == "SET_TRACKING_INTERVAL_60":
        return "set_tracking_interval_60"
    if command_name == "GET_LOCATION" or command_name == "LOCATION":
        return "update_vehicle_location"
    if command_name == "LOCATION":
        return "update_vehicle_location"
    
    return command_name
