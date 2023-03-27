from settings import config, toConfig
cnfg = config()

envFile=open('env.txt', 'r')
lines=envFile.readlines()

enData={}
for line in lines:
    enKey=line[:line.find('='):]
    enVal=line[line.find('=')+1::].strip()
    enData[enKey]=enVal

# print(enData)

need2write=False

def changeConfigData(cnfg, envKey, cnfgRootKey, cnfgDataKey):
    need2write=False
    if envKey in enData:
        if len(enData[envKey])>0:
            if cnfgRootKey not in cnfg:
                need2write=True
                cnfg[cnfgRootKey]={}
            if cnfgDataKey not in cnfg[cnfgRootKey]:
                need2write=True
                cnfg[cnfgRootKey][cnfgDataKey]=enData[envKey]
            else:
                if isinstance(cnfg[cnfgRootKey][cnfgDataKey], str) or  isinstance(cnfg[cnfgRootKey][cnfgDataKey], int):
                    need2write=True
                    cnfg[cnfgRootKey][cnfgDataKey]=enData[envKey]
                    if isinstance(cnfg[cnfgRootKey][cnfgDataKey], int):
                        cnfg[cnfgRootKey][cnfgDataKey]=int(enData[envKey])
                else:
                    raise Exception("Trying to set string / integer configuration value into a predefined array value, check configuraion YAML file for '"+cnfgRootKey+"' >> '"+cnfgDataKey+"'")
        else:
            if cnfgRootKey in cnfg and cnfgDataKey in cnfg[cnfgRootKey]:
                if isinstance(cnfg[cnfgRootKey][cnfgDataKey], str):
                    need2write=True
                    nData={}
                    for dk in cnfg[cnfgRootKey].keys():
                        if dk!=cnfgDataKey: nData[dk]=cnfg[cnfgRootKey][dk]
                    if len(nData)>0:
                        cnfg[cnfgRootKey]=nData
                    else:
                        nCnfg={}
                        for dk in cnfg.keys():
                            if dk!=cnfgRootKey: nCnfg[dk]=cnfg[dk]
                        cnfg=nCnfg
                else:
                    raise Exception("Trying to remote string configuration value from a predefined array value, check configuraion YAML file for '"+cnfgRootKey+"' >> '"+cnfgDataKey+"'")
    return [need2write, cnfg]


nData=changeConfigData(cnfg, 'OPENAI_KEY', 'openai', 'key')
if nData[0]==True:
    need2write=True
    cnfg=nData[1]
nData=changeConfigData(cnfg, 'SERVER_HOST', 'server', 'host')
if nData[0]==True:
    need2write=True
    cnfg=nData[1]
nData=changeConfigData(cnfg, 'SERVER_PORT', 'server', 'port')
if nData[0]==True:
    need2write=True
    cnfg=nData[1]
nData=changeConfigData(cnfg, 'CRAWL_DOMAIN', 'crawl', 'domain')
if nData[0]==True:
    need2write=True
    cnfg=nData[1]
nData=changeConfigData(cnfg, 'CRAWL_ROOT', 'crawl', 'root')

if True==need2write:
    toConfig(cnfg)
    print('New configuration data written')
    print(cnfg)


# sudo docker build --build-arg OPENAI_KEY="super-secret-key" -t tmp2test .
# {'HOSTNAME': '1fabfdd58553', 'PYTHON_PIP_VERSION': '22.3.1', 'HOME': '/root', 'OPENAI_KEY': 'super-secret-key', 'GPG_KEY': 'A035C8C19219BA821ECEA86B64E628F8D684696D', 'PYTHON_GET_PIP_URL': 'https://github.com/pypa/get-pip/raw/d5cb0afaf23b8520f1bbcfed521017b4a95f5c01/public/get-pip.py', 'PATH': '/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin', 'LANG': 'C.UTF-8', 'PYTHON_VERSION': '3.10.10', 'PYTHON_SETUPTOOLS_VERSION': '65.5.1', 'SERVER_HOST': 'python.site4chatgptrnd.shahadathossain.com', 'PWD': '/code', 'PYTHON_GET_PIP_SHA256': '394be00f13fa1b9aaa47e911bdb59a09c3b2986472130f30aa0bfaf7f3980637', 'SERVER_PORT': '59014'}

#toConfig(fData)

