Sistema de Monitoreo y Telecomando de Satélite Simulado

(Satellite Monitoring and Telecommand – Conceptual Prototype)

Descripción general

Este proyecto corresponde a un prototipo conceptual de un sistema de monitoreo, control y telecomando de un satélite simulado, desarrollado con el objetivo de estudiar y comprender el funcionamiento operativo real de una misión satelital, desde la perspectiva del segmento terreno y las operaciones de misión.

El enfoque del proyecto no es la simulación física detallada del entorno espacial, sino la reproducción de los flujos operacionales, decisiones y actividades que se ejecutan durante la preparación de pasadas, el enlace en tiempo real y el post-procesamiento de datos, tal como ocurre en un centro de control satelital.

Objetivo principal: 
Analizar y modelar las actividades operativas asociadas al monitoreo, control y telecomando de un satélite, mediante un prototipo de simulación que permita comprender la interacción entre telemetría, telecomandos, estados del sistema y procedimientos operacionales durante una misión.

Alcance: 

Incluye

-Simulación lógica de un satélite con sus estados operacionales definidos.
-Generación de telemetría en tiempo real.
-Ejecución de telecomandos desde una estación terrena simulada.
-Monitoreo y análisis de parámetros críticos del sistema (Temperatura, batería).
-Simulacion de datos por descargar (datos_pendientes_mb)
-Simulación del ciclo completo de una pasada (Tiempo limitado, verificación de estados para realizar acciones)
-Operación durante el enlace

No incluye 

-Dinámicas orbitales.
-Protocolos CCSDS reales.
-Comunicaciones RF.
-Modelos térmicos, eléctricos o estructurales detallados.
-Validación ambiental o física.

Arquitectura conceptual: 
1. Satélite simulado
-Mantiene un estado interno del sistema.
-Genera telemetría periódica.
-Responde a telecomandos válidos según su estado operacional.
-Implementa lógica de transición entre estados.

2. Estación terrena simulada
-Recibe y visualiza telemetría.
-Ejecuta telecomandos.
-Monitorea los parámetros críticos del satélite.
-Registra datos operacionales para análisis posterior.
3. Canal de comunicacion 
-Simula un enlace satélite-tierra por el protocolo TCP.
-Iintercambio de mensajes de telemetría y comandos. 