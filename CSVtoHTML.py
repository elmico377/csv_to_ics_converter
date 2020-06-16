import glob
from datetime import datetime, timedelta
import os
import csv

def strIsOneOfList(strToCompare, listOfStrings):
    for curStr in listOfStrings:
        if curStr == strToCompare:
            return True
    
    return False

def verifyResponse(responseList):
    responseStatus = True

    try:
        studyYear = int(responseList[0][0])
        responseStatus = True if studyYear <= 4 and studyYear > 0 else False
        if responseStatus:
            studyTerm = responseList[0][1]
            responseStatus = True if studyTerm == 'A' or studyTerm == 'B' else False
            if responseStatus:
                responseStatus = True if strIsOneOfList(responseList[1], ['SYDE','BME']) else False
                if responseStatus:
                    responseStatus = strIsOneOfList(responseList[2],['spring','fall','winter'])
                    if responseStatus:
                        try:
                            curYear = int(responseList[3])
                        except:
                            responseStatus = False
                            print('Year must be in numerical format e.g. [2020]')
                    else:
                        print('Season can only be [spring], [fall], or [winter]')
                else:
                    print('Class can only be [SYDE] or [BME]')
            else:
                print('Term can only be [A] or [B]')
        else:
            print('Term year out of bounds can only be [1], [2], [3], or [4]')
    except:
        responseStatus = False
        print('Term year was not found')

    return responseStatus

def createHTMLFromDirectory():
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
                fileName = currentCsv + ".html"

            fileName = "output/" + datetime.now().strftime("%Y-%m-%d-%H-%M-%S-")  + fileName 
            outFile = open(fileName, "w")
            outFile.write("<!DOCTYPE html>\n<html>\n<head>\n</head>\n<body>")
            
            acceptableResponse = False

            while acceptableResponse == False:
                responses = input("Enter the Term (1A to 4B), class (SYDE/BME), season (Spring, Summer, Fall) and year (2020) separated by commas: ")

                responseList = responses.split(",")
                if len(responseList) == 4:
                    responseList[0] = responseList[0].upper()
                    responseList[0] = responseList[0].strip()
                    responseList[1] = responseList[1].upper()
                    responseList[1] = responseList[1].strip()
                    responseList[2] = responseList[2].lower()
                    responseList[2] = responseList[2].strip()
                    responseList[3] = responseList[3].strip()

                    acceptableResponse = verifyResponse(responseList)
                else:
                    print('Incorrect number of responses')
            
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
