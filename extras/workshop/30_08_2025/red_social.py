# RED SOCIAL MINI 👥
# Proyecto: Simulador de red social con estructuras de datos
# Duración: 2 horas con rotación de equipos cada 15 minutos

class RedSocial:
    """
    Clase principal que gestiona toda la red social
    """
    def __init__(self):
        # Diccionario principal: ID usuario -> datos del usuario
        self.usuarios = {}
        self.siguiente_id = 1
    
    # ========== GESTIÓN DE USUARIOS ==========
    def crear_usuario(self, nombre, edad):
        """
        Crea un nuevo usuario con estructura de diccionario
        Retorna: ID del usuario creado
        """
        usuario_id = self.siguiente_id
        self.usuarios[usuario_id] = {
            'id': usuario_id,
            'nombre': nombre,
            'edad': edad,
            'amigos': set(),  # Set para evitar duplicados y operaciones rápidas
            'publicaciones': [],  # Lista que funcionará como pila (LIFO)
        }
        self.siguiente_id += 1
        print(f"✅ Usuario '{nombre}' creado con ID: {usuario_id}")
        return usuario_id
    
    # ========== GESTIÓN DE AMISTADES ==========
    def agregar_amistad(self, id_usuario1, id_usuario2):
        """
        Agrega una amistad bidireccional entre dos usuarios
        """
        if id_usuario1 in self.usuarios:
            self.usuarios[id_usuario1]["amigos"].add(id_usuario2)
            return True
        return False
        #if id_usuario1 in self.usuarios and id_usuario2 in self.usuarios:
        #    self.usuarios[id_usuario1]["amigos"].add(id_usuario2)
        #    return self.usuarios[id_usuario1]["amigos"]

    
    def eliminar_amistad(self, id_usuario1, id_usuario2):
        """
        Elimina la amistad entre dos usuarios
        """
        if id_usuario1 in self.usuarios:
            return self.usuarios[id_usuario1]["amigos"].discard(id_usuario2)
    
    # ========== GESTIÓN DE PUBLICACIONES ==========
    def crear_publicacion(self, id_usuario, contenido):
        """
        Crea una publicación para un usuario
        Las publicaciones se guardan como pila (última primero)
        """
        if id_usuario in self.usuarios:
            publicacion = {
                'contenido': contenido,
                'likes': set(),  # Set de IDs de usuarios que dieron like
                'timestamp': None  # TODO: Agregar timestamp si es necesario
            }
            # TODO: Implementar agregar a la pila
            self.usuarios[id_usuario]["publicaciones"].append(publicacion)
    
    def dar_like(self, id_usuario, id_publicacion_owner, indice_publicacion):
        """
        Un usuario da like a una publicación específica
        """
        # TODO: Implementar
        self.usuarios[id_publicacion_owner]["publicaciones"][indice_publicacion]["likes"].add(id_usuario)
    
    # ========== BÚSQUEDAS Y CONSULTAS ==========
    def amigos_en_comun(self, id_usuario1, id_usuario2):
        """
        Encuentra amigos en común entre dos usuarios usando operaciones de sets
        """
        if id_usuario1 in self.usuarios and id_usuario2 in self.usuarios:
            # TODO: Usar intersección de sets
            pass
    
    def mostrar_usuario(self, id_usuario):
        """
        Muestra información completa de un usuario
        """
        if id_usuario in self.usuarios:
            usuario = self.usuarios[id_usuario]
            print(f"\n👤 Usuario: {usuario['nombre']} (ID: {usuario['id']})")
            print(f"   Edad: {usuario['edad']}")
            print(f"   Amigos: {len(usuario['amigos'])}")
            print(f"   Publicaciones: {len(usuario['publicaciones'])}")
            print(f"  Likes: {len(usuario['Li'])}")
    
    # ========== BONUS: CÍRCULOS SOCIALES ==========
    def detectar_circulos_sociales(self, id_usuario):
        """
        BONUS GOD: Detecta círculos sociales (ciclos en el grafo)
        """
        # TODO: Implementar búsqueda de ciclos
        pass


# ========== PROGRAMA PRINCIPAL ==========
def main():
    print("=" * 50)
    print("🌐 RED SOCIAL MINI - INICIANDO")
    print("=" * 50)
    
    # Crear instancia de la red social
    red = RedSocial()
    
    # Datos de prueba para verificar que funciona
    print("\n📝 Creando usuarios de prueba...")
    user1 = red.crear_usuario("Alice", 25)
    user2 = red.crear_usuario("Bob", 30)
    user3 = red.crear_usuario("Carlos", 22)
    
    # Agregar amigos.
    print("\nAmigos")
    if red.agregar_amistad(user1,user2):
        print("Se agrego un nuevo amigo.")
    else:
        print("No se pudo agregar nuevo usuario.")
    
    # Agregar amigos.
    print("\nAmigos")
    if red.agregar_amistad(user1,user3):
        print("Se agrego un nuevo amigo.")
    else:
        print("No se pudo agregar nuevo usuario.")

    # Eliminar amigo
    print(red.eliminar_amistad(user1, user2))

    # Crear publicacion
    red.crear_publicacion(user1, "Hello World")
    red.crear_publicacion(user1, "ABC")
    red.crear_publicacion(user2, "XD")

    # Dar likes
    red.dar_like(user2, user1, 0)
    red.dar_like(user3, user1, 0)
    red.dar_like(user1, user2, 0)

    # Mostrar usuarios creados
    red.mostrar_usuario(user1)
    red.mostrar_usuario(user2)
    red.mostrar_usuario(user3)
    
    # TODO: Menú interactivo
    print("\n⚠️  SIGUIENTE EQUIPO:")
    print("1. Completar función agregar_amistad()")
    print("2. Completar función crear_publicacion()")
    print("3. Implementar menú interactivo")
    print("4. Agregar más funcionalidades")


if __name__ == "__main__":
    main()