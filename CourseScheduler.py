import MySQLdb as mdb
import time

def getLHSchedule(quarter, hall, day, con):
    cur = con.cursor()
    cur.execute("SELECT * FROM " + quarter + " WHERE building=\'" + hall + "\' and days REGEXP \'.*" + day + ".*\'")
    return cur.fetchall()

def toTimes(tString):
    tStrings = tString.split('-')
    fString = '%I:%M%p'
    return (time.strptime(tStrings[0] + "m", fString), time.strptime(tStrings[1] + "m", fString)), 

if __name__ == '__main__':
    q = 'WI14'
    h = raw_input('hall')
    d = raw_input('day')
    con = mdb.connect('localhost', 'reader', '', 'UCSD')
    results = getLHSchedule(q, h, d, con)
    fResults = [(n, r, toTimes(t)) for (n, d, t, b, r) in results]
    fResults.sort(key=lambda tup: tup[2][0])
    for res in fResults:
         print res[0] + " " + res[1] + "  " + time.strftime("%H:%M" ,res[2][0][0]) + "-" + time.strftime("%H:%M" ,res[2][0][1])
