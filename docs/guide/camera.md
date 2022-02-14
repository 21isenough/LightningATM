##  Installation und Test der Kamera

Die 5MP Camera OV5647 für den Raspberry Pi gibt es von verschiedenen Herstellern und mit leicht unterschiedlichen Bauarten.
Einige haben ein verstellbares Objektiv und wieder andere ein festes Objektiv.
Um die Funktion und das Bild er Kamera zu testen, kann man ein Bild aufnehmen, dass man dann auf den PC betrachten kann.

### Montage

Das Flachbandkabel zur Verbindung der Camera und des Raspberry Pi Zero ist ein spezielles,
da von etwas größeren Schnittstelle der Kamera erst einmal auf ein etwas kleinern Anschluss verjüngt wird.
Bevor man die Kabel in den Slot schiebt, muss die schwarze Arretierung durch leichts ziehen nach oben gelöst werden.
Dann läßt sich das Kabel leicht einschieben. Die silbernen Kontakt müssen von der Arretierung weg schauen.
Sitzt das Kabel zentriert kann man die Arretierungen durch leichtes zurückdrücken fixieren. 

### Kamera aktivieren 

- Einloggen auf den Raspberry Pi

      $ ssh admin@192.168.x.x
      
- Angezeigtes Verzeichnis: `pi@raspberrypi:~ $`
    
- Die Raspi-Config aufrufen und die Kamera aktivieren

      $ sudo raspi-config
    
- Choose: `3 Interface Options    Configure connections to peripherals` 
- Choose: `I1 Legacy Camera Enable/disable legacy camera support` 
- When ask for: `Would you like to enable legacy camera support?` choose `\<YES>` and then `\<OK>`
- Choose: `\<Finish>`
- Raspberry Pi einmal neu starten 

      $ sudo reboot
      
- Nach ein paar Minuten kann ein neue Login erfolgen
      
### Zum Test ein Bild aufnehmen 

- Nach dem einloggen auf den Raspberry Pi ein Bild aufnehmen 

      $ raspistill -v -o test.jpg

  Note: Das -v ist nur optional und zeigt weiter Daten an. Das -o ist notwendig um die Datei zu schreiben.
  
- Kontrollieren ob das Bild abelegt wurde

      $ ls -l
      
  Da müsst jetzt in der Liste die Datei `test.jpg` erscheinen.
  
- Verzeichnisstruktur überbrüfen

      $ pwd
   
  Das Bild sollte hier liegen: `/home/pi/`
  
 ### Bild auf dem PC/Notebook übertragen
 
 - Am PC ein zweites Terminal Fenster eröffnen 
 - In einen Ordner seiner Wahl wechseln (Hier Beispielhaft `C:\temp>`)
 - Den Befehl zum kopieren für ein Windows Sytem lautet

      $ scp pi@192.168.168.24:/home/pi/test.jpg .
      
 - Zur bestätigung muss noch das Passwort vom Raspberry Pi eingegeben werden

 - Wenn alles geklappt hat, wurde das Bild auf dem PC/Notebook übertragen und kann jetzt betrachtet werden
      
 - Note: Beim einem Mac oder Linux System ist der Befehl leicht abgewandelt

      $ scp 'pi@192.168.168.24:/home/pi/test.jpg' ./
      
### Hinweise

- Die Kamera nimmt ein paar Sekunden verzögert auf
- Möchte man mehrer Bilder aufnehmen, müssen die Bilder durchnummeriert werden. Z.B. test1.jpg, test2.jpg etc.
- Dann kann man alle Bilder auf einmal Übertragen 

      $ scp pi@192.168.168.24:/home/pi/*.jpg .
      
- Weiter Funktionen für ein Aufnahme findet man in der Hilfe

      $ raspistill --help





