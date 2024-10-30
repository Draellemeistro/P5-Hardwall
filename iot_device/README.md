# idk some title
text

## USB passthrough -- USB/IP:
Some primary options:
- VirtualHere
- USB/IP
- USB-redirecor(?)
- USB-proxy
### VirtualHere
Link: 
https://www.virtualhere.com/

Alternatives(?)
https://www.reddit.com/r/cloudygamer/comments/11bz9bz/virtualhere_alternatives/

Video about VirtualHere on Raspberry Pi:
https://www.youtube.com/watch?v=YsHzJHykxNA

### USB-proxy
Maybe good link:
https://github.com/AristoChen/usb-proxy

One attempt:
https://github.com/usb-tools/USBProxy-legacy?tab=readme-ov-file

#### Science stuff
USB Proxy:
https://robbiedumitru.github.io/PDFs/DumitruBHW23.pdf

#### Facedancer
Link:
https://github.com/greatscottgadgets/facedancer?tab=readme-ov-file

##### What is a facedancer?
Facedancer boards are simple hardware devices that act as "remote-controlled" USB controllers. 
With the proper software, you can use these boards to quickly and easily emulate USB devices -- and to fuzz USB host controllers!

### USB/IP
Link:
https://usbip.sourceforge.net/

#### Summary
The USB/IP Project aims to develop a general USB device sharing system over IP network. 
To share USB devices between computers with their full functionality, USB/IP encapsulates USB I/O requests into IP packets and transmits them between computers.

#### User Comments
"`usbip` works well when connected but there is no good handling of disconnects and reconnects from both sides. 
I wanted to use that for a printer and it was a pain. 
Ended up using CUPS on a raspberry pi."

"Late, but I tested doing this on a Raspberry pi host to a Windows client. 
The host and the client will have to run a script to start the service each time. 
You can have the script run automatically on startup for both devices if you'd like. 
I got this working pretty well over Wifi, but had issues when switching over to Ethernet (client couldn't connect to the host, I'm blaming my double NAT Internet for it).
I had better compatibility with the app version of USBIP (the one with the unsigned driver which is a pain to install) than older versions of it."
### USB-Redirector
Link:
https://www.net-usb.com/usb-redirector/

Relevant:
https://github.com/OliverRieder/Usb-Over-Ethernet/blob/master/USB-Redirector.md

#### Use cases
- USB redirection to a remote desktop
- USB devices in a virtual machine session
- Access MFD from any room of your office
- USB redirection for thin/zero clients
- Access USB devices from blade servers

### Basic functionality on an esp32
Discussion of viability:
https://www.esp32.com/viewtopic.php?t=26952

https://github.com/chegewara/esp32-usbip-poc

#### Why?
RaspPis are expensive, large, not made to turn on/off, more power, overkill
VirtualHere and similar are mnot availablefor esp32. 
Esp32 has built-in full USB stack, that should be powerful enough though.

## Extra / maybe useful
https://code.google.com/archive/p/busdog/
https://www.lineeye.com/html/p_LE-650H2.html
https://github.com/ataradov/usb-sniffer
https://learn.microsoft.com/en-us/defender-endpoint/device-discovery

### USB Analyzers / USB sniffers
https://hhdsoftware.com/usb-sniffer
