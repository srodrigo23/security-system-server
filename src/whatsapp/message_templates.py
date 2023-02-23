
new_camera_connected = lambda cam_id, time, date, link: f"""
    📹⚡️⚡️🔌 Se conectó una cámara 🔌⚡️⚡️📹
    ID de Cámara : {cam_id}
    Hora de conexión : {time}
    Fecha de conexión : {date}
    Enlace de transmisión : {link}
"""

camera_disconnected = lambda cam_id, time, date, : f"""
    📹🚫🔌 Se desconectó una cámara 🔌🚫📹
    ID de Cámara : {cam_id}
    Hora de desconexión : {time}
    Fecha de desconexión : {date}
""" 