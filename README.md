NautilusExt-HaveSeen
====================

This is primitive python implementation with ruby back-end to support "have seen" functionality across multiple machines.

Covered scenario. There is multiple ubuntu box on my local network. There is collaborative effort to review bunch of files on main computer. 
It would be good to have some functionality to when someone review the file he/she should put some tag as have-seen. This tag should be promoted on every box across local network.

Nautilus-ext

Install: Script should be copied to ~/.local/share/nautilus-python/extensions and some constants updated.

Implemented functionality for Ubuntu Nautilus. Main idea if I reviewed file I put with gvfs-set-attribute set icon and send to remote box the file name. Next script fetch all have-seen files and synchronize them.


Pre-request: Back-end on ruby. Should be installed ruby with some plugins. Also apache should be configured to support ruby as cgi.

Install: Copy scripts to some non-root user public_html folder all scripts. 

Nautilus extension will send to http://127.0.0.1/~user/have-seen/api/append.rb and fetch read already seen from http://127.0.0.1/~user/have-seen/api/fetch.rb. data will be stored in non-sufficient pretty-json format in ~/public_html/have-seen/repo/seen.json
