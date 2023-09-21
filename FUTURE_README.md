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
