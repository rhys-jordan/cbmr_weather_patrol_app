from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, Image
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import StringIO
from flask import send_file

import sqlite3
import os

#idk about this false on threading, this may be dangerous and we could run into problems.
db_path = os.path.join("instance", "CBMR_Weather.db")
connection = sqlite3.connect(db_path, check_same_thread=False)
cursor = connection.cursor()

pdf_date =  ''

styles = getSampleStyleSheet()

def create_header():
    img = Image('./static/CB_Logo.jpg', width=100, height=50)
    data = [[img, 'CBSP Morning Weather and Avalanche Report', '']]
    t = Table(data)
    t.setStyle(TableStyle([('TEXTCOLOR', (0, 0), (2, -1), colors.black),
                           ('FONTSIZE', (0, 0), (2, -1), 20),
                           ('SPAN', (1, 0), (2, 0)),

                           ('ALIGN', (0, 0), (2, 0), 'CENTER'),
                           ('VALIGN', (0, 0), (2, 0), 'MIDDLE')]))
    return t

def create_basic_info():
    command = 'SELECT date, forecaster, time FROM snow WHERE date = "' + str(pdf_date) + '"'
    cursor.execute(command)
    results = cursor.fetchall()
    date_components = results[0][0].split('-')
    date = 'Date: ' + date_components[1] + '/' + date_components[2] + '/' + date_components[0]
    forecaster = 'Forecaster: ' + str(results[0][1])
    hour = int(results[0][2].split(':')[0])
    min = results[0][2].split(':')[1]
    if(hour > 12):
        hour = hour - 12
        time = 'Time: ' + str(hour) + ':' + min + " PM"
    else:
        time = 'Time: ' + str(hour) + ':' + min + " AM"

    data = [[date,time,forecaster]]
    t = Table(data, spaceAfter= 20)
    t.setStyle(TableStyle([('TEXTCOLOR', (0, 0), (2, -1), colors.black),
                           ('FONTSIZE', (0, 0), (2, -1), 13),

                           ('ALIGN', (0, 0), (2, 0), 'CENTER'),
                           ('VALIGN', (0, 0), (2, 0), 'MIDDLE')]))
    return t

def create_basic_stats():
    command = 'SELECT hs,hn24,hst,ytd, critical_info FROM snow WHERE date = "' + str(pdf_date) + '"'
    cursor.execute(command)
    results = cursor.fetchall()
    hs = 'HS: ' + str(results[0][0])
    hn24 = 'HN24: ' + str(results[0][1])
    hst = 'HST: ' + str(results[0][2])
    ytd = 'YTD: ' + str(results[0][3])
    if(results[0][4] != None):
        crit_info = Paragraph('Critical Info? ' +  results[0][4], styles['Normal'])
    else:
        crit_info = Paragraph('Critical Info? ', styles['Normal'])
    data = [[hs, hn24, hst, ytd, crit_info, '']]

    t = Table(data, colWidths=[95 for x in range(6)], spaceAfter=10 )
    t.setStyle(TableStyle([('TEXTCOLOR', (0, 0), (2, -1), colors.black),
                           ('GRID', (0, 0), (6, 0), 1, colors.black),

                           ('SPAN', (4, 0), (5, 0)),

                           ('ALIGN', (0, 0), (3, 0), 'LEFT'),
                           ('VALIGN', (0, 0), (2, 0), 'MIDDLE')]))

    return t


