import subprocess
import time
import os

LIBIMOBILE_PATH = 'libimobile'

def check_libimobile_path():
    if not os.path.exists(LIBIMOBILE_PATH):
        print('libimobile directory not found...')
        print('Downloading libimobile...')
    else:
        print('libimobile directory found!')
    print()


def get_devices():
    path = os.path.join(LIBIMOBILE_PATH, 'idevice_id.exe')
    devices_process = subprocess.run([path, '-l'], stdout=subprocess.PIPE)

    if devices_process.returncode != 0:
        print('Error getting devices...')
        return

    devices = devices_process.stdout.decode('utf-8').split('\n')
    devices = [{device.replace('\r', '') : identifier_to_model_name(get_iphone_model(device.replace('\r', '')))} for device in devices if device]
    
    return devices

def get_device_info(udid):

    path = os.path.join(LIBIMOBILE_PATH, 'ideviceinfo.exe')

    info_process = subprocess.run([path, '-u', udid], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if info_process.returncode != 0:
        print(f'Error getting device info (Return Code {info_process.returncode}) {info_process.stderr if info_process.stderr else info_process.stdout}')
        return
    
    info = info_process.stdout.split('\n')
    info = [i for i in info if i]
    for i in info:
        print(i)

def get_activation_state(udid):

    path = os.path.join(LIBIMOBILE_PATH, 'ideviceactivation.exe')

    activation_process = subprocess.run([path, '-u', udid, 'state'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    activation = activation_process.stdout
    activation = activation.split(':')[-1].strip()
    return activation.split(':')[-1].strip()
    
def get_iphone_model(udid):

    path = os.path.join(LIBIMOBILE_PATH, 'ideviceinfo.exe')

    info_process = subprocess.run([path, '-u', udid], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if info_process.returncode != 0:
        print(f'Error getting device info (Return Code {info_process.returncode}) {info_process.stderr if info_process.stderr else info_process.stdout}')
        return
    
    info = info_process.stdout.split('\n')
    info = [i for i in info if i]
    for i in info:
        if 'ProductType' in i:
            return i.split(':')[-1].strip()
        
def identifier_to_model_name(identifier):
    model_names = {
        "Iphone 4" : ["iPhone3,1", "iPhone3,2", "iPhone3,3"],
        "Iphone 4S" : ["iPhone4,1"],
        "Iphone 5" : ["iPhone5,1", "iPhone5,2"],
        "Iphone 5C" : ["iPhone5,3", "iPhone5,4"],
        "Iphone 5S" : ["iPhone6,1", "iPhone6,2"],
        "Iphone 6" : ["iPhone7,2"],
        "Iphone 6 Plus" : ["iPhone7,1"],
        "Iphone 6S" : ["iPhone8,1"],
        "Iphone 6S Plus" : ["iPhone8,2"],
        "Iphone SE" : ["iPhone8,4"],
        "Iphone 7" : ["iPhone9,1", "iPhone9,3"],
        "Iphone 7 Plus" : ["iPhone9,2", "iPhone9,4"],
        "Iphone 8" : ["iPhone10,1", "iPhone10,4"],
        "Iphone 8 Plus" : ["iPhone10,2", "iPhone10,5"],
        "Iphone X" : ["iPhone10,3", "iPhone10,6"],
        "Iphone XS" : ["iPhone11,2"],
        "Iphone XS Max" : ["iPhone11,4", "iPhone11,6"],
        "Iphone XR" : ["iPhone11,8"],
        "Iphone 11" : ["iPhone12,1"],
        "Iphone 11 Pro" : ["iPhone12,3"],
        "Iphone 11 Pro Max" : ["iPhone12,5"],
        "Iphone SE 2" : ["iPhone12,8"],
        "Iphone 12 Mini" : ["iPhone13,1"],
        "Iphone 12" : ["iPhone13,2"],
        "Iphone 12 Pro" : ["iPhone13,3"],
        "Iphone 12 Pro Max" : ["iPhone13,4"],
        "Iphone 13 Mini" : ["iPhone14,4"],
        "Iphone 13" : ["iPhone14,2", "iPhone14,5"],
        "Iphone 13 Pro" : ["iPhone14,3"],
        "Iphone 13 Pro Max" : ["iPhone14,1"]
    }
    
    for model_name, identifiers in model_names.items():
        if identifier in identifiers:
            return model_name
    return "Unknown"

def interact_menu():
    print('1. Only Jailbreak')
    print('2. Jailbreak + Bypass')
    print('3. Exit')
    print()
    return int(input('Choose an option: '))

def menu(option):
    if option == 1:
        udid = input('Enter device UDID: ')
        get_device_info(udid)
        print()
    elif option == 2:
        udid = input('Enter device UDID: ')
        activation_state = get_activation_state(udid)
        print(f"Activation state: {activation_state}")
        print()
    elif option == 3:
        udid = input('Enter device UDID: ')
        model = get_iphone_model(udid)
        print(f"Model: {model}")
        print()
    elif option == 4:
        udid = input('Enter device UDID: ')
        model = get_iphone_model(udid)
        model_name = identifier_to_model_name(model)
        print(f"Model Name: {model_name}")
        print()
    else:
        print('Invalid option...')
        print()


def main():
    check_libimobile_path()
    
    while True:    
        devices = get_devices()
        if devices:
            print(f"--- {len(devices)} device(s) Founded ---")
            for device in devices:
                for udid, model in device.items():
                    print(f"Model: {model} - UDID: {udid}")
            print("--- --- ---")
        else:
            print("Aucun Iphone branché...")
            return
        print()

        option = interact_menu()
        menu(option)

if __name__ == '__main__':
    main()