
title = """<p style = 'font-weight: bold; font-size: large; text-align: center; font-size: 2rem;'>
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
                        font-family: Arial, Helvetica, sans-serif; font-size: 1rem; padding: 1rem;'>
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

def get_body_mail_event_happen(detection_code : str, detection_info : dict, num_pics_ad:int) -> str:
    
    colors = {
        'fire': '#F1948A',
        'movement': '#D6EAF8',
        'human_siluhete': '#F5EEF8',
        'smoke': '#E5E7E9',
    }
    
    detection = {
        'fire': 'Fuego',
        'movement': 'Movimiento',
        'human_siluhete': 'Intruso',
        'smoke': 'Humo',
    }
    
    # icons={
    #     'fire': "https://cdn.cdnlogo.com/logos/p/6/psg.svg",
    #     # 'fire': 'tcpserver/src/mail/img/fire.png',
    #     'movement': './src/mail/img/human.png',
    #     'human_siluhete': './src/mail/img/movement.png',
    #     'smoke': './src/mail/img/smoke.png',
    # }
    # <!-- < p >
    #     <img src = '{#icons[detection_code]}' alt = '{detection[detection_code]}' >
    # <p>-->
    
    template = f""" 
            <html>
                <body>
                    <div style='background-color:{colors[detection_code]};
                    font-family: Arial, Helvetica, sans-serif; font-size: 1rem; padding: 2rem;'>
                        { title }
                        <p>Se ha detectado : </p>
                        <center><h1 style='font-size: 2rem;'>{detection[detection_code]}</h1></center>
                        <p>
                            <div>
                                <table border='1' align='center'>
                                    <tr>
                                        <th>Id de Cámara</th>
                                        <th>Fecha</th>
                                        <th>Hora</th>
                                        <th>Transmisión</th>
                                    </tr>
                                    <tr>
                                        <th>{detection_info['id']}</th>
                                        <th>{detection_info['date_detection']}</th>
                                        <th>{detection_info['time_detection']}</th>
                                        <th><a href=\"{detection_info['link']}\">En vivo</a></th>
                                    </tr>
                                </table>
                            </div>
                        </p>
                        <p>{num_pics_ad} imágen(es) adjunta(s).</p>                        
                    </div>                    
                </body>
            </html>
        """
    return template
