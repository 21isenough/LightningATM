##  Installation und Test der Kamera

Die Raspberry Pi 5MP Camera OV5647 gibt es von verschiedenen Herstellern und mit leicht unterschiedlichen Bauarten.
Einige haben ein verstellbares Objektiv und wieder andere ein festes Objektiv.
Um die Funktion und das Bild er Kamera zu testen, kann man ein Bild aufnehmen, dass man dann auf den PC betrachten kann.

#### Montage

Das Flachbandkabel zur Verbindung der Camera und des Raspberry Pi Zero ist ein spezielles,
da von etwas größeren Schnittstelle der Kamera erst einmal auf ein etwas kleinern Anschluss verjüngt wird.
Bevor man die Kabel in den Slot schiebt, muss die schwarze Arretierung durch leichts ziehen nach oben gelöst werden.
Dann läßt sich das Kabel leicht einschieben. Die silbernen Kontakt müssen von der Arretierung weg schauen.
Sitzt das Kabel zentriert kann man die Arretierungen durch leichtes zurückdrücken fixieren. 

#### Kamera aktivieren und ein Bild machen

- Einloggen auf Raspberry Pi

      $ ssh admin@192.168.x.x
    
- Die Raspi-Config aufrufen

      $ sudo raspi-config
    
- Choose: `3 Interface Options    Configure connections to peripherals` 
- Choose: `I1 Legacy Camera Enable/disable legacy camera support` 
- When ask for: `Would you like to enable legacy camera support?` choose `\<YES>` and then `\<OK>`
- Choose: `\<Finish>`
- Raspberry Pi einmal neu starten 

      $ sudo reboot
      
- Ein Bild machen

      $ raspistill -v -o test.jpg

  Das -v ist optional und zeigt weiter Daten an. Das -o 



