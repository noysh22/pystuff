
import os, glob

TORRENT_DIR = r'torrents/'

def main():
	files = glob.glob(TORRENT_DIR + r'\*.torrent')
	for f in files:
		os.remove(f)
		print 'removed <%s>\n' % (f)

	print 'removed total of: %d files' % (len(files))
if __name__ == '__main__':
	main()