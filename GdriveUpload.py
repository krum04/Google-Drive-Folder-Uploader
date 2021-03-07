from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
import os

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

gauth = GoogleAuth()

drive = GoogleDrive(gauth)
curDir = os.getcwd()


def newFolder(folderName):  # Create a new folder

    folder = drive.CreateFile(
        {'title': folderName, 'mimeType': 'application/vnd.google-apps.folder'})
    folder.Upload()

    # List drive id for new folder
    fileList = drive.ListFile(
        {'q': "'root' in parents and trashed=false"}).GetList()
    for file in fileList:
        if file['title'] == folderName:
            print('Title: %s, ID: %s' % (file['title'], file['id']))
            folderId = file['id']

            # Get the folder ID that you want
            if(file['title'] == "To Share"):
                folderId = file['id']
    print(folderId)
    return folderId


def listFiles(folderID):  # look up new folder ID
    with open('LinkSummary.tsv', 'w') as newFile:
        file_list = drive.ListFile(
            {'q': f"'{folderID}' in parents and trashed=false"}).GetList()
        newFile.write("FileName\tShareURL\t\n")
        for folder in file_list:
            print(folder['originalFilename'], folder['embedLink'])
            # newFile.write('"' + folder['originalFilename'] + '"' + ', ' + folder['embedLink'] + ', \n')
            newFile.write(
                '"' + folder['originalFilename'] + '"' + '\t' + folder['embedLink'] + '\t\n')
    os.open(uplFldEntry.get()+'/LinkSummary.tsv', os.O_RDWR)


def fileUpload(folderName, file):  # Upload files
    gauth.LocalWebserverAuth()
    folders = drive.ListFile(
        {'q': "title='" + folderName + "' and mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()
    for folder in folders:
        if folder['title'] == folderName:
            file2 = drive.CreateFile({'parents': [{'id': folder['id']}]})
            file2.SetContentFile(file)
            file2.Upload()
    return True

# Functions for Tkinter


def uploadPath():  # Create File Dialog to to select export folder
    value = filedialog.askdirectory(
        initialdir=os.getcwd(), title="Upload Folder")
    uplFldEntry.delete(0, "end")
    uplFldEntry.insert(0, value)


def upload(folderName, path):
    folder = folderName
    folderID = newFolder(folder)
    os.chdir(path)
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for file in files:
        fileUpload(folder, file)
    listFiles(folderID)


# Create window
window = tk.Tk()
window.title("G Drive Upload")
window.lift()
window.resizable(width=False, height=False)
window.columnconfigure(2, weight=1, minsize=75)
window.rowconfigure(2, weight=1, minsize=50)

# Select Upload Folder
uplFldLbl = tk.Label(text='Upload Folder')
uplFldLbl.grid(row=1, column=0, padx=5, pady=5, sticky='e')
uplFldEntry = tk.Entry(width=25)
uplFldEntry.grid(row=1, column=1, padx=5, pady=5)
uplFldBtn = tk.Button(text="Select Folder",
                      command=lambda: uploadPath())
uplFldBtn.grid(row=1, column=2, padx=5, pady=5, sticky='w')

# Folder Name
nameLbl = tk.Label(text='Folder Name')
nameLbl.grid(row=2, column=0, padx=5, pady=5, sticky='e')
nameEntry = tk.Entry(width=25)
nameEntry.grid(row=2, column=1, padx=5, pady=5)

# Upload file button
uplBtn = tk.Button(text="Upload",
                   command=lambda: upload(nameEntry.get(), uplFldEntry.get()))
uplBtn.grid(row=2, column=2, padx=5, pady=2, sticky='w')


window.mainloop()
