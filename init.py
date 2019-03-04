#! /usr/bin/python3

#   Copyright 2017-2019 Jack Stout
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import random
import re


def main(args):
    tokens = get_tokens_from_file(args.filename)
    actors = get_actors_from_tokens(tokens)
    initiative_order = roll_and_organize_initiative_order(actors)
    for row in initiative_order:
        pretty_print(row)


def get_tokens_from_file(filename):
    f = open(filename, 'r')
    lines_of_tokens = []
    for line in f.readlines():
        line = line.strip()
        # Ignore blank lines.
        if not line:
            continue
        # Ignore comments.
        if line.startswith("//"):
            continue
        lines_of_tokens.append(line.split())
    f.close()
    return lines_of_tokens


def get_actors_from_tokens(tokens):
    # XXX Does not enforce specific ordering of elements.
    # XXX     [name parts, bonus, keywords]
    actors = []
    group = ""
    for row in tokens:
        # Handle labels.
        if row[0].startswith(':'):
            group = ' '.join(row)[1:]
            continue
        # Handle actors.
        actor = {"name": [], "bonus": 0,
                 "flags": [], "group": group}
        for element in row:
            # Handle integers.
            if re.fullmatch("-?\d+", element):
                # XXX Does not handle multiple bonuses overwriting eachother.
                actor["bonus"] = int(element)
                continue
            # Handle keywords.
            # XXX Does not handle conflicting or duplicate flags.
            # XXX     Perhaps conflicts are better handled, later.
            if re.fullmatch("adv", element):
                actor["flags"].append("adv")
                continue
            if re.fullmatch("disadv", element):
                actor["flags"].append("disadv")
                continue
            # Handle names.
            actor["name"].append(element)
        # Turn list of names into one space-separated string.
        actor["name"] = " ".join(actor["name"])

        actors.append(actor)
    return actors


def roll_and_organize_initiative_order(actors):
    # Roll and add bonus. Create clean list of actors for sorting.
    rolled_actors = []
    for actor in actors:
        # Creates list: [Group, Name]
        rolled = [actor["group"], actor["name"]]
        if not actor["flags"]:
            roll = d20()
        if "adv" in actor["flags"]:
            two_rolls = [d20() for _ in range(2)]
            roll = max(two_rolls)
        elif "disadv" in actor["flags"]:
            two_rolls = [d20() for _ in range(2)]
            roll = min(two_rolls)
        # Modifies list: [Score, Group, Name]
        rolled.insert(0, roll + actor["bonus"])
        rolled_actors.append(rolled)

    # Build tree to organize grouping and score conflicts.
    working_order = {}
    for actor in rolled_actors:
        score = actor[0]
        group = actor[1]
        name = actor[2]
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
    args = parser.parse_args()
    main(args)
