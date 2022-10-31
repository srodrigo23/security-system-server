
title = """<p style = 'font-weight: bold; font-size: large; text-align: center;'>
                SISTEMA DE VIDEO VIGILANCIA INTELIGENTE \"LIVE EYE SMART\"
            </p>"""

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
                            <div style='width: 50px; height: 50px; overflow: scroll; border: 1px solid #777777;'>
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
                                        transmission if (status and link != '') else ''              
                                    }
                                </table>
                            </div>
                        </p> 
                    </div>                    
                </body>
            </html>
        """
    return template