def get_weather_obser_data():
    command = ('SELECT sky, current_precip_rate, temperature, wind_mph, wind_direction '
               'FROM snow'
               ' WHERE date = "') + str(pdf_date) + '"'
    cursor.execute(command)
    results_current = cursor.fetchall()

    command = ('SELECT past_24_hn24_hst_date_cir, past_24_hn24_swe, past_24_wind_mph_direction, past_24_temp_high, past_24_temp_low'
               ' FROM snow '
               'WHERE date = "') + str(pdf_date) + '"'
    cursor.execute(command)
    results_past = cursor.fetchall()

    command = ('SELECT future_precip_rate, future_temp_high, future_temp_low, future_wind_mph, future_wind_direction'
                  ' FROM snow '
                  'WHERE date = "') + str(pdf_date) + '"'
    cursor.execute(command)
    results_future = cursor.fetchall()

    data = [['Pertinent Weather Observations Past and Future', '', '', '', '', ''],
            ['Current', '', 'PAST 24 hour', '', 'Future 24 hours', ''],
            ['Sky', results_current[0][0], 'HN24/ HST data clr', results_past[0][0], 'Precip/Rate', results_future[0][0]],
            ['Precip/Rate', str(results_current[0][1]), 'HN24 SWE',  str(results_past[0][1]), 'Temp HIGH', results_future[0][1]],
            ['Temp', str(results_current[0][2]), 'Wind mph/direction',  results_past[0][2], 'Temp LOW', results_future[0][2]],
            ['Wind mph', results_current[0][3], 'Temp HIGH',  str(results_past[0][3]), 'Wind mph', results_future[0][3]],
            ['Wind Direction', results_current[0][4], 'Temp LOW',  str(results_past[0][4]), 'Wind Direction', results_future[0][4]]]
    return data

#Possible send data table rather than hardcode
#Make things paragraphs
def create_weather_observation_table():
    data = get_weather_obser_data()

    t = Table(data, colWidths=[95 for x in range(6)],
              rowHeights=[20 for x in range(len(data))], spaceAfter= 20)
    t.setStyle(TableStyle([('TEXTCOLOR', (0, 0), (1, -1), colors.black),
                           ('GRID', (0, 0), (5, 6), 1, colors.black),

                           ('SPAN', (0, 0), (5, 0)),
                           ('ALIGN', (0, 0), (5, 0), 'CENTER'),
                           ('VALIGN', (0, 0), (5, 0), 'MIDDLE'),

                           ('SPAN', (0, 1), (1, 1)),
                           ('ALIGN', (0, 1), (1, 1), 'CENTER'),
                           ('VALIGN', (0, 1), (1, 1), 'MIDDLE'),

                           ('SPAN', (2, 1), (3, 1)),
                           ('ALIGN', (2, 1), (3, 1), 'CENTER'),
                           ('VALIGN', (2, 1), (3, 1), 'MIDDLE'),

                           ('SPAN', (4, 1), (5, 1)),
                           ('ALIGN', (4, 1), (5, 1), 'CENTER'),
                           ('VALIGN', (4, 1), (5, 1), 'MIDDLE')
                           ]))
    return t


def create_weather_forcast_table():
    #make paragraph with data to put into table
    data2 = [['Weather Forecast'],
            ['']]

    t = Table(data2, colWidths=[570 for x in range(1)],
              rowHeights=[20 for x in range(len(data2))], spaceAfter= 20)
    t.setStyle(TableStyle([('TEXTCOLOR', (0, 0), (1, -1), colors.black),
                           ('GRID', (0, 0), (0, 1), 1, colors.black),

                           ('ALIGN', (0, 0), (0, 0), 'CENTER'),
                           ('VALIGN', (0, 0), (0, 0), 'MIDDLE')]))
    return t


def get_avalanche_danger_data():
    command = ('SELECT problem, aspect_elevation, size_likelihood, trend FROM avalanche '
               'WHERE Snow_id in '
               '(SELECT snow.id '
               'FROM snow '
               'WHERE date = "'+ str(pdf_date) + '")')
    cursor.execute(command)
    results_ava= cursor.fetchall()
    return results_ava



def create_avalanche_danger_table(ava_results):
    data = [['Avalanche Danger in the BC/on the other side of the rope', '', '', '', '', '', '', '']]
    for i in range(len(ava_results)):
        ava_problem_name = 'Avalanche Problem ' + str(i + 1)
        ava_prob = Paragraph(ava_problem_name, styles['Normal'])
        aspect_elevation = Paragraph('Aspect/   Elevation', styles['Normal'])
        size_likelihood = Paragraph('Size/  Likelihood', styles['Normal'])
        trend = Paragraph('Trend', styles['Normal'])
        data.append([ava_prob, ava_results[i][0], aspect_elevation, ava_results[i][1],size_likelihood , ava_results[i][2], trend, ava_results[i][2]])


    #t = Table(data, colWidths=[71 for x in range(len(data[0]))],
              #rowHeights=[30 for x in range(len(data))], spaceAfter= 20)
    t = Table(data, colWidths=[65,110,65,65,65,65,65,65],
              rowHeights=[30 for x in range(len(data))], spaceAfter= 20)
    t.setStyle(TableStyle([('TEXTCOLOR', (0, 0), (2, -1), colors.black),
                           ('GRID', (0, 0), (8, len(ava_results)), 1, colors.black),
                           ('SPAN', (0, 0), (7, 0)),
                           ('ALIGN', (0, 0), (8, 0), 'CENTER'),
                           ('VALIGN', (0, 0), (8, 0), 'MIDDLE'),
                           ]))
    return t



