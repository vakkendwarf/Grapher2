import Graph as Mg
import Sql as SqlI
import sys
import datetime

#if sys.argv[1] and sys.argv[2] is not None:
#    SqlI.insert_into_db(sys.argv[1], sys.argv[2])
Mg.streamit(datetime.date(2018, 9, 27), 300000, "total")

daydb = SqlI.pull_daily_db()
alldb = SqlI.pull_entire_db()

Mg.plotarray(alldb)
Mg.plotdailyarr(daydb)
