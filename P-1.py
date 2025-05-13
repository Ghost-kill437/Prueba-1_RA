import os
import re

# Lista de campus inicial
campus = ["🌐 zona core", "🏫 campus uno", "🏢 campus matriz", "💼 sector outsourcing"]

# --- FUNCIONES DE VALIDACIÓN ---
def validar_ip(ip):
    """Valida una dirección IPv4"""
    patron = r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    return bool(re.match(patron, ip))

def validar_vlan(vlan):
    """Valida que el formato de VLAN sea correcto (1-4095)"""
    return vlan.isdigit() and 1 <= int(vlan) <= 4095

def validar_nombre_dispositivo(nombre):
    """Valida que el nombre solo contenga caracteres permitidos"""
    return bool(re.match(r"^[a-zA-Z0-9\-_]+$", nombre))

def hacer_backup(archivo):
    """Crea una copia de seguridad básica"""
    if os.path.exists(archivo):
        with open(archivo, 'r') as original:
            data = original.read()
        with open(archivo + '.bak', 'w') as backup:
            backup.write(data)
        print("🔁 Backup creado exitosamente")

# --- FUNCIONES PRINCIPALES ---
def mostrar_campus():
    """Muestra la lista de campus"""
    print("\n🏛️ === LISTA DE CAMPUS ===")
    for i, c in enumerate(campus, 1):
        print(f"{i}. {c.capitalize()}")

def agregar_dispositivo():
    mostrar_campus()
    try:
        opcion = int(input("\n🔘 Seleccione campus para agregar dispositivo: ")) - 1
        nombre_archivo = campus[opcion].replace(" ", "_") + ".txt"
    except (IndexError, ValueError):
        print("\n❌⚠️ Selección inválida.")
        return

    # 1. Tipo de dispositivo
    print("\n🖥️ === TIPOS DE DISPOSITIVO ===")
    tipos = {
        "1": "📶 Router",
        "2": "🔀 Switch",
        "3": "🔷 Switch Multicapa",
        "4": "💻 PC",
        "5": "📡 Access Point",
        "6": "🖨️ Impresora",
        "7": "☁️ Servidor Cloud"
    }
    for k, v in tipos.items():
        print(f"{k}. {v}")
    
    tipo = input("\n⌨️ Seleccione el tipo de dispositivo: ")
    while tipo not in tipos:
        print("❌ Opción inválida")
        tipo = input("⌨️ Seleccione el tipo de dispositivo: ")

    # 2. Nombre del dispositivo
    nombre = input("\n🏷️ Nombre del dispositivo: ").strip()
    while not validar_nombre_dispositivo(nombre):
        print("❌ Nombre inválido. Solo use letras, números, guiones (-) y guiones bajos (_)")
        nombre = input("🏷️ Nombre del dispositivo: ").strip()

    # 3. Dirección IP (solo para dispositivos de red)
    ip = ""
    if tipo in ["1", "2", "3", "5"]:
        ip = input("\n🌍 Dirección IP del dispositivo: ").strip()
        while not validar_ip(ip):
            print("❌ IP inválida. Ejemplo válido: 192.168.1.1")
            ip = input("🌍 Ingrese una IP válida: ").strip()

    # 4. Configuración de VLANs (solo para switches)
    vlans = []
    if tipo in ["2", "3"]:
        print("\n🏷️ === CONFIGURACIÓN DE VLANS ===")
        print("ℹ️ Ingrese '0' para terminar")
        print("ℹ️ Las VLANs válidas son números entre 1 y 4095")
        while True:
            vlan = input("🔢 Ingrese VLAN: ").strip()
            if vlan == "0":
                break
            if validar_vlan(vlan):
                vlans.append(vlan)
            else:
                print("❌ VLAN inválida. Debe ser entre 1 y 4095")

    # 5. Capa jerárquica (solo para dispositivos de red)
    capa = "N/A"
    if tipo in ["1", "2", "3", "5"]:
        print("\n📊 === CAPA JERÁRQUICA ===")
        capas = {
            "1": "💎 Núcleo (Core)",
            "2": "🔗 Distribución",
            "3": "🖥️ Acceso",
            "4": "🌐 Edge"
        }
        for k, v in capas.items():
            print(f"{k}. {v}")
        capa_sel = input("\n🔘 Seleccione la capa: ")
        while capa_sel not in capas:
            print("❌ Opción inválida")
            capa_sel = input("🔘 Seleccione la capa: ")
        capa = capas[capa_sel]

    # 6. Servicios de red (solo para dispositivos de red)
    servicios = []
    if tipo in ["1", "2", "3", "5"]:
        print("\n🛠️ === SERVICIOS DE RED ===")
        servicios_opciones = {
            "1": "🔄 DHCP",
            "2": "🔍 DNS",
            "3": "🔄 NAT",
            "4": "🔒 VPN",
            "5": "⚖️ QoS",
            "6": "📞 VoIP"
        }
        
        print("🔘 Seleccione servicios (ingrese números separados por comas):")
        for k, v in servicios_opciones.items():
            print(f"{k}. {v}")
        
        seleccion = input("\n⌨️ Ingrese los números de servicios (ej: 1,3,5): ").split(",")
        for s in seleccion:
            if s.strip() in servicios_opciones:
                servicios.append(servicios_opciones[s.strip()])

    # Guardar información
    hacer_backup(nombre_archivo)
    with open(nombre_archivo, "a") as f:
        f.write("\n" + "="*50 + "\n")
        f.write(f"🔧 TIPO: {tipos[tipo]}\n")
        f.write(f"🏷️ NOMBRE: {nombre}\n")
        if ip: f.write(f"🌍 IP: {ip}\n")
        if capa != "N/A": f.write(f"📊 CAPA: {capa}\n")
        if vlans: f.write(f"🏷️ VLANS: {', '.join(vlans)}\n")
        if servicios: f.write(f"🛠️ SERVICIOS: {', '.join(servicios)}\n")
        f.write("="*50 + "\n")
    
    print("\n🎉✅ Dispositivo agregado correctamente!")
    print(f"📋📝 Resumen: {tipos[tipo]} {nombre}" + (f" ({ip})" if ip else ""))

