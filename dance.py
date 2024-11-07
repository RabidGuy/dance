#! /usr/bin/python3

# MIT License
# 
# Copyright (c) 2019-2024 Jack Stout
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


# Dance - Automated initiative for rolling every round.


import os
import pathlib
import random
import re


def main(args):
    expanded_file = pre_process(args)
    actors = get_actors_from_tokens(expanded_file)
    initiative_order = roll_and_organize_initiative_order(actors, args)
    for row in initiative_order:
        pretty_print(row)


def pre_process(args):
    expanded_file = insert(args.filename)
    return expanded_file


def insert(filename, parentdir="."):
    expanded_file = []
    filepath = pathlib.Path(os.sep.join([parentdir, filename])).resolve()
    linenumber = 0
    with open(filepath) as f:
        for line in f.readlines():
            linenumber += 1
            terms = line.split()
            if not terms:
                continue
            elif terms[0].startswith("#"):
                continue
            elif terms[0] == "insert":
                pd = os.path.dirname(filepath)
                target = line[7:].strip()
                if not target.endswith(".init"):
                    target = target + ".init"
                expanded_file.extend(insert(target, pd))
            else:
                row = {
                    "text": line,
                    "filepath": filepath,
                    "linenumber": linenumber
                }
                expanded_file.append(row)
    return expanded_file

def get_actors_from_tokens(lines):
    actors = []
    group = ""
    for line in lines:
        print(line)
        if line["text"].startswith("@"):
            group = ' '.join(line["text"][1:].split())
            continue
        actor = {"name": None, "bonus": 0,
                 "flag": None, "group": group}
        name, values = line["text"].split(":")
        actor["name"] = ' '.join(name.split())
        values = values.split()
        if len(values) == 1:
            actor["bonus"] = int(values[0])
        elif len(values) == 2:
            actor["bonus"] = int(values[0])
            actor["flag"] = values[1]
        else:
            raise ValueError("File \"{}\", line {}\nToo many values".format(
                line["filepath"], line["linenumber"]))
        actors.append(actor)
    return actors

def roll_and_organize_initiative_order(actors, args):
    # Roll and add bonus. Create clean list of actors for sorting.
    rolled_actors = []
    for actor in actors:
        # Creates list: [Group, Name]
        rolled = {"group": actor["group"], "name": actor["name"]}
        if not actor["flag"]:
            roll = d20()
        if actor["flag"] == "force":
            roll = actor["bonus"]
        elif actor["flag"] == "adv":
            two_rolls = [d20() for _ in range(2)]
            roll = max(two_rolls)
        elif actor["flag"] == "disadv":
            two_rolls = [d20() for _ in range(2)]
            roll = min(two_rolls)
        # Modifies list: [Score, Group, Name]
        rolled["score"] = roll + actor["bonus"]
        if actor["flag"] == "force":
            rolled["score"] = roll
        if args.verbose:
            if actor["flags" == "force"]:
                rolled["expression"] = (" <%i>" % (roll))
            else:
                rolled["expression"] = (" [%i] + %i" % (roll, actor["bonus"]))
        else:
            rolled["expression"] = ""
        rolled_actors.append(rolled)

    # Build tree to organize grouping and score conflicts.
    working_order = {}
    for actor in rolled_actors:
        score = actor["score"]
        group = actor["group"]
        name = actor["name"] + actor["expression"]
        if score not in working_order:
            working_order[score] = {}
        if group not in working_order[score]:
            working_order[score][group] = []
        working_order[score][group].append(name)

    ordered_actors = []
    inits = list(working_order.keys())
    inits.sort()
    inits.reverse()
    for init in inits:
        groups = list(working_order[init].keys())
        random.shuffle(groups)
        for group in groups:
            actors = working_order[init][group][:]
            actors.sort()
            actors.reverse()
            ordered_actors.append( (init, ", ".join(actors)) )

    return ordered_actors


def d20():
    return random.randint(1, 20)


def pretty_print(row):
    print("{}: {}".format(str(row[0]).rjust(2), row[1]))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="store_true")
    args = parser.parse_args()
    main(args)
