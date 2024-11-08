import subprocess
import usb.core # se https://github.com/pyusb/pyusb/blob/master/docs/tutorial.rst
import usb.util
import sys
import time

    
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
    proc = subprocess.Popen(
        ['udevadm', 'monitor', '--subsystem-match=usb', '--property'], 
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    continue_monitoring = True
    time.sleep(10)

    while continue_monitoring:
        outs = proc.stdout.readline()
        outstr = outs.decode('utf-8')
        if not outs:
            pass
        else:
            print(outstr)
            if 'DRIVER' in outstr:
                print(outstr)
                break
      
    print('USB is connected')

    # proevede at finde ud af hvordan det nedenunder virker. 
    # hapset fra https://github.com/pyusb/pyusb/blob/master/docs/tutorial.rst
    storage_usbs = usb.core.find(find_all=1, custom_match=find_class(8))
    if storage_usbs is None:
        print('No storage USBs found')
    else:
        for cfg in storage_usbs:
            sys.stdout.write(str(cfg.configurations) + '\n')
            sys.stdout.write(str(cfg._get_full_descriptor_str) + '\n')

    HID_usbs = usb.core.find(find_all=1, custom_match=find_class(3))               
    if HID_usbs is None:
        print('No HID USBs found')
    else:
        for cfg in HID_usbs:
            sys.stdout.write(str(cfg.configurations) + '\n')
            sys.stdout.write(str(cfg._get_full_descriptor_str) + '\n')

    network_usbs = usb.core.find(find_all=1, custom_match=find_class(2))
    if network_usbs is None:
        print('No network USBs found')
    else:
        for cfg in network_usbs:
            sys.stdout.write(str(cfg.configurations) + '\n')
            sys.stdout.write(str(cfg._get_full_descriptor_str) + '\n')
