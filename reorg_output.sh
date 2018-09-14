#!/bin/bash

p="$1"
plate_in="All plates 20x_Plate${p}_1"
plate_out="plate-$p"
mkdir -p "$plate_out"
for well in `ls "$plate_in"`; do
  for field in `seq 0 8`; do
    mv "$plate_in/$well/aligned_$field.tif" "$plate_out/$well-$field.tif"
  done
done
