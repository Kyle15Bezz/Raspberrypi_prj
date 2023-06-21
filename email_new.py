from email.message import EmailMessage
import datetime
import ssl, smtplib


def snd_email(weather, humid, temp, wind, icon, city, receiver):
    # URL for weather icon image
    icon_url = "https://openweathermap.org/img/w/" + icon + ".png"
    # App-specific password for Gmail
    app_pass = "dasdasfewfer"
    # Email sender and receiver addresses
    email_sender = "kyle@gmail.com"
    email_receiver = receiver

    # Get current date and time
    date = datetime.datetime.now()
    subject = "Weather Update at " + str(date)

    # HTML template for the email body
    msg = '''
    <html>
    <head>
        <style>
            .weather-container {
                background-color: #f1f1f1;
                border-radius: 8px;
                padding: 20px;
                text-align: center;
                max-width: 400px;
                margin: 0 auto;
                font-family: Arial, sans-serif;
            }

            .weather-icon {
                width: 100px;
                height: 100px;
                margin: 0 auto;
            }

            .weather-details {
                margin-top: 20px;
                font-size: 18px;
                color: #333;
            }
        </style>
    </head>''' + f'''
    <body>
     <div style="background-color:#eee;padding:10px 20px;">
                <h2 style="font-family:Georgia, 'Times New Roman', Times, serif;color#454349;">Weather Update : {city}</h2>
            </div>
          
        <div class="weather-container">
           
            <img class="weather-icon" src="{icon_url}" alt="Weather Icon">
            <div class="weather-details">
            <p>Condition: <strong>{weather}</strong></p>
                <p>Temperature: <strong>{temp}°C</strong></p>
                <p>Humidity: <strong>{humid}%</strong></p>
                <p>Wind: <strong>{wind} m/s</strong></p>
                
            </div>
        </div>
    </body>
    </html>
    '''

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(msg, subtype='html')

    contxt = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=contxt) as smtp:
        smtp.login(email_sender, app_pass)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
