import zipfile, os

def unzip_file(file, extract_file_path):
	with zipfile.ZipFile(file, 'r') as zipObj:
		zipObj.extractall(extract_file_path)

def zip_file(source_file, zip_file_name):
	z = zipfile.ZipFile(zip_file_name,'w',zipfile.ZIP_DEFLATED) 
	for dirpath, dirnames, filenames in os.walk(source_file):
	    fpath = dirpath.replace(source_file,'') 
	    fpath = fpath and fpath + os.sep or ''
	    for filename in filenames:
	        z.write(os.path.join(dirpath, filename),fpath+filename)
	z.close()
