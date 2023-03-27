import yaml

def config():
  config={}
  with open(r'.config.yaml', 'r') as cnfg:
    config=yaml.safe_load(cnfg)
  return config
#print(config)

def toConfig(data):
  with open(r'.config.yaml', 'w') as file:
    yaml.dump(data, file)

def getConfigAfterChangingData(cnfg, data2change, cnfgRootKey, cnfgDataKey):
    need2write=False
    if (isinstance(data2change, str) and len(data2change)>0) or (isinstance(data2change, int) and data2change>0):
        if cnfgRootKey not in cnfg:
            need2write=True
            cnfg[cnfgRootKey]={}
        if cnfgDataKey not in cnfg[cnfgRootKey]:
            need2write=True
            cnfg[cnfgRootKey][cnfgDataKey]=data2change
        else:
            if isinstance(cnfg[cnfgRootKey][cnfgDataKey], str) or  isinstance(cnfg[cnfgRootKey][cnfgDataKey], int):
                if isinstance(cnfg[cnfgRootKey][cnfgDataKey], int) and cnfg[cnfgRootKey][cnfgDataKey]!=int(data2change):
                    data2changeX=data2change
                    if isinstance(data2change, int): data2changeX=str(data2change)
                    need2write=True
                    cnfg[cnfgRootKey][cnfgDataKey]=int(data2changeX)
                else:
                    if cnfg[cnfgRootKey][cnfgDataKey]!=data2change:
                        need2write=True
                        cnfg[cnfgRootKey][cnfgDataKey]=data2change
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



