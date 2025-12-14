#!/usr/bin/env python3

import psutil
import socket
import os
import time
import distro
import subprocess

def get_system_info():
    # ---------------------------------INFO SYSTEM------------------------------------------
    system_name = socket.gethostname()                  # Nom de la machine
    os_name = distro.name()                             # Récupère le nom de la distribution
    os_version = distro.version()                       # Récupère la version de la distribution

    uptime_seconds = time.time() - psutil.boot_time()                       # Temps depuis le démarrage
    uptime = time.strftime("%H:%M:%S", time.gmtime(uptime_seconds))         # Format de l'uptime
    
    # Utilisation de `who` pour détecter les utilisateurs connectés
    try:
        # Utilise 'who' pour obtenir les utilisateurs connectés
        users_output = subprocess.check_output("who", shell=True, universal_newlines=True)
        user_list = users_output.strip().split("\n")                                            # Découpe les résultats ligne par ligne
        user_count = len(user_list)                                                             # Compte le nombre d'utilisateurs
    except subprocess.CalledProcessError:
        user_count = 0                              # Si 'who' échoue, aucun utilisateur n'est détecté

    ip_address = socket.gethostbyname(system_name)  # Adresse IP principale

    # -----------------------------------INFO CPU-------------------------------------------
    cpu_cores = psutil.cpu_count(logical=False)                         # Nombre de coeurs
    cpu_frequency = round(psutil.cpu_freq().current / 1000, 2)          # Fréquence 
    cpu_usage = round(psutil.cpu_percent(interval=1), 2)                # Pourcentage d'utilisation

    # --------------------------------- INFO MEMOIRE-------------------------------------------
    memory = psutil.virtual_memory()
    total_ram = round(memory.total / (1024 ** 3), 2)  # RAM totale
    used_ram = round(memory.used / (1024 ** 3), 2)    # RAM utilisé
    ram_usage = round(memory.percent, 2)              # Pourcentage de RAM utilisé

    # Récupérer les 3 processus les plus gourmands
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    # Trier les processus par utilisation
    processes_cpu = sorted(processes, key=lambda p: p['cpu_percent'], reverse=True)[:3]
    processes_memory = sorted(processes, key=lambda p: p['memory_percent'], reverse=True)[:3]

    # Stocker les informations des 3 processus
    top_processes_cpu = [f"{p['name']} (PID {p['pid']}): {round(p['cpu_percent'], 2)}% CPU" for p in processes_cpu]
    top_processes_memory = [f"{p['name']} (PID {p['pid']}): {round(p['memory_percent'], 2)}% RAM" for p in processes_memory]

    # Analyse des fichiers
    folder_path = "/home/monkey"
    extensions = ['.txt','.py','.pdf','.jpg','.html','.css']
    file_counts = {ext: 0 for ext in extensions}

    for root, _, files in os.walk(folder_path):
        for file in files:
            for ext in extensions:
                if file.endswith(ext):
                    file_counts[ext] += 1

    # Calcul des pourcentages
    total_files = sum(file_counts.values())
    file_percentages = {ext: (count / total_files) * 100 if total_files > 0 else 0 for ext, count in file_counts.items()}

    
    
    # Rassembler toute les information dans un dictionnaire
    return {
        'system_name': system_name,
        'os_name': os_name,
        'os_version': os_version,
        'uptime': uptime,
        'user_count': user_count,
        'ip_address': ip_address,
        'cpu_cores': cpu_cores,
        'cpu_frequency': cpu_frequency,
        'cpu_usage': cpu_usage,
        'total_ram': total_ram,
        'used_ram': used_ram,
        'ram_usage': ram_usage,
        'txt_count': file_counts['.txt'],
        'py_count': file_counts['.py'],
        'pdf_count': file_counts['.pdf'],
        'jpg_count': file_counts['.jpg'],
        'html_count': file_counts['.html'],
        'css_count': file_counts['.css'],
        'txt_percentage': round(file_percentages['.txt'], 2),
        'py_percentage': round(file_percentages['.py'], 2),
        'pdf_percentage': round(file_percentages['.pdf'], 2),
        'jpg_percentage': round(file_percentages['.jpg'], 2),
        'html_percentage': round(file_percentages['.html'], 2),
        'css_percentage': round(file_percentages['.css'], 2),
        'top_process_1': top_processes_cpu[0] if top_processes_cpu else "N/A",
        'top_process_2': top_processes_cpu[1] if len(top_processes_cpu) > 1 else "N/A",
        'top_process_3': top_processes_cpu[2] if len(top_processes_cpu) > 2 else "N/A",
        'top_process_memory_1': top_processes_memory[0] if top_processes_memory else "N/A",
        'top_process_memory_2': top_processes_memory[1] if len(top_processes_memory) > 1 else "N/A",
        'top_process_memory_3': top_processes_memory[2] if len(top_processes_memory) > 2 else "N/A",
        'current_time': time.strftime("%Y-%m-%d %H:%M:%S")
    }

def print_system_info(info):
    # Vérif de l'affichage des données
    print(f"Système : {info['system_name']}")
    print(f"OS : {info['os_name']} {info['os_version']}")
    print(f"Uptime : {info['uptime']}")
    print(f"Utilisateurs connectés : {info['user_count']}")
    print(f"Adresse IP : {info['ip_address']}")
    print(f"CPU : {info['cpu_cores']} cœurs, {info['cpu_frequency']} GHz, {info['cpu_usage']}% utilisation")
    print(f"RAM : {info['used_ram']} Go sur {info['total_ram']} Go, {info['ram_usage']}% utilisée")
    print(f"Fichiers .txt : {info['txt_count']} ({info['txt_percentage']}%)")
    print(f"Fichiers .py : {info['py_count']} ({info['py_percentage']}%)")
    print(f"Fichiers .pdf : {info['pdf_count']} ({info['pdf_percentage']}%)")
    print(f"Fichiers .jpg : {info['jpg_count']} ({info['jpg_percentage']}%)")
    print(f"Heure de génération : {info['current_time']}")
    print(f"Top 3 des processus CPU :")
    print(f"  - {info['top_process_1']}")
    print(f"  - {info['top_process_2']}")
    print(f"  - {info['top_process_3']}")
    print(f"Top 3 des processus RAM :")
    print(f"  - {info['top_process_memory_1']}")
    print(f"  - {info['top_process_memory_2']}")
    print(f"  - {info['top_process_memory_3']}")

#---------------------------------MAIN------------------------------------------
if __name__ == "__main__":
    system_info = get_system_info()
    print_system_info(system_info)

#-----------------------------GENERER LA PAGE HTML------------------------------

from jinja2 import Template

# Charger le fichier template.html
with open("template.html", "r") as f:
    template_content = f.read()

# Remplir les variables dans template.html
template = Template(template_content)
output_html = template.render(system_info)

# Sauvegarder le fichier HTML générer
with open("output.html", "w") as f:
    f.write(output_html)

print("Le fichier HTML a été générer avec succès.")
