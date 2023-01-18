import csv
import subprocess
from datetime import date
import convert_to_dict as cd
import email_script 

### file names

today=date.today()
#this_year=today.year
#last_year=this_year-1
date_str=today.strftime('%m_%d_%y')

network_file='sample_network.csv'
email_file='email_files/'+date_str+'_email_script.csv'


### make sure the network is appropriately organized with each of these
### tags
### select which of these you would like to email

#use_these_org_types={'other','library'}
#use_these_org_types={'elementary'}
use_these_org_types={'middle', 'high'}
#use_these_org_types={'other','library','elementary','middle', 'high'}
use_these_org_types={'elementary', 'middle','library'}

### list names

network_list=[]
email_script_list=[['Email','Name','Body']]


### read network file and create dictionary

network_list_of_dicts=cd.file_to_dict(network_file,'Organization Name')

for i in range(0,len(network_list_of_dicts)):

    row=network_list_of_dicts[i]
    # pull inputs for write_email function
    email_address=row['Contact Email'].strip()
    name=row['Contact Name']
    org=row['Organization Name']
    org_type=row['Organization Type (elementary, middle, high, library, other)']
    num_visits=row['Number of Times Visited']
    recent_visit=row['Year of Most Recent Visit']
    subscribed=row['Subscribed'].strip().lower()


    # add a new row to the email_script_list if the contact is subscribed
    # and the org_type is in the use_these_org_types set
    if subscribed!='no' and email_address!='' and org_type in use_these_org_types:

        # apply write_email from email_script.py to inputs 
        the_email=email_script.write_email(name,org,org_type,num_visits,recent_visit)
        # append to list that will be written to csv
        email_script_list.append([email_address, name, the_email])

# write email_script_list to the email_file, ready for mail_merge 

with open(email_file, 'w+') as write_file:
    write=csv.writer(write_file)
    write.writerows(email_script_list)


# open the email_file to make sure it worked

subprocess.run(['open', email_file], check=True)



