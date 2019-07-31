# Warbot San Adrián 2019
Este es el código del bot oficial de la Guerra de Cuadrillas de San Adrián.
No olvides seguirnos en Instagram: [@guerracuadrillassanadrian](https://instagram.com/guerracuadrillassanadrian)

### Pre-requisitos

Se trata de un conjunto de scripts bash y python3

Necesita Python3 y la librería numpy para generar números aleatorios, el proceso dependerá de la distribución:
https://docs.python-guide.org/starting/install3/linux/

En el caso concreto de Ubuntu 16.10 sería tan simple como:

```
sudo apt-get update
sudo apt-get install python3.6
sudo apt install python3-pip
sudo pip install numpy
```

### Inicialización
El bot utiliza los participantes que se encuentran en el fichero _backup/alive.txt_ cuya sintaxis es la siguiente:
```
Nombre Cuadrilla@usuarioinstagram
```
Cada participante debe aparecer en una línea diferente. El usuario de instagram es opcional.
Aquí podemos ver un [ejemplo](https://github.com/GuerraCuadrillasSanAdrian/warbot/blob/master/backup/alive.txt) de fichero bien formado.
El fichero _backup/dead.txt_ debería estar vacío inicialmente. Una vez todos los participantes están listos el estado de la batalla puede ser inicializado:
```
sh restart.sh
```

### Batalla
Cada ronda es independiente del resto y puede ser invocada en cualquier momento, el estado se mantiene mediante el uso de ficheros. El bot además genera automáticamente la publicación que se subirá a Instagram, haciendo uso de las plantillas de la carpeta _templates_.
Cada línea del fichero es un índice, usando la librería _numpy_ se generan dos números aleatorios entre 0 y N-1 (siendo N el número de participantes vivos), el primero resultará ganador y el segundo será el perdedor. Si ambos coinciden el participante se habrá autodestruído. Dado que cada vez es más probable este caso, la autodestrucción se desactiva cuando quedan menos de 5 participantes. 
Para generar una nueva ronda simplemente hay que ejecutar:
```
python fight.py
```
Al finalizar cada ronda se genera un número aleatorio entre 0 y 10 y si éste es cero, uno de los participantes muertos revivirá. La probabilidad está por debajo del 10% por lo que debería ocurrir muy pocas veces.
Una vez todos los participantes excepto uno hayan sido eliminados, se habrá alcanzado el estado final y habrá un único ganador, por lo que seguir intentando ejecutar nuevas rondas no tendrá efecto.


### Logs de guerras anteriores

Aquí podréis encontrar los logs generados por el bot durante las guerras ya finalizadas.

Verano 2019: https://pastebin.com/1eSjR3bi
