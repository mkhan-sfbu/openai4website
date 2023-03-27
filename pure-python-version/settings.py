import yaml
def config():
  with open('.config.yaml', 'r') as cnfg:
    config=yaml.safe_load(cnfg)
  return config
#print(config)
