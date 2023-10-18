# Project Hosting
## Introdcution
In het tweede jaar van de opleiding Cloud and Cyber Security heb ik samen met een team van 5 personen een platform opgezet waar de studenten van het tweede jaar Application Development hun websites konden hosten. 

Hieronder vindt u een afbeelding van hoe onze uiteindelijke infrastructuur eruitzag.
Afbeelding met tekst, schermopname, Lettertype

Automatisch gegenereerde beschrijving
De omgeving draaide volledig op het datacenter (vSphere) van de school. Hier hebben wij meerdere VM's opgezet, maar omdat de resources gelimiteerd waren, moesten wij bepaalde delen samen op één VM plaatsen. De Kubernetes-cluster werd opgezet met behulp van Rancher en werd vervolgens beheerd via de API.

## Proces
Een korte samenvatting van hoe het proces van begin tot eind verliep voor de klant. De klant maakt een account aan via de API, waarna hij direct zijn eigen project kan aanmaken. Vervolgens kan hij zijn projectbestanden eenvoudig uploaden via de SFTP-server. Tot slot kan hij zijn project zien via de DNS-naam die de klant heeft gekregen bij het aanmaken van het project.
