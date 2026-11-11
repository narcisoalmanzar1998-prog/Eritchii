# Menú avanzado de Ocarina of Time en español (Eritchii / Lichii)

Este añadido **opcional** usa [sloperinaGZ v0.0.4.1](https://github.com/PracticeROM/sloperina/releases/tag/v0.0.4.1) (GPL-3.0) para *Ocarina of Time Switch 2*, 1.0.0/1.1.1 (`0400486024DEC000`). No copia directamente el menú de Hookshot: son arquitecturas distintas.

## Funciones disponibles

- Vida, contenedores, rupias, magia y munición infinitas.
- Levitar, velocidad de movimiento x2, atravesar paredes.
- Guardar/recuperar posición (dentro del mismo mapa), teletransportarse a distintos lugares.
- Cambiar la edad de Link y recargar el mapa.
- Editor de inventario, equipo, mejoras, objetos de misiones, escenas y herramientas de depuración.
- Idioma español mediante `sdmc/sloperinaGZ/lang/es.json`, con `language=es` en `sdmc/sloperinaGZ/settings.ini`.

No incluye aún las funciones exactas **Cámara libre** ni **Establecer hora** de Hookshot. Los nombres y las ayudas del idioma dependen del diccionario traducido; las entradas que falten se muestran en inglés. Los acentos se simplifican en la fuente del juego.

## Instalación

1. Copia tus partidas y cierra Zelda.
2. Instala el módulo, cuyo ZIP oficial está disponible [aquí](https://github.com/PracticeROM/sloperina/releases/download/v0.0.4.1/sloperinaGZ-0.0.4.1.zip), siguiendo las [instrucciones oficiales](https://github.com/PracticeROM/sloperina/blob/main/INSTALLATION.md). Confirma que su SHA-256 sea `7c119938897e4ecd84c974148caf46855eccce3b93f4ac5df94d483fa3cc3e75`.
3. En Eritchii, utiliza **File > Open Lichii Folders > Root Data Folder** para localizar la carpeta real. En instalaciones anteriores suele ser `%APPDATA%\eden`.
4. Antes de instalar, desactiva el anterior `cheatvm` o retira su carpeta `load/0400486024DEC000/cheatvm` a una ubicación de copia: ambos incluyen un módulo `subsdk9` y pueden entrar en conflicto. No elimines las partidas ni los datos de `sdmc`.
5. Copia la traducción `es.json` a `<Root Data Folder>/sdmc/sloperinaGZ/lang/es.json` y elige **settings > language > Español**; si hace falta, reinicia.
6. En el juego abre con **R + stick derecho abajo**; cruceta para navegar, **L** para elegir, **R + cruceta izquierda** para volver.

Esta es una alternativa de mayor cobertura a `cheatvm`; evita activar los dos mods a la vez. La compatibilidad final debe comprobarse en una partida real con una copia de seguridad.