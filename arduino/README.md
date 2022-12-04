# Códigos de Arduino y NodeMCU

### Estructura de `networkData.h`:
Este archivo de debe crear dentro del directorio `nodeMCU`.
```c++
#include <Arduino.h>

// Red a conectar el NodeMCU
String ssid = "";
String password = "";

// URL completo del dominio/IP donde se hará el HTTP POST request
char host[] = "";
int port = 80;
```
