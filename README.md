// [comment]

:<label>
<name> <bonus>

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
// cavern_entrance.init

// Entrance to inhabited cavern

include l_party.init
Prisoner -1

:goblins
include wolf_guards.init
Goblin Mage 1
```

```
// l_party.init

:party
John 0
Danny 2
Brenna 1
Kyle -1
```

```
// wolf_guards.init

Guards 1
Wolves 2
```