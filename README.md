# Project Hosting
## Introdcution
In het tweede jaar van de opleiding Cloud and Cyber Security heb ik samen met een team van 5 personen een platform opgezet waar de studenten van het tweede jaar Application Development hun websites konden hosten. 

Hieronder vindt u een afbeelding van hoe onze uiteindelijke infrastructuur eruitzag.
Afbeelding met tekst, schermopname, Lettertype

Automatisch gegenereerde beschrijving
De omgeving draaide volledig op het datacenter (vSphere) van de school. Hier hebben wij meerdere VM's opgezet, maar omdat de resources gelimiteerd waren, moesten wij bepaalde delen samen op één VM plaatsen. De Kubernetes-cluster werd opgezet met behulp van Rancher en werd vervolgens beheerd via de API.

## Proces
Een korte samenvatting van hoe het proces van begin tot eind verliep voor de klant. De klant maakt een account aan via de API, waarna hij direct zijn eigen project kan aanmaken. Vervolgens kan hij zijn projectbestanden eenvoudig uploaden via de SFTP-server. Tot slot kan hij zijn project zien via de DNS-naam die de klant heeft gekregen bij het aanmaken van het project.

## API
De API was de kern van het project. Van hieruit kon de gebruiker zijn volledige project beheren en aanpassen naar zijn wensen. Ook kon de gebruiker zijn account hier beheren.
### Framework
Het framework dat werd gebruikt om de API te draaien, was FastAPI. Ik heb ervoor gekozen met dit framework te werken omdat ik ermee bekend was en omdat het in Python is geschreven.
### Voorbereiding
Om alles soepel te laten verlopen, had ik een script geschreven voor het opzetten van de basis (setupFastAPI.sh). Dit script zorgde ervoor dat de juiste mappen werden aangemaakt en de benodigde vereisten werden geïnstalleerd. Aan het einde van het script werd een extra script gemaakt met de naam startAPI.sh. Dit script zorgt ervoor dat de API draait. Later werd dit script gebruikt in mijn service om ervoor te zorgen dat de API continu kon draaien en automatisch opnieuw kon worden opgestart.
### Auth.py
In dit bestand bevindt zich alles met betrekking tot de authenticatie van de gebruiker. Hier worden de wachtwoorden gehasht. Ook bevat het een functie om te controleren of de gebruiker mag inloggen.
### Database.py
Alles met betrekking tot de database. Functies van dezelfde soort staan bij elkaar (CRUD).
### Functions.py
Hierin bevindt zich een functie die een unieke naam genereert. Dit was nodig om accounts op de server aan te maken en conflicten te voorkomen. Deze naam werd ook gebruikt om in te loggen via SFTP.
### Main.py
In dit bestand worden alle functies uit andere bestanden opgeroepen en wordt de invoer van de gebruiker gevalideerd.
### Server.py
Hierin bevinden zich functies voor het opzetten van projecten in het cluster en het beheren van de gebruiker op de server. 
## MySQL
De gegevens van de projecten, machines en gebruikers werden opgeslagen in een database. Deze database werd in een Docker-container gedraaid.
## Scripts
De API maakte gebruik van verschillende scripts die opdrachten uitvoerden op het systeem en in het cluster. De API draaide met beheerdersrechten, zodat hij alle scripts kon uitvoeren.
## Templates
Om een soepele werking te garanderen met de API, had ik van tevoren YAML-bestanden geschreven voor alle verschillende services in het cluster. Deze sjablonen werden later aangepast op basis van de projectvereisten.

