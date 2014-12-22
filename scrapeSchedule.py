# scrapeSchedule.py
# scrapes the UCSD schedule and turns it into a .csv file
#

from bs4 import BeautifulSoup
import requests
import urllib.parse
import re

FILENAME = "data"

rawPost = "selectedTerm=WI14&xsoc_term=&loggedIn=false&tabNum=&selectedSubjects=AIP+&selectedSubjects=AAS+&selectedSubjects=ANES&selectedSubjects=ANBI&selectedSubjects=ANAR&selectedSubjects=ANTH&selectedSubjects=ANSC&selectedSubjects=AUD+&selectedSubjects=BENG&selectedSubjects=BNFO&selectedSubjects=BIEB&selectedSubjects=BICD&selectedSubjects=BIPN&selectedSubjects=BIBC&selectedSubjects=BGGN&selectedSubjects=BGRD&selectedSubjects=BGSE&selectedSubjects=BILD&selectedSubjects=BIMM&selectedSubjects=BISP&selectedSubjects=BIOM&selectedSubjects=CMM+&selectedSubjects=CENG&selectedSubjects=CHEM&selectedSubjects=CHIN&selectedSubjects=CLAS&selectedSubjects=CLIN&selectedSubjects=CLRE&selectedSubjects=COGS&selectedSubjects=COMM&selectedSubjects=COGR&selectedSubjects=CSE+&selectedSubjects=ICAM&selectedSubjects=CONT&selectedSubjects=CGS+&selectedSubjects=CAT+&selectedSubjects=TDCH&selectedSubjects=TDHD&selectedSubjects=TDMV&selectedSubjects=TDPF&selectedSubjects=TDTR&selectedSubjects=DOC+&selectedSubjects=ECON&selectedSubjects=EDS+&selectedSubjects=ERC+&selectedSubjects=ECE+&selectedSubjects=EMED&selectedSubjects=ENG+&selectedSubjects=ENVR&selectedSubjects=ESYS&selectedSubjects=ETHN&selectedSubjects=FPM+&selectedSubjects=FPMU&selectedSubjects=FILM&selectedSubjects=GLBH&selectedSubjects=HLAW&selectedSubjects=HITO&selectedSubjects=HIAF&selectedSubjects=HIEA&selectedSubjects=HIEU&selectedSubjects=HILA&selectedSubjects=HISC&selectedSubjects=HINE&selectedSubjects=HIUS&selectedSubjects=HIGR&selectedSubjects=HILD&selectedSubjects=HDP+&selectedSubjects=HUM+&selectedSubjects=INTL&selectedSubjects=IRCO&selectedSubjects=IRGN&selectedSubjects=IRLA&selectedSubjects=JAPN&selectedSubjects=JUDA&selectedSubjects=LATI&selectedSubjects=LAWS&selectedSubjects=LHCO&selectedSubjects=LISL&selectedSubjects=LIAB&selectedSubjects=LIDS&selectedSubjects=LIFR&selectedSubjects=LIGN&selectedSubjects=LIGM&selectedSubjects=LIHL&selectedSubjects=LIIT&selectedSubjects=LIPO&selectedSubjects=LISP&selectedSubjects=LTAM&selectedSubjects=LTCO&selectedSubjects=LTCS&selectedSubjects=LTEU&selectedSubjects=LTFR&selectedSubjects=LTGM&selectedSubjects=LTGK&selectedSubjects=LTIT&selectedSubjects=LTKO&selectedSubjects=LTLA&selectedSubjects=LTRU&selectedSubjects=LTSP&selectedSubjects=LTTH&selectedSubjects=LTWR&selectedSubjects=LTEN&selectedSubjects=LTWL&selectedSubjects=LTEA&selectedSubjects=MMW+&selectedSubjects=MBC+&selectedSubjects=MATS&selectedSubjects=MATH&selectedSubjects=MSED&selectedSubjects=MAE+&selectedSubjects=MDE+&selectedSubjects=MED+&selectedSubjects=MUIR&selectedSubjects=MCWP&selectedSubjects=MUS+&selectedSubjects=NANO&selectedSubjects=NEU+&selectedSubjects=OPTH&selectedSubjects=ORTH&selectedSubjects=PATH&selectedSubjects=PEDS&selectedSubjects=PHAR&selectedSubjects=SPPS&selectedSubjects=PHIL&selectedSubjects=PHYS&selectedSubjects=POLI&selectedSubjects=PSY+&selectedSubjects=PSYC&selectedSubjects=RMAS&selectedSubjects=RAD+&selectedSubjects=MGTF&selectedSubjects=MGT+&selectedSubjects=RELI&selectedSubjects=RMED&selectedSubjects=REV+&selectedSubjects=SDCC&selectedSubjects=SOMI&selectedSubjects=SOMC&selectedSubjects=SIO+&selectedSubjects=SXTH&selectedSubjects=SOCG&selectedSubjects=SOCI&selectedSubjects=SE++&selectedSubjects=SURG&selectedSubjects=TDAC&selectedSubjects=TDDE&selectedSubjects=TDDR&selectedSubjects=TDGE&selectedSubjects=TDGR&selectedSubjects=TDHT&selectedSubjects=TDPW&selectedSubjects=TDPR&selectedSubjects=TWS+&selectedSubjects=TMC+&selectedSubjects=USP+&selectedSubjects=VIS+&selectedSubjects=WARR&selectedSubjects=WCWP&selectedSubjects=WES+&_selectedSubjects=1&schedOption1=true&_schedOption1=on&_schedOption11=on&_schedOption12=on&schedOption2=true&_schedOption2=on&_schedOption4=on&_schedOption5=on&_schedOption3=on&_schedOption7=on&_schedOption8=on&_schedOption13=on&_schedOption10=on&_schedOption9=on&schDay=M&_schDay=on&schDay=T&_schDay=on&schDay=W&_schDay=on&schDay=R&_schDay=on&schDay=F&_schDay=on&schDay=S&_schDay=on&schStartTime=12%3A00&schStartAmPm=0&schEndTime=12%3A00&schEndAmPm=0&_selectedDepartments=1&schedOption1Dept=true&_schedOption1Dept=on&_schedOption11Dept=on&_schedOption12Dept=on&schedOption2Dept=true&_schedOption2Dept=on&_schedOption4Dept=on&_schedOption5Dept=on&_schedOption3Dept=on&_schedOption7Dept=on&_schedOption8Dept=on&_schedOption13Dept=on&_schedOption10Dept=on&_schedOption9Dept=on&schDayDept=M&_schDayDept=on&schDayDept=T&_schDayDept=on&schDayDept=W&_schDayDept=on&schDayDept=R&_schDayDept=on&schDayDept=F&_schDayDept=on&schDayDept=S&_schDayDept=on&schStartTimeDept=12%3A00&schStartAmPmDept=0&schEndTimeDept=12%3A00&schEndAmPmDept=0&courses=&sections=&instructorType=begin&instructor=&titleType=contain&title=&_hideFullSec=on&_showPopup=on"

