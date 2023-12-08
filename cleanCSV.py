import os
import csv 
import pandas
import re
import json
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
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    location_data = {
        "ip": ip_address,
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country_name")
    }
    return location_data["city"] + ", " + location_data["country"]

def parseRaw():
    # Open file  
    with open('raw.csv') as file_obj: 
        reader_obj = csv.reader(file_obj)
        i = -1
        for row in reader_obj: 
            i=i+1
            if row[0] in ids_to_ignore:
                continue

            if i == 0:
                write_list.append([
                    #Identifications
                    'id', #A - 0
                    'geo', #E - 4

                    #Descriptor
                    'Genealogical researcher', #J - 9
                    'GLAM professional', #K - 10
                    'Government employee', #L - 11
                    'Legal researcher',	#M - 12
                    'Member of the general public', #N - 13
                    'Post-secondary researcher', #O - 14
                    'Student', #P - 15
                    'Teacher', #Q - 16
                    'Other Identification',	#R - 17

                    #Interests
                    'Computer Science', #S - 18
                    'Digital Humanities', #T - 19
                    'Education', #U - 20
                    'Environment/Climate', #V - 21
                    'Gender Studies', #W - 22
                    'Genealogy', #X - 23
                    'Geography', #Y - 24
                    'Health', #Z - 25
                    'History', #AA - 26
                    'Indigenous Land Claims', #AB - 27
                    'Indigenous Studies', #AC - 28
                    'Information Science', #AD - 29
                    'Law', #AE - 30
                    'Linguistics', #AF - 31
                    'Literature', #AG - 32
                    'Political Science', #AH - 33
                    'Other Interest' #AI - 34
                ])
                print(write_list[0])
            else:
                try:
                    geo = get_location(row[4])
                except:
                    geo = "N/A"

                row_list = [
                    #Identifications
                    row[0],
                    geo,

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
                if 'librarian' in row_list[10] or 'archivist' in row_list[10] or 'library' in row_list[10] or 'archive' in row_list[10]:
                    row_list[3] = 1

                # 10, 27 - still need to normalize
                print(row_list)
                write_list.append(row_list)

    df = pandas.DataFrame(write_list)
    df.to_csv("cleaned.csv", encoding='utf-8', index=False)

def byGeo():
    # Open file  
    with open('cleaned.csv') as file_obj: 
        reader_obj = csv.reader(file_obj)
        i = -1
        geo_map_a = {}
        geo_map_b = {}
        for row in reader_obj: 
            i=i+1
            if i != 0:
                if row[1] in geo_map_a:
                    list_one = geo_map_a[row[1]]
                    list_two = row[2:10]
                    geo_map_a[row[1]] = [int(x) + int(y) for x, y in zip(list_one, list_two)]

                    list_one = geo_map_b[row[1]]
                    list_two = row[11:27]
                    geo_map_b[row[1]] = [int(x) + int(y) for x, y in zip(list_one, list_two)]
                else:
                    geo_map_a[row[1]] = [int(x) for x in row[2:10]]
                    geo_map_b[row[1]] = [int(x) for x in row[11:27]]
                    
        

        def make_sheet(titles, geo_map):
            csv_list = [titles]
            for k in geo_map:
                row_list = [k]
                row_list += geo_map[k]
                csv_list.append(row_list)
            return csv_list

        titles_a = [
        'Geo',
        'Genealogical researcher', #J - 9
        'GLAM professional', #K - 10
        'Government employee', #L - 11
        'Legal researcher',	#M - 12
        'Member of the general public', #N - 13
        'Post-secondary researcher', #O - 14
        'Student', #P - 15
        'Teacher', #Q - 16
        ]

        df = pandas.DataFrame(make_sheet(titles_a, geo_map_a))
        df.to_csv("geo_q1.csv", encoding='utf-8', index=False)
        
        titles_b = [
            'Geo',
            'Computer Science', #S - 18
            'Digital Humanities', #T - 19
            'Education', #U - 20
            'Environment/Climate', #V - 21
            'Gender Studies', #W - 22
            'Genealogy', #X - 23
            'Geography', #Y - 24
            'Health', #Z - 25
            'History', #AA - 26
            'Indigenous Land Claims', #AB - 27
            'Indigenous Studies', #AC - 28
            'Information Science', #AD - 29
            'Law', #AE - 30
            'Linguistics', #AF - 31
            'Literature', #AG - 32
            'Political Science', #AH - 33
        ]

        df = pandas.DataFrame(make_sheet(titles_b, geo_map_b))
        df.to_csv("geo_q2.csv", encoding='utf-8', index=False)

byGeo()