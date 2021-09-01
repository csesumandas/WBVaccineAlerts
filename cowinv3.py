import cloudscraper
import requests
import sys
import json
import datetime
import time
import os
import random
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart




def send_message(API_KEY,channel_id,message):
    """This method is used to send message to telegram channel"""
    try:
        tele_api_url = f"https://api.telegram.org/bot{API_KEY}/sendMessage?chat_id={channel_id}&text={message}&parse_mode=html&disable_web_page_preview=True"
        res = requests.get(tele_api_url)
    except Exception as e:
        print(f"{datetime.datetime.now()} - {e}\n")



def check_vaccine_availibility(dist):
    """Check the availibility of vaccine for given range."""
    # Get the parameters
    DIST_NAME = dist["NAME"]
    DISTRICT_ID = dist["DISTRICT_ID"]
    TELEKEY = dist["TELEKEY"]
    MIN_DELAY = dist["MIN_DELAY"]
    MAX_DELAY = dist["MAX_DELAY"]

    
    
    # Counter to check and send emails about the condition of the script
    counter = 0
    hrs = 0
    err_cnt = 0
    tot_cnt = 0
    
    # Send initial mail of script started
    send_message(TELEKEY,"@wbvaccinealerterror",f"{DIST_NAME} Bot Script Started - {datetime.datetime.now()}")

    avl_vac = {}

    err_ratios = [0,0,0]

    # last date variable
    last_date = ""

    # Loop for eternity
    while True:
        
        # Get Current Datetime for logging
        curr_datetime = datetime.datetime.now()
        curr_date = curr_datetime.strftime("%d-%m-%Y")

        # If date changes then reset avl_vac to save memory
        if last_date != curr_date:
            avl_vac = {}
        
        # Prepare the API URL for checking
        url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={DISTRICT_ID}&date={curr_date}"

        # Increament the total counter
        tot_cnt += 1

        try:
            scraper = cloudscraper.create_scraper()
            #print(scraper.get(url).text)
            res = json.loads(scraper.get(url).text)
             
            for center in res["centers"]:
                
                # Get the center informations
                centerid = center["center_id"]
                pin = center["pincode"]
                name = center["name"]
                address = center["address"]

                # Flag for checking vaccine availibility
                has_vaccine_ei = False
                has_vaccine_ff = False

                # Templates for sending message
                dist_label = "DISTRICT"
                age_label = "AGE GROUP"
                pin_label = "PIN"
                center_name_label = "CENTER NAME"
                address_label = "ADDRESS"
                hr = "-" * 31

                ei_message_prefix = f"<b>{dist_label}:</b> {DIST_NAME}\n<b>{age_label}:</b> 18-44\n<b>{pin_label}:</b> {pin}\n<b>{center_name_label}:</b> {name}\n<b>{address_label}:</b> {address}\n\n"
                ff_message_prefix = f"<b>{dist_label}:</b> {DIST_NAME}\n<b>{age_label}:</b> 45 Above\n<b>{pin_label}:</b> {pin}\n<b>{center_name_label}:</b> {name}\n<b>{address_label}:</b> {address}\n\n"
                

                session_msg_template = "{0:<10}{1:>7}{2:>7}{3:>7}"

                dose_heading = session_msg_template.format("","DOSE","DOSE","") + "\n" + session_msg_template.format("DATE","ONE","TWO","TOTAL") + "\n" + hr


                ei_message_suffix = f"\n\n<b><i>45 Above Channel Link</i></b><i>: https://t.me/vaccinealertswb45</i>\n<b><i>Registration Portal</i></b><i>: https://selfregistration.cowin.gov.in/</i>"
                ff_message_suffix = f"\n\n<b><i>18-44 Channel Link</i></b><i>: https://t.me/vaccinealertswb</i>\n<b><i>Registration Portal</i></b><i>: https://selfregistration.cowin.gov.in/</i>"


                ei_date_msgs = []
                ff_date_msgs = []

                for session in center["sessions"]:
                    
                    # Get the session informations
                    date = session["date"]
                    session_id = session["session_id"]
                    min_age = session["min_age_limit"]
                    vaccine = session.get("vaccine","NA")
                    available_dose1 = session.get("available_capacity_dose1",0)
                    available_dose2 = session.get("available_capacity_dose2",0)
                    available = available_dose1 + available_dose2

                    # Create the dict key
                    key = (centerid,session_id,date,min_age)
                    
                    # Get the already existing dose 1 vaccine
                    prev_available_dose1 = avl_vac.get(key,[0,0])[0]
                    prev_available_dose2 = avl_vac.get(key,[0,0])[1]
                    
                    # Lists for holding session messages
                    ei_session_msgs = []
                    ff_session_msgs = []


                    if ((available_dose1 > 5 and prev_available_dose1 == 0) or (available_dose2 > 5 and prev_available_dose2 == 0)) and min_age == 18:

                        has_vaccine_ei = True
                        ei_date_msgs.append("\n"+session_msg_template.format(date,"","","")+"\n"+session_msg_template.format(vaccine[0:10],available_dose1,available_dose2,available)+"\n")
                       

                    if ((available_dose1 > 5 and prev_available_dose1 == 0) or (available_dose2 > 5 and prev_available_dose2 == 0)) and min_age == 45:

                        has_vaccine_ff = True
                        ff_date_msgs.append("\n"+session_msg_template.format(date,"","","")+"\n"+session_msg_template.format(vaccine[0:10],available_dose1,available_dose2,available)+"\n")
                    
                    
                    # For each iteration keep track of the current available dose 1 vaccine
                    if available_dose1 > 0 or available_dose2 > 0:
                        avl_vac[key] = [available_dose1,available_dose2]

                

                # Send message to 18-44 Channel
                if has_vaccine_ei:
                    
                    ei_date_msg_str = hr.join(ei_date_msgs)
                    message_body = f"{ei_message_prefix}<pre>{dose_heading}{ei_date_msg_str}{hr}</pre>{ei_message_suffix}"

                    send_message(TELEKEY,"@vaccinealertswb",message_body)
                    
                
                # Send message to 45+ Channel
                if has_vaccine_ff:

                    ff_date_msg_str = hr.join(ff_date_msgs)
                    message_body = f"{ff_message_prefix}<pre>{dose_heading}{ff_date_msg_str}{hr}</pre>{ff_message_suffix}"
                    
                    send_message(TELEKEY,"@vaccinealertswb45",message_body)
                    

                
                # Set the vaccine availibility flags as false
                has_vaccine_ei = False
                has_vaccine_ff = False


        except Exception as e:
            err_cnt += 1
            if err_cnt % 100 == 0:
                err_ratio = err_cnt/tot_cnt
                err_ratios[0] = err_ratios[1]
                err_ratios[1] = err_ratios[2]
                err_ratios[2] = err_ratio
                send_message(TELEKEY,"@wbvaccinealerterror",f"{curr_datetime} - {DIST_NAME} - BOT - Unable to connect \n1. {round(err_ratios[0],2)}\n2. {round(err_ratios[1],2)}\n3.{round(err_ratios[2],2)}\n\n{e}")
            print(f"{datetime.datetime.now()} - {e}\n")

        # For each 3 hours send script status mail
        if counter // 10800 > hrs:
            hrs = counter // 10800
            send_message(TELEKEY,"@wbvaccinealerterror",f"{curr_datetime} - {DIST_NAME} - BOT is running fine")
        
        
        # Set the last_date as curr_date
        last_date = curr_date

        # Wait for random secs
        sleep_secs = random.randint(MIN_DELAY,MAX_DELAY)
        
        # Increment counter
        counter += sleep_secs
        
        # Sleep for random seconds
        time.sleep(sleep_secs)



if __name__ == "__main__":

    dists = {}

    with open("config.json") as f_obj:
        dists = json.loads(f_obj.read())
    
    dist = dists[sys.argv[1]]

    check_vaccine_availibility(dist)



