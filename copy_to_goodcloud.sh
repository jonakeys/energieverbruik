#!/bin/bash
HUBRPIPATH=/goodcloud/python/hubrpi

cp gasverbruik.png $HUBRPIPATH/graphics/
echo "1/6"
cp elektriciteitsverbruik.png $HUBRPIPATH/graphics/
echo "2/6"
cp waterverbruik.png $HUBRPIPATH/graphics/
echo "3/6"
cp energieverbruik_HdgJr.txt $HUBRPIPATH/data/
echo "4/6"
cp energieverbruik_HdgJr_overzicht.txt $HUBRPIPATH/data/
echo "5/6"
cp energie_hubrpi.csv $HUBRPIPATH/data/
echo "6/6"
echo "Copy to goodcloud complete."
