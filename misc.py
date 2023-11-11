from bs4 import BeautifulSoup as bs
import os
import json
import requests as req

# Links & Files
with open('Gears.json', 'r') as f:
    Gears = json.load(f)

APIUrl = 'https://assetdelivery.roblox.com/v1/asset/?ID={0}'

def TypeCheck(Text):
    try:
        # Check For XML
        print('1')
        return 'XML'
    except:
        # Check For Binary

        return 'Binary'

# Main Loop
Counter = 0
for GearName, GearData in Gears.items():
    Counter += 1
    if Counter >= 3:
        break
    # Variable & Directory Setup
    GearId = GearData['ID']
    if not os.path.exists(f'./GearScripts/{GearId}'):
        os.makedirs(f'./GearScripts/{GearId}')
    MainDir = f'./GearScripts/{GearId}'

    #GearName Text File
    TextFile = open(f'{MainDir}/GearName.txt', 'w')
    TextFile.write(GearName)
    TextFile.close()

    # XML Write
    Request = req.get(APIUrl.format(GearId))
    if TypeCheck(Request.text) == 'Binary':
        print('Binary')
    elif TypeCheck(Request.text) == 'XML':
        print('XML')
        BSData = bs(Request.text, 'xml')
        print(BSData.attrs)
        XMLFile = open(f'{MainDir}/{GearId}.xml', 'w')
        XMLFile.write(Request.text)
        XMLFile.close()

    # Read XML File
    print(GearName)
    XMLFile = open(f'{MainDir}/{GearId}.xml', 'r')
    XMLData = XMLFile.read()
    BSData = bs(XMLData, 'xml')

    #Find Scripts
    ServerScripts = BSData.find_all('Item', {'class':'Script'})
    LocalScripts = BSData.find_all('Item', {'class':'LocalScript'})
    ModuleScripts = BSData.find_all('Item', {'class':'ModuleScript'})

    #Loop Through Scripts
    for Item in ServerScripts: #ServerScripts
        ScriptName = Item.find('string', {'name':'Name'}).text
        ScriptSource = Item.find('ProtectedString', {'name':'Source'}).text
        ScriptFile = open(f'{MainDir}/{ScriptName}.lua', 'w')
        ScriptFile.write('--ServerScript\n' + ScriptSource)
        ScriptFile.close()

    for Item in LocalScripts: #LocalScripts
        ScriptName = Item.find('string', {'name':'Name'}).text
        ScriptSource = Item.find('ProtectedString', {'name':'Source'}).text
        ScriptFile = open(f'{MainDir}/{ScriptName}.lua', 'w')
        ScriptFile.write('--LocalScript\n' + ScriptSource)
        ScriptFile.close()

    for Item in ModuleScripts: #ModuleScripts
        ScriptName = Item.find('string', {'name':'Name'}).text
        ScriptSource = Item.find('ProtectedString', {'name':'Source'}).text
        ScriptFile = open(f'{MainDir}/{ScriptName}.lua', 'w')
        ScriptFile.write('--ModuleScript\n' + ScriptSource)
        ScriptFile.close()

    # Close XML File
    XMLFile.close()

print('Finished')