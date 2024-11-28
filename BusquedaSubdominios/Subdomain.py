import requests
from os import path
import argparse
import sys
import time

# Configuración de argumentos
parser = argparse.ArgumentParser(description="Buscador de subdominios activos.")
parser.add_argument('-t', '--target', help='Indica el dominio de la víctima', required=True)
parser.add_argument('-w', '--wordlist', help='Ruta al archivo de wordlist', default='subdominio-10000.txt')
parser.add_argument('-o', '--output', help='Archivo para guardar resultados', default='resultados.txt')
args = parser.parse_args()

# Cabeceras HTTP para evitar bloqueos
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Función para verificar subdominios
def verificar_subdominio(subdominio, target, encontrados):
    base_url = f"{subdominio}.{target}"  # Subdominio base sin protocolo
    if base_url in encontrados:
        return None
    
    resultados = []
    for protocolo in ['http://', 'https://']:
        url = f"{protocolo}{subdominio}.{target}"
        try:
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code < 400:
                print(f"[+] Subdominio encontrado: {url} (HTTP {response.status_code})")
                resultados.append(f"{url} (HTTP {response.status_code})")
        except requests.ConnectionError:
            pass
        except requests.exceptions.Timeout:
            print(f"[-] Timeout al intentar acceder: {url}")
    return resultados

def main():
    # Verificar existencia de la wordlist
    if not path.exists(args.wordlist):
        print(f"[-] Wordlist no encontrada: {args.wordlist}")
        sys.exit()

    # Cargar subdominios desde la wordlist
    with open(args.wordlist, 'r') as file:
        wordlist = file.read().splitlines()

    # Evitar duplicados
    wordlist = set(wordlist)
    
    # Almacenar subdominios únicos encontrados
    encontrados = set()

    # Verificar subdominios
    resultados = []
    print(f"[+] Iniciando búsqueda en el dominio: {args.target} \n")
    for subdominio in wordlist:
        resultado = verificar_subdominio(subdominio, args.target, encontrados)
        if resultado:
            resultados.extend(resultado)
            time.sleep(1)

    # Guardar resultados
    if resultados:
        with open(args.output, 'w') as output_file:
            output_file.write("\n".join(resultados))
        print(f"[+] Resultados guardados en: {args.output}")
    else:
        print("[-] No se encontraron subdominios activos.")

if __name__ == "__main__":
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n[-] Ejecución interrumpida por el usuario.")
        sys.exit()
