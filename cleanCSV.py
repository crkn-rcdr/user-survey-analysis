import csv 
import pandas
import requests

ids_to_ignore = [
    '',
    '118483853289',
    '118463536757',
    '118462539466',
    '118462536448',
    '118462533717',
    '118462520699',
    '118481419260',
    '118481416764',
    '118479331393'
]

write_list = []


def get_location(ip_address):
    response = requests.get(f'https://ipinfo.io/{ip_address}/json?token=3f84cc6db67539').json()
    print(response)
    loc = response.get('loc').split(",")
    return [response.get("city"), response.get("region"), response.get("country"), loc[0], loc[1]]

def parseRaw():
    # Open file  
    with open('raw.csv', encoding="utf8", errors='replace') as file_obj: 
        reader_obj = csv.reader(file_obj, delimiter = ',')
        i = -1
        for row in reader_obj: 
            i=i+1
            print("ROW: ", i)
            if row[0] in ids_to_ignore:
                continue

            if i == 0:
                write_list.append([
                    #Identifications
                    'id', 
                    'city', 
                    'region', 
                    'country_name', 
                    'latitude', 
                    'longitude', 

                    #Descriptor
                    'Genealogical researcher', 
                    'GLAM professional', 
                    'Government employee', 
                    'Legal researcher',	
                    'Member of the general public',
                    'Post-secondary researcher', 
                    'Student', 
                    'Teacher', 
                    'Other Identification',	

                    #Interests
                    'Computer Science', 
                    'Digital Humanities', 
                    'Education', 
                    'Environment/Climate', 
                    'Gender Studies', 
                    'Genealogy', 
                    'Geography', 
                    'Health', 
                    'History', 
                    'Indigenous Land Claims',
                    'Indigenous Studies', 
                    'Information Science', 
                    'Law', 
                    'Linguistics',
                    'Literature', 
                    'Political Science', 
                    'Other Interest' 
                ])
                print(write_list[0])
            else:
                try:
                    geo = get_location(row[4])
                except:
                    geo = ["N/A", "N/A", "N/A", "N/A", "N/A"]

                row_list = [
                    #Identifications
                    row[0],
                    geo[0],
                    geo[1],
                    geo[2],
                    geo[3],
                    geo[4],


                    #Descriptor
                    1 if len(row[9]) else 0,
                    1 if len(row[10]) else 0,
                    1 if len(row[11]) else 0,
                    1 if len(row[12]) else 0,
                    1 if len(row[13]) else 0,
                    1 if len(row[14]) else 0,
                    1 if len(row[15]) else 0,
                    1 if len(row[16]) else 0,
                    row[17].lower(), 

                    #Interests
                    1 if len(row[18]) else 0,
                    1 if len(row[19]) else 0,
                    1 if len(row[20]) else 0,
                    1 if len(row[21]) else 0,
                    1 if len(row[22]) else 0,
                    1 if len(row[23]) else 0,
                    1 if len(row[24]) else 0,
                    1 if len(row[25]) else 0,
                    1 if len(row[26]) else 0,
                    1 if len(row[27]) else 0,
                    1 if len(row[28]) else 0,
                    1 if len(row[29]) else 0,
                    1 if len(row[30]) else 0,
                    1 if len(row[31]) else 0,
                    1 if len(row[32]) else 0,
                    1 if len(row[33]) else 0,
                    row[34].lower()
                ]

                # Some glam people didn't say glam when they should have
                if 'librarian' in row_list[14] or 'archivist' in row_list[14] or 'library' in row_list[14] or 'archive' in row_list[14]:
                    row_list[7] = 1
                    row_list[14] = ''


                # 10, 27 - still need to normalize
                print(row_list)
                write_list.append(row_list)

    df = pandas.DataFrame(write_list)
    df.to_csv("cleaned.csv", encoding='utf-8', index=False)

parseRaw()