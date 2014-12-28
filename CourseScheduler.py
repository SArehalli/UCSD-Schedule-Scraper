import MySQLdb as mdb
import time

def getLHSchedule(quarter, hall, day, con):
    # Search the DB for matching courses
    cur = con.cursor()
    cur.execute("SELECT * FROM " + quarter + " WHERE building=\'" + hall + "\' and days REGEXP \'.*" + day + ".*\'")
    res = cur.fetchall()
    
    # Extract the name, room, and time from the database's response. Change the time parameter so it's sortable
    Results = [(n, r, toTimes(t)) for (n, d, t, b, r) in res]
    
    # Sort them to temporal order
    Results.sort(key=lambda tup: tup[2][0])

    # Turn the time result into something human readable
    Results = [(n, r, time.strftime("%I:%M", t[0][0]) + "-" + time.strftime("%I:%M %p", t[0][1]) ) for (n, r, t) in Results]

    return Results 

def toTimes(tString):
    # Turn the time string into a tuple of sortable time objects
    
    tStrings = tString.split('-')
    fString = '%I:%M%p'
    return (time.strptime(tStrings[0] + "m", fString), time.strptime(tStrings[1] + "m", fString)), 

if __name__ == '__main__':
    q = 'WI15'
    h = raw_input('hall')
    d = raw_input('day')
    con = mdb.connect('localhost', 'reader', '', 'UCSD')
    results = getLHSchedule(q, h, d, con)
    for res in results:
         print res[0] + " " + res[1] + "  " + res[2] 
