#!/bin/bash
#mount /mnt/goodcloud
#sleep 10

cp elektriciteitsverbruik.png /mnt/goodcloud/python/hubrpi/graphics/
echo "1/6"
cp gasverbruik.png /mnt/goodcloud/python/hubrpi/graphics/
echo "2/6"
cp waterverbruik.png /mnt/goodcloud/python/hubrpi/graphics/
echo "3/6"
cp energie_hubrpi.csv /mnt/goodcloud/python/hubrpi/data/
echo "4/6"
cp energieverbruik_2022.txt /mnt/goodcloud/python/hubrpi/data/
echo "5/6"
cp energieverbruik_2022_overzicht.txt /mnt/goodcloud/python/hubrpi/data/
echo "6/6"
echo "Copy to goodcloud complete."

#scp elektriciteitsverbruik.png alarm@alarmpi:/home/alarm/python/hubrpi/graphics/
#scp gasverbruik.png alarm@alarmpi:/home/alarm/python/hubrpi/graphics/
#scp waterverbruik.png alarm@alarmpi:/home/alarm/python/hubrpi/graphics/
#scp energie_hubrpi.csv alarm@alarmpi:/home/alarm/python/hubrpi/data/
#scp energieverbruik_2022.txt alarm@alarmpi:/home/alarm/python/hubrpi/data/
#scp energieverbruik_2022_overzicht.txt alarm@alarmpi:/home/alarm/python/hubrpi/data/
#echo "Copy to alarmpi complete."
