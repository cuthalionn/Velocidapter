# Copyright (c) Facebook, Inc. and its affiliates
import os 
from datetime import datetime
import argparse
now = datetime.now()
date = now.strftime("%d.%m.%Y.%H.%M.%S")
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-nt","--new_templates",action='store_true', help="Generate new templates")
    parser.add_argument("-ur","--use_rules", action='store_true', help="Use the the defined rules within input folder")
    parser.add_argument("-gf","--greetings_file", type=str,default="Data/greetings.txt", help="Path to greetings file")
    parser.add_argument("-if","--input_folder", type=str,default="Data/Taxi", help="Path to input files")
    parser.add_argument("-of","--output_folder", type=str,default=("Results/out" + date), help="Path to output files")
    
    
    parser.add_argument("-maxTryD","--max_number_tries_dial", type=int,default=10, help="Number of max tries before giving up on dialogue generation.")
    parser.add_argument("-maxTryT","--max_number_tries_temp", type=int,default=10, help="Number of max tries before giving up on template generation.")
    parser.add_argument("-maxD","--max_dialogue_count", type=int,default=10, help="Number of max dialogues to generate.")
    parser.add_argument("-maxT","--max_template_count", type=int,default=1000, help="Number of max templates to generate.")
    parser.add_argument("-vs","--val_split", type=float,default=0.4, help="Proportion for validation set.")

    args = vars(parser.parse_args())
    print(args)
    return args