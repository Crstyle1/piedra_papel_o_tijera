#  Piedra, Papel o Tijera

**Autor:** Cristian Suárez  
**Fecha:** 27 de Febrero 2026   

---

## 📌 Descripción

Este es un juego clásico de **Piedra, Papel o Tijera** desarrollado en Python con una interfaz gráfica moderna utilizando `tkinter`. Permite a un usuario jugar contra la CPU, con un sistema de puntuación acumulada, ventanas emergentes informativas y un diseño visual atractivo.

El código sigue una arquitectura limpia por capas (lógica, controlador y presentación), lo que facilita su mantenimiento y escalabilidad.

---

## ✨ Funcionalidades

- **Interfaz gráfica intuitiva** con colores oscuros y tipografía clara.
- **Jugabilidad fluida**: elige tu movimiento con botones (Piedra ✊, Papel ✋, Tijera ✌️).
- **Generación aleatoria justa** para la jugada de la CPU.
- **Puntuación visible** de rondas ganadas por el jugador y la CPU.
- **Ventanas emergentes (popups)** profesionales:
  - **Bienvenida**: al iniciar, permite comenzar una nueva ronda o salir.
  - **Resultado**: tras cada ronda, muestra quién ganó y ofrece jugar de nuevo o salir.
- **Reinicio de puntuación** en cualquier momento con un botón.
- **Ventana principal centrada** en la pantalla para una mejor experiencia.
- **Código estructurado** en capas: Core (lógica), Controlador y UI.

---

## 🚀 Cómo jugar

1. Ejecuta el programa.
2. En la ventana de bienvenida, haz clic en **"Nueva ronda"**.
3. En la pantalla principal, elige tu movimiento:
   - **Piedra ✊**
   - **Papel ✋**
   - **Tijera ✌️**
4. La CPU generará su jugada automáticamente.
5. El resultado se mostrará en pantalla y en un popup.
6. Decide si quieres jugar otra ronda o salir.
7. Puedes reiniciar el contador de puntuación con el botón **"Reiniciar puntuación"**.

---

## 🧱 Estructura del Código: Arquitectura en Capas

El proyecto está diseñado siguiendo una **arquitectura limpia y modular**, separando claramente la lógica del negocio, la coordinación del juego y la interfaz gráfica. Esto facilita el mantenimiento, las pruebas y la escalabilidad. A continuación, se describe cada capa y sus componentes:

---

### 1. Capa de Lógica (Core)

Esta capa contiene las reglas fundamentales del juego y los servicios independientes de la interfaz. No tiene conocimiento de la existencia de la GUI.

#### `Move` (Enum)
- Representa las tres jugadas posibles: `ROCK`, `PAPER`, `SCISSORS`.
- Cada miembro del enum tiene una propiedad `symbol` que devuelve el emoji correspondiente (✊, ✋, ✌️). Esto permite mostrar los íconos de forma coherente en toda la interfaz.

#### `RulesEngine`
- Clase estática que encapsula la lógica para determinar el ganador de una ronda.
- Método `determine_winner(player: Move, cpu: Move) -> str`: compara las dos jugadas y retorna `"Jugador"`, `"CPU"` o `"Empate"` según las reglas clásicas del juego.
- Utiliza un diccionario de combinaciones ganadoras para hacer la comparación de manera eficiente y legible.

#### `RNGService`
- Servicio encargado de generar la jugada aleatoria de la CPU.
- Método `get_random_choice() -> Move`: utiliza `random.choice` sobre la lista de valores del enum `Move`, garantizando una distribución uniforme (33.3% de probabilidad para cada opción).

---

### 2. Capa de Control (Controlador)

Actúa como puente entre la lógica y la interfaz. Gestiona el estado de la partida y coordina las acciones.

#### `GameController`
- Mantiene el estado de la puntuación (`player_score`, `cpu_score`) y los últimos movimientos realizados (opcional).
- Método `play_round(player_choice: Move)`: 
  1. Obtiene la jugada de la CPU mediante `RNGService`.
  2. Determina el resultado usando `RulesEngine`.
  3. Actualiza las puntuaciones según el resultado.
  4. Retorna una tupla con el resultado y las jugadas.
