from src import TextExtract
import re
import os
import logging

# Path to directory containing invoice scans
PATH = '/PATH/to/files/'
# Destination of filed invoices
dest = '/PATH/to/files/'
# Destination for invoices that fail
prob = '/PATH/to/files/'

# Logging for module
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(message)s')

file_handler = logging.FileHandler('%sInvoice_EFile.log' % PATH)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

# Get list of all files in PATH
pdfs = os.listdir(PATH)

# Split PDF pages into seperate documents
for i in pdfs:
	if '.pdf' in i:
		try:
			TextExtract.pdf_split('%s%s'%(PATH,i), output_path=PATH)
			logger.info('Split pdf %s' % i)

			# Extract text from PDF pages
			text = TextExtract.pdf_text_extract('%s%s'%(PATH,i))
			logger.info('Text extracted from pdf %s' % i)

			# Extract inv #s and accounts - combine them into pdf_names
			# pdf_names = []
			for j in text:
				try:
					logger.debug('Renaming pdf %s page %d' % (i , text.index(j)))
					inv_num = re.search('E-\d{4,5}', j).group(0)
					# list of unique words in account name
					l = re.search('(Ship|Bill) To:\n+.*\n', j).group(0).split('\n')[-2].split()
					ulist = [] #list to collect unique values in acct
					for x in l: # cut out duplicated names
						if x not in ulist:
							ulist.append(x)
					acct = '_'.join(ulist)
					pdf_name = '%s.%s.pdf' % (acct, inv_num)

					# Create dir for acct if doesn't exist
					if os.path.isdir('%s%s'%(dest, acct)) == False:
						os.mkdir('%s%s'%(dest, acct))
						logger.info('Dir for %s does not exist. Created dir' % 
									acct)

					# Rename pdf with 
					os.rename('%s%s.pdf'%(PATH, str(text.index(j))), 
						      '%s%s/%s'%(dest, acct, pdf_name))
					logger.debug('Renaming pdf %s page %d as %s' % 
								(i, text.index(j), pdf_name))
				except AttributeError:
					logger.exception('Unable to find regex in pdf %s page %d. '
									 'Files moved to Problem_pdfs dir' % 
									 (i, text.index(j)))
					os.rename('%s%s.pdf'%(PATH, str(text.index(j))),
						      '%s%s_page%s.pdf'%(prob, i, str(text.index(j))))
				except OSError:
					logger.exception('Error moving pdf %s page %d '
						             'to acct dir. Files moved to '
						             'Problem_pdfs dir' % (i, text.index(j)))
					os.rename('%s%s.pdf'%(PATH, str(text.index(j))),
						      '%s%s_page%s.pdf'%(prob, i, str(text.index(j))))
				except:
					logger.exception('Text Error at pdf %s page %d' % 
									(i, text.index(j)))
			# Delete pdf file i after split, pages renamed, and pages filed
			os.remove('%s%s' % (PATH, i))
			logger.info('Deleted pdf %s' % i)
		except:
			logger.exception('Failure at pdf %s page %d' % (i, text.index(j)))
			os.rename('%s%s' % (PATH, i), '%s%s' % (prob, i))
	else:
		logger.info('file %s not a pdf file' % i)			

	# Rename Split PDF page documents
	# for j in pdf_names:
	# 	if os.path.isdir(dest+acct) == False:
	# 		os.mkdir(dest+acct)
	# 	os.rename('%s.pdf'%str(pdf_names.index(j)), dest+acct+'%s'%j)


# TODO: Make filepaths absolute
#		Test for .pdf file type to avoid exceptions
#		Adjust logger so it's readily apparent how many files read - use levels (debug, info, etc.)
#		remove scan file after run