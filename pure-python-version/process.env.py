from settings import config, toConfig, getConfigAfterChangingData
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



def getConfigDataChange(cnfg, enData, envKey, cnfgRootKey, cnfgDataKey):
    if envKey in enData:
        return getConfigAfterChangingData(cnfg, enData[envKey], cnfgRootKey, cnfgDataKey)
    return [False, {}]


nData=getConfigDataChange(cnfg, enData, 'OPENAI_KEY', 'openai', 'key')
if nData[0]==True:
    need2write=True
    cnfg=nData[1]
nData=getConfigDataChange(cnfg, enData, 'SERVER_HOST', 'server', 'host')
if nData[0]==True:
    need2write=True
    cnfg=nData[1]
nData=getConfigDataChange(cnfg, enData, 'SERVER_PORT', 'server', 'port')
if nData[0]==True:
    need2write=True
    cnfg=nData[1]
nData=getConfigDataChange(cnfg, enData, 'CRAWL_ROOT', 'crawl', 'root')
if nData[0]==True:
    need2write=True
    cnfg=nData[1]
'''
nData=getConfigDataChange(cnfg, enData, 'CRAWL_DOMAIN', 'crawl', 'domain')
if nData[0]==True:
    need2write=True
    cnfg=nData[1]
'''


if True==need2write:
    toConfig(cnfg)
    print('New configuration data written')
    print(cnfg)


# sudo docker build --build-arg OPENAI_KEY="super-secret-key" -t tmp2test .
# {'HOSTNAME': '1fabfdd58553', 'PYTHON_PIP_VERSION': '22.3.1', 'HOME': '/root', 'OPENAI_KEY': 'super-secret-key', 'GPG_KEY': 'A035C8C19219BA821ECEA86B64E628F8D684696D', 'PYTHON_GET_PIP_URL': 'https://github.com/pypa/get-pip/raw/d5cb0afaf23b8520f1bbcfed521017b4a95f5c01/public/get-pip.py', 'PATH': '/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin', 'LANG': 'C.UTF-8', 'PYTHON_VERSION': '3.10.10', 'PYTHON_SETUPTOOLS_VERSION': '65.5.1', 'SERVER_HOST': 'python.site4chatgptrnd.shahadathossain.com', 'PWD': '/code', 'PYTHON_GET_PIP_SHA256': '394be00f13fa1b9aaa47e911bdb59a09c3b2986472130f30aa0bfaf7f3980637', 'SERVER_PORT': '59014'}

#toConfig(fData)

