from src import TextExtract
import re
import os

def invoice_number_rename(PATH):
	'''renames the pdf files in the provided path with invoice numbers
	extracted from the document. If the invoice number cannot be extracted,
	the filename is left unchanged.'''

	pdfs = os.listdir(PATH)

	for i in pdfs:
		if '.pdf' in i:
			#extract text from pdf
			text = TextExtract.pdf_text_extract('%s%s' % (PATH, i))

			for j in text:
				# search for invoice number in extracted text
				inv_num = re.search('E-\d{4,5}', j)

			if inv_num == None:
				print "no invoice number found in file %s" % i
			else:
				print 'invoice number found in %s' % i
				inv_num = inv_num.group(0)
				# print inv_num				
				pdf_name = '%s.pdf' % inv_num
				# print pdf_name

				# rename file with invoice number
				os.rename('%s%s' % (PATH, i), '%s%s' % (PATH, pdf_name))
				print 'file %s renamed' % i

	return
