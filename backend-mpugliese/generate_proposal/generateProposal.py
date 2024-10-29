import io
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from PIL import Image

def ajustar_proporcao_imagem(caminho_imagem, altura_desejada):
    try:
        with Image.open(caminho_imagem) as img:
            width, height = img.size
            proporcao = altura_desejada / height
            largura_ajustada = width * proporcao
            return largura_ajustada, altura_desejada
    except:
        print(f"Erro ao abrir a imagem: {caminho_imagem}. Usando tamanhos padrões.")
        return 120, 100 

def gerar_orcamento(numero_proposta, cliente, pessoa_recebe, email_recebe, telefone_recebe, obra, objeto_obra, itens, prazo, condicoes_pagamento, responsabilidades_contratada, responsabilidades_contratante):
    # Criar um buffer de memória para o PDF
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Encontre o caminho absoluto da pasta de fontes
    font_path = "./arq/fonts/Montserrat"

    if not os.path.exists(font_path):
        raise FileNotFoundError(f"A pasta de fontes não foi encontrada: {font_path}")

    # Registre as fontes Montserrat
    pdfmetrics.registerFont(TTFont('Montserrat', os.path.join(font_path, 'Montserrat-Regular.ttf')))
    pdfmetrics.registerFont(TTFont('Montserrat-Bold', os.path.join(font_path, 'Montserrat-Bold.ttf')))

    c.setFont("Montserrat", 12)

    margem_superior = height - 50
    y_position = margem_superior

    logo_path = "./arq/images/logo.jpg"  
    altura_desejada = 40  

    logo_width, logo_height = ajustar_proporcao_imagem(logo_path, altura_desejada)
    logo_x_position = (width - logo_width) / 2  

    try:
        c.drawImage(logo_path, logo_x_position, y_position - logo_height, width=logo_width, height=logo_height)
    except:
        print(f"Logo não encontrado no caminho: {logo_path}. Continuando sem o logo.")

    y_position -= (logo_height + 20)

    c.setFont("Montserrat-Bold", 12)
    c.drawString(40, y_position, f"PRP N° {numero_proposta}")

    y_position -= 30

    c.setFont("Montserrat", 12)
    c.drawString(40, y_position, f"À {cliente}.")
    c.drawString(300, y_position, f"E-mail: {email_recebe}")
    y_position -= 20
    c.drawString(40, y_position, f"Pessoa Responsável: {pessoa_recebe}")
    c.drawString(300, y_position, f"Telefone: {telefone_recebe}")

    y_position -= 20
    c.drawString(40, y_position, f"Obra: {obra}")
    
    y_position -= 20
    c.drawString(40, y_position, f"Objeto: {objeto_obra}")

    y_position -= 40

    data = [["ITEM", "DESCRIÇÃO", "QTD.", "UNID.", "UNIT.", "TOTAL"]]

    valor_total_orcamento = 0 

    for item in itens:
        valor_total_item = int(item["qtd"]) * float(item["unitario"])  
        valor_total_orcamento += valor_total_item  
        data.append([item["item"], item["descricao"], item["qtd"], item["unidade"], f"R$ {item['unitario']}", f"R$ {valor_total_item:.2f}"])

    col_widths = [50, 250, 60, 50, 70, 80]
    table = Table(data, colWidths=col_widths)

    total_table_width = sum(col_widths)
    page_width, _ = A4

    x_position = (page_width - total_table_width) / 2

    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),  
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white), 
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Montserrat-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),  
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    table.setStyle(style)
    
    table_width, table_height = table.wrap(0, 0)
    table.drawOn(c, x_position, y_position - table_height)
    
    y_position -= (table_height + 40)

    c.setFont("Montserrat-Bold", 12)
    c.drawRightString(width - 40, y_position, f"Valor Total do Orçamento: R$ {valor_total_orcamento:.2f}")
    
    y_position -= 20
    c.setFont("Montserrat", 12)
    c.drawString(40, y_position, f"Prazo estimado: {prazo}")

    y_position -= 30
    c.setFont("Montserrat-Bold", 12)
    c.drawString(40, y_position, "Condições de Pagamento:")

    y_position -= 20
    c.setFont("Montserrat", 12)
    for condicao in condicoes_pagamento:
        c.drawString(60, y_position, f"- {condicao}")
        y_position -= 20

    y_position -= 10
    c.setFont("Montserrat-Bold", 12)
    c.drawString(40, y_position, "Responsabilidades da Contratada:")
    y_position -= 20
    c.setFont("Montserrat", 12)
    for responsa in responsabilidades_contratada:
        c.drawString(60, y_position, f"- {responsa}")
        y_position -= 20

    y_position -= 10
    c.setFont("Montserrat-Bold", 12)
    c.drawString(40, y_position, "Responsabilidades da Contratante:")
    y_position -= 20
    c.setFont("Montserrat", 12)
    for responsa in responsabilidades_contratante:
        c.drawString(60, y_position, f"- {responsa}")
        y_position -= 20

    c.showPage()
    c.save()

    # Mover o ponteiro de leitura para o início do buffer
    buffer.seek(0)

    return buffer
