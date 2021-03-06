import mysql.connector as Sql
import datetime
import enum


class DBType(enum.Enum):
    ALL = 1
    DAILY = 2

# this is not safe
# TODO: read credentials from a file (possibly encrypted)

db = Sql.connect(host="localhost",
                 user="db-user",
                 passwd='1yJwn7AOISKDfMEi',
                 db="grand_wave_db")


def pull_entire_db():

    # this will get slow af
    # TODO (in 2020): pull only last x entries

    print("Begin pulling database...")

    # sql mumbo jumbo (get me that data)

    cur = db.cursor()

    query = "SELECT * FROM GRAND_WAVE_ALLDATA"

    cur.execute(query)

    data = cur.fetchall()

    print("Database pulling finished.")

    return data


def pull_last_n_entries(n):

    db.connect()
    cur = db.cursor()
    query = "SELECT * FROM GRAND_WAVE_ALLDATA ORDER BY I DESC LIMIT 1"
    cur.execute(query)
    data = cur.fetchall()
    id = data[0][0]
    n = id - n
    query = "SELECT * FROM GRAND_WAVE_ALLDATA WHERE I > %s"
    args = n
    cur.execute(query, [args])
    data = cur.fetchall()
    db.close()
    return data


def pull_daily_db():

    # only gets midnight values (for per day graph)

    print("Begin pulling database...")

    # Hulk, query my database. (but only midnight data)

    cur = db.cursor()

    query = "SELECT * FROM GRAND_WAVE_ALLDATA WHERE cast(datev as time)=%s"

    args = datetime.time(0, 0, 0)

    cur.execute(query, [args])

    data = cur.fetchall()

    print("Database pulling finished.")

    return data


def insert_into_db(datev, amt):

    print("Begin database insertion...")

    # Hulk here is pulling us existing data to be compared

    cur = db.cursor()

    query = "SELECT * FROM GRAND_WAVE_ALLDATA WHERE datev = %s"

    args = datev

    cur.execute(query, [args])

    data = cur.fetchall()

    # this here analyzes existing data
    # fun fact: this will be very rarely used (in an event where there are two or more messages sent in one second)
    # it will only use the biggest amount.

    if str(data) != "[]":

        # mostly debug console prints, very useful.

        print("Data already present.")
        print("Old data: ", data[0][0], " : ", data[0][1])
        print("New data: ", datev, " : ", amt)

        # what to do if we do have two messages with the same time

        if data[0][1] <= amt:
            print("New amount is bigger. Replacing...")

            # Hulk's sql. (for replacing same second messages)

            query = "UPDATE GRAND_WAVE_ALLDATA SET amt = %s WHERE datev = %s"
            args = (amt, datev)

            cur.execute(query, args)
            db.commit()

            print("Data replaced successfully.")

        else:
            print("New amount is same or lower. Doing nothing...")

            # technically it is not possible for an amount to be lower, but hey, what do i know? (error validation?)

    else:

        # this will be used 99.99% of the time, when we get a new data, that we do not yet have
        # TODO: Should this call a graph streaming function straight away?

        print("Data not present yet.")
        print("New data: ", datev, " : ", amt)

        # HULK, SQL!

        query = "INSERT INTO GRAND_WAVE_ALLDATA (datev, amt) VALUES (%s, %s)"
        args = (datev, amt)

        cur.execute(query, args)
        db.commit()

        print("New data inserted.")




