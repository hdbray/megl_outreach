import csv
import subprocess
from datetime import date

### file names

today=date.today()
date_str=today.strftime('%m_%d_%y')

network_file='network_old.csv'
updated_network_file=date_str+'network_updated.csv'
fall_events_file='fall_2020_events.csv'
spring_events_file='spring_2021_events.csv'


### functions which reads a file and creates a dictionary

def file_to_dict(file_name,optional_first_header=''):

    file_to_list=[]
    
    # open file and write to a list
    
    with open(file_name) as open_file:
        reader=csv.reader(open_file, quotechar='"')
        for row in reader:
            file_to_list.append(row)
    
    # convert to dict
    
    file_to_list_of_dicts=[]
    
    headers=file_to_list[0]

    # fair warning, if you open the csv file with excel it will add a weird
    # symbol to the top left entry in the headers. so the optional argument
    # helps with that

    if optional_first_header!='':
        headers[0]=optional_first_header
    
    for i in range(len(file_to_list)):
        file_to_list_of_dicts.append({})
        for j in range(len(headers)):
            file_to_list_of_dicts[i][headers[j]]=file_to_list[i][j]

    return file_to_list_of_dicts[1:] #the list slicing removes the row of the list which just had the headers

### list names

network_list_of_dicts=file_to_dict(network_file,'NAME')
fall_events_list_of_dicts=file_to_dict(fall_events_file,'Date')
spring_events_list_of_dicts=file_to_dict(spring_events_file,'Date')


updated_network_list_headers=['Organization Name', 'Organization Type (elementary, middle, high, library, other)', 'Contact Name', 'Contact Email', 'Title 1 School', 'Number of Times Visited', 'Year of Most Recent Visit', 'Subscribed', 'Notes']

updated_network_list_of_dicts=[]

# generate updated_network_list_of_dicts from the network_list_of_dicts

for i in range(len(network_list_of_dicts)):

    updated_network_list_of_dicts.append({})

    row=network_list_of_dicts[i]

    updated_network_list_of_dicts[i]['Organization Name']=row['NAME']
    updated_network_list_of_dicts[i]['Organization Type (elementary, middle, high, library, other)']=row['TYPE (elementary, middle, high, library, other)']
    updated_network_list_of_dicts[i]['Contact Name']=row['CONTACT 1 NAME']
    updated_network_list_of_dicts[i]['Contact Email'] =row['CONTACT 1 EMAIL']
    updated_network_list_of_dicts[i]['Title 1 School']=row['TITLE I SCHOOL']
    updated_network_list_of_dicts[i]['Number of Times Visited']=row['NUMBER OF TIMES VISITED']
    updated_network_list_of_dicts[i]['Subscribed']=row['SUBSCRIBED']
    updated_network_list_of_dicts[i]['Year of Most Recent Visit']=''
    updated_network_list_of_dicts[i]['Notes']=''


# update the updated_network_list based on fall 2020 events

# loop through the fall events
for i in range(len(fall_events_list_of_dicts)):
    row=fall_events_list_of_dicts[i]
    is_on_list=False

    # loop through the updated list to see if the teacher has worked with
    # us before
    for j in range(len(updated_network_list_of_dicts)):
        if updated_network_list_of_dicts[j]['Contact Email'].lower().strip()==row[' Contact Email'].lower().strip():
            is_on_list=True
            num_visits=updated_network_list_of_dicts[j]['Number of Times Visited']

            if num_visits!='':  # some entries have nothing entered for Number of Times Visited
                num_visits=int(num_visits)
            else: 
                num_visits=0

            updated_network_list_of_dicts[j]['Number of Times Visited']=num_visits+1
            updated_network_list_of_dicts[j]['Year of Most Recent Visit']='2020'
            break

    # If the teacher hasn't worked with us before, create a new entry
    if is_on_list==False:
        new_dict_row={}
        new_dict_row['Organization Name']=fall_events_list_of_dicts[i][' Location'].strip()
        new_dict_row['Organization Type (elementary, middle, high, library, other)']=fall_events_list_of_dicts[i][' Location Type'].strip().lower()
        new_dict_row['Contact Name']=fall_events_list_of_dicts[i][' Contact Name'].strip()
        new_dict_row['Contact Email']=fall_events_list_of_dicts[i][' Contact Email'].strip()
        new_dict_row['Title 1 School']=fall_events_list_of_dicts[i]['Title 1 School'].strip()
        new_dict_row['Number of Times Visited']='1'
        new_dict_row['Year of Most Recent Visit']='2020'
        new_dict_row['Subscribed']=''
        new_dict_row['Notes']=''
        
        updated_network_list_of_dicts.append(new_dict_row)

# update the updated_network_list based on spring 2021 events

# loop through the spring events
for i in range(len(spring_events_list_of_dicts)):
    row=spring_events_list_of_dicts[i]
    is_on_list=False

    # loop through the updated list to see if the teacher has worked with
    # us before
    for j in range(len(updated_network_list_of_dicts)):
        if updated_network_list_of_dicts[j]['Contact Email'].lower().strip()==row['Contact Email'].lower().strip():
            is_on_list=True
            num_visits=updated_network_list_of_dicts[j]['Number of Times Visited']

            if num_visits!='':  # some entries have nothing entered for Number of Times Visited
                num_visits=int(num_visits)
            else: 
                num_visits=0

            updated_network_list_of_dicts[j]['Number of Times Visited']=num_visits+1
            updated_network_list_of_dicts[j]['Year of Most Recent Visit']='2021'
            break

    # If the teacher hasn't worked with us before, create a new entry
    if is_on_list==False:
        new_dict_row={}
        new_dict_row['Organization Name']=row['Location'].strip()
        new_dict_row['Organization Type (elementary, middle, high, library, other)']=row['Location Type'].strip().lower()
        new_dict_row['Contact Name']=row['Contact Name'].strip()
        new_dict_row['Contact Email']=row['Contact Email'].strip()
        new_dict_row['Title 1 School']=row['Title 1 School'].strip()
        new_dict_row['Number of Times Visited']='1'
        new_dict_row['Year of Most Recent Visit']='2021'
        new_dict_row['Subscribed']=''
        new_dict_row['Notes']=''
#        
        updated_network_list_of_dicts.append(new_dict_row)

# convert updated_network_list_of_dicts to updated_network_list

updated_network_list=[]

updated_network_list.append(updated_network_list_headers)

for i in range(len(updated_network_list_of_dicts)):
    row=updated_network_list_of_dicts[i]
    new_row=[]
    for key in updated_network_list_headers:
        new_row.append(row[key])
    
    updated_network_list.append(new_row)





# write updated_network_file

with open(updated_network_file, 'w+') as write_file:
    write=csv.writer(write_file)
    write.writerows(updated_network_list)


# open the updated_network_file to make sure it worked

subprocess.run(['open', updated_network_file], check=True)