def eliminar_dispositivo():
    mostrar_campus()
    try:
        opcion = int(input("\n🗑️ Seleccione campus para eliminar dispositivo: ")) - 1
        nombre_archivo = campus[opcion].replace(" ", "_") + ".txt"
        
        if not os.path.exists(nombre_archivo):
            print("\n📭❌ No hay dispositivos registrados en este campus.")
            return
            
        with open(nombre_archivo, "r") as f:
            contenido = f.read()
            dispositivos = contenido.split("\n" + "="*50 + "\n")
            
        if len(dispositivos) <= 1:
            print("\n📭❌ No hay dispositivos para eliminar.")
            return
            
        print("\n📋 Dispositivos disponibles:")
        for i, disp in enumerate(dispositivos[1:], 1):
            if disp.strip():
                print(f"\n🔢 Opción {i}:")
                print(disp.strip())
            
        try:
            opcion_disp = int(input("\n🔢 Seleccione el número de dispositivo a eliminar: "))
            if 1 <= opcion_disp < len(dispositivos):
                confirmar = input("\n⚠️ ¿Está seguro de eliminar este dispositivo? (s/n): ").lower()
                if confirmar == "s":
                    nuevos_dispositivos = dispositivos[:opcion_disp] + dispositivos[opcion_disp+1:]
                    hacer_backup(nombre_archivo)
                    with open(nombre_archivo, "w") as f:
                        f.write(("\n" + "="*50 + "\n").join(filter(None, nuevos_dispositivos)))
                    print("\n🗑️✅ Dispositivo eliminado correctamente!")
                else:
                    print("\n❌ Eliminación cancelada")
            else:
                print("\n❌ Opción inválida")
        except ValueError:
            print("\n❌ Debe ingresar un número válido")
            
    except (IndexError, ValueError):
        print("\n❌⚠️ Selección de campus inválida.")

def ver_dispositivos():
    mostrar_campus()
    try:
        opcion = int(input("\n👀 Seleccione un campus para ver sus dispositivos: ")) - 1
        nombre_archivo = campus[opcion].replace(" ", "_") + ".txt"
        if os.path.exists(nombre_archivo):
            print(f"\n📋📊 === DISPOSITIVOS EN {campus[opcion].upper()} ===")
            with open(nombre_archivo, "r") as f:
                print(f.read())
        else:
            print("\n📭❌ No hay dispositivos registrados en este campus.")
    except (IndexError, ValueError):
        print("\n⚠️❌ Opción inválida.")

def menu():
    """Menú principal"""
    while True:
        print("\n" + "="*50)
        print("🖥️🌐 ADMINISTRADOR DE DISPOSITIVOS DE RED")
        print("="*50)
        print("1. 👁️ Ver dispositivos")
        print("2. ➕ Añadir dispositivo")
        print("3. 🗑️ Eliminar dispositivo")
        print("4. 🚪 Salir")
        
        opcion = input("\n🔘 Seleccione una opción: ")

        if opcion == "1":
            ver_dispositivos()
        elif opcion == "2":
            agregar_dispositivo()
        elif opcion == "3":
            eliminar_dispositivo()
        elif opcion == "4":
            print("\n👋¡Hasta pronto! ¡Vuelve pronto!👋")
            break
        else:
            print("\n❌⚠️ Opción inválida. Intente nuevamente.")

if __name__ == "__main__":
    menu()
