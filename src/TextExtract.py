#!/usr/bin/env python3
from wand.image import Image
from PIL import Image as PI
import pyocr
import pyocr.builders
import io
from PyPDF2 import PdfFileWriter, PdfFileReader

'''Depends on installation of Tesseract-OCR, ImageMagick, and Ghostwriter.
All are available for installation on Homebrew (Mac) or apt (Linux)
Unsure about Windows installation; Google is your friend'''


def pdf_text_extract(file, resolution=300, tool=0, lang=0):
	'''uses wand.image to convert provided pdf file to jpeg,
	then extract text from jpeg files. Returns list of extracted
	text'''
	engine = pyocr.get_available_tools()[tool] #tesseract engine
	lang = engine.get_available_languages()[lang] #first language is eng for tesseract. May be different for different engine

	#create lists to capture images and text from pdfs
	req_image = []
	final_text = []

	#open pdf
	image_pdf = Image(filename=file, resolution=resolution)
	#convert pdf to jpegs
	image_jpeg = image_pdf.convert('jpeg')

	#convert each page in pdf file to individual jpeg
	for img in image_jpeg.sequence:
		img_page = Image(image=img)
		req_image.append(img_page.make_blob('jpeg'))

	for img in req_image:
		txt = engine.image_to_string(PI.open(io.BytesIO(img)),
			lang=lang,
			builder=pyocr.builders.TextBuilder()
			)
		final_text.append(txt)

	return final_text


def pdf_split(file, output_path='.'):
	'''Splits given pdf file into individual pdf files named for page
	numbers. Writes new pdfs into current directory'''
	
	# Open pdf
	inputpdf = PdfFileReader(open(file, 'rb'))

	# Cycle through pages in pdf file
	for i in range(inputpdf.numPages):
		output = PdfFileWriter()
		output.addPage(inputpdf.getPage(i))
		with open('{}/{}.pdf'.format(output_path, i), 'wb') as outputStream:
			output.write(outputStream)

	return

if __name__ == '__main__':
	print('Success!')

