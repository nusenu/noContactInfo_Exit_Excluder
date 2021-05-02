import sys
from stem.control import Controller
from stem.util.tor_tools import *

torsocketpath='/home/-replace-me-/.tor-control.socket'

try:
    controller = Controller.from_socket_file(path=torsocketpath)
    controller.authenticate()
except:
    print('Failed to connect to your local tor process using socket "%s". Is Tor Browser running? (it should be running)' % torsocketpath)
    sys.exit(1)

if not controller.is_set('UseMicrodescriptors'):
    print('"UseMicrodescriptors 0" is required in your torrc configuration. Exiting.')
    sys.exit(2)

try:
    relays = controller.get_server_descriptors()
except:
    print('Failed to get relay descriptors. Exiting.')
    sys.exit(3)

if controller.is_set('ExcludeExitNodes'):
    print('ExcludeExitNodes is in use already. Exiting.')
    sys.exit(4)

exit_excludelist=[]
print("Excluded exit relays:")
for relay in relays:
    if relay.exit_policy.is_exiting_allowed() and not relay.contact:
        if is_valid_fingerprint(relay.fingerprint):
            exit_excludelist.append(relay.fingerprint)
            print("https://metrics.torproject.org/rs.html#details/%s" % relay.fingerprint)
        else:
            print('Invalid Fingerprint: %s' % relay.fingerprint)

try:
    controller.set_conf('ExcludeExitNodes', exit_excludelist)
    print('##################################################################################')
    print('Excluded a total of %s exit relays without ContactInfo from the exit position.' % len(exit_excludelist))
    print('This tor configuration change is not permanently stored (non-persistent). A Tor Browser restart will revert this change.')
except:
    print('Failed to exclude ExitNodes!')
