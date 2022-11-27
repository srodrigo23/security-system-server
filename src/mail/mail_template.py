
title = """<p style = 'font-weight: bold; font-size: large; text-align: center;'>
                SISTEMA DE VIDEO VIGILANCIA INTELIGENTE \"LIVE EYE SMART\"
            </p>"""

def get_body_mail_camera_connected(camera_data: dict, status: bool, link: str, other_cams:list) -> str:
    
    table_other_cams = ''
    if len(other_cams) > 0:
        rows  = ""
        for cam in other_cams:
            rows += f"<tr><td>{cam['id']}</td><td>{cam['time_connection']}</td><td>{cam['date_connection']}</td><td><a href=\"{cam['link']}\">En vivo</a></td></tr>"
            
        table_other_cams = f"""
            <table border='1' align='center'>
                <tr>
                    <th>Id de la Cámara</th>
                    <th>Fecha de conexión</th>
                    <th>Hora de conexión</th>
                    <th>Transmisión</th>
                </tr>
                {
                    rows
                } 
            </table>
        """    
    
    transmission = f"""
        <tr>
            <th>Transmisión</th>
            <td>
                <a href="{link}">En vivo</a>
            </td>
        </tr>"""
        
    template = f""" 
            <html>
                <body>
                    <div style='background-color:{'#CAFAF8' if status else ' #FAF3CA'};
                        font-family: Arial, Helvetica, sans-serif; font-size: 1rem;'>
                        { title }
                        <p>{'Se ha detectado una nueva cámara :' if status else 'Se ha desconectado una cámara : ' }</p>
                        <p>
                            <div>
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
                        <p>{f'{len(other_cams)} cámara(s) también esta(n) disponible(s) :' if len(other_cams)>0 else 'No hay más cámaras disponibles'}</p>
                        <p>
                            {
                                table_other_cams if len(other_cams)>0 else ''
                            }
                        </p>
                    </div>                    
                </body>
            </html>
        """
    return template