def create_discuss_box(heading, summary):
    sum_paragraph = Paragraph(summary, styles['Normal'])
    data = [[heading],
             [sum_paragraph]]

    t = Table(data, colWidths=[570 for x in range(1)], spaceAfter=20)
    t.setStyle(TableStyle([('TEXTCOLOR', (0, 0), (1, -1), colors.black),
                           ('GRID', (0, 0), (0, 1), 1, colors.black),

                           ('ALIGN', (0, 0), (0, 0), 'CENTER'),
                           ('VALIGN', (0, 0), (0, 0), 'MIDDLE')]))
    return t




def get_information(category_name):
    command = 'SELECT ' + category_name + ' FROM snow WHERE date = "' + str(pdf_date) + '"'
    cursor.execute(command)
    results = cursor.fetchall()
    if(results[0][0] != None):
        return results[0][0]
    else:
        return ''


def make_file_name():
    str_date = str(pdf_date)

    date_components = str_date.split('-')
    filename = date_components[1] + '_' + date_components[2] + '_' + date_components[0]

    #split_date = str_date.split("-")
    #filename = "_".join(split_date)
    return filename


def generate_pdf(date):
    #connection = sqlite3.connect(".\\instance\\CBMR_Weather.db", check_same_thread=False)
    #cursor = connection.cursor()

    global pdf_date
    pdf_date = date
    print(pdf_date)

    cursor = connection.cursor()
    command = 'SELECT date FROM snow WHERE date = "' + str(pdf_date) + '"'
    cursor.execute(command)
    results = cursor.fetchall()
    if(len(results) == 0):
        print("No date")
        return -1

    filename_date = make_file_name()
    pdf_file_name = 'CBMR_' + filename_date + '.pdf'
    filepath = './past_pdfs/'
    #added to ensure directory exists
    os.makedirs(filepath, exist_ok=True)
    doc = SimpleDocTemplate(filepath+pdf_file_name,
                            pagesize=letter,
                            rightMargin=72,
                            leftMargin=72,
                            topMargin=18,
                            bottomMargin=18)

    elements = []

    header = create_header()
    basic_info = create_basic_info()
    basic_stats = create_basic_stats()

    weather_obser = create_weather_observation_table()

    weather_forecast = create_discuss_box('Weather Forecast', get_information('weather_forecast'))
    elements.append(header)
    elements.append(basic_info)
    elements.append(basic_stats)
    elements.append(weather_obser)
    elements.append(weather_forecast)
    ava_results = get_avalanche_danger_data()
    #for i in range(len(ava_results)):
    ava_danger = create_avalanche_danger_table(ava_results)
    elements.append(ava_danger)

    ava_forecast = create_discuss_box(
        'Avalanche Forecast and discussion, How it relates to our Mtn and Our Strategic Mindset',
        get_information('avalanche_forecast_discussion'))
    sum_prev_work = create_discuss_box('Summary of Previous Day(s) Work', get_information('summary_previous_day'))
    mitigation_plan = create_discuss_box('Mitigation Plan', get_information('mitigation_plan'))
    terrain_opening = create_discuss_box('Pertinent Terrain Opening/Closing', get_information('pertinent_terrain_info'))


    elements.append(ava_forecast)
    elements.append(sum_prev_work)
    elements.append(mitigation_plan)
    elements.append(terrain_opening)

    doc.build(elements)
    #connection.close()

    return filepath+pdf_file_name


def main():
    generate_pdf('2025-03-04')
    #connection.close()


if __name__ == '__main__':
    main()