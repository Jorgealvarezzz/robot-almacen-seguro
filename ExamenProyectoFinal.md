# Examen Proyecto Final
## Arquitectura de Sistemas
### Caso integrador: **Robot de almacén seguro**
## 1. Presentación del examen

### ¿Qué es este examen?

Este examen final **no es una lista de preguntas sueltas**.

Es un **reto práctico integrador por equipos**.

Eso significa que ustedes deberán:

* analizar un caso de uso,
* diseñar una solución,
* documentarla,
* implementar una versión mínima funcional,
* aplicar controles de seguridad,
* y justificar por qué su solución tiene sentido.

### ¿Qué se espera de ustedes?

Que trabajen como un **equipo de arquitectura y desarrollo** que recibe un problema real y debe proponer una solución inicial **coherente, segura, documentada y defendible**.

### Duración máxima

**2 dias**

### Modalidad

**Por equipos**

### Recursos permitidos
Sí pueden usar:
* Google
* IA
* documentación oficial
* apuntes de clase
* repositorios de apoyo
* material de laboratorios previos

## 2. Reglas generales del examen
1. Trabajo por equipos
2. Debe existir evidencia de colaboración
3. Su repositorio debe mostrar trabajo colaborativo real
4. Pueden consultar información y usar IA.
5. No se evalúa perfección estética
6. Se evaluará si la solución:
* tiene sentido,
* está bien estructurada,
* funciona en lo esencial,
* y aplica seguridad de forma razonable.

## 3. Entregables
## 3.1 Repositorio del proyecto

* `README.md`
* documentación arquitectónica
* código o archivos de configuración
* evidencias o instrucciones de prueba
* organización clara por carpetas

## 3.2 La documentación debe incluir como mínimo

* 1 diagrama **C4 Context**
* 1 diagrama **C4 Container**
* 1 diagrama **UML**
* 2 **ADR**
* una **matriz STRIDE breve**
* descripción de atributos de calidad y trade-offs

## 3.3 La solución técnica debe incluir como mínimo
* un componente que simule el robot o la capa edge,
* un mecanismo para enviar datos/eventos,
* un backend o servicio receptor,
* una interfaz de consulta, dashboard o visualización,
* un punto claro de entrada al sistema.

## 3.4 La solución debe incluir seguridad mínima aplicable
Deben implementar y demostrar al menos varios controles razonables, por ejemplo:
* autenticación y autorización,
* TLS o canal seguro,
* restricción de puertos o exposición mínima,
* gateway,
* validación de entradas,
* segmentación lógica,
* manejo de secretos fuera del código,
* separación de responsabilidades.

>> # AQUI INICIA EL EXAMEN 

## Caso: **Robot de almacén seguro**

Una empresa quiere modernizar una parte de su almacén usando un robot móvil.

Este robot debe poder:

* detectar presencia u obstáculos,
* reportar su estado,
* enviar eventos o telemetría,
* ser monitoreado desde una interfaz web,
* y permitir ciertas operaciones o consultas por parte de usuarios autorizados.

La empresa **no quiere una demo improvisada**, sino una propuesta inicial de arquitectura que tome en cuenta:

* operación real,
* seguridad,
* trazabilidad,
* documentación,
* trabajo colaborativo,
* y posibilidad de crecer en el futuro.

### Situación del negocio

El robot todavía está en una fase inicial. La empresa quiere validar una arquitectura base para responder preguntas como:

* ¿Cómo se comunicará el robot con el resto del sistema?
* ¿Qué partes estarán en edge, cuáles en backend y cuáles en visualización?
* ¿Cómo se protegerá la comunicación?
* ¿Cómo se controlará quién puede ver o ejecutar acciones?
* ¿Cómo se documentarán las decisiones de arquitectura?
* ¿Qué riesgos de seguridad existen desde el inicio?

### Su reto como equipo

Ustedes son el equipo encargado de construir una **propuesta inicial funcional y segura**.

No necesitan construir “el producto final de una empresa multinacional”.

Sí necesitan construir una solución que demuestre que ustedes saben:

* pensar como arquitectos,
* desarrollar una solución mínima,
* aplicar controles de seguridad,
* documentar correctamente,
* y justificar decisiones técnicas.


> ### Nota importante:
> La evidencia de trabajo colaborativo que **sí se tomará en cuenta para evaluar** será el trabajo visible de cada integrante en el repositorio.
> Esto significa que se revisará:
> * que **cada miembro del equipo haya hecho pushes al repositorio**;
> * que esos pushes correspondan a trabajo real;
> * y que exista participación visible en el desarrollo de la solución.
> En otras palabras:
>  ** si una persona no tiene evidencia de trabajo subida al repositorio, esa falta de participación sí afectará la evaluación del trabajo colaborativo.**

