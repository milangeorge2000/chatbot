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
    print(cust_email)
    print(cust_name)
    intent = result.get("intent").get('displayName')
    try:
      if (intent=='Products' or intent == 'Default Fallback Intent - custom - no'):
        message = MIMEMultipart()
        message1 = MIMEMultipart()

        sender_address = 'amphflow723@gmail.com'
        sender_pass = '723@AMPhflow'

        mail_content = "Thank you visiting our page. Our Support team will call you soon"

        # mail_content1 = "person with name {0} have some queries regarding {4}." \
                #    "Please reach to {0} at his mobile number {1} and email id {2}".format(cust_name,cust_contact,cust_email,work_name)
        
        mail_content1 = f"Person with name {cust_name} have some queries regarding {work_name}. Given phone number {cust_contact} is  and emailId is {cust_email}.Please reach out to him."
        print(mail_content1)
        receiver_address = cust_email
        contact_address = "amaluanayu@gmail.com"

        message['From'] = sender_address
        message['To'] = receiver_address 
        message['Subject'] = 'Amphflow Service Mail'
        message.attach(MIMEText(mail_content, 'plain'))

        message1['From'] = sender_address
        message1['To'] =  contact_address
        message1['Subject'] = 'Amphflow Service Mail'
        message1.attach(MIMEText(mail_content1, 'plain'))

        #Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port

        session.starttls() #enable security
        session.login(sender_address, sender_pass) #login with mail_id and password
        text = message.as_string()
        text1 = message1.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.sendmail(sender_address,contact_address , text1)
        session.quit()
        fulfillmentText="We have sent your details to the support team. They will contact you soon"
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
