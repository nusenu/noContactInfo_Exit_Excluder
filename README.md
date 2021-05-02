# exclude tor exit relays without ContactInfo

This proof-of-concept script connects to a tor client daemon via the tor control socket and tells it to avoid 
[exit relays that have no ContactInfo](https://nusenu.github.io/OrNetStats/no-contactinfo-exits) set. It uses 
the [ExcludeExitNodes](https://2019.www.torproject.org/docs/tor-manual.html.en#ExcludeExitNodes) torrc configution
option, that means the excluded exits will only be avoided in the exit position but continue to be used for other positions (first and second hop).

The configuration change is non-persistent, meaning that restarting the tor daemon will revert the change.

For every excluded exit relay the URL for the Relay Search page is printed to standard output.

If the current tor daemon configuration already has an exit relay exclusion list it aborts and does not change the configuration.

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

exclude_noContactInfo_Exits depends on two torrc options, that must be present in Browser/TorBrowser/Data/Tor/torrc before Tor Browser is started:

```
ControlSocket /home/-replace-me-/.tor-control.socket
UseMicrodescriptors 0
```


## Python Dependencies

* [stem](https://stem.torproject.org/) - tested with version 1.8.0


## Warning 


This is an experimental proof-of-concept script! 
