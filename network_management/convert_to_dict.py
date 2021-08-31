import csv

### function which reads a csv file and creates a dictionary

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

