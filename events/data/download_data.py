from urllib.request import Request, urlopen
from urllib.error import  URLError
import re
import logging
from io import BytesIO
from zipfile import ZipFile
import psycopg2

# Setup logging
logging.basicConfig(filename='../root/platinum/events/data/download_log.log', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

# Check for the last file downloaded
olddownload = open('../root/platinum/events/data/download_last.txt', 'r+')
oldurl = olddownload.read()
olddownload.close()

# Read the new file and location from GDELT
req = Request('http://data.gdeltproject.org/gdeltv2/lastupdate.txt')
try:
    response = urlopen(req)
except URLError as e:
    if hasattr(e, 'reason'):
        logging.error('Location File - Failed to reach the server: ' + e.reason)
    elif hasattr(e, 'code'):
        logging.error('Location File - The Server couldn\'t fulfill the request: ' + e.code)
else:
    # Parse the location file
    list = re.split('[ \n]', response.read().decode('utf-8'))
    url = list[2]

    # Confirm that the file has not changed shape and we have a correct URL
    if url.startswith('http://') and url.lower().endswith('.export.csv.zip'):

        # Make sure the URL we have is not the same as the last one
        if url != oldurl:
            newdownload = open('../root/platinum/events/data/download_last.txt', 'w+')
            newdownload.write(url)
            newdownload.close()

            # Download the data file
            req = Request(url)
            try:
                response = urlopen(req)
            except URLError as e:
                if hasattr(e, 'reason'):
                    logging.error('Data File - Failed to reach the server: ' + e.reason)
                elif hasattr(e, 'code'):
                    logging.error('Data File - The Server couldn\'t fulfill the request: ' + e.code)
            else:

                # Open a link to the database
                conn = psycopg2.connect('host=localhost dbname=platinum user=platinum password=platinum1')
                cur = conn.cursor()

                # Open the zip file and extract the csv
                with ZipFile(BytesIO(response.read())) as my_zip_file:
                    for contained_file in my_zip_file.namelist():

                        # Open the CSV and write to a database
                        for line in my_zip_file.open(contained_file).readlines():
                            line = re.split('\t', line.decode('utf-8'))

                            if line[4] == '':
                                line[4] = '0.0'
                            if line[30] == '':
                                line[30] = '0.0'
                            if line[34] == '':
                                line[34] = '0.0'
                            if line[40] == '':
                                line[40] = '0.0'
                            if line[41] == '':
                                line[41] = '0.0'
                            if line[48] == '':
                                line[48] = '0.0'
                            if line[49] == '':
                                line[49] = '0.0'
                            if line[56] == '':
                                line[56] = '0.0'
                            if line[57] == '':
                                line[57] = '0.0'

                            if line[26][:2] == '01':
                            	line[26] = 'Public Statement'
                            if line[26][:2] == '02':
                            	line[26] = 'Appealing'
                            if line[26][:2] == '03':
                            	line[26] = 'Intending to cooperate'
                            if line[26][:2] == '04':
                            	line[26] = 'Consulting'
                            if line[26][:2] == '05':
                            	line[26] = 'Diplomatic cooperation'
                            if line[26][:2] == '06':
                            	line[26] = 'Material cooperation'
                            if line[26][:2] == '07':
                            	line[26] = 'Providing aid'
                            if line[26][:2] == '08':
                            	line[26] = 'Yielding'
                            if line[26][:2] == '09':
                            	line[26] = 'Investigating'
                            if line[26][:2] == '10':
                            	line[26] = 'Demanding'
                            if line[26][:2] == '11':
                            	line[26] = 'Disapproving'
                            if line[26][:2] == '12':
                            	line[26] = 'Rejecting'
                            if line[26][:2] == '13':
                            	line[26] = 'Threatening'
                            if line[26][:2] == '14':
                            	line[26] = 'Protesting'
                            if line[26][:2] == '15':
                            	line[26] = 'Exhibiting a force posture'
                            if line[26][:2] == '16':
                            	line[26] = 'Reducing relations'
                            if line[26][:2] == '17':
                            	line[26] = 'Coercing'
                            if line[26][:2] == '18':
                            	line[26] = 'Assaulting'
                            if line[26][:2] == '19':
                            	line[26] = 'Fighting'
                            if line[26][:2] == '20':
                            	line[26] = 'Unconditional mass violence'

                            line[59] = line[59][6:8] + '/' + line[59][4:6] + '/' + line[59][0:4] + ' ' + line[59][8:10] + ':' + line[59][10:12] + ':' + line[59][12:]

                            list1 = line[60].replace('.', '/').replace('_', '/').split('/')
                            best = 0
                            for value1 in list1:
                                if best < value1.count('-'):
                                     line[60] = value1.replace('-', ' ')
                            list2 = line[60].split(' ')
                            for value2 in list2:
                                if isinstance(value2, int) and value2 > 9999:
                                    line[60].replace(value2, '')

                            try:
                                cur.execute('INSERT INTO events_event ("GlobalEventID", "Day", "MonthYear", "Year", "FractionDate", "Actor1Code", "Actor1Name", "Actor1CountryCode", "Actor1KnownGroupCode", "Actor1EthnicCode", "Actor1Religion1Code", "Actor1Religion2Code", "Actor1Type1Code", "Actor1Type2Code", "Actor1Type3Code", "Actor2Code", "Actor2Name", "Actor2CountryCode", "Actor2KnownGroupCode", "Actor2EthnicCode", "Actor2Religion1Code", "Actor2Religion2Code", "Actor2Type1Code", "Actor2Type2Code", "Actor2Type3Code", "IsRootEvent", "EventCode", "EventBaseCode", "EventRootCode", "QuadClass", "GoldsteinScale", "NumMentions", "NumSources", "NumArticles", "AvgTone", "Actor1Geo_Type", "Actor1Geo_Fullname", "Actor1Geo_CountryCode", "Actor1Geo_ADM1Code", "Actor1Geo_ADM2Code", "Actor1Geo_Lat", "Actor1Geo_Long", "Actor1Geo_FeatureID", "Actor2Geo_Type", "Actor2Geo_Fullname", "Actor2Geo_CountryCode", "Actor2Geo_ADM1Code", "Actor2Geo_ADM2Code", "Actor2Geo_Lat", "Actor2Geo_Long", "Actor2Geo_FeatureID", "ActionGeo_Type", "ActionGeo_Fullname", "ActionGeo_CountryCode", "ActionGeo_ADM1Code", "ActionGeo_ADM2Code", "ActionGeo_Lat", "ActionGeo_Long", "ActionGeo_FeatureID", "DateAdded", "SourceURL") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8], line[9], line[10], line[11], line[12], line[13], line[14], line[15], line[16], line[17], line[18], line[19], line[20], line[21], line[22], line[23], line[24], line[25], line[26], line[27], line[28], line[29], line[30], line[31], line[32], line[33], line[34], line[35], line[36], line[37], line[38], line[39], line[40], line[41], line[42], line[43], line[44], line[45], line[46], line[47], line[48], line[49], line[50], line[51], line[52], line[53], line[54], line[55], line[56], line[57], line[58], line[59], line[60].capitalize()))
                            except:
                                pass

                            conn.commit()

        else:
            logging.error('Location File - The data file location has not been updated.')