- Método `reset_scores()`: reinicia los contadores de puntuación a cero.

Este controlador no sabe nada de la interfaz gráfica; simplemente procesa datos y devuelve resultados. Esto permite que la lógica del juego sea probada de forma independiente.

---

### 3. Capa de Presentación (Interfaz Gráfica)

Construida con `tkinter`, se encarga de mostrar la información al usuario y capturar sus interacciones. Está dividida en la ventana principal y popups modales.

#### `RockPaperScissorsGUI`
- Clase principal que crea la ventana del juego.
- **Métodos clave:**
  - `__init__`: configura la ventana, la centra, crea los widgets y muestra el popup de bienvenida.
  - `_create_widgets()`: construye todos los elementos visuales: títulos, etiquetas de jugadas, botones de movimiento, marcador de puntuación y botones de control.
  - `disable_move_buttons()` / `enable_move_buttons()`: controlan el estado de los botones de movimiento para evitar jugadas mientras se muestra un popup.
  - `_on_move_selected(player_move)`: se ejecuta al hacer clic en un botón; llama al controlador, actualiza la interfaz y muestra el popup de resultado.
  - `_update_ui()`: actualiza las etiquetas de jugadas, resultado y puntuación.
  - `_reset_scores()`: reinicia las puntuaciones y limpia la pantalla.

#### Popups personalizados
- **`BasePopup`**: clase base para todas las ventanas emergentes.
  - Hereda de `tk.Toplevel` y se configura como modal (`grab_set`).
  - Proporciona un diseño consistente: fondo oscuro, mensaje centrado y botones con el mismo estilo.
  - Método `center_window()` para centrar el popup en la pantalla.
- **`WelcomePopup`**: hereda de `BasePopup`.
  - Muestra un mensaje de bienvenida y dos botones: "Nueva ronda" y "Salir".
- **`ResultPopup`**: hereda de `BasePopup`.
  - Muestra el resultado de la ronda (con emoji y color según ganador) y la puntuación actual.
  - Ofrece las opciones "Nueva ronda" y "Salir".
  - El color del mensaje cambia dinámicamente (verde si gana el jugador, rojo si gana la CPU, amarillo en empate).

 
### ✅ Ventajas de esta estructura

- **Separación de responsabilidades**: cada capa tiene una función clara y bien definida.
- **Facilidad de prueba**: la lógica del juego puede ser probada sin necesidad de la interfaz gráfica.
- **Mantenibilidad**: los cambios en la interfaz no afectan la lógica y viceversa.
- **Escalabilidad**: es sencillo agregar nuevas funcionalidades (como sonidos, animaciones o multijugador) sin reescribir el núcleo.
- **Reutilización**: los servicios (`RNGService`, `RulesEngine`) podrían ser utilizados en otros proyectos (por ejemplo, una versión web o de consola).

Esta arquitectura sigue principios de diseño de software como la **inyección de dependencias** (aunque aquí es sencilla) y el **patrón de controlador**, lo que la hace profesional y robusta.
---

## 🛠️ Tecnologías utilizadas

El proyecto ha sido desarrollado íntegramente en **Python 3**, aprovechando su versatilidad y la amplia disponibilidad de bibliotecas estándar. A continuación, se detallan las tecnologías y módulos específicos empleados:

### 🐍 Python 3.x
- **Lenguaje base**: Python 3 es el núcleo del proyecto. Se ha utilizado la sintaxis moderna de Python (type hints, f-strings, enumeraciones) para garantizar un código claro, mantenible y con alto rendimiento.
- **Versión recomendada**: Python 3.8 o superior (aunque el código es compatible con versiones anteriores hasta 3.6, se recomienda la última estable para disfrutar de todas las mejoras).

### 🖼️ Tkinter (Interfaz Gráfica de Usuario)
- **Librería estándar**: Tkinter es la biblioteca gráfica oficial de Python, incluida por defecto en la mayoría de las distribuciones. No requiere instalación adicional, lo que facilita la ejecución del programa en cualquier sistema con Python.
- **Ventajas**:
  - **Multiplataforma**: Funciona en Windows, macOS y Linux sin cambios en el código.
  - **Ligereza**: Consume pocos recursos y es ideal para aplicaciones de escritorio simples como este juego.
  - **Personalización**: Permite un control detallado sobre la apariencia (colores, fuentes, estilos) mediante opciones como `bg`, `fg`, `font`, `relief`, etc.