> ## No se busca que hagan “algo enorme”, se busca que hagan **algo bien pensado**.

# Etapas
## Etapa 1. Entender el problema y definir el sistema
* ¿Cuál es el problema que se quiere resolver?
* ¿Qué hace el robot?
* ¿Quién usa el sistema?
* ¿Qué partes están dentro del sistema y cuáles fuera?
* ¿Qué riesgos iniciales existen?
* ¿Qué necesita la empresa realmente?

### Resultados mínimos de esta etapa:
* definición del sistema,
* actores principales,
* objetivo del sistema,
* alcance inicial,
* restricciones,
* lista breve de riesgos y prioridades.

### Temas y Laboratorios que les ayudan en esta etapa

* **Semana 1:** calidad y atributos de calidad
* **Semana 2:** estilos arquitectónicos
* **Semana 6:** securing systems and winning buy-in

## Etapa 2. Diseñar la arquitectura y documentarla

Aquí deben transformar la idea en una propuesta estructurada.
**No basta con decir “vamos a usar microservicios” o “vamos a usar MQTT”.**
Deben mostrar:
* qué componentes existirán,
* cómo se comunican,
* qué función cumple cada uno,
* qué decisiones arquitectónicas tomaron,
* y por qué.

### Resultados mínimos de esta etapa:
#### A) C4 Context
#### B) C4 Container
#### C) 1 diagrama UML
#### D) 2 ADR

### Temas y Laboratorios que les ayudan en esta etapa
* **Semana 2:** estilos arquitectónicos
* **Semana 3:** documentación, C4, UML, ADR
* **Semana 5:** sistemas distribuidos y CAP
* **Semana 4:** Docs as Code y repositorio colaborativo
* **Semana 9:** arquitectura IoT edge-fog-cloud
* **Semana 10:** MQTT seguro
* **Semana 11:** microservicios y OAuth2

## Etapa 3. Construir la solución mínima funcional

Aquí deben implementar una versión mínima que funcione.
No tiene que ser gigantesca.
Sí debe mostrar el flujo principal.
1. el robot o simulador genera un evento o dato;
2. ese dato viaja a un backend, broker o servicio;
3. el sistema procesa, reenvía o expone la información;
4. una interfaz o endpoint permite ver el resultado;
5. al menos una parte del sistema está protegida.

### Ejemplo de lo que pueden implementar
* simulador web del robot;
* API con FastAPI, Node o similar;
* broker MQTT;
* Node-RED;
* gateway con NGINX;
* microservicios simples;
* autenticación con token;
* dashboard básico;
* separación edge / backend / visualización.

**No se trata de usar “todas las herramientas posibles”. Se trata de elegir una combinación **razonable** para resolver el caso.**

### Temas y Laboratorios que les ayudan en esta etapa
* **Semana 2:** estilos arquitectónicos
* **Semana 5:** trade-offs de sistemas distribuidos
* **Semana 7:** Zero Trust, Docker, secretos
* **Semana 9:** edge-fog-cloud
* **Semana 10:** MQTT seguro
* **Semana 11:** OAuth2, Keycloak, gateway, FastAPI

## Etapa 4. Aplicar seguridad y validar riesgos
### ¿Qué deben incluir como mínimo?
* una identificación de amenazas relevante;
* controles de seguridad aplicados;
* evidencia de que ciertas rutas o componentes están protegidos;
* decisiones razonables sobre exposición de servicios y validación.
### Deben construir una matriz STRIDE breve
Sí deben identificar amenazas reales del caso.
Ejemplos:
* **Spoofing:** un atacante se hace pasar por operador legítimo;
* **Tampering:** alguien altera telemetría o comandos;
* **Repudiation:** no queda evidencia de quién ejecutó una acción;
* **Information Disclosure:** el panel expone datos o errores sensibles;
* **Denial of Service:** saturación del broker, API o gateway;
* **Elevation of Privilege:** un usuario accede a funciones que no le corresponden.

### Seguridad mínima esperada
Deben aplicar y demostrar mas de un control, por ejemplo:
* TLS o HTTPS;
* autenticación con token;
* roles o permisos básicos;
* gateway;
* backend no expuesto directamente;
* secretos fuera de código;
* validación de entradas;
* reducción de superficie expuesta.

### Temas y Laboratorios que les ayudan en esta etapa
* **Semana 1:** seguridad como atributo de calidad
* **Semana 6:** justificación y priorización de seguridad
* **Semana 7:** Zero Trust
* **Semana 8:** STRIDE y DevSecOps
* **Semana 10:** MQTT seguro
* **Semana 11:** OAuth2 y microservicios
* **Semana 12:** OWASP y superficie web

