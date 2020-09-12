import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, request,make_response,jsonify,render_template
from flask import Response
import os
import json

app = Flask(__name__)








@app.route('/webhook', methods=['POST'])
def webhook():

    req = request.get_json(silent=True, force=True)

    #print("Request:")
    #print(json.dumps(req, indent=4))

    res = processRequest(req)
    res = json.dumps(res, indent=4)
    #print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):


    sessionID=req.get('responseId')


    result = req.get("queryResult")
    user_says=result.get("queryText")
    parameters = result.get("parameters")
    cust_name=parameters.get("cust_name")
    cust_contact = parameters.get("cust_phone")
    cust_email=parameters.get("cust_email")
    work_name= parameters.get("topic_name")
    intent = result.get("intent").get('displayName')
    try:
      if (intent=='Products' or intent == 'Default Fallback Intent - custom - no'):
        message = MIMEMultipart()

        sender_address = 'amphflow723@gmail.com'
        sender_pass = '723@AMPhflow'

        mail_content = "Thank you visiting our page. Our Support team will call you soon"

        receiver_address = cust_email
        contact_address = "amaluanayu@gmail.com"

        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = 'Amphflow Service Mail'
        message.attach(MIMEText(mail_content, 'plain'))

        #Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port

        session.starttls() #enable security
        session.login(sender_address, sender_pass) #login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.sendmail(sender_address,contact_address , text)
        session.quit()
        fulfillmentText="We have sent the course syllabus"
        return {
            "fulfillmentText": fulfillmentText
        }

    except ValueError:
        return Response("Error Occurred! %s" %ValueError)
    except KeyError:
        return Response("Error Occurred! %s" %KeyError)
    except Exception as e:
        return Response("Error Occurred! %s" %e)



if __name__ == "__main__":
    app.run(debug=True)
