from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

def generate_pdf(dataframe, filename="sales_report.pdf"):

    pdf = SimpleDocTemplate(filename)

    data = [list(dataframe.columns)]

    for row in dataframe.values.tolist():
        data.append(row)

    table = Table(data)

    style = TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.darkblue),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 1, colors.black),
        ("BACKGROUND", (0,1), (-1,-1), colors.beige),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0,0), (-1,0), 10),
    ])

    table.setStyle(style)

    pdf.build([table])

    return filename