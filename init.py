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
    expanded_file = include(args.filename)
    # for line in expanded_file:
    #     print(line)
    return expanded_file


def include(filename, parentdir="."):
    expanded_file = []
    filepath = pathlib.Path(os.sep.join([parentdir, filename])).resolve()
    with open(filepath) as f:
        for line in f.readlines():
            terms = line.split()
            if not terms:
                continue
            elif terms[0].startswith("//"):
                continue
            elif terms[0] == "include":
                pd = os.path.dirname(filepath)
                expanded_file.extend(include(terms[1], pd))
            else:
                expanded_file.append(' '.join(terms))
    return expanded_file


def get_actors_from_tokens(lines):
    # XXX Does not enforce specific ordering of elements.
    # XXX     [<namewords>: <bonus> <keywords>]
    def get_actors(lines):
        for line in lines:
            yield line.split()
    tokens = get_actors(lines)
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


def roll_and_organize_initiative_order(actors, args):
    # Roll and add bonus. Create clean list of actors for sorting.
    rolled_actors = []
    for actor in actors:
        # Creates list: [Group, Name]
        rolled = {"group": actor["group"], "name": actor["name"]}
        if not actor["flags"]:
            roll = d20()
        if "adv" in actor["flags"]:
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
