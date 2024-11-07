#! /usr/bin/python3

# Dance - Automated initiative for rolling every round.
# Copyright (C) 2019-2023  Jack Stout
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import pathlib
import random
import re


def main(args):
    expanded_file = pre_process(args)
    # process()
    # shuffle()
    # post_process()
    actors = get_actors_from_tokens(expanded_file)
    initiative_order = roll_and_organize_initiative_order(actors, args)
    for row in initiative_order:
        pretty_print(row)


def pre_process(args):
    expanded_file = insert(args.filename)
    # for line in expanded_file:
    #     print(line)
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
                # expanded_file.append(' '.join(terms))
                row = {
                    "text": line,
                    "filepath": filepath,
                    "linenumber": linenumber
                }
                expanded_file.append(row)
    return expanded_file


def get_actors_from_tokens(lines):
    # !!! Does not enforce specific ordering of elements.
    # !!!     [<namewords>: <bonus> <keywords>]
    def get_actors(lines):
        for line in lines:
            # print(line["filepath"], line["linenumber"])
            yield line["text"].split()
    tokens = get_actors(lines)
    actors = []
    group = ""
    for row in tokens:
        # Handle groups.
        if row[0].startswith('@'):
            group = ' '.join(row)[1:]
            continue
        # Handle actors.
        actor = {"name": [], "bonus": 0,
                 "flags": [], "group": group}
        for element in row:
            # Handle integers.
            if re.fullmatch("-?[0-9]+", element):
                # !!! Does not handle multiple bonuses overwriting eachother.
                actor["bonus"] = int(element)
                continue
            # Handle keywords.
            # !!! Does not handle conflicting or duplicate flags.
            # !!!     Perhaps conflicts are better handled, later.
            if re.fullmatch("adv", element):
                actor["flags"].append("adv")
                continue
            if re.fullmatch("disadv", element):
                actor["flags"].append("disadv")
                continue
            if re.fullmatch("force", element):
                actor["flags"].append("force")
                continue
            # Handle names.
            actor["name"].append(element)
        # Trim colon.
        actor["name"][-1] = actor["name"][-1][:-1]
        # Turn list of names into one space-separated string.
        actor["name"] = " ".join(actor["name"])

        actors.append(actor)
    return actors


def roll_and_organize_initiative_order(actors, args):
    # Roll and add bonus. Create clean list of actors for sorting.
    rolled_actors = []
    for actor in actors:
        # Creates list: [Group, Name]
        rolled = {"group": actor["group"], "name": actor["name"]}
        if not actor["flags"]:
            roll = d20()
        # !!!next Force not working. Test on "basic_example\rooms\5_ceremonial_room.init".
        if "force" in actor["flags"]:
            roll = actor["bonus"]
        elif "adv" in actor["flags"]:
            two_rolls = [d20() for _ in range(2)]
            roll = max(two_rolls)
        elif "disadv" in actor["flags"]:
            two_rolls = [d20() for _ in range(2)]
            roll = min(two_rolls)
        # Modifies list: [Score, Group, Name]
        rolled["score"] = roll + actor["bonus"]
        if args.verbose:
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
