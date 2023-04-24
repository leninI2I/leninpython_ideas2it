import numpy as np
import pandas as pd
import itertools
from statistics import mean
from random import randint
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table


try:

    # Open a CSV File using pandas
    openFile = pd.read_csv("PropertyUseCaseCSV.csv", index_col=0)
    # Changing the index[0] to proper align
    openFile = openFile.reset_index()

    """Group by"""

    print('AVG price of properties in each location')
    # AVG price of properties in each location
    openFile['newgdval'] = openFile['price'] * openFile['sqfootage']
    # print(openFile['newgdval'])

    avgprice = openFile.groupby((['location', 'propertyType'])).agg(
        AveragePrice=('price', 'mean'),
    ).reset_index()
    print(avgprice)
    # newfiles = np.array(avgprice)
    # #print(newfiles)

    print('AVGB&B for each property')
    # AVGB&B for each property
    avgbb = openFile.groupby(['propertyType']).agg(
        AverageBedroom=('bedrooms', 'mean'),
        AverageBathroom=('bathrooms', 'mean')

    ).reset_index()
    print(avgbb)

    # Total Average
    totavg = openFile.groupby(['propertyType', 'location']).agg(
        AveragePrice=('price', 'mean'),
        AverageBedroom=('bedrooms', 'mean'),
        AverageBathroom=('bathrooms', 'mean'),
        Avgsf=('sqfootage', 'mean')
    ).reset_index()

    # numpy
    FinResult = np.array(totavg)


    # reportlab
    w, h = A4
    def grouper(iterable, n):
        args = [iter(iterable)] * n
        return itertools.zip_longest(*args)

    c = canvas.Canvas("PropertyData.pdf", pagesize=letter)
    c.drawString(50,50,'PROPERTY DATA')
    c.setFillColor(aColor='red')
    max_rows_per_page = 45
    # Margin.
    x_offset = 50
    y_offset = 100
    # Space between rows.
    padding = 15

    #Setting Off-set
    xlist = [x + x_offset for x in [0, 120, 200, 260, 360, 450, 500]]
    ylist = [h - y_offset - i * padding for i in range(max_rows_per_page + 1)]

    #Heading
    Reportdata = [("PROPERTY TYPE", "LOCATION", "PRICE", "BEDROOMS", "BATHROOMS", "SQFT")]

    #Looping and saving data into table
    for i in FinResult:

        proptype, locat, price, bath, bed, sqft = i[0], i[1], int(i[2]), round(i[3]), round(i[4]), round(i[5])
        Reportdata.append((proptype, locat, price, bath, bed, sqft))

    for xyz in grouper(Reportdata, max_rows_per_page):
        xyz = tuple(filter(bool, xyz))
        c.grid(xlist, ylist[:len(xyz) + 1])
        for y, row in zip(ylist[:-1], xyz):
            for x, cell in zip(xlist, row):
                c.drawString(x + 2, y - padding + 3, str(cell))

    #Finally saving the data in pdf
    c.save()
except Exception as ex:
    print(ex)
    