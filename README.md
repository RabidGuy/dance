Syntax overview:
```
# [comment]
@<group_name>
<name>: <bonus> [keyword]
insert <relative_path>
```

```
usage:

$ python dance.py cavern_entrance.init
22: Wolves
17: Danny
17: Goblin Mage
14: Prisoner, Brenna
 8: Guards
 7: Kyle
 3: John
```

```
# cavern_entrance.init

# Entrance to inhabited cavern

insert party_group
Prisoner: -1

@goblins
insert wolf_guards
Goblin Mage: 1
```

```
# party_group.init

@party
John: 0
Danny: 2 adv
Brenna: 1
Kyle: -1
```

```
# wolf_guards.init

Guards: 1
Wolves: 2
```