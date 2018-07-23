# -*- coding:ISO8859-1 -*-

# this file only normalize the file which fields arent between ""
""" USE
cd CSV
python3
import normalizeCSV
normalizeCSV.normalize('fileName.csv')
"""

def normalize(fileName):
    try:
        reader = open(fileName, 'r')                    # file to normalize
        writer = open('normalized_' + fileName, 'w')    # file normalized

        for line in reader.readlines():                 # each line
            fields = line.split(',')                    # get the fields

            for pos, field in enumerate(fields):        # each field in line

                if(not field.__eq__(fields[-1])):       # the field dosent is the last
                    writer.write('"' + field + '",')    # normalize to "value",
                else:
                    #field.replace('\n', '')
                    writer.write('"' + field.strip('\n') + '"\n')   # normalize to "value"\n

    except FileNotFoundError:
        print("File not found: " + fileName)
    except Exception as ex:
        print("Error: " + str(ex))
    else:
        reader.close()
        writer.close()