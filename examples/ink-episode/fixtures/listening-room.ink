VAR disclosure_heard = false
VAR excerpt_shared = false

-> listening_room

=== listening_room ===
An archive listening room holds a recording and an empty envelope.
* {not disclosure_heard} [Hear the introduction]
    The voice is an imitation, not a recovered witness.
    ~ disclosure_heard = true
    -> listening_room
* {disclosure_heard} [Share the excerpt]
    ~ excerpt_shared = true
    You place the excerpt and its imitation notice in the envelope.
    -> END
+ [Leave the room]
    You return the headphones and leave the envelope open.
    -> END