## Etapa 5. Consolidar evidencias y cerrar la entrega
### ¿Qué debe incluir el cierre?
#### README claro
El README debe explicar:
* qué problema resuelve su solución,
* qué componentes tiene,
* cómo correrla o probarla,
* cómo está organizada,
* qué controles de seguridad implementaron,
* qué parte funciona y qué quedó fuera.

#### Evidencias
Deben agregar evidencia como:
* capturas,
* comandos,
* logs,
* respuestas HTTP,
* flujos visibles,
* pruebas de acceso exitoso o denegado.

#### Repositorio ordenado
Debe ser fácil encontrar:
* documentación,
* código,
* configuración,
* pruebas,
* y evidencias.

### Temas y Laboratorios que les ayudan en esta etapa
* **Semana 3:** documentación
* **Semana 6:** comunicar y justificar decisiones
* **Semana 4:** Docs as Code y GitHub
* **Semana 8:** hallazgos y mitigaciones
* **Semana 12:** evidencia y análisis técnico

## 4. Checklist de entrega
### Repositorio
* [ ] Repositorio accesible
* [ ] Estructura clara
* [ ] `README.md`
* [ ] ramas por feature
* [ ] commits comprensibles
* [ ] al menos 3 Pull Requests
* [ ] al menos 1 revisión por otro integrante
### Documentación arquitectónica
* [ ] C4 Context
* [ ] C4 Container
* [ ] 1 UML
* [ ] 2 ADR
### Implementación mínima
* [ ] simulador del robot o edge
* [ ] envío de telemetría, datos o eventos
* [ ] backend o servicio receptor
* [ ] visualización, consulta o dashboard
* [ ] punto de entrada definido
### Seguridad mínima
* [ ] al menos **dos** controles de seguridad aplicados
* [ ] evidencia de protección de alguna ruta, API o canal
* [ ] exposición mínima de servicios
* [ ] validación o control de acceso en alguna parte del sistema
### Análisis
* [ ] matriz STRIDE breve
* [ ] mitigaciones propuestas
* [ ] atributos de calidad priorizados
* [ ] trade-offs explicados
### Evidencias
* [ ] instrucciones de ejecución o prueba
* [ ] screenshots, logs o comandos
* [ ] evidencia de funcionamiento principal

> ## Una solución pequeña pero coherente puede valer más que una solución grande pero desordenada.



# 5. Rúbrica de evaluación

| Criterio                                          | Qué se evalúa                                                                            | Puntos |
| - | - | --: |
| Comprensión del caso y planteamiento del problema | Si identifican correctamente el sistema, actores, riesgos, objetivos y alcance           |     15 |
| Arquitectura propuesta                            | Coherencia del diseño, estilo arquitectónico, separación de componentes y flujo de datos |     15 |
| Documentación arquitectónica                      | Calidad, claridad y consistencia de C4, UML y ADR                                        |     15 |
| Implementación funcional                          | Funcionamiento del flujo principal del sistema                                           |     10 |
| Seguridad aplicada                                | Controles implementados y justificados                                                   |     15 |
| Análisis de amenazas y calidad                    | STRIDE, mitigaciones, atributos de calidad y trade-offs                                  |     15 |
| Trabajo colaborativo y repositorio                | Uso correcto de ramas, commits, PR, review y organización del repo                       |     10 |
| Evidencias y defensa técnica                      | README, pruebas, claridad para explicar la solución                                      |      5 |

**Total: 100 puntos**



# Anexos
## A. Formato sugerido del repositorio

Pueden adaptar la estructura, pero debe ser clara.

Ejemplo sugerido:

```text
/
README.md
docs/
  c4/
    context.*
    containers.*
  uml/
    secuencia.*
  adr/
    0001-....md
    0002-....md
  threat-model/
    stride.md
src/
  edge/
  backend/
  gateway/
  dashboard/
config/
evidence/
```



## B. Declaración de uso ético de IA

Cada equipo deberá incluir en su entrega una sección breve y explícita sobre el uso de herramientas de Inteligencia Artificial.
### ¿Qué deben declarar?
En el `README.md` o en un archivo aparte dentro del repositorio, deberán incluir una sección titulada:
### Declaración de uso ético de IA
Responder, de manera breve y clara, al menos lo siguiente:
1. **Qué herramienta(s) de IA usaron**
2. **En qué parte del trabajo la usaron**
3. **Para qué la usaron exactamente**
4. **Qué parte fue revisada, corregida o adaptada por el equipo**
5. **Qué parte NO fue generada por IA**
