

new_camera_connected =lambda cam_id, time, date, link: f"""
    🔌 Una nueva cámara ha sido conectada 🔌
    ID de Cámara : {cam_id}
    Hora de conección : {time}
    Fecha de conección : {date}
    Enlace de transmision : {link}
"""

camera_disconnected = lambda cam_id, time, date, : f"""
    🔌 Una nueva cámara ha sido conectada 🔌
    ID de Cámara : {cam_id}
    Hora de conección : {time}
    Fecha de conección : {date}
""" 