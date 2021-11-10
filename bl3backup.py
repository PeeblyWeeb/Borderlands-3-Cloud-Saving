import dropbox
import zipfile
import os
import time
import webbrowser
import secrets


# [Definitions]
def cc():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)


def zip_file(path, zip_h):
    for root, dirs, files in os.walk(path):
        for file in files:
            zip_h.write(os.path.join(BL3SavDir, file))


def upload_file(ff, ft):
    box = dropbox.Dropbox(dbx_access)
    f = open(ff, 'rb')
    box.files_upload(f.read(), ft)
# [/Definitions]


# Assign Dropbox variables
dbx_access = secrets.dbxtoken
dbx = dropbox.Dropbox(dbx_access)

# Get required information to find save location
SystemUser = os.getenv('USERNAME')

print('SystemUser: ' + SystemUser)
print("If you don't know how to get your steam id, Check out this video here!\nhttps://youtu.be/GQ2zR3W0Czc")

SteamID = input("Please enter your SteamID (Only Numbers):\n> ")

# Assign upload parameters
ff = f'{SteamID}.zip'
ft = f'/Borderlands Saves/{SteamID}.zip'

cc()

# Check if a save has already been uploaded
f_e = str(dbx.files_search(query=f'{SteamID}.zip', path='/Borderlands Saves'))
f_e = f_e[22:23]  # Theres probably a way better way to do this and i'm just dumb, please tell me how.

cc()

print(f'SystemUser: {SystemUser}')
print(f'SteamID: {SteamID}')

time.sleep(1)

cc()

# Construct Directory to Save Files
BL3SavDir = f'C:/Users/{SystemUser}/Documents/My Games/Borderlands 3/Saved/SaveGames/{SteamID}'

print('Backing up Borderlands 3 Saves.... (This might take a moment)')

# Create zip file
zip_f = zipfile.ZipFile(f'{SteamID}.zip', 'w', zipfile.ZIP_DEFLATED)
zip_file(BL3SavDir + '/', zip_f)
zip_f.close()

# Delete old cloud save if it exists
if f_e == 'S':
    print('Deleting old cloud save...')

    dbx = dropbox.Dropbox(dbx_access)
    dbx.files_delete_v2(path=f'/Borderlands Saves/{SteamID}.zip')

    cc()

    print('Deleting old cloud save... OK')

# Upload file to dropbox
print('Uploading local save to the cloud...')

upload_file(ff, ft)

cc()

if f_e == 'S':
    print('Deleting old cloud save... OK')
print('Uploading local save to the cloud... OK')

# Delete zipped file from system
print('Deleting temporary files...')

os.remove(f'{SteamID}.zip')

cc()

if f_e == 'S':
    print('Deleting old cloud save... OK')
print('Uploading local save to the cloud... OK')
print('Deleting temporary files... OK')

dlf = input('Download backup to local computer? (y/n)\n> ')

if dlf == 'y':
    print('Downloading save from cloud...')
    dbx = dropbox.Dropbox(dbx_access)
    t_l = str(dbx.files_get_temporary_link(path=f'/Borderlands Saves/{SteamID}.zip'))

    idx = t_l.find("ile', metadata")

    dl = t_l[29:idx + 3]  # Theres gotta be a better way to do this right?!?!?
    webbrowser.open_new_tab(dl)

cc()

if f_e == 'S':
    print('Deleting old cloud save... OK')

print('Uploading local save to the cloud... OK')
print('Deleting temporary files... OK')

if dlf == 'y':
    print('Downloading save from cloud... OK')

print('\n[ You can now close this window ]')

# haha funny
time.sleep(69420)
