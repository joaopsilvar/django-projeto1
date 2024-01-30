import subprocess
import os
import platform

def set_display_windows_if_execute_wsl():
    # Configurar interface grafica do wsl no windows local
    if platform.system() == 'Linux' and 'WSL' in platform.release():
        resultado = subprocess.run("cat /etc/resolv.conf | grep nameserver | awk '{print $2; exit;}'", shell=True, capture_output=True, text=True)
        display = resultado.stdout.strip() + ":0.0"
        os.environ["DISPLAY"] = display