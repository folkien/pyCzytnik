#!/bin/bash
# Zapisuje log z czytnika w katalogu roboczym.
mojczytnik > tmp.file
wait
sudo mv tmp.file /media/S/Roboczy/s.paszko/logPracy.txt

