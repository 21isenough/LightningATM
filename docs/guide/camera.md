##  Installation und Test der Kamera

The 5MP Camera OV5647 for the Raspberry Pi is available from different manufacturers and with slightly different designs.
To test the function of the camera you can take a picture and download it to you computer.

### Installation

The ribbon cable is a bit special as the connectors on the camera and the Raspberry Pi are slightly different sizes. So the cable tapers.
Before sliding the cable into the slot, the black latch must be released by gently pulling upwards.
The cable can then simply be pushed in. The silver contacts must point away from the detent. See image!
When the cable is centered, you can lock the latches in place by sliding them back slightly.  

connection

<img src="https://i.imgur.com/exqHrU4.jpg" width="300">

### Activate camera

- Login to the Raspberry Pi

      $ ssh admin@192.168.x.x
      
- Directory displayed: `pi@raspberrypi:~ $`
    
- Call up the Raspi-Config and activate the camera

      $ sudo raspi-config
    
- Choose: `Interfacing Options  Configure connections to peripherals` 
- Choose: `Camera      Enable/Disable connection to the Raspberry Pi Camera`
- Confirm: `Would you like the camera interface to be enabled?` -> `\<YES>` 
- Confirm: `The camera interface is enabled` -> `\<OK>`
- Go To: `\<Finish>`
- When ask for: `Would you like to reboot now?` -> `\<YES>`
- Wenn nicht schon aus dem Menü heraus neu gestartet wurden, dann einmal manuell neu starten 

      $ sudo reboot
      
  raspi-config
  
  ![](https://i.imgur.com/h5geHZk.png)
  ![](https://i.imgur.com/M0DIO6i.png)
  
  Your config menu can look slightly different, depends of you hard- and software
      
### Ein Bild aufnehmen 

- Nach dem einloggen auf den Raspberry Pi ein Bild aufnehmen 

      $ raspistill -v -o test.jpg

  Hinweis: Das -v ist nur optional und zeigt weiter Daten an. Das -o ist notwendig um die Datei zu schreiben.
  
  Die Aufnahme dauert 5 Sekunden (time delay 5000 (ms)). Man kann die Aufnahmezeit verkürzen, sollte die Zeit aber nicht zu kurz machen, da sonst das Bild in der Qualität leidet. Ein Sekunde (= 1000 ms) geht aber auf jeden Fall. So sieht der Befehl dann wie folgt aus
    
   $ raspistill -v -o test.jpg -t 1000
   
  Weiter Funktionen für ein Aufnahme findet man in der Hilfe `$ raspistill --help`
  
- Kontrollieren ob das Bild abelegt wurde

      $ ls -l
      
  Da müsst jetzt in der Liste die Datei `test.jpg` erscheinen.
  
- Überprüfen der Verzeichnisstruktur

      $ pwd
   
  Das Verzeichnis sollte lauten: `/home/pi/`
  
  raspistill command

   <img src="https://i.imgur.com/VdU17HW.png" width="500">
  
 ### Bild auf dem PC/Notebook übertragen
 
 - Am Computer ein **zweites Terminal Fenster** öffnen 
 - In einen Ordner seiner Wahl wechseln (Hier Beispielhaft `C:\temp>`)
 - Den Befehl zum kopieren für ein Windows System lautet

       $ scp pi@192.168.x.x:/home/pi/test.jpg .
      
 - Zur bestätigung muss noch das Passwort vom Raspberry Pi eingegeben werden

 - Wenn alles geklappt hat, wurde das Bild auf dem PC/Notebook übertragen und kann jetzt betrachtet werden
      
 - Note: Beim einem Mac oder Linux System ist der Befehl leicht abgewandelt

       $ scp 'pi@192.168.x.x:/home/pi/test.jpg' ./
       
   copy image to storage

   <img src="https://i.imgur.com/J19kInz.png" width="700">
      
### Hinweise

- Die Kamera nimmt ein paar Sekunden verzögert auf
- Möchte man mehrer Bilder aufnehmen, müssen die Bilder durchnummeriert werden. Z.B. test1.jpg, test2.jpg etc.
- Dann kann man alle Bilder auf einmal Übertragen 

      $ scp pi@192.168.x.x:/home/pi/*.jpg .   bzw.    scp 'pi@192.168.x.x:/home/pi/*.jpg' ./
      
- Weiter Funktionen für ein Aufnahme findet man in der Hilfe

      $ raspistill --help





