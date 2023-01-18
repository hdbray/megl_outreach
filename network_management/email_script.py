from datetime import date

today=date.today()
this_year=today.year
last_year=this_year-1

### function which generates email script

def write_email(name,org,org_type,num_visits,recent_visit):
    if name!='':
        email_greeting='''Dear %s,
        ''' % (name)
    else:
        email_greeting='''Hello,
        '''

    if org_type!='other':
        email_opener='''
I'm Harry Bray, the director of outreach for the Mason Experimental Geometry Lab (MEGL) at George Mason University, writing to ask whether you'd be interested in having us in your classroom at %s for a mathematics enrichment activity this semester.
        ''' % (org)
    else: 
        email_opener= '''
I'm Harry Bray, the director of outreach for the Mason Experimental Geometry Lab (MEGL) at George Mason University, writing to ask whether you'd be interested in having us work with your student group for a mathematics enrichment activity this semester.
        ''' 

    email_opener=email_greeting+email_opener


    returning=''

    if num_visits.strip()!='':
        if recent_visit==str(this_year) or recent_visit==str(last_year):
            returning='''
We had a great time working with your students last year, and we'd be thrilled to join you again. '''
        else: 
            returning='''
You may remember the MEGL team from past activities we've run with your students. You likely worked with Dr Jack Love or Dr Sean Lawton, the previous directors of the MEGL outreach program. '''
        returning+='''As a reminder, here is a short blurb about us: 
        '''

    about_us='''
The MEGL team is a group of students and faculty at George Mason University with a passion for sharing the fun side of mathematics with K-12 students.  We have been offering free mathematics enrichment activities to local schools and other organizations since 2015, and we would be delighted to share our enthusiasm for mathematics with your students.
    '''

    covid_disclaimer='''
Due to COVID-19, we will be implementing modifications of our standard activities for safety. We can run in-person activities under the conditions that all individuals in the activity room are masked, and with the MEGL facilitators maintaining a safe distance from children, teachers, and organization leaders.  We also have virtual versions of our activities, and we can lead these for a class or group that is meeting in-person, hybrid, or online. If the school system moves to online instruction at any point this semester, then our outreach events can be run online.
    '''

    signature='''
Please let me know if you're interested in scheduling an activity with us this fall. I am happy to send more information about our available activities and to answer any questions. You can also peruse our webpage: http://megl.geometrylabs.net/outreach/activities/. 

Best,
Harry


Harry Bray, Ph. D.
MEGL Director of Outreach
Faculty, George Mason University
Pronouns: he/him/his
meglout@gmu.edu

(Unsubscribe) If you would like to be removed from our mailing list, please reply to this email. 
    '''


    email_body=email_opener+returning+about_us+covid_disclaimer+signature

    return email_body




