import json
import os
import shutil
import subprocess
from datetime import datetime

print("Loading config...") 
with open('Configs/config.json') as json_data_file:
    data = json.load(json_data_file)
mods = data['Mods'];
islands = data['Islands']
missions = data['Missions']
addons = data['Addons']
for scfg in data['Subconfigs']:
    print("Parsing config "+scfg)    
    with open(scfg) as json_adata:  
        adata = json.load(json_adata)  
        mods = mods + adata['Mods'];
        islands = islands + adata['Islands'];
        missions = missions + adata['Missions'];
        addons = addons + adata['Addons']
#Add devbuild number to version
#if os.environ['GIT_BRANCH'] == "develop":
data['replace']['VERSION'] += ' dev ' + datetime.today().strftime("%y%m%d %H%M")
data['replace']['RELEASE'] = 'Mission'
cpbo = data['cpbo'];

for directory in [data['BuildDir'], data['PackedDir']+'/Addons', data['PackedDir']+'/Missions']:
    os.makedirs(directory, exist_ok=True)

for the_file in os.listdir(data['BuildDir']):
    file_path = os.path.join(data['BuildDir'], the_file)
    if os.path.isfile(file_path):
        os.unlink(file_path)
for mission in missions:
    modname =  mission['mod']
    islandname = mission['island']
    print ('Creating a mission with mod', modname, 'on', islandname)
    missionMod = None
    missionIsland = None
    for mod in mods:
        if mod['name'] == modname:
            missionMod = mod
    for island in islands:
        if island['name'] == islandname:
            missionIsland = island
    if missionMod is None:
        raise NameError('Mod was not found')
    if missionIsland is None:
        raise NameError('Island was not found')
    if not 'name' in mission:
        mission['name'] = data['Missionname']+'_'+missionMod['name']
    missiondir = data['BuildDir'] + '/missionfiles/' +mission['name']+'.'+ missionIsland['class']
    if os.path.exists(missiondir):
        shutil.rmtree(missiondir)
    shutil.copytree(data['Code']+'/',missiondir)
    shutil.copytree(missionIsland['path']+'/',missiondir+'/Island/')
    shutil.copytree(missionMod['path']+'/',missiondir+'/Units')
    
    required = ''
    for req in missionMod['require']:
        required = required + '"'+ req + '",'
    #if len(required) == 0 :
    #    required = '\b\b'

    shutil.copy('./Missions/'+mission['sqm']+'/mission.sqm',missiondir+'/mission.sqm')
    replace = dict(list(data['replace'].items()) + list(missionMod['replace'].items()) + list(missionIsland['replace'].items()));
    replace['REQUIRE'] = required
    for root, subFolders, files in os.walk(missiondir):
        for rfile in data['ParsedFiles']:
            if rfile in files:
                print('Found',rfile,'at',os.path.join(root, rfile))
                s=open(os.path.join(root, rfile)).read()
                for key in replace:
                    if '{* '+key+' *}' in s:
                        print('Found occurance of',key,'in file. Replacing with',replace[key])
                        s=s.replace('{* '+key+' *}', replace[key])
                    f=open(os.path.join(root, rfile), 'w')
                    f.write(s)
                    f.flush()
                    f.close()
    subprocess.call(["cpbo.exe", "-y", "-p", missiondir])
    shutil.copyfile(missiondir + ".pbo", data['PackedDir']+'/Missions/'+mission['name']+'.'+ missionIsland['class']+'.pbo') #Copy build artifact
t = []
for m in missions:
    t.append(m['name'].lower())
