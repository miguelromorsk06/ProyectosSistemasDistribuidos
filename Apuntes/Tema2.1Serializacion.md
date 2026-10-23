

## 1. Fundamentos: Procesamiento de Información y Código Binario

* **Naturaleza del Almacenamiento:** Las computadoras digitales procesan y almacenan datos de forma exclusiva mediante código binario (`0`s y `1`s).
* **Necesidad de Interpretación:** Una secuencia pura de bits (por ejemplo, `01100011 01100001...`) carece de significado por sí misma y no es directamente legible por humanos; requiere de reglas explícitas de interpretación para convertirse en texto, números o estructuras complejas.

---

## 2. Representación, Codificación y Serialización

### A. Definiciones de las Diapositivas (Tema 2.1)
* **Representación (*Representation*):** Es la forma lógica o notación gráfica en la que se visualizan los ceros y unos almacenados internamente. Un mismo valor lógico interno puede representarse en notación binaria (`0b`), decimal, hexadecimal (`hex()`) u octal (`oct()`) sin alterar su contenido matemático.
* **Codificación (*Encoding*):** Es la regla o tabla de equivalencia que determina qué patrón de bits o secuencia de bytes corresponde a cada símbolo o valor lógico. Establece dónde empieza y termina cada dato dentro de una secuencia.
* **Serialización (*Serialization*):** Es el proceso de convertir estructuras de datos complejas (objetos, registros, diccionarios) en una secuencia o flujo lineal de bytes (*byte stream*) continuo para permitir su almacenamiento en disco o su transmisión por red.

---

### B. Ampliación Teórica: EDR vs. Marshalling (Completado con Coulouris)

> **Lo que simplifica la diapositiva:** Trata la serialización y la codificación de forma conjunta como una conversión directa a bytes mediante funciones de biblioteca (como `json.dumps()` o `pickle.dumps()`).
> 
> **Lo que precisa Coulouris:** Formaliza la distinción entre el estándar de representación de datos y el proceso algorítmico que lo ejecuta:

* **Representación Externa de Datos (*External Data Representation - EDR*):** Es el **estándar o norma acordada** que especifica la codificación exacta y la estructura física de tipos primitivos y compuestos en el flujo de bytes (ej. CORBA CDR, Sun XDR, Java Serialization, Protocol Buffers).
* **Marshalling (Empaquetamiento):** Es la **acción o algoritmo** que toma una colección de estructuras de datos nativas del programa y las traduce/ensambla al formato EDR adecuado para el mensaje de red.
* **Unmarshalling (Desempaquetamiento):** Es el proceso inverso que reconstruye las estructuras de datos nativas a partir de la secuencia de bytes EDR recibida en el nodo destino.

---

## 3. Codificación de Datos Primitivos y Texto

### A. Enteros y Tipos Multibyte
* **Capacidad de 1 byte:** Un byte (8 bits) solo puede representar $256$ ($2^8$) valores distintos (de $0$ a $255$ en sin signo, o de $-128$ a $127$ con signo).
* **Tipos Multibyte:** Para números enteros mayores o datos de mayor rango, los lenguajes y protocolos emplean secuencias multibyte: `int8` (1 byte), `int16` (2 bytes), `int32` (4 bytes) e `int64` (8 bytes).

### B. Codificación de Caracteres y Cadenas
* **Conjunto de Caracteres vs. Codificación:** Un conjunto de caracteres (como Unicode) asigna un número identificador (*code-point*) a cada símbolo. La codificación (ASCII, UTF-8, UTF-16, UTF-32) define cómo se traduce ese número a una secuencia concreta de bytes.
* **ASCII:** Codificación de 7 bits (extendida a 1 byte) que representa 128 caracteres básicos (coincide con Unicode hasta el código 127).
* **UTF-8 (Codificación de Longitud Variable Autosincronizable):**
  * **1 byte (`0xxxxxxx`):** Compatible de forma nativa con ASCII.
  * **Multibyte (2 a 4 bytes):** Utiliza bytes de cabecera (*leader bytes*) que indican la longitud (`110xxxxx` para 2 bytes, `1110xxxx` para 3 bytes, `11110000` para 4 bytes) y bytes de continuación con prefijo `10xxxxxx`.
  * **Propiedad de Autosincronización:** Cada byte revela su propio rol mediante su prefijo binario, impidiendo que un byte de datos se confunda con un delimitador.

---

## 4. Ordenamiento de Bytes (*Endianness*) y Alineación en Memoria

### A. Big-Endian vs. Little-Endian
Las arquitecturas de procesador organizan los bytes de un tipo multibyte de dos formas:

* **Little-Endian (LSB primero):** El byte menos significativo (*Least Significant Byte*) se almacena en la dirección de memoria más baja (utilizado en procesadores AMD e Intel).
* **Big-Endian (MSB primero):** El byte más significativo (*Most Significant Byte*) se almacena en la dirección de memoria más baja (adoptado como el **Network Byte Order** en los protocolos TCP/IP).

---

### B. Estrategias de Red y Alineación (Completado con Coulouris)

