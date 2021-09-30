# AWS-S3-Archiver



A feladatrész:

A feladat megoldása elég egyszerű python-ban. A file nevéből kinyerem a dátumot a datetime könyvtárral és 
a mai nappal összehasonlítom. Ha 30 napnál régebbi, az shutil könyvtárral zippelem a ./zip mappába. Majd boto3-al 
feltöltöm AWS S3 bucketembe. Az access kulcsokat egy külön file-ban tartom, ezek nincsnek githubra feltöltve. 
S3 bucket elkészítése elég egyszerű. Regisztráltam AWS-re majd létrehoztam egy bucketet, hakatikibucket néven. Majd ebben
egy archives mappát. A kulcsokat sajnos rootként töltöttem le, ez egy security issue lehet később. 
Ezekután nem felejtem el a fileokat és a zipeket törölni a mappákból, miután feltöltöttem a fileokat a felhőbe. 
Boto3 telepítésével voltak problémáim. A python verzióm valamiért 2.7 volt. Mire ezt kiderítettem elég sok víz lefolyt a Dunán.
Utánna a fix erre az volt, hogy letöltöttem 3.9-et.

B feladatrész:

Az ütemezést cron-al tettem. Mac-et használok és interneten ezt láttam a leggyakrabban. 
A pontos command a Crontab.txt fileban is olvasható.

	> crontab -e
  
	> i
  
	> 0 1 * * * cd /Users/takatsbalint/Dokumentumok/Vs_Code/Devops/ && /
		usr/local/bin/python /Users/takatsbalint/Dokumentumok/Vs_Code/Devops/Solution.py 
		&> /Users/takatsbalint/Dokumentumok/Vs_Code/Devops/crontab.log
    
	> esc
  
	> :wq
  
Ezeknek a parancsoknak a kiadásával készen is van az ütemezés. Loggolást is hozzáadtam, crontab.log fileba kerülnek mentésre 
a fileok amiket archiválok. 

C feladatrész:

Ennek a feladatnak a dokumentációja ugyan az mint az első résznek. Hiszen mindent csak a másik irányba kell megcsinálni.
Így a részletekkel nem is vesztegetném az időt, ugyan azokat a könyvtárakat használtam csak zip helyett unzipet például.
Ami említésre méltó a user input validálása. Próbáltam olyan kódot írni oda, hogy a felhasználó ne tudjon olyan dátumot
megadni ami valótlan. 
