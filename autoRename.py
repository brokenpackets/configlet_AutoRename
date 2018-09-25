import re
from cvprac.cvp_client import CvpClient ## CVPRAC, https://github.com/aristanetworks/cvprac  
# Note: PR in place for get_configlets(), but has not been merged yet.
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #ignores ssl-cert validation.

clnt = CvpClient() #Create CVPClient session.

### User Variables
username = 'admin'
password = 'Arista'
cvp_ip = '192.168.255.50'

### Rest of script
regex_body = re.compile('^!DynConfig (.*?)\n') # match first line of configlet
                                               # if !DynConfig exists (used for
                                               # name of configlet.

regex_name = re.compile('^dyn_.*') # don't process multiple times
                                   # against same configlet.
output = []
clnt.connect([cvp_ip], username, password, protocol='https')
              #Create connection to CVP IP, with creds in-line.
configlets = clnt.api.get_configlets(configletType='generated', searchstring='')['data']
              #Grab all 'generated' configlets.
def main():
    for item in configlets: #Loop through configlets
        if regex_body.match(item['config']): #Inspect configlet for regex_body.
            if regex_name.match(item['name']): #If already renamed, ignore.
                pass #Do nothing, skip to next item.
            else:
                configlet = item['config'] #Store config as variable.
                configletname = 'dyn_'+regex_body.match(configlet).group(1)
                #Create new name with dyn_ configlet regex match
                #Eg. '!DynConfig Arista-10_VLAN_151' -> dyn_Arista-10_VLAN_151
                output = clnt.api.update_configlet(configlet, item['key'], configletname)
                #key used to match configlet unique ID. Updates Body and Name.
                print item['name']+'--->'+output['data']
                #Simple output to show old and new configlet name

if __name__ == "__main__":
    main()
