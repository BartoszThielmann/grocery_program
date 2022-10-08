import argparse
import api

parser = argparse.ArgumentParser()
g = parser.add_mutually_exclusive_group()
g.add_argument("--adddish", help="Add new dish", action="store_true",
default=None)
g.add_argument("--showdish", help="Show specified dish", action="store_true", 
default=None)
g.add_argument("--showall", help="Show all saved dishes", action="store_true", 
default=None)
g.add_argument("--rmdish", help="Remove specified dish", action="store_true", 
default=None)
args = parser.parse_args()

if args.adddish:
    api.add_dish()
elif args.showdish:
    api.show_dish()
elif args.showall:
    api.show_all()
elif args.rmdish:
    api.rm_dish()
