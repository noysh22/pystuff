
import os
import sys
import fnmatch
import shutil

PATH = r"src"
DEST = r"dest"
PATTERN = r'*.jpg'

def copyfiles(files):
	for file_name in files:
		print 'moving %s to %s' % (file_name, DEST)
		try:
			shutil.move(file_name, DEST)
		except shutil.Error, e:
			dest_file = DEST + '\\' + os.path.basename(file_name)
			print 'removing %s' % file_name
			os.remove(dest_file)
			shutil.move(file_name, DEST)
		print 'done moving %s' % file_name

def find_files():
	matches = []
	for root, dirnames, filenames in os.walk(PATH):
		for filename in fnmatch.filter(filenames, PATTERN):
			matches.append(os.path.join(root, filename))

	return matches

def main():
	
	files = find_files()

	if len(files) > 0:
		copyfiles(files)
	else:
		print 'no files found in %s matches the pattern %s' % (PATH, PATTERN)

if __name__ == '__main__':
	main()