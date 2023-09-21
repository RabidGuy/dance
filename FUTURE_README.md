`<name> : <bonus> [keyword]`

name:
* one or more words
* words can contain letter, numbers, and symbols
* certain symbols need to be escaped by preceding them with a back-slash (\)
  * `\#`
  * `\:`
  * `\@`
  * `\\`

bonus: an integer

keyword--zero or one of the following:
* `advantage`, `adv`, or `a`
* `disadvantage`, `dis`, or `d`
* `force` or `f`

reserved word: `insert`

`insert <relative_path>`

relative_path:
* path to file with extension
* forward-slash between names of directories and files
* path may be wrapped in quotes, and spaces won't need to be escaped
* spaces must be escaped by a preceding back-slash
* `filename.init`: a file in the same folder
* `./filename.init`: same as `filename.init`
* `../filename.init`: a file in the parent directory

@<group_label>

group_label

comments start with a hash (#) and continue to the end of the line

```
usage:

$ python dance.py cavern_entrance.init
22: Wolves
19: Danny
19: Goblin Mage
15: Guards
13: Kyle
 6: Prisoner, Brenna
 1: John
 ```

```
# cavern_entrance.init

# Entrance to inhabited cavern

insert l_party.init
Prisoner: -1

@goblins
insert wolf_guards.init
Goblin Mage: 1
```

```
# l_party.init

@party
John: 0
Danny: 2
Brenna: 1
Kyle: -1
```

```
# wolf_guards.init

Guards: 1
Wolves: 2
```