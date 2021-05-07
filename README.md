# noContactInfo Tor Exit Relay Excluder

Tor (Browser) does not have an option to allow users to say "do not use tor exit relays without ContactInfo in the exit position".
This script virtually implements such an option.

Setting a tor relay ContactInfo is considered an [expectations for tor relay operators](https://gitlab.torproject.org/tpo/community/team/-/wikis/Expectations-for-Relay-Operators).

This proof-of-concept script connects to a tor client daemon via the tor control socket and tells it to avoid 
[exit relays that have no ContactInfo](https://nusenu.github.io/OrNetStats/no-contactinfo-exits) set. It uses 
the [ExcludeExitNodes](https://2019.www.torproject.org/docs/tor-manual.html.en#ExcludeExitNodes) torrc configuration
option, that means the excluded exits will only be avoided in the exit position but continue to be used for other 
tor circuit positions (first and second hop). Tor exit relays are in the position to manipulate non-encrypted traffic
and malicious exit relays usally pose a higher risk to tor users than malicious middle relays.

The configuration change triggered by this script is non-persistent, meaning that restarting Tor (Browser) will revert the change.

For every excluded exit relay the URL for the [Relay Search](https://metrics.torproject.org/rs.html#search) page is written to standardout.

If the current tor daemon configuration already has an exit relay exclusion list it aborts and does not change the configuration.

The script also excludes relays that allow exiting but do not have the exit flag if they do not have a ContactInfo set.

Tor (Browser) must be running when the script is invoked.

## Example Output

```
Excluded exit relays:
https://metrics.torproject.org/rs.html#details/BBE2858B38C2E21310B182A84D951C27B366F00F
https://metrics.torproject.org/rs.html#details/7EECBAB900DFD29BF5F07AAD41EAF1E2BFF467E9
https://metrics.torproject.org/rs.html#details/9493135BC3EC01A29707EACA058FCEBD619F3BB1
[...]
##################################################################################
Excluded a total of 178 exit relays without ContactInfo from the exit position.
This tor configuration change is not permanently stored (non-persistent). A Tor Browser restart will revert this change.
```


## torrc Dependencies

The script depends on two torrc options, that must be present in the torrc file (Browser/TorBrowser/Data/Tor/torrc) before Tor Browser is started.

Choose a suitable path for the ControlSocket file (that only your user can access) in your home folder, replace the "-replace-me-" string here and in the script.
When tor starts it will create the file.

```
ControlSocket /home/-replace-me-/.tor-control.socket
UseMicrodescriptors 0
```


## Python Dependencies

* [stem](https://stem.torproject.org/) - tested with version 1.8.0


## Warning 


This is an experimental proof-of-concept script! 
