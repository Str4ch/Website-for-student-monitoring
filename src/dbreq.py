import jaydebeapi
import time
from src import generate_charts

path_to_h2_jar = open("src/path_to_h2_jar_file").read()
url: str = open("src/url_file").read()

first_chart_data = open("site/static/data_for_first_chart").read()
second_chart_data = open("site/static/data_for_second_chart").read()

page1_req1 = open("src/sql_scripts/p1r1").read()

page1_req2 = open("src/sql_scripts/p1r2").read()

page2_req1 = open("src/sql_scripts/p2r1").read()

page2_req2 = open("src/sql_scripts/p2r2").read()

page3_req = open("src/sql_scripts/p3").read()

page4_req = open("src/sql_scripts/p4").read()

def parse_data_for_charts(data):
    labels_data = []
    values_data = []
    for i in range(len(data)):
        labels_data.append(f"{data[i][0]} - {data[i][1]} {data[i][2]}")
        values_data.append(data[i][3])
    return  values_data, labels_data


def rewrite_in_file_format(data):
    ret_str = ""
    for i in data:
        for k in i:
            ret_str += str(k) +" "
        ret_str +="\n"
    return ret_str

def connect(db_user: str, db_password: str) -> jaydebeapi.Connection:
    conn = jaydebeapi.connect("org.h2.Driver", url, [db_user, db_password], path_to_h2_jar)
    return conn

def first_page(curs):
    curs.execute(page1_req1)
    data: list[tuple] = curs.fetchall()

    curs.execute(page1_req2)
    data2 = curs.fetchall()
    return data, data2

def second_page(curs, args):
    curs.execute(page2_req1.format(course=args[0], year=args[1], period=args[2]))
    data: list[tuple] = curs.fetchall()

    curs.execute(page2_req2.format(course=args[0], year=args[1], period=args[2]))
    data2: list[tuple] = curs.fetchall()

    return data, data2

def third_page(curs, args):
    curs.execute(page3_req.format(email = args[0]))
    data: list[tuple] = curs.fetchall()
    return data

def fourth_page(curs, args):
    curs.execute(page4_req.format(course=args[0], year=args[1], period=args[2]))
    data: list[tuple] = curs.fetchall()
    return data

def execute_req_for_pages(db_user, db_password, page_num: int, *args):
    connection = connect(db_user, db_password)
    curs = connection.cursor()

    #TODO: upgrade python to use switch case

    if page_num == 1:
        first_chart_data = open("site/static/data_for_first_chart", 'r')
        second_chart_data = open("site/static/data_for_second_chart", 'r')

        data = first_page(curs)
        data_formed_1 = rewrite_in_file_format(data[0])
        data_formed_2 = rewrite_in_file_format(data[1])
        flag = False

        if data_formed_1 != first_chart_data.read():
            first_chart_data = open("site/static/data_for_first_chart", 'w')
            first_chart_data.write(data_formed_1)

            students, labels = parse_data_for_charts(data[0])
            generate_charts.generate_first_chart(students, labels)

            flag = True


        if data_formed_2 != second_chart_data.read():
            second_chart_data = open("site/static/data_for_second_chart", 'w')
            second_chart_data.write(data_formed_2)

            percents, courses = parse_data_for_charts(data[1])
            generate_charts.generate_second_chart(percents, courses)

            flag = True

        if flag:
            t = time.localtime()
            current_time = time.strftime("%m/%d/%Y, %H:%M:%S", t)
            time_f = open("site/static/last_time_generated", "w")
            time_f.write(current_time)
            time_f.close()
        timet = open("site/static/last_time_generated").read()
        data = list(data)
        data.append(timet)
        data = tuple(data)
    elif page_num == 2:
        data = second_page(curs, args)
    elif page_num == 3:
        data = third_page(curs, args)
    elif page_num == 4:
        data = fourth_page(curs, args)
    curs.close()
    connection.close()
    return data
