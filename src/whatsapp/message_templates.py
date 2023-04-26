
new_camera_connected = lambda cam_id, time, date, link: f"""
    📹⚡️⚡️🔌 Se conectó una cámara 🔌⚡️⚡️📹
    ID de Cámara : {cam_id}
    Hora de conexión : {time}
    Fecha de conexión : {date}
    Transmision en vivo : {"Revisa tu correo electrónico para ver el enlace" if link else "La transmisión en vivo esta desactivada"}
"""
# Enlace de transmisión : {link if link is not None else "No disponible"}

camera_disconnected = lambda cam_id, time, date, : f"""
    📹🚫🔌 Se desconectó una cámara 🔌🚫📹
    ID de Cámara : {cam_id}
    Hora de desconexión : {time}
    Fecha de desconexión : {date}
""" 

fire_detection = lambda cam_id : f"🔥🔥 Se ha detectado fuego en la cámara {cam_id}.🔥🔥"
motion_detection = lambda cam_id : f"⬅️⬅️ Se ha detectado movimiento en la cámara {cam_id}.⬅️⬅️"
human_detection = lambda cam_id : f"🚶🏻‍♂️🚶🏻‍♂️ Se ha detectado silueta humana en la cámara {cam_id}.🚶🏻‍♂️🚶🏻‍♂️"