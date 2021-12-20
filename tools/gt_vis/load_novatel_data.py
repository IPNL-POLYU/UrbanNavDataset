
import os

def load_novatel_data(novatel_path):
  print(novatel_path)

  novatel = [];
  fp =  open(novatel_path);
  for line in fp:
    str_list = line.strip().split();
    novatel.append(str_list);
  return novatel;