- **Componentes Tkinter utilizados**:
  - `tk.Tk`: Ventana principal de la aplicación.
  - `tk.Toplevel`: Ventanas emergentes modales (popups).
  - `tk.Frame`: Organización en contenedores para una disposición ordenada.
  - `tk.Label`: Etiquetas para títulos, resultados y puntuaciones.
  - `tk.Button`: Botones interactivos con comandos asociados.
  - `tk.Button.config`: Modificación dinámica de propiedades (habilitar/deshabilitar, cambiar texto).
  - `grab_set()`: Para hacer los popups modales y evitar interacción con la ventana principal.
  - `update_idletasks()`: Actualización forzada del layout para centrar ventanas correctamente.

### 🔢 Módulo `enum` (Enumeraciones)
- **Propósito**: Definir un conjunto fijo de constantes con nombre para las jugadas (`Move`).
- **Ventajas**:
  - **Legibilidad**: El código utiliza `Move.ROCK` en lugar de cadenas mágicas como `"Piedra"`.
  - **Seguridad**: Evita errores tipográficos y facilita el autocompletado en editores.
  - **Extensibilidad**: Añadir nuevas jugadas (por ejemplo, "Lagarto" o "Spock") es trivial.
- **Uso concreto**: La clase `Move(Enum)` asigna a cada opción un valor (`"Piedra"`, `"Papel"`, `"Tijera"`) y una propiedad `symbol` que retorna el emoji correspondiente.

### 🎲 Módulo `random` (Generación Aleatoria)
- **Propósito**: Proporcionar aleatoriedad para la jugada de la CPU.
- **Método empleado**: `random.choice(list(Move))` selecciona uniformemente un elemento del enumerado `Move`.
- **Distribución**: Se garantiza que cada jugada tenga exactamente 1/3 de probabilidad, cumpliendo con el requisito de equidad del juego.
- **Nota**: No se requiere `random.seed()` en producción, pero podría usarse para pruebas con resultados predecibles.

### 📦 Módulos estándar adicionales
- **`tkinter.messagebox`**: Aunque no se usa directamente en el código final (se reemplazó por popups personalizados), se importa inicialmente para posibles mensajes de error o depuración.
- **`__name__ == "__main__"`**: Estructura típica de Python que permite ejecutar el archivo como script principal o importarlo como módulo sin ejecutar la GUI automáticamente.

---

## 🔧 Herramientas de desarrollo (no incluidas en el código, pero utilizadas)

- **Editor de código**: Cualquier editor moderno (VS Code, PyCharm, Sublime Text) con soporte para Python.
- **Control de versiones**: Git para el seguimiento de cambios y GitHub para alojar el repositorio.
- **Documentación**: Markdown para redactar este README.

---

## 📈 Justificación de la elección tecnológica

- **Python** se eligió por su simplicidad, curva de aprendizaje suave y amplia comunidad, lo que lo hace ideal para proyectos educativos y de demostración de conceptos de arquitectura de software.
- **Tkinter** se adoptó por ser nativo de Python, evitando dependencias externas que complicarían la ejecución del programa por parte de los usuarios. A pesar de su apariencia algo "clásica", permite un diseño moderno mediante la personalización de colores, fuentes y estilos.
- **Enum** mejora la robustez del código frente al uso de cadenas o números enteros, alineándose con buenas prácticas de desarrollo.
- **Random** es suficiente para el propósito del juego; no se requiere criptografía ni alta entropía.

Esta combinación de tecnologías garantiza un equilibrio entre simplicidad, funcionalidad y buenas prácticas de programación.

## ▶️ Cómo ejecutar

1. Asegúrate de tener Python 3 instalado.
2. Descarga o clona este repositorio.
3. Abre una terminal en la carpeta del proyecto.
4. Ejecuta:

```bash
python piedra_papel_tijera.py

---
 
