import psycopg2
conn = psycopg2.connect(database="raspisanie_db", user="postgres", password="2004", host="localhost", port="5432")
cursor = conn.cursor()

def getResponseDay(day, status):
    cursor.execute(
        "SELECT timetable.start_time, timetable.subject_name, teacher.full_name, timetable.room_numb FROM timetable, 
        teacher WHERE timetable.status = %s AND timetable.day_name = %s AND timetable.subject_name = teacher.subject_name ORDER BY timetable.start_time", (status, day))
    records = list(cursor.fetchall())
    response = day + "\n—————————\n"
    for elem in records:
        if elem[1] == "Занятий нет":
            response += elem[1]
        else:
            response += "\n".join(elem) + "\n—————————\n"
    return response

def getResponseWeek(status):
    cursor.execute(
        "SELECT timetable.day_name, timetable.start_time, timetable.subject_name, teacher.full_name, timetable.room_numb FROM timetable,
        teacher WHERE (timetable.status = %s AND timetable.subject_name = teacher.subject_name) ORDER BY timetable.orders, timetable.start_time", (status))
    records = list(cursor.fetchall())
    day = records[0][0]
    response = ""
    k = 0
    for elem in records:
        if elem[2] == "Занятий нет":
            response += "\n" + elem[0] + "\n—————————\n" + elem[2] + "\n————————\n"
        else:
            if elem[0] == day:
                if k == 0:
                    response += day + "\n—————————\n"
                    k = 1
                response += "\n".join(elem[1:]) + "\n—————————\n"
            elif elem[0] != day:
                day = elem[0]
                k = 0
                if k == 0:
                    response += "\n" + day + "\n—————————\n"
                    k = 1
                response += "\n".join(elem[1:]) + "\n—————————\n"
    return response
