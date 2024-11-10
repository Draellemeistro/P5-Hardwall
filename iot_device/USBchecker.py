import subprocess
import os
import usb # se https://github.com/pyusb/pyusb/blob/master/docs/tutorial.rst
import sys
import time
import re

    
class find_class(object):
    def __init__(self, class_):
        self._class = class_
    def __call__(self, device):
        # first, let's check the device
        if device.bDeviceClass == self._class:
            return True
        # ok, transverse all devices to find an
        # interface that matches our class
        for cfg in device:
            # find_descriptor: what's it?
            intf = usb.util.find_descriptor(
                                        cfg,
                                        bInterfaceClass=self._class
                                )
            if intf is not None:
                return True

        return False


if __name__ == '__main__':
    # Monitor incomming USB connections. See: https://www.man7.org/linux/man-pages/man8/udevadm.8.html
    #subprocess.run(['udevadm', 'monitor', '--subsystem-match=usb', '--property'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    continue_monitoring = True
    linetracker = 0
    outstr_list = []

    #  udev management tool for monitoring the kernel's udev device event manager
    # Hasnt been tested for a lot of devices, but it should work \(hopefully)
    proc = subprocess.Popen(
        ['udevadm', 'monitor', '--subsystem-match=usb', '--property'], 
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   
    while continue_monitoring:
        try:
            outs = proc.stdout.readline()
            if not outs:
                pass
            else:
                outstr = outs.decode('utf-8')
                outstr_list.append(outstr)
                print(outstr)
                if 'DRIVER' in outstr:
                    print('USB connected')
                    print(outstr)
                    proc.terminate()
                    break
                linetracker += 1
        except KeyboardInterrupt:
            print('USB monitoring stopped\n', KeyboardInterrupt)
            proc.terminate()
            time.sleep(1)
            break

    for num in range(linetracker, -1, -1):
        # Find device ID: regex for string after 'PRODUCT=' containing 'str' '\' 'str'
        devid = re.search(r'(?<=PRODUCT=)(\w+/\w+)', outstr_list[num-1])

        if devid: 
            #format device ID and add leading zeros if needed
            id_parts = str(devid.group(0)).split('/')
            vendor_id = id_parts[0].zfill(4)
            product_id = id_parts[1].zfill(4)
            devid = ':'.join([vendor_id, product_id])
            break

    if not devid:
        print('No device ID found')
        print(outstr_list)

    # Find device in lsusb output for more info
    lsusb_proc = subprocess.run(['lsusb', '-t', '-v'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    lsusb_outs = lsusb_proc.stdout
    lsusb_outstr = lsusb_outs.splitlines()

    busnr = 0
    device_matches = []
    if devid:
        for index, line in enumerate(lsusb_outstr):     
            line = line.decode('utf-8')
            if 'Bus' in line:
                busstr = re.search('(?<=Bus )(\d+)', line).group(0)
                if (int(busstr)):
                    busnr = int(busstr)
                    
            if devid in line:
                # find device description from stringline. 
                # e.g. 'ID 058f:6387 Alcor Micro Corp. Flash Drive'
                splitline = line.split("ID "+devid, 1)
                devdescr = splitline[1].strip()

                prior_line = lsusb_outstr[index-1].decode('utf-8')
                # find bus, port, device and interface number from prior line. 
                # e.g. '|__ Port 1: Dev 16, If 0, Class=Mass Storage, Driver=usb-storage, 5000M'
                portnr = int(re.search('(?<= Port )(\d+)', prior_line).group(0))
                devnr = int(re.search('(?<=Dev )(\d+)', prior_line).group(0))
                intfnr = int(re.search('(?<=If )(\d+)', prior_line).group(0))
                dev_class = re.search(r'(?<=Driver=)([^,]+)', prior_line).group(0)
                device_matches.append([devid, devdescr, busnr, portnr, devnr, intfnr])
            
        print("\n\n=====================================\n",
            '[ID, Description, Bus, Port, Device, Interface]')
        print(device_matches)
        # kan lave lsusb -d <vendor_id>:<product_id> -v for mere info
        lsusb_d_proc = subprocess.run(['lsusb', '-d', devid], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        lsusb_d_outs = lsusb_d_proc.stdout.decode('utf-8')
        print(lsusb_d_outs)
    else:
        print('No device ID found. Printing lsusb output')
        for line in lsusb_outstr:
            print(line.decode('utf-8'))
        
    # proevede at finde ud af hvordan det nedenunder virker. 
    # hapset fra https://github.com/pyusb/pyusb/blob/master/docs/tutorial.rst
    #detailed_devices = []
    #for dev in usb.core.find(find_all=True):
    #    dev = dev._get_full_descriptor_str().split('\n')
    #    detailed_devices.append(dev)
    
        
