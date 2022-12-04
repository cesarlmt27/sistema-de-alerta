# sistema-de-alterta
Sistema de alerta para el cuidado de adultos mayores

### Estructura de `networkData.h`
```c++
#include <Arduino.h>

// Red a conectar el NodeMCU
String ssid = "";
String password = "";

// URL completo del dominio/IP donde se hará el HTTP POST request
char host[] = "";
int port = 80;
```
