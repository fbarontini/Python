# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 22:46:45 2020

@author: fbarontini

Funcao de conexao com a Amazon AWS. Aqui eu crio uma classe
de conexao com o serviço Textract para rodar o OCR nas
imagens que o usuario subir. As imagens podem ser convertidas
em 2 modelos, sendo um arquivo PNG ou JPG em base64 ou
uma imagem direto do bucket da aws (S3).

Documentacao Textract:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html

"""
import boto3 as aws # biblioteca da AWS

PATH_TO_IMG_FILE = 'img_01.png' 


# Crio a visualizacao da imagem em base64
# necessário para enviar à API da AWS-OCR
with open(PATH_TO_IMG_FILE, 'rb') as file:
    image = bytearray(file.read())


# Crio o objeto "ocerizador" textract
# Estou usando a config do awscli,
# por isso não necessita dos dados de login
textract = aws.client('textract')
 
"""
Funçoes dentro do aws.client.textract:
    
    analyze_document()
    can_paginate()
    detect_document_text()
    generate_presigned_url()
    get_paginator()
    get_waiter()
    
    # Funcoes assincronas
    start_document_analysis()
    get_document_analysis()
    start_document_text_detection()
    get_document_text_detection()
"""

# rodo o serviço de detecção de texto da imagem.
ocr = textract.detect_document_text(Document = {'Bytes': image})

"""
linhas = []
if ocr:
    for item in ocr['Blocks']:
        if item['BlockType'] == 'LINE':
            linhas.append( item["Text"])
            
"""