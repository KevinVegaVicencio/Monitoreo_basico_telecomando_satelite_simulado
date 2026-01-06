Monitoreo básico y telecomando de un satélite simulado
Descripción general
Este proyecto corresponde a un prototipo de simulación orientado a la comprensión del funcionamiento operativo de un satélite y de las actividades asociadas a su monitoreo y telecomando desde un segmento terreno.
El objetivo principal no es replicar de forma exacta un sistema espacial real, sino modelar de forma simplificada los procesos, las decisiones y flujos operacionales que se realizan durante la operación diaria de una misión satelital, tales como la preparación de pasadas, la recepción y análisis de telemetría, la ejecución de telecomandos y el post-procesamiento de información.
El proyecto fue desarrollado con un enfoque educativo y conceptual, orientado a reforzar el entendimiento de las operaciones espaciales desde una perspectiva de ingeniería de sistemas y control de misión.
Objetivos del proyecto
·	Comprender el flujo operacional de un satélite durante una pasada sobre una estación terrena.
·	Simular la generación y análisis de telemetría en tiempo (pseudo) real.
·	Modelar la ejecución de telecomandos y su impacto en el estado del sistema.
·	Representar estados operativos típicos de un satélite (nominal, etc.).
·	Analizar el comportamiento del sistema antes, durante y después de una pasada.
·	Familiarizarse con conceptos propios del dominio espacial, tales como:
o	Telemetría
o	Telecomando
o	Pasadas
o	Estados operativos
o	Post-procesamiento de datos
Alcance y enfoque
El proyecto no pretende:
·	Implementar protocolos espaciales reales (CCSDS).
·	Modelar dinámica orbital real ni enlaces RF.
·	Reemplazar sistemas de control de misión profesionales.
El proyecto sí pretende:
·	Representar correctamente la lógica operacional.
·	Simular el rol del operador satelital.
·	Reforzar la toma de decisiones basada en parámetros del sistema.
·	Servir como base conceptual para comprender sistemas reales de control de satélites.
Arquitectura conceptual del sistema
Satélite simulado
·	Mantiene un estado interno del sistema.
·	Genera telemetría periódica.
·	Responde a telecomandos enviados desde la estación terrena.
·	Simula condiciones operativas básicas (por ejemplo, niveles de batería o estados de operación).
Estación terrena simulada
·	Recibe y visualiza la telemetría generada por el satélite.
·	Permite el envío de telecomandos.
·	Registra información para su posterior análisis.
·	Representa el rol del operador durante una pasada.
Canal de comunicación
·	Simula el enlace entre satélite y estación terrena.
·	Permite la transmisión de datos de telemetría y comandos.
·	No representa un enlace físico real, sino un canal lógico de comunicación.
Estados operativos simulados
El satélite simulado considera estados operativos básicos, típicos en sistemas espaciales:
·	INIT: estado inicial del sistema.
·	STANDBY: sistema operativo, pero sin carga útil activa.
·	NOMINAL: operación normal del satélite.
·	SAFE: estado seguro ante condiciones anómalas (por ejemplo, batería baja).
La transición entre estados se realiza mediante telecomandos o como respuesta a eventos simulados.
Flujo operacional simulado
1. Preparación de la pasada
·	Revisión del último estado conocido del satélite.
·	Definición de acciones a ejecutar durante el enlace.
·	Inicio de la estación terrena.
2. Operación durante la pasada
·	Recepción continua de telemetría.
·	Monitoreo de parámetros críticos.
·	Envío de telecomandos.
·	Evaluación del estado del sistema en tiempo real.
3. Post-procesamiento
·	Registro de la información recibida.
·	Análisis de los datos generados durante la pasada.
·	Evaluación del comportamiento del sistema.
Tecnologías utilizadas
·	Lenguaje de programación: Python
·	Comunicación: simulación mediante mecanismos de software
·	Ejecución: entorno local
Se eligieron estas tecnologías debido a su simplicidad y claridad para poder desarrollar este prototipo con fines educativos y de análisis conceptual. 
Resultados y aprendizajes
A través del desarrollo y análisis de este prototipo se logró:
·	Comprender el rol operativo del segmento terreno.
·	Familiarizarse con el lenguaje y la lógica de las operaciones satelitales.
·	Reforzar el análisis de sistemas en tiempo real.
·	Entender la importancia del monitoreo continuo y la trazabilidad de eventos.
·	Visualizar la relación entre telemetría, telecomando y estados del sistema.
Limitaciones conocidas
·	El sistema no representa condiciones físicas reales del espacio.
·	No se implementan estándares espaciales formales.
·	La simulación es determinista y simplificada.
Estas limitaciones son coherentes en base al objetivo educativo del proyecto.
Motivación y contexto
Este proyecto fue desarrollado como parte de un proceso de formación y acercamiento al dominio de las operaciones espaciales, con especial interés en las actividades de monitoreo, control y telecomando de satélites, alineadas a funciones propias de centros de control y operación de misiones espaciales.
Autor
Kevin Vega Vicencio
 Ingeniero Informático

