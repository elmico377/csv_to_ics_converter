import glob
from datetime import datetime, timedelta
import os
import csv

if not os.path.exists('output'):
    os.makedirs('output')

csvFiles = []
for file in glob.glob("*.csv"):
    csvFiles.append(file)

for currentCsv in csvFiles:
    with open(currentCsv, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        firstRow = True
        eventsByWeek = {}
        for row in spamreader:
            if firstRow == False:
                row[1] = datetime.strptime(row[1], '%Y-%m-%d')

                nearestMonday = row[1]

                if row[1].weekday() != 0:
                    nearestMonday = row[1] - timedelta(days=row[1].weekday())

                if nearestMonday in eventsByWeek:
                    eventsByWeek[nearestMonday].append(row[0])
                else:
                    eventsByWeek[nearestMonday] = [row[0]]
            else:
                firstRow = False
        
        sortedEventsByWeek = sorted(eventsByWeek.items())

        if ".CSV" in currentCsv:
            fileName = currentCsv.replace('.CSV','.html')
        elif ".csv" in currentCsv:
            fileName = currentCsv.replace('.csv','.html')
        else:
            filename = currentCsv + ".html"

        outFile = open(fileName, "w")
        outFile.write("<!DOCTYPE html>\n<html>\n<head>\n</head>\n<body>")
        
        responses = input("Enter the Term (1A to 4B), class (SYDE/BME), term (Spring, Summer, Fall) and year separated by commas: ")

        acceptableResponse = True
        responseList = responses.split(",")
        for response in responseList:
            response = response.strip()

        # acceptableResponse = True if responseList[0][0]

        if not acceptableResponse:
            responses = input("Enter the Term (1A to 4B), class (SYDE/BME), term (Spring, Summer, Fall) and year separated by commas: ")

        
        title = "Tentative schedule for " + responseList[0] + " " + responseList[1] + " classes for " + responseList[2] + " " + responseList[3] + "."
        warning = "To be used for PLANNING PURPOSES ONLY. Confirm due dates with the course instructors."

        outFile.write("<h2><span style=\"font-family: tahoma, sans-serif;\"><strong>" + title + "<br /><br /><span style=\"color: #9900ff;\">" + warning + "</span><br /><br /></strong></span></h2>")
        outFile.write("<table style=\"width: 946px;\" height=\"1004\">\n<tbody>")

        for currentItem in sortedEventsByWeek:
            outFile.write("<tr style=\"width: 233.542px;\">\n<td><span style=\"font-family: tahoma, sans-serif;\"><strong> Week of " + currentItem[0].strftime("%B %d") + " &mdash; <br />Deliverables &amp;&nbsp;Weights </strong></span></td>")
            outFile.write("<td style=\"width: 697.708px;\"> <span style=\"font-family: tahoma, sans-serif;\">" + "<br />".join(currentItem[1]) + "</span></td>")
            outFile.write("</tr>")

        outFile.write("</tbody>\n</table>\n<pre><br /><br /></pre>\n</body>\n</html>")
        
        outFile.close()