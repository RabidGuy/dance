# Reducing File Complexity
I would like to see the addition of importing with macro replacements as well as improved options for commenting. Three files have been generated to illustrate what a user/gm might prepare for a game, and the resource files that they would archive for reuse.

Throughout these files, C-style comments are used without explanation. It is assumed that the reader is familiar with them.

## Prairie
The prairie scene pits our party against gnolls and their hyenas. A storm threatens all creatures in play.

### Input files
`prairie.init`

    # "inc/l_party"
    
    :gnolls
    # "inc/gnolls_with_hyenas"
     
    :environment
    Storm 5

`inc/l_party.init`

    :party
    Stub Hikels 4
    Donlof Dreamtide 3 adv
    Occepi 2
    // Greykurren 0
    Hurgan Garromarsh 0

`inc/gnolls_with_hyenas.init`

    Gnolls 1
    Hyenas 1

### Final version after macro expansion
    :party
    Stub Hikels 4
    Donlof Dreamtide 3 adv
    Occepi 2
    Hurgan Garromarsh 0
    
    :gnolls
    Gnolls 1
    Hyenas 1
     
    :environment
    Storm 5
    
### An explanation
The first line of `prairie.init` tells the program to include the party, which is located at `inc/l_party.init`. The file extension is left out. Inside this file, we find a label followed by five lines that define the party. One of those lines is commented out, but the label and four other definitions are inserted into the working version of our base file, verbatim.

Next, we see a new label that creates a group of gnolls. The following line includes content from `inc/gnolls_with_hyenas` which has two defintions and no labels. The label `:gnolls` is needed in the base file to ensure that unlabeled definitions aren't appended to the `:party` group.

The last part starts with an `:environment` label and a `Storm 5` definition. Both parts are written directly in the file without external references.

### Prairie - Conclusion
Labels and definitions can be combined with external references to create more organized files. Local content and external content will interact as though they're in a single document.

## Shady Meadow
The Shady Meadow presents a fight between our party and a group of berserkers lead by a veteran and their blood hawk.

### Input files
`shady_meadow.init`

    # "inc/l_party"

    :bandits
    # "inc/falconer" // Veteran, Blood Hawk
    # "inc/berserkers"

`inc/falconer.init`

    Veteran 3
    Falcon (Blood Hawk) 2

`inc/berserkers.init`

    Berserkers 1

### Final version after macro expansion
    :party
    Stub Hikels 4
    Donlof Dreamtide 3 adv
    Occepi 2
    Hurgan Garromarsh 0

    :bandits
    Veteran 3
    Falcon (Blood Hawk) 2
    Berserkers 1

### An explanation
We've included a pair of files that create a unique challenge, `inc/falconer.init` and `inc/berserkers.init`. Neither of these files contains a label, so we add `:bandits` immediately before their inclusion.

### Shady Meadow - Conclusion
It is possible to define many small combat elements and to quickly combine them to create more interesting situations. It would not be difficult to generate a set of ten random encounters for the region your players are heading into only by combining assets from your own archive.

    // A forest protector. Accepts no outsiders.
    # "inc/l_party"
    
    :guardian
    # "inc/druid"
    # "inc/owlbear"

... or ...

    // Heavy rain. Visibility is low and beasts are driven from their
    // flooded burrows. They're scared and ready to attack.
    # "inc/l_party"
    
    :wildlife
    # "inc/badgers"
    # "inc/boars"
    # "inc/snake_mix"

A large benefit to this method is the time saved keeping track of dexterity modifiers for each type of creature. It's also easy to make themed sets, such as `inc/snake_mix.init`.

## Burnt Courtyard
Our party enters the burnt courtyard and finds Rasilis waiting for them. He is accompanied by his familiar and his nephew. Several trained wolves sit nearby, waiting for the command to attack.

### Input files

`burnt_courtyard.init`

    # "inc/l_party"   // Has label.

    # "inc/l_rasilis" // Has label.
    # "inc/wolves"    // Does not have label.

`inc/l_rasilis.init`

    :rasilis
    Rasilis (Mage) 2
    Quasit 3
    Leydwen (Cult Fanatic) 2

`inc/wolves.init`

    Wolves 2

### Final version after macro expansion
    :party
    Stub Hikels 4
    Donlof Dreamtide 3 adv
    Occepi 2
    Hurgan Garromarsh 0

    :rasilis
    Rasilis (Mage) 2
    Quasit 3
    Leydwen (Cult Fanatic) 2
    Wolves 2

### An explanation
We've created a file that contains a recurring NPC and their two allies. We add to this group some interesting beasts from our archive. This encounter has continuity built into the primary opponent but also offers a unique challenge to other conflicts with this person.

By using a label within the NPCs file but not within the appended beast's, we automatically assign the beast to the NPCs group.

### Burnt Courtyard - Conclusion
Creating files for known NPCs, factions, and other named creatures allows you to make any number of fights with those entities without becoming stale. Your archive of creatures and packs becomes a toolbox for modifying threat levels while mainting a set of recurring characters.
