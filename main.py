from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import zipfile, os, sys, shutil, string, time


gauth = GoogleAuth()
drive = GoogleDrive(gauth)

def fileDownload(fileID):
	os.system('~/drive download -i ' + fileID)


def zipExtract(fileName):
	print "Extracting: " + fileName
	thing = open(fileName, 'rb')
	z = zipfile.ZipFile(thing)
	z.extractall(fileName[:-4])


def zipDelete(fileName):
	print "Removing zip: " + fileName
	os.remove(fileName)


def dirUpload(folderID,dirName):
	print "Uploading: " + dirName
	command = '~/drive upload -f ~/'+ dirName + '/ -p ' + folderID
	print command
	os.system(str(command))


def dirDelete(dirName):
	print "Removing directory: " + dirName
	shutil.rmtree(dirName, ignore_errors=True)


def dirRename(dirName):
	print "Renamming Dir: " + dirName
	shutil.move(dirName,dirName.replace(" ","_"))


def isProcessed(fileObj):
	fileObj['title'] += 'fileProcesseD'
	print "Marking as Processed: " + fileObj['title']
	fileObj.Upload()


def isSizeValid(fileObj):
	fileSize = fileObj['fileSize']
	if int(fileSize) > 23000000000:
		print "File larger than 23GB"
		return False
	else:
		return True


foldersToWatch = ['0B9QXXYkcdR1SZHNQaTVsVTBEeEE', '0B0H8DkL_HW8zTGxZSW9VdmJXaVk', '0B9QXXYkcdR1Sdl9uNFU5blVScEE', '0B0H8DkL_HW8zYVNqN1NUNi1ObU0', '0B0H8DkL_HW8zRjFrYkFUTl9abW8', '0B0H8DkL_HW8zZWJEdHZyb3pVeFU', '0B0H8DkL_HW8zUHkyeVo4bnBzelE']
runNumber = 1
while True:
	print "Run #: " + str(runNumber)
	runNumber += 1
	time.sleep(300)
	for folderID in foldersToWatch:
		time.sleep(10)
		if folderID == '0B0H8DkL_HW8zTGxZSW9VdmJXaVk':
			folderIDtoUpload = '0B9QXXYkcdR1SZHNQaTVsVTBEeEE'
		else:
			folderIDtoUpload = folderID

		file_list = drive.ListFile({'q': "'" + folderID + "' in parents"}).GetList()
		for file1 in file_list:
		  if file1['title'][-4:] == '.zip' and isSizeValid(file1):
		  	print "Downloading: " + file1['title']
		  	fileDownload(file1['id'])
		  	zipExtract(file1['title'])
		  	zipDelete(file1['title'])
		  	dirRename(file1['title'][:-4])
		  	dirUpload(folderIDtoUpload,file1['title'][:-4].replace(" ","_"))
		  	dirDelete(file1['title'][:-4].replace(" ","_"))
		  	isProcessed(file1)



