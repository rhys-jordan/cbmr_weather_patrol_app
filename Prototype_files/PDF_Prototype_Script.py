from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table


#Possible send data table rather then hardcode
def create_weather_observation_table():
    data = [['Pertinent Weather Observations Past and Future', '', '', '', '', ''],
            ['Current', '', 'PAST 24 hour', '', 'Future 24 hours', ''],
            ['Sky', '01', 'HN24/ HST data clr', '03', 'Precip/Rate', ''],
            ['Precip/Rate', '11', 'HN24 SWE', '13', 'Temp HIGH', ''],
            ['Temp', '21', 'Wind mph/direction', '23', 'Temp LOW', ''],
            ['Wind mph', '31', 'Temp HIGH', '33', 'Wind mph', ''],
            ['Wind Direction', '31', 'Temp LOW', '33', 'Wind Direction', '']]

    t = Table(data, colWidths=[95 for x in range(6)],
              rowHeights=[45 for x in range(len(data))], spaceAfter= 20)
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
    data2 = [['Weather Forecast'],
            ['Blah blah blah blah blah']]

    t = Table(data2, colWidths=[570 for x in range(1)],
              rowHeights=[45 for x in range(len(data2))])
    t.setStyle(TableStyle([('TEXTCOLOR', (0, 0), (1, -1), colors.black),
                           ('GRID', (0, 0), (0, 1), 1, colors.black),

                           ('ALIGN', (0, 0), (0, 0), 'CENTER'),
                           ('VALIGN', (0, 0), (0, 0), 'MIDDLE')]))
    return t



def main():
    doc = SimpleDocTemplate("prototype_pdf_AM_report.pdf", pagesize=letter)

    # container for the 'Flowable' objects
    elements = []


    weather_obser = create_weather_observation_table()
    elements.append(weather_obser)
    weather_forecast = create_weather_forcast_table()

    elements.append(weather_forecast)

    # write the document to disk
    doc.build(elements)


if __name__ == '__main__':
    main()