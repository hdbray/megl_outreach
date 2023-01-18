import csv
import subprocess
from datetime import date


#functions

def activity_to_full_activity(activity):
    if activity=='monsters':
        return 'You Can Count on Monsters'
    if activity=='numbers':
        return 'Really Big Numbers'
    if activity=='liars':
        return 'Your Teachers are Lying to You'
    if activity=='infinity':
        return 'Playground of the Infinite'

def prep_script(activity):
    activityname=activity_to_full_activity(activity)
    start_script=''
    instructions_script=''
    start_script='''
For the activity "%s," please ask the students to come prepared by bringing the following: 
    ''' % (activityname)
    if activity=='monsters':
        instructions_script='''
    1. paper and pens, pencils, or coloring tools like crayons and markers.
    2. 25-30 small objects that they can count, about the size of a coin.  Past students have brought dried beans, macaroni pasta, cereal pieces, and other small objects.  
    3. a space where they can draw on their papers.
    4. if possible, please join with a laptop and a video camera, so we can see your lovely creations! 
        ''' 
    if activity=='numbers':
        instructions_script='''
    1. a large collection of things to count. You could bring a bag of dried beans, a large pile of coins, or a box of your favorite cereal.  
    2.  pens/pencils/markers, and paper.  
    3. a working space where you can draw.
    4. if possible, please join on a laptop with a video camera, so you can show everyone your work!
        '''

    if activity=='infinity':
        instructions_script='''
    1. Two different kinds of objects, and between 10 and 20 of each object.  For example, you could bring 10 lego blocks and 14 coins. 
    2. If possible, please join on a laptop so you can draw on the virtual whiteboards with us. 
        '''

    if activity=='liars':
        instructions_script='''
    1. At least two strips of paper, each of them about 2"x11.5" long.
    2. Some tape and a pen or pencil.
    3. If possible, a balloon (or two, in case the first one pops) and a sharpie or marker to draw on it. 
        '''

    return start_script+instructions_script

def create_email_schedule(weekday,date,starttime,endtime,activity,agegrp):
    event_schedule='''
    %s %s at %s-%s : %s with %s''' % (weekday, date, starttime, endtime, activity, agegrp)
    return event_schedule



#implementation

today=date.today()

date_str=today.strftime('%m_%d_%y')
event_csv_filename='spring_2022_events.csv'
new_csv_filename='email_files/'+date_str+'_for_email_confirmation_'+event_csv_filename

# create the events list from the source file

events_list=[]
events_list_of_dicts=[]

events_list_for_mail_merge=[['Email','Name','Body']]

#read the csv

with open(event_csv_filename) as open_file:
    reader=csv.reader(open_file, quotechar='"')
    for row in reader:
        events_list.append(row)

#convert to dictionary

k=len(events_list)

for i in range(k):
    events_list_of_dicts.append({})
 
headers=['Date']+events_list[0][1:]

for i in range(k):
    for j in range(len(headers)):
        events_list_of_dicts[i][headers[j]]=events_list[i][j]

emails_set=set()

# only keep the entries which you have flagged as needed a confirmation
# email
# I'm sure this code could be more direct

short_list_of_dicts=[]

for i in range(len(events_list_of_dicts)):
    event_entry=events_list_of_dicts[i]
    needs_email=event_entry['Prep email'].strip()
    if needs_email=='y':
        email=event_entry['Contact Email']
        name=event_entry['Contact Name']
        school=event_entry['Organization']
        emails_set.add((email,name,school))
        short_list_of_dicts.append(event_entry)


# for_emailing_list_of_dicts is an interesting data structure and needs
# explanation but the goal is going to be that for each unique email
# address, we consolidate all the events happening into a dictionary, so
# that this person only receives one email for all, say, five events
# instead of receiving five different emails for the five different events. 

for_emailing_list_of_dicts=[]

# emails_list is just to keep things in some semblance of order for adding to
# for_emailing_list_of_dicts, which is needed (or helpful) for conversion
# to a csv at the end. 

emails_list=list(emails_set)


for i in range(len(emails_list)):
    for_emailing_list_of_dicts.append({})
    for_emailing_list_of_dicts[i]['Contact Email']=emails_list[i][0]
    for_emailing_list_of_dicts[i]['Contact Name']=emails_list[i][1]
    for_emailing_list_of_dicts[i]['Location']=emails_list[i][2]


for i in range(len(for_emailing_list_of_dicts)):
    email=for_emailing_list_of_dicts[i]['Contact Email']
    events_with_contact=[]
    activity_set=set()
    for j in range(len(short_list_of_dicts)):
        if short_list_of_dicts[j]['Contact Email']==email:
            event_entry=short_list_of_dicts[j]
            key_set=('Weekday','Date','Start Time','End Time','Activity','Age Group')
            new_event=dict((k,event_entry[k]) for k in key_set if k in event_entry)
#            weekday=event_entry['Weekday']
#            date=event_entry['Date']
#            starttime=event_entry['Start Time']
#            endtime=event_entry['End Time']
            activity=event_entry['Activity']
#            name=event_entry['Contact Name']
#            agegrp=event_entry['Age Group']
    
#            events_with_contact.append([weekday,date,starttime, endtime,activity,agegrp])
            events_with_contact.append(new_event)
            activity_set.add(activity)

    for_emailing_list_of_dicts[i]['All Events']=events_with_contact
    for_emailing_list_of_dicts[i]['All Activities']=activity_set



# ok now you have a fun looking list of dictionariez with all these
# subdictionaries and you can generate an interesting email from this. 

# I think it's just about ready to implement 
# Now you have to change your other code though

for i in range(len(for_emailing_list_of_dicts)):
    event_entry=for_emailing_list_of_dicts[i]
    email=event_entry['Contact Email']
    contact=event_entry['Contact Name']
    school=event_entry['Location']

    opener='''Dear %s,

I'm looking forward to the following upcoming MEGL events with your %s students:
        ''' % (contact,school)

    schedule=''

    events_list=event_entry['All Events']

    for specific_event_dict in events_list:
        weekday=specific_event_dict['Weekday']
        date=specific_event_dict['Date']
        starttime=specific_event_dict['Start Time']
        endtime=specific_event_dict['End Time']
        activity=specific_event_dict['Activity']
        agegrp=specific_event_dict['Age Group']

        specific_event_sched_str=create_email_schedule(weekday,date,starttime,endtime,activity,agegrp)
        schedule=schedule+specific_event_sched_str

    prep_instructions=''

    all_activities=event_entry['All Activities']
    for specific_activity in all_activities: 
        specific_activity_prep=prep_script(specific_activity)
        prep_instructions=prep_instructions+specific_activity_prep

    spacer='''
    '''

    signature=''' 
Please do let me know if any of the above looks off to you!  If you have not yet sent a meeting link, please do send that along when you can, or let me know if you need me to send you my meeting link.  Feel free to send any questions my way. I look forward to it!

Best,
Harry
        '''

    body=opener+schedule+spacer+prep_instructions+signature
    events_list_for_mail_merge.append([email,contact,body])


# write the new list to a csv

with open(new_csv_filename, 'w+') as write_file:
    write=csv.writer(write_file)
    write.writerows(events_list_for_mail_merge)
#
#
#with open(event_csv_filename, 'w+') as write_file:
#    write=csv.writer(write_file)
#    write.writerows(events_list)
#
subprocess.run(['open', new_csv_filename], check=True)
#subprocess.run(['open', event_csv_filename], check=True)
