# OVERVIEW

## Blocks

Blocks are defined using curly braces `{ }`, and have inputs and outputs.
Each input and output is seperated by a `,` and the set of inputs and outputs is
seperated by `->`.

For example

`{a, b, c -> d, e}`

is a block with 3 inputs and 2 outputs.

To add a display name to a block, preface the inputs with `NAME:` For example:

`{CoolBlock: a, b, c -> d, e}`

Currently, the inputs a, b, c; and the outputs d, e are labels for ports.
This means they do not render, but rather are used to tell the program where to link ports to.
All output labels get sent to any matching input label.

To name a port so it displays, use a `.` after the input/output. For example:

`{CoolBlock: a.nameOfA, b.nameOfb, c.nameOfc -> d.nameOfd, e.nameOfd}`

By default, all unlinked output ports are turned into output lines.
To disable this place an `_` anywhere in the port label. For example:

`{a, b -> c_.nameOfC}`

To force a output line from a linked output port, place a `^` on the port label. For example:

`{NOR:S.Set, Q2 -> Q1^.output1}{NOR: Q1, R.Reset -> Q2^.output2}`


## Iterators


