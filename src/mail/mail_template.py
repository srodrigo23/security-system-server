
title = """<p style = 'font-weight: bold; font-size: large; text-align: center;'>
                SISTEMA DE VIDEO VIGILANCIA INTELIGENTE \"LIVE EYE SMART\"
            </p>"""

def get_mail_template(message: str, hls_stream_link:str) -> str:
    return  f"""
            <html>
                <body>
                    <div style='background-color:#FCF3CF; 
                                font-family: "Lucida Console", "Courier New", monospace;'>
                        <p style='font-weight: bold; font-size: large; text-align: center;'>
                            SISTEMA DE VIDEO VIGILANCIA INTELIGENTE "LIVE EYE SMART"
                        </p>
                        <p>{ message }</p>
                        <p>
                            <table border='1' align='center'>
                                <tr>
                                    <th>Hoy</th>
                                    <th>Mañana</th>
                                    <th>Domingo</th>
                                </tr>
                                <tr>
                                    <td>Soleado</td>
                                    <td>Mayormente soleado</td>
                                    <td>Parcialmente nublado</td>
                                </tr>
                                <tr>
                                    <td>19°C</td>
                                    <td>17°C</td>
                                    <td>12°C</td>
                                </tr>
                                <tr>
                                    <td>E 13 km/h</td>
                                    <td>E 11 km/h</td>
                                    <td>S 16 km/h</td>
                                </tr>
                            </table>
                        </p>

                        <p>
                            <table border='1' align='center'>
                                <tr>
                                    <th>Hoy</th>
                                    <th>Mañana</th>
                                    <th>Domingo</th>
                                </tr>
                                <tr>
                                    <td>Soleado</td>
                                    <td>Mayormente soleado</td>
                                    <td>Parcialmente nublado</td>
                                </tr>
                                <tr>
                                    <td>19°C</td>
                                    <td>17°C</td>
                                    <td>12°C</td>
                                </tr>
                                <tr>
                                    <td>E 13 km/h</td>
                                    <td>E 11 km/h</td>
                                    <td>S 16 km/h</td>
                                </tr>
                            </table>
                        </p>
                        <p>
                            Puedes ver <a href='{hls_stream_link}'>aqui</a> la transmision en vivo.
                        <p/>
                    </div>
                </body>
            </html>"""


def get_body_mail_camera_connected(camera_data: dict, status: bool, link: str) -> str:
    transmission = f"""
        <tr>
            <th>Transmision en vivo:</th>
            <td>
                <button><a href="{link}">Ver transmision</a></button>
            </td>
        </tr>"""
        
    template = f""" 
            <html>
                <body>
                    <div style='background-color:#FCF3CF;
                        font-family: "Lucida Console", "Courier New", monospace;'>
                        { title }
                        <p>{'Se ha detectado una nueva cámara :' if status else 'Se ha desconectado una cámara : ' }</p>
                        <p>
                            <table border='1' align='center'>
                                <tr>
                                    <th>Id de la Cámara</th>
                                    <td>{camera_data['id']}</td>
                                </tr>
                                <tr>
                                    <th>Hora de {'conexión' if status else 'desconexión'}</th>
                                    <td>{camera_data['time_connection']}</td>
                                </tr>
                                <tr>
                                    <th>Fecha de {'conexión' if status else 'desconexión'}</th>
                                    <td>{camera_data['date_connection']}</td>
                                </tr>
                                {
                                    transmission if status else ''              
                                }
                            </table>
                        </p> 
                    </div>                    
                </body>
            </html>
        """
    return template