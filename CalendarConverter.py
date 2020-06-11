from datetime import datetime, timedelta
from csv_ical import Convert
import glob
import os

if not os.path.exists('output'):
    os.makedirs('output')

csvFiles = []
for file in glob.glob("*.csv"):
    csvFiles.append(file)


for currentCsv in csvFiles:
    convert = Convert()
    csvFileLocation = currentCsv

    outputFile = currentCsv.replace('.CSV','')
    outputFile = outputFile.replace('.csv','')
    outputFileDir = 'output/' + outputFile + '.ics'
    icalFileLocation = outputFileDir

    csv_configs = {
        'HEADER_ROWS_TO_SKIP': 1,
        'CSV_NAME': 0,
        'CSV_START_DATE': 1,
        'CSV_START_TIME': 2,
        'CSV_END_DATE': 3,
        'CSV_END_TIME': 4,
        'CSV_DESCRIPTION': 15,
        'CSV_LOCATION': 16,
    }

    convert.read_csv(csvFileLocation, csv_configs)

    i = 0
    while i < len (convert.csv_data):
        row = convert.csv_data[i]
        try:
            start_date = row[csv_configs['CSV_START_DATE']] + '-' + row[csv_configs['CSV_START_TIME']]
            row[csv_configs['CSV_START_DATE']] = datetime.strptime(start_date, '%Y-%m-%d-%H:%M:%S %p')

            end_date = row[csv_configs['CSV_END_DATE']] + '-' + row[csv_configs['CSV_END_TIME']]
            row[csv_configs['CSV_END_DATE']] = datetime.strptime(end_date, '%Y-%m-%d-%H:%M:%S %p')
            
            i += 1
        except ValueError:
            convert.csv_data.pop(i)

    convert.make_ical(csv_configs)
    convert.save_ical(icalFileLocation)