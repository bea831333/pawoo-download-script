import os, sys, urllib.request

def increment_file_name(filename, multiple):
    filenameparts = filename.split('.')
    return ('.'.join(filenameparts[:-1]) + " - " + str(multiple) + "." + filenameparts[1])

if __name__ == "__main__":
    artistname = sys.argv[1]
    downloadfolder = "downloads"
    urlbase = "https://baraag.net/@" + artistname + "/media?page="
    pagenum = 1
    flag = True
    while flag:
        flag = False
        url = urlbase + str(pagenum)
        print(url)
        page = urllib.request.urlopen(url).read().decode("utf-8")
        lines = page.split('\n')
        for line in lines:
            if line.startswith("<a href=\"/system/media_attachments"):
                if not os.path.exists(downloadfolder):
                    os.makedirs(downloadfolder)
                if not os.path.exists(os.path.join(downloadfolder, artistname)):
                    os.makedirs(os.path.join(downloadfolder, artistname))
                
                download = "https://baraag.net" + line.split('"')[1]
                filename = download.split('/')[11]
                
                if os.path.exists(os.path.join(downloadfolder, artistname, filename)):
                    multiple = 1
                    newfilename = increment_file_name(filename, multiple)
                    while os.path.exists(os.path.join(downloadfolder, artistname, newfilename)):
                        multiple += 1
                        newfilename = increment_file_name(filename, multiple)
                    urllib.request.urlretrieve(download, os.path.join(downloadfolder, artistname, newfilename))
                    print("Downloaded '" + filename + "' as '" + newfilename + "'")
                else:
                    urllib.request.urlretrieve(download, os.path.join(downloadfolder, artistname, filename))
                    print("Downloaded '" + filename + "'")
            elif "Show older" in line:
                pagenum += 1
                flag = True