# turn the raw Post data into a formatted dict to use with requests
data_dict = urllib.parse.parse_qsl(rawPost)
page = 1
data_dict.append(('page', page))

# Open a request and the csv
r = requests.post("https://act.ucsd.edu/scheduleOfClasses/scheduleOfClassesStudentResult.htm", data=data_dict)
database = open("./" + FILENAME + ".csv", 'r+')

# Loop through the pages until we get an error
while ("Exception report" not in r.text):
    
    # Increment the page count
    page+=1
    data_dict[-1] = ('page', page)
   
    # turn the raw html into soup
    soup = BeautifulSoup(r.text)
    
    # Find class section divs
    classTimes = soup.find_all("tr", {"class":"sectxt"})
    
    # Iterate through the list of results
    for classDef in classTimes:
        
        # Ensure they're the right divs (other divs are sectxt too). This is how many sub-elements the div has
        if len(list(classDef)) == 27:

            # Find the department the class is in (the last h2)
            department = classDef.find_previous("h2").span.string
            
            # And extract it from the formatting
            department = department[department.find("(") + 1 : department.find(")")] 
            
            # Go through each of the sub-elements in the class's div
            for i, tag in enumerate(classDef):
                
                # See if it's the day of the week
                if re.match("^(M)?(Tu)?(W)?(Th)?(F)?\s*$", str(tag.string)) and tag.string not in ["\n", ""]:
                    
                    # Get Course Number
                    numFind = classDef.find_all_previous("td", {"class":"crsheader"})
                    for num in numFind:
                        if re.match("[1-9].*", str(num.string)):
                            print(department + num.string)
                            database.write("\"" + str(department + num.string) + "\",")
                            break;
                    
                    # Iterate through the the section information: date, time, building, room. 
                    for j in range(0,7,2):
                        print(list(classDef)[i + j].string)
                        database.write(str(list(classDef)[i + j].string).strip() + ",")
                    database.write("\n")
                    break

    # update the request to the next page                
    r = requests.post("https://act.ucsd.edu/scheduleOfClasses/scheduleOfClassesStudentResult.htm", data=data_dict)

