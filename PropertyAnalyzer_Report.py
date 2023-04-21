import pandas as pd
import numpy as np
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle

# Read the property data from a CSV file
data = pd.DataFrame(pd.read_csv(
    'C:\\Users\\rsang\\OneDrive\\Desktop\\Python DJango Upskilling\\Task\\samplecsvformat.csv'))

# Calculate the average price and square footage of properties in each location
avg_price_sqft = data.groupby(['location'])[['price', 'square_footage']].mean(
).apply(lambda x: np.round(x, 2)).reset_index()

# Calculate the average number of bedrooms and bathrooms for each property type.
avg_bed_bath = data.groupby(['property_type'])[
    ['num_bedrooms', 'num_bathrooms']].mean().round(2).reset_index()

# Calculate the average price , square footage ,  num_bedrooms , num_bathrooms of properties in each location
loc_property_summary = data.groupby(['location', 'property_type'])[
    ['price', 'square_footage', 'num_bedrooms', 'num_bathrooms']].mean()

# Generate a report that summarizes the data for each location and property type
filename = 'property_report.pdf'
report = canvas.Canvas(filename, pagesize=letter)
# Define the report style
report.setTitle('Property Summary')
report.setFont('Helvetica-Bold', 12)
heading_text = "Property Detail Summary Report"
report.drawString(200, 750, heading_text)

plot_y_coordinates = 720
iterator = 25
report.drawString(100, plot_y_coordinates,
                  'Calculation of the average price and square footage of properties in each location')
# Define a style for the table
style = TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 14),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
    ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 1), (-1, -1), 12),
    ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
])
# Create the table object and add style
table = Table([list(avg_price_sqft)] + avg_price_sqft.values.tolist())
table.setStyle(style)

# Draw the table on the canvas
table.wrapOn(report, 0, 0)
table.drawOn(report, 150, 570)

plot_y_coordinates = 750
report.drawString(
    100, 530, 'Calculation of the average number of bedrooms and bathrooms for each property type')

# Create the table object and add style
# print([list(avg_bed_bath)] + avg_bed_bath.values.tolist())
table = Table([list(avg_bed_bath)] + avg_bed_bath.values.tolist())
table.setStyle(style)

# Draw the table on the canvas
table.wrapOn(report, 0, 0)
table.drawOn(report, 150, 400)

report.drawString(
    100, 350, 'Report that summarizes the data for each location and property type')
report.setFont('Helvetica', 12)
plot_y_coordinates = 320
for index, row in loc_property_summary.iterrows():
    data_dict = {
        "location": index[0],  # type: ignore
        "property_type": index[1],  # type: ignore
        "price": row["price"],
        "square_footage": row["square_footage"],
        "num_bedrooms": row["num_bedrooms"],
        "num_bathrooms": row["num_bathrooms"]
    }

    summary_row = "Location: {}".format(data_dict['location']) + ' having ' + "Property Type: {}".format(
        data_dict['property_type'] + ' holds below average data: ')

    report.drawString(100, plot_y_coordinates, summary_row)
    plot_y_coordinates = plot_y_coordinates - iterator
    report.drawString(100, plot_y_coordinates,
                      "Average Price: ${:,.2f}".format(data_dict['price']))
    plot_y_coordinates = plot_y_coordinates - iterator
    report.drawString(100, plot_y_coordinates, "Average Square Footage: {:.2f} sq.ft.".format(
        data_dict['square_footage']))
    plot_y_coordinates = plot_y_coordinates - iterator
    report.drawString(100, plot_y_coordinates, "Average Number of Bedrooms: {}".format(
        data_dict['num_bedrooms']))
    plot_y_coordinates = plot_y_coordinates - iterator
    report.drawString(100, plot_y_coordinates, "Average Number of Bathrooms: {}".format(
        data_dict['num_bathrooms']))
    plot_y_coordinates = plot_y_coordinates - iterator

    # Save the page with the current location and property type information
    if plot_y_coordinates <= 100:
        report.showPage()
        plot_y_coordinates = 700

# Save the PDF file
report.save()
