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
db_path = os.path.join("instance", "CBMR_Weather.db") #Local
#db_path = "/home/CBMRPatrolApp/database/CBMR_Weather.db" #pythonAnywhere
connection = sqlite3.connect(db_path, check_same_thread=False)
cursor = connection.cursor()

pdf_date = ''

styles = getSampleStyleSheet()

def create_header():
    img = Image('./static/CB_Logo.jpg', width=100, height=50) #local
    #img = Image('/home/CBMRPatrolApp/cbmr_weather_patrol_app/CBMR_Weather/static/CB_Logo.jpg', width=100, height=50)  # pythonAnywhere
    data = [[img, 'CBSP Evening Report', '']]
    t = Table(data)
    t.setStyle(TableStyle([('TEXTCOLOR', (0, 0), (2, -1), colors.black),
                           ('FONTSIZE', (0, 0), (2, -1), 20),
                           ('SPAN', (1, 0), (2, 0)),

                           ('ALIGN', (0, 0), (2, 0), 'CENTER'),
                           ('VALIGN', (0, 0), (2, 0), 'MIDDLE')]))
    return t

def create_basic_info(date_input, forecaster_input):

    datetime = date_input.split('T')
    date_components = datetime[0].split('-')
    time_components = datetime[1]
    date = 'Date: ' + date_components[1] + '/' + date_components[2] + '/' + date_components[0]
    forecaster = 'Forecaster: ' + forecaster_input
    hour = int(time_components.split(':')[0])
    min = time_components.split(':')[1]
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
#
def create_basic_stats(basic_stats_input):

    hs = 'HS: ' + basic_stats_input[0]
    hn24 = 'HN24: ' + basic_stats_input[1]
    ytd_snow = 'YTD Snow: ' + basic_stats_input[2]
    uphill_access = 'Uphill Access: ' + basic_stats_input[3]
    data = [[hs, hn24, ytd_snow, uphill_access]]

    t = Table(data, colWidths=[126, 126, 126, 206], spaceAfter=10)

    t.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('GRID', (0, 0), (-1, -1), 1.5, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
    ]))

    return t


def create_discuss_box(heading, summary):
    sum_paragraph = Paragraph(summary, styles['Normal'])
    data = [[heading],
             [sum_paragraph]]

    t = Table(data, colWidths=[584 for x in range(1)], spaceAfter=10)
    t.setStyle(TableStyle([('TEXTCOLOR', (0, 0), (1, -1), colors.black),
                           ('GRID', (0, 0), (0, 1), 1.5, colors.black),

                           ('ALIGN', (0, 0), (0, 0), 'CENTER'),
                           ('VALIGN', (0, 0), (0, 0), 'MIDDLE')]))
    return t


def make_file_name(date_input):

    datetime = date_input.split('T')
    date_components = datetime[0].split('-')
    filename = date_components[1] + '_' + date_components[2] + '_' + date_components[0]

    #split_date = str_date.split("-")
    #filename = "_".join(split_date)
    return filename


def generate_pdf_pm(date, forecaster, basic_stats_input, weather_fx_input, tonight_input, tomorrow_input, tomorrow_night_input, mitigation_input):

    global pdf_date
    pdf_date = date

    filename_date = make_file_name(date)
    pdf_file_name = 'CBMR_PM_' + filename_date + '.pdf'
    filepath = '/home/CBMRPatrolApp/past_pdfs'
    # added to ensure directory exists
    os.makedirs(filepath, exist_ok=True)
    doc = SimpleDocTemplate(filepath + pdf_file_name,
                            pagesize=letter,
                            rightMargin=72,
                            leftMargin=72,
                            topMargin=18,
                            bottomMargin=18)

    elements = []

    header = create_header()
    basic_info = create_basic_info(date, forecaster)
    basic_stats = create_basic_stats(basic_stats_input)
    weather_fx = create_discuss_box('Weather Forecast', weather_fx_input)
    tonight = create_discuss_box('Tonight', tonight_input)
    tomorrow = create_discuss_box('Tomorrow', tomorrow_input)
    tomorrow_night = create_discuss_box('Tomorrow Morning', tomorrow_night_input)
    mitigation = create_discuss_box('Mitigation Plan', mitigation_input)


    elements.append(header)
    elements.append(basic_info)
    elements.append(basic_stats)
    elements.append(weather_fx)
    elements.append(tonight)
    elements.append(tomorrow)
    elements.append(tomorrow_night)
    elements.append(mitigation)

    doc.build(elements)

    return pdf_file_name


def main():
    generate_pdf_pm('2025-03-14', '', ['', '', '', ''], '', '', '', '', '')
    connection.close()


if __name__ == '__main__':
    main()