1. **Formato Canónico vs. Formato del Emisor (Coulouris):**
   * **Formato Canónico (ej. Sun XDR / TCP/IP):** Todos los datos se convierten obligatoriamente a Big-Endian antes de la transmisión.
   * **El Emisor Decide (*Sender-Makes-Right*, ej. CORBA CDR):** Transmite en el orden nativo del emisor e incluye una bandera de *endianness* en la cabecera; el receptor convierte solo si su arquitectura es diferente.
2. **Alineación de Datos (*Padding* - Coulouris):**
   * **Regla de CORBA CDR:** Un tipo primitivo de tamaño $n$ bytes (donde $n = 1, 2, 4, 8$) debe ubicarse en un índice de byte del flujo que sea múltiplo exacto de $n$, insertando bytes de relleno con ceros si es necesario.
   * **Regla de Sun XDR:** Alinea absolutamente todos los tipos en límites fijos de 4 bytes.

---

## 5. Empaquetamiento Binario en Python: Módulo `struct`

El módulo `struct` permite convertir valores de Python a datos binarios planos en formato `bytes`, ofreciendo control sobre el *endianness* y la estructura física.

### A. Funciones Principales
* `struct.pack(format, v1, v2, ...)`: Convierte valores de Python a un objeto de tipo `bytes` según la cadena de formato especificada.
* `struct.unpack(format, buffer)`: Desempaqueta una secuencia de `bytes` devolviendo una tupla de valores nativos.
* `struct.calcsize(format)`: Devuelve el tamaño exacto en bytes de la estructura resultante según la cadena de formato.

### B. Opciones de Formato y Prefijos de Endianness
* `@`: Endianness nativo con alineación del compilador C.
* `=`: Endianness nativo con tamaño estándar y sin alineación (*no padding*).
* `<`: Little-endian con tamaño estándar.
* `>`: Big-endian con tamaño estándar.
* `!`: Estándar de red (*network byte order*, equivalente a Big-Endian `>`).
* **Detección del sistema:** `sys.byteorder` devuelve `'little'` o `'big'` para indicar el orden nativo del procesador.

---

## 6. Taxonomía Comparativa de Formatos EDR (Completado con Coulouris)

Coulouris clasifica los formatos de serialización y EDR en tres categorías según la presencia de metadatos de tipo y su codificación:

```
                                  FORMATOS EDR
                                       |
                   +-------------------+-------------------+
                   |                                       |
            FORMATOS BINARIOS                       FORMATOS TEXTUALES
                   |                                       |
         +---------+---------+                   +---------+---------+
         |                   |                   |                   |
    Tipado Implícito    Tipado Explícito     Autodescriptivos     Basados en Esquema
    (CORBA CDR, XDR,   (Java Serialization,     (JSON, XML,         (XML + XSD,
    Protobuf, struct)    Python Pickle)            SOAP)              WSDL)
```

| Criterio | Formatos de Tipado Implícito (CORBA CDR, Sun XDR, Protobuf) | Formatos de Tipado Explícito / Reflexivos (Java Serialization) | Formatos Textuales (JSON, XML, SOAP) |
| :--- | :--- | :--- | :--- |
| **Información de tipo en el mensaje** | **Ninguna.** El mensaje contiene solo los valores ordenados. | **Incluida.** El mensaje transporta el nombre de las clases, versiones y nombres/tipos de variables. | **Incluida.** Etiquetas de texto y esquemas definen la estructura y tipos. |
| **Mecanismo de Reconstrucción** | Requiere una especificación previa mediante un lenguaje IDL o esquema compartido. | Utiliza la API de **Reflexión** para inspeccionar las clases y construir objetos dinámicamente. | Procesado mediante *parsers* (DOM/SAX) y mapeo a clases locales. |
| **Manejo de Grafos de Objetos** | No soporta punteros ni referencias circulares directas. | Asigna **manejadores (*handles*)** a cada objeto para escribirlo una sola vez en el flujo. | No soporta referencias circulares de forma nativa. |
| **Campos Omitidos** | Gestionado por la definición IDL o etiquetas de campo. | Uso de la palabra clave `transient` para ignorar variables ligadas a recursos locales. | Elementos o atributos opcionales en el marcado. |
| **Rendimiento y Tamaño** | Altamente compacto y muy rápido de procesar. | Tamaño intermedio; añade sobrecarga por metadatos de clase. | Mensajes voluminosos (hasta 14 veces mayores) y procesamiento más lento. |
| **Datos Binarios** | Transmisión binaria directa. | Transmisión binaria directa. | Requiere codificación **Base64** para incluir datos binarios. |

---

## 7. Importancia Práctica en el Diseño de Protocolos de Red

* **El Protocolo como Regla de Interpretación:** Los protocolos de red son únicamente conjuntos de reglas acordadas entre las partes para interpretar una secuencia de bytes binarios recibidos a través de un socket.
* **Encuadre de Mensajes (*Framing*):** Debido a que protocolos como TCP ofrecen una abstracción de flujo continuo de bytes (*byte stream*) sin fronteras de mensaje, el protocolo de aplicación utiliza el marshalling/unmarshalling (asociado a formatos binarios como `struct` o cabeceras de longitud explícitas) para segmentar, delimitar e interpretar los datos correctamente.
```


