import argparse

import ctypes, sys

#find operating system type
def findOs():
    from sys import platform
    host = r"C:\Windows\System32\drivers\etc\hosts"
    if platform == "linux" or platform == "linux2":
        host = '/etc/hosts'
    elif platform == "win32":
        host = r"C:\Windows\System32\drivers\etc\hosts"
    elif platform == "MacOs":
        host = '/private/etc/hosts'
    return host

#split siteName 
def splitSiteName(siteName):
    try:
        begin = siteName.index("//", 0) + 2
    except:
        begin = 0
    try:
        end = siteName.index('/', begin)
    except:
        end = len(siteName)
    return siteName[begin:end]

#siteName to insert to host page to block
def webSiteToBlockInWin32(sites_to_block):
    existsAddress = False
    #check if in last line in host file exists address "127.0.0.1"
    with open(host, 'r') as f:
        lines = f.read().splitlines()
        if len(lines) > 0:
            last_line = lines[-1]
            if "127.0.0.1" in last_line:
                existsAddress = True
    #if not exists "127.0.0.1" add it with siteName to block ,anyway blocked the siteName
    with open(host, 'a') as f:
        if existsAddress is False:
            f.write("127.0.0.1   ")
        for site in sites_to_block:
            f.write(site + "    ")
            print("the web site  successfully blocked is : "f'{site}')
    #else:
        # Re-run the program with admin rights
        #ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        
#check if the user is  administrator   
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

#get siteName to unBlock
def unBlockeWebSite(siteName):
    new_text = ""
    name = splitSiteName(siteName)
    with open(host, 'r') as file:
        text = file.read().split('\n')
    for i in text:
        if i[0:9] == '127.0.0.1':
            if name in i.split(' '):
                print("found the site's name in host page")
                i = i.replace(name, '')
        if len(i) > 1:
            new_text = new_text + '\n' + i
    with open(host, 'w') as file:
        file.write(new_text)

#return list of site to block that arn't already blocked
def checkWebSiteToAdd(listSiteName):
    with open(host, 'r') as file:
        text = file.read().split('\n')
    resArr = []
    arr = []
    for line in text:
        if "127.0.0.1" in line:
            arr = line.split(" ")
            for i in arr:
                resArr.append(i)
    website_name = [x for x in listSiteName if not x in resArr]
    print([x + " is already blocked" for x in resArr if x in listSiteName])
    return website_name


parser = argparse.ArgumentParser(description = "My sites blocker")
parser.add_argument('--arrSite','-nameSite',nargs='*', help = 'insert site to Block')
parser.add_argument('--site','-s', help = 'insert site to unBlock')
args = parser.parse_args()

if __name__ == '__main__':
    if is_admin():
        host = findOs()
        web_sites_to_block=[]
        web_sites_to_block = args.arrSite
        if args.arrSite:
            for i, site in enumerate(web_sites_to_block):
                web_sites_to_block[i] = splitSiteName(site)
            sites_to_block = checkWebSiteToAdd(web_sites_to_block)
            webSiteToBlockInWin32(sites_to_block)
        if args.site:
            unBlockeWebSite(args.site)
    else:
        print("please set your user as administrator")

