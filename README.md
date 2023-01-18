# MEGL outreach data mangement 

These materials are for the outreach management team at the Mason
Experimental Geometry Lab (MEGL). 

### In the network_management folder

1. updated_network.py: updates the network based on a list of
events from a given semester
2. generate_email.py: parses the network csv based on certain criteria and
   generates a convenient, customized csv file for mass emails 
3. email_script.py: the text used to construct the body of the email in
   generate_email
4. sample files with sensitive data redacted

Make sure to preserve the file structure. 

### In the event_management folder

1. email_confirmation.py: uses the current events csv file to generate a
   customized confirmation email of all scheduled activities with a given
   contact  
2. create_calendar.py: uses the current events csv file to generate a csv
   file of selected events for mass upload to the google calendar. Warning:
   google calendar cannot recognize a new event as a replacement of an old
   event, so to make edits, you need to delete the old event. Also, if any 
   of the entries in the csv are duplicates, then google calendar will only
   generate a single entry. 

As of January 18 2023, the files in the event_management folder have not be
tested. 

### Packages used include:

- csv 1.0
- datetime
- subprocess (only to open the files at the end for convenience, might need
  os operating system)

Hopefully that is all of them. 

