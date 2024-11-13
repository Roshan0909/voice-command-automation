import subprocess
import webbrowser

try:
    subprocess.Popen(["whatsapp"])
except FileNotFoundError:
    try:
        webbrowser.open("https://web.whatsapp.com/")
    except:
        print("Unable to open WhatsApp.")