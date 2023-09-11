from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import *
from reportlab.lib.styles import *
import numpy
import json
from reportlab.lib import colors


def get_values(data):
    etapas = []
    rangos = []
    fs = []
    ds = []
    opt = []
    sol = []
    dest = []

    for i in data.get_etapas():
        etapas.append(i)
    for i in data.get_rangos():
        rangos.append(i)
    for i in data.get_fs():
        fs.append(i)
    for i in data.get_formated_ds():
        ds.append(i)
    for i in data.get_opciones():
        opt.append(i)
    for i in data.get_solution():
        sol.append(i)
    for i in data.get_destinos():
        dest.append(i)

    return (etapas, rangos, fs, ds, opt, sol, dest)


def create_pdf(name, data):
    etapas, rangos, fs, ds, opts, sols, dests = get_values(data)

    combined_lists = zip(etapas, rangos, fs)
    elements = []
    etapaJunta = createIterations(combined_lists)
    # print(etapaJunta)
    doc = SimpleDocTemplate(name, pagesize=A4)
    styles = getSampleStyleSheet()

    custom_style = ParagraphStyle(
        name='CustomStyle',
        fontSize=14,
        leading=14,  # Espaciado entre líneas
        textColor=colors.black,  # Color del texto
        alignment=0,  # Alineación (0=izquierda, 1=centro, 2=derecha)
        leftIndent=20,  # Sangría izquierda
        rightIndent=20,  # Sangría derecha
        spaceAfter=10  # Espaciado después del párrafo
    )

    style = ParagraphStyle(
        name="Custom2",
        fontSize=10,
        leading=14,
        alignment=1,
        spaceAfter=10
    )

    texto = f"Funcion Objetivo:\n"

    paragraph = Paragraph(texto, custom_style)
    elements.append(paragraph)
    elements.append(Spacer(1, 20))

    texto = f"{data.get_funcion_objetivo()}"
    paragraph = Paragraph(texto, style)
    elements.append(paragraph)
    elements.append(Spacer(1, 20))

    texto = f"Restricciones: "
    paragraph = Paragraph(texto, custom_style)
    elements.append(paragraph)
    elements.append(Spacer(1, 20))

    r1 = f"{data.get_eficiencia()}"
    r2 = f"{data.get_transicion()}"
    paragraph1 = Paragraph(r1, style)
    paragraph2 = Paragraph(r2, style)
    elements.append(paragraph1)
    elements.append(Spacer(1, 20))
    elements.append(paragraph2)
    elements.append(Spacer(1, 20))

    texto = f"Iteraciones: "
    paragraph = Paragraph(texto, custom_style)
    elements.append(paragraph)
    elements.append(Spacer(1, 20))
    s = styles["BodyText"]
    s.wordWrap = 'CJK'
    i = 0
    for etapa, d in zip(etapaJunta, ds):
        nc = numpy.array(d, dtype=object)
        if i == len(etapaJunta) - 1:
            etp = etapa.tolist()
            # print(etp[0])
            etp[0].append(nc)

        else:
            etp = numpy.hstack((etapa, nc.reshape(-1, 1)))

        # print(etp)

        etapa_matrix_str = [[str(cell) for cell in row]
                            for row in etp]

        data2 = [[Paragraph(cell, s) for cell in row]
                 for row in etapa_matrix_str]
        t = Table(data2)
        t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.beige),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                               ('GRID', (0, 0), (-1, -1), 1, colors.black),
                               ('BACKGROUND', (-2, 0), (-2, -1), colors.green)]))

        texto = f"Iteracion: {i+1} "
        paragraph = Paragraph(texto, custom_style)
        elements.append(paragraph)
        elements.append(Spacer(1, 20))

        elements.append(t)
        elements.append(Spacer(1, 12))

        i += 1
    sols = create_sol(sols, dests)
    i = 0

    for sol in sols:
        t = Table(sol)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.beige),  # Fila de encabezado
            # Color del texto en la fila de encabezado
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            # Alinear todo el contenido al centro
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            # Fuente en la fila de encabezado
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            # Espaciado inferior en la fila de encabezado
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            # Color de fondo de las filas de datos
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (-2, 0), (-2, -1), colors.green)  # Líneas de cuadrícula
        ]))

        texto = f"Solucion: {i+1} "
        paragraph = Paragraph(texto, custom_style)
        elements.append(paragraph)
        elements.append(Spacer(1, 20))

        elements.append(t)
        elements.append(Spacer(1, 12))

    doc.build(elements)


def createIterations(combinedList):
    ret = []
    i = 0
    combinedList = list(combinedList)
    for etapa, rango, f in combinedList:
        rango = rango.reshape(-1, 1)
        f = f.reshape(-1, 1)
        # d = d.reshape(-1, 1)
        if i == len(combinedList) - 1:

            etapamat = numpy.concatenate(([rango[-1]], etapa.matrix), axis=1)
            etapamat = numpy.concatenate((etapamat, f), axis=1)
        else:

            # print(rango)
            etapamat = numpy.concatenate((rango, etapa.matrix), axis=1)
            etapamat = numpy.concatenate((etapamat, f), axis=1)
        # print(etapamat)
        ret.append(etapamat)
        i += 1
    return ret


def create_sol(sols, dests):
    re = []
    for i in sols:
        a = []
        for j, d in enumerate(dests):
            i[j].insert(0, d.get_nombre())
            a.append(i[j])
        re.append(a)
    return re
