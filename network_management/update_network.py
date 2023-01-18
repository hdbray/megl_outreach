import csv
import convert_to_dict as cd
import subprocess
from datetime import date

### file names

today=date.today()
date_str=today.strftime('%m_%d_%y')

network_file='sample_network.csv'
updated_network_file=date_str+'_network_updated.csv'
add_events_file='sample_events.csv'
year='2022'


### list names

### file_to_dict converts the file to a list of dictionaries; each row is a
### #dictionary with header determined by the column entry

network_list_of_dicts=cd.file_to_dict(network_file,'Organization Name')
events_list_of_dicts=cd.file_to_dict(add_events_file,'Date')

updated_network_list_of_dicts=network_list_of_dicts

updated_network_list_headers=updated_network_list_of_dicts[0].keys()


### update the updated_network_list based on add_events_file

### loop through the events
for i in range(len(events_list_of_dicts)):
    row=events_list_of_dicts[i]
    is_on_list=False

    # loop through the updated list to see if the teacher has worked with
    # us before
    # make sure the email addresses in the events file are always populated
    # so you don't get errors here

    for j in range(len(updated_network_list_of_dicts)):
        if updated_network_list_of_dicts[j]['Contact Email'].lower().strip()==row['Contact Email'].lower().strip() and updated_network_list_of_dicts[j]['Contact Email'].lower().strip()!='':
            is_on_list=True
            num_visits=updated_network_list_of_dicts[j]['Number of Times Visited']

            if num_visits!='':  # some entries have nothing entered for Number of Times Visited
                num_visits=int(num_visits)
            else: 
                num_visits=0

                # note that this data sheet is recording a lower bound on
                # total number of visits to a teacher

            updated_network_list_of_dicts[j]['Number of Times Visited']=num_visits+1
            updated_network_list_of_dicts[j]['Year of Most Recent Visit']='2022'
            break

    # If the teacher hasn't worked with us before, create a new entry

    if is_on_list==False:
        new_dict_row={}
        new_dict_row['Organization Name']=events_list_of_dicts[i]['Organization Name'].strip()
        new_dict_row['Organization Type (elementary, middle, high, library, other)']=events_list_of_dicts[i]['Organization Type'].strip().lower()
        new_dict_row['Contact Name']=events_list_of_dicts[i]['Contact Name'].strip()
        new_dict_row['Contact Email']=events_list_of_dicts[i]['Contact Email'].strip()
        new_dict_row['Title 1 School']=events_list_of_dicts[i]['Title 1 School'].strip()
        new_dict_row['Number of Times Visited']='1'
        new_dict_row['Year of Most Recent Visit']='2020'
        new_dict_row['Subscribed']=''
        new_dict_row['Notes']=''
        
        updated_network_list_of_dicts.append(new_dict_row)

### convert the list of dicts to a list of lists 
### need to be able to write to csv file

updated_network_list=[]

updated_network_list.append(updated_network_list_headers)

for i in range(len(updated_network_list_of_dicts)):
    row=updated_network_list_of_dicts[i]
    new_row=[]
    for key in updated_network_list_headers:
        new_row.append(row[key])
    
    updated_network_list.append(new_row)


### write updated_network_file

with open(updated_network_file, 'w+') as write_file:
    write=csv.writer(write_file)
    write.writerows(updated_network_list)


### open the updated_network_file to make sure it worked
### this might only work with os operating system

subprocess.run(['open', updated_network_file], check=True)


