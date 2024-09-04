import requests

# URL de la API
LT_URL_API = 'http://52.204.72.228:8080'

# Variable global para almacenar el RUT del usuario actual
LT_rut_actual = None

# Funcion para crear un nuevo usuario
def LT_CrearUsuario():
    global LT_rut_actual
    LT_rut = input("Ingrese el RUT para crear el nuevo usuario: ")
    try:
        LT_respuesta = requests.post(f"{LT_URL_API}/usuarios", json={'rut': LT_rut})
        LT_respuesta.raise_for_status()
        print("Usuario creado exitosamente.")
        LT_rut_actual = LT_rut
    except requests.RequestException as e:
        print(f"Error al crear el usuario: {e}")

# Funcion para iniciar sesion
def LT_IniciarSesion():
    global LT_rut_actual
    LT_rut = input("Ingrese su RUT para iniciar sesion: ")
    try:
        # Verificar si el usuario existe (no se realiza en el servidor, así que asumimos que si existe si el RUT es valido)
        LT_respuesta = requests.get(f"{LT_URL_API}/usuarios/{LT_rut}")
        if LT_respuesta.status_code == 200:
            LT_rut_actual = LT_rut
            print("Inicio de sesion exitoso.")
        else:
            print("RUT no encontrado. Por favor, registrese.")
    except requests.RequestException as e:
        print(f"Error al iniciar sesion: {e}")

# Funcion para obtener todas las tareas de un usuario por RUT
def LT_ObtenerTareas():
    global LT_rut_actual
    if LT_rut_actual is None:
        print("No ha iniciado sesion.")
        return

    try:
        LT_respuesta = requests.get(f"{LT_URL_API}/tareas/{LT_rut_actual}")
        LT_respuesta.raise_for_status()
        LT_tareas = LT_respuesta.json()
        print("Tareas pendientes:")
        for tarea in LT_tareas:
            # Asegurarse de que 'id' se maneje correctamente
            print(f"ID: {tarea.get('id')}, Titulo: {tarea.get('titulo')}, Descripcion: {tarea.get('descripcion')}, Completado: {tarea.get('completado')}")
    except requests.RequestException as e:
        print(f"Error al obtener las tareas: {e}")

# Funcion para agregar una nueva tarea a un usuario por RUT
def LT_AgregarTarea():
    global LT_rut_actual
    if LT_rut_actual is None:
        print("No ha iniciado sesion.")
        return

    titulo = input("Ingrese el titulo de la tarea: ")
    descripcion = input("Ingrese la descripcion de la tarea: ")
    try:
        LT_respuesta = requests.post(f"{LT_URL_API}/tareas", json={'rut': LT_rut_actual, 'titulo': titulo, 'descripcion': descripcion})
        LT_respuesta.raise_for_status()
        LT_mensaje = LT_respuesta.json()
        print(LT_mensaje.get('mensaje', 'Tarea agregada exitosamente'))
    except requests.RequestException as e:
        print(f"Error al agregar la tarea: {e}")

# Funcion para actualizar una tarea existente por ID y RUT
def LT_ActualizarTarea():
    global LT_rut_actual
    if LT_rut_actual is None:
        print("No ha iniciado sesion.")
        return

    LT_id = input("Ingrese el ID de la tarea: ")
    LT_titulo = input("Ingrese el nuevo titulo de la tarea (dejar en blanco si no se cambia): ")
    LT_descripcion = input("Ingrese la nueva descripcion de la tarea (dejar en blanco si no se cambia): ")
    LT_completado = input("Ingrese el estado de la tarea (completado/pendiente, dejar en blanco si no se cambia): ")

    data = {}
    if LT_titulo:
        data['titulo'] = LT_titulo
    if LT_descripcion:
        data['descripcion'] = LT_descripcion
    if LT_completado:
        # Convertir completado a booleano
        if LT_completado.lower() in ['completado', 'pendiente']:
            data['completado'] = LT_completado.lower() == 'completado'
        else:
            print("Estado de tarea inválido. Debe ser completado o pediente.")
            return

    try:
        LT_respuesta = requests.put(f"{LT_URL_API}/tareas/{LT_rut_actual}/{LT_id}", json=data)
        LT_respuesta.raise_for_status()
        mensaje = LT_respuesta.json()
        print(mensaje.get('mensaje', 'Tarea actualizada exitosamente'))
    except requests.RequestException as e:
        print(f"Error al actualizar la tarea: {e}")

# Funcion para eliminar una tarea por ID y RUT
def LT_EliminarTarea():
    global LT_rut_actual
    if LT_rut_actual is None:
        print("No ha iniciado sesion.")
        return

    LT_id = input("Ingrese el ID de la tarea a eliminar: ")
    try:
        respuesta = requests.delete(f"{LT_URL_API}/tareas/{LT_rut_actual}/{LT_id}")
        respuesta.raise_for_status()
        mensaje = respuesta.json()
        print(mensaje.get('mensaje', 'Tarea eliminada exitosamente'))
    except requests.RequestException as e:
        print(f"Error al eliminar la tarea: {e}")

# Funcion principal para interactuar con el usuario
def LT_main():
    global LT_rut_actual

    while True:
        if LT_rut_actual is None:
            print("|-----------------------------------|")
            print("|    |Inicio de Sesion/Registro|    |")
            print("|-----------------------------------|")
            print("| [1] Crear Usuario                 |")
            print("| [2] Iniciar Sesion                |")
            print("| [0] Salir                         |")
            print("|-----------------------------------|")

            LT_opcion = input("Seleccione una opcion: ")

            if LT_opcion == '0':
                break
            elif LT_opcion == '1':
                LT_CrearUsuario()
            elif LT_opcion == '2':
                LT_IniciarSesion()
            else:
                print("Ingrese una opcion valida (0, 1, 2)")
        else:
            print("|-----------------------------------|")
            print("|        |Gestion de Tareas|        |")
            print("|-----------------------------------|")
            print("| [1] Obtener todas las tareas      |")
            print("| [2] Agregar tarea a la lista      |")
            print("| [3] Actualizar tarea              |")
            print("| [4] Eliminar tarea                |")
            print("| [5] Cerrar sesion                 |")
            print("|-----------------------------------|")

            LT_opcion = input("Seleccione una opcion: ")

            if LT_opcion == '5':
                LT_rut_actual = None
                print("Sesion cerrada")
            elif LT_opcion == '1':
                LT_ObtenerTareas()
            elif LT_opcion == '2':
                LT_AgregarTarea()
            elif LT_opcion == '3':
                LT_ActualizarTarea()
            elif LT_opcion == '4':
                LT_EliminarTarea()
            else:
                print("Ingrese una opcion valida (1, 2, 3, 4, 5)")

if __name__ == '__main__':
    LT_main()
