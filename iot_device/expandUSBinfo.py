import subprocess
import sys
import usb
import re


def usb_get_individual_descriptor(dev):
    #print("-Device Descriptor:")
    print("  bLength: %d (%s)" % (dev.bLength, hex(dev.bLength)))
    print("  bDescriptorType: %d (%s)" % (dev.bDescriptorType, hex(dev.bDescriptorType)))
    print("  idVendor: %d (%s)" % (dev.idVendor, hex(dev.idVendor)))
    print("  idProduct: %d (%s)" % (dev.idProduct, hex(dev.idProduct)))
    print("  bDeviceClass: %d (%s)" % (dev.bDeviceClass, hex(dev.bDeviceClass)))
    print("  bDeviceSubClass: %d (%s)" % (dev.bDeviceSubClass, hex(dev.bDeviceSubClass)))
    print("  bDeviceProtocol: %d (%s)" % (dev.bDeviceProtocol, hex(dev.bDeviceProtocol)))
    print("  number of configurations (dev.bNumConfigurations): %d (%s)\n" % (dev.bNumConfigurations, hex(dev.bNumConfigurations)))

def usb_dev_get_configuration_descriptor(cfg):
    #print("  -Configuration Descriptor:")
    print("    cfg.bConfigurationValue: %d (%s)" % (cfg.bConfigurationValue, hex(cfg.bConfigurationValue)))
    print("    number of interfaces (cfg.bNumInterfaces): %d (%s)\n" % (cfg.bNumInterfaces, hex(cfg.bNumInterfaces)))
    alt = usb.util.find_descriptor(cfg, find_all=True, bInterfaceNumber=1)
    
def usb_dev_cfg_get_interface_descriptor(intf):
    #print("    -Interface Descriptor:")
    print("      bInterfaceNumber: %d (%s)" % (intf.bInterfaceNumber, hex(intf.bInterfaceNumber)))
    print("      bAlternateSetting: %d (%s)" % (intf.bAlternateSetting, hex(intf.bAlternateSetting)))
    print("      number of endpoints (intf.bNumEndpoints): %d (%s)\n" % (intf.bNumEndpoints, hex(intf.bNumEndpoints)))

def usb_dev_cfg_intf_get_endpoint_descriptor(ep):
    #print("      -Endpoint Descriptor:")
    print("        bEndpointAddress: %d (%s)" % (ep.bEndpointAddress, hex(ep.bEndpointAddress)))
    print("        bmAttributes: %d (%s)" % (ep.bmAttributes, hex(ep.bmAttributes)))
    print("        wMaxPacketSize: %d (%s)" % (ep.wMaxPacketSize, hex(ep.wMaxPacketSize)))
    print("        bInterval: %d (%s)" % (ep.bInterval, hex(ep.bInterval)))

def usb_get_full_descriptor_str(dev):
    #print(dev._get_full_descriptor_str())
    #print("\n")
    return dev._get_full_descriptor_str()

def lsusb_way():
    d= 0
    proc = subprocess.Popen('lsusb', '-t')
    outs = proc.stdout.readline()
    outstr = outs.decode('utf-8')
    busnr = 0
    for line in outstr:
        if 'Bus' in line:
            busnr = line.split(' ')[1].split('.')[0]    
        print(busnr)
        if 'Class=Human Interface Device' in line:
            print('HID device found')
    # Bus 02.Port 1: Dev 1, Class=root_hub, Driver=xhci_hcd/9p, 480M
    # |__ Port 1: Dev 27, If 0, Class=Human Interface Device, Driver=usbhid, 12M
    # lsusb -s 02 27 -v:
    # Do same for Mass storage

def opt_one(dev, devnr):
        print("\n----------------------------------\n")
        try:
            print("==== Device #", devnr, ": ", dev.filename, " ====")
        except:
            print("==== Device #", devnr, ": None...? ====")
        usb_get_individual_descriptor(dev)

        cfgnr = 0
        for cfg in dev:
            print("  -Configuration(#%d) Descriptor:" % cfgnr)
            usb_dev_get_configuration_descriptor(cfg)
            cfgnr += 1

            intfnr = 0
            for intf in cfg:
                print("    -Interface Descriptor(# %d):" % intfnr)
                usb_dev_cfg_get_interface_descriptor(intf)
                intfnr += 1

                epnr = 0
                for ep in intf:
                    print("      -Endpoint Descriptor(#%d):" % epnr)
                    usb_dev_cfg_intf_get_endpoint_descriptor(ep)
                    epnr += 1

def find_class_devices(classstr, outline, outlinenext):
    searchstr = 'Class=' + classstr
    if searchstr in outline:
        portnr = int(re.search('(?<= Port )(\d+)', line).group(0))
        devnr = int(re.search('(?<=Dev )(\d+)', line).group(0))
        intfnr = int(re.search('(?<=If )(\d+)', line).group(0))
        devid = re.search('(?<=ID )(\w+:\w+)', outlinenext).group(0)
        devdescr = re.sub('(\s+\w+\s\w+:\w+)', '', outlinenext)
        devdescr = re.sub(r'^\s+', '', devdescr).lstrip()
        return 1, [devid, devdescr, busnr, portnr, devnr, intfnr]
    return 0, None
       
def print_findings(classlist, USBDict):
    try:
        print(" //=====  Device list  =====")
        print('||\n|| [ID, Description, Bus, Port, Device, Interface]')
        for classstr in classlist:
            if USBDict[classstr]:
                print("||\n||---%s---" %classstr)
                for device in USBDict[classstr]:
                    print('|| ',device)
        print('\\\ \n []=========================')
    except:
        print('No devices found ERROR')

def print_all_devices(USBDict):
    print(" []=====  Device list  =====")
    print('//\n|| [ID, Description, Bus, Port, Device, Interface]')
    for classstr in USBDict:
        print('\\\\')
        print(" ||---%s---\n//" %classstr)
        if USBDict[classstr]:
            for device in USBDict[classstr]:
                print('|| ',device)
    print('\\\ \n []=========================')


if __name__ == '__main__':
    devnr = 0
    detailed_devices = []
    classlist = ['Hub', 'Human Interface Device', 'Mass Storage', 'Wireless']
    USBDict = {}
    for classstr in classlist:
        USBDict[classstr] = []
        
    for dev in usb.core.find(find_all=True):
        detailed_devices.append(usb_get_full_descriptor_str(dev))
        #opt_one(dev, devnr)
        devnr += 1

    for dev in detailed_devices:
        # Man kunne lave noget regex her for at finde tonsvis af info
        dev = dev.split('\n')
        for index, line in enumerate(dev):
            print(index, line)
        print('\n')
            
    

        
    
        
    proc = subprocess.run(['lsusb', '-t', '-v'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    outs = proc.stdout
    outstr = outs.splitlines()
    busnr = 0

    for index, line in enumerate(outstr):        
        line = line.decode('utf-8')
        if 'Bus' in line:
            busstr = re.search('(?<=Bus )(\d+)', line).group(0)
            if (int(busstr)):
                busnr = int(busstr)
        
        for classstr in classlist:
            try:
                success, result = find_class_devices(classstr, line, outstr[index+1].decode('utf-8'))
                if success:
                    USBDict[classstr].append(result)
            except:
                pass  
  
            
    
    #print_findings(classlist, USBDict)
    #print('\n\n\n\n')
    print_all_devices(USBDict)