# The cold read of v1: the questions

KIT-0, section 9, step 8: a fresh agent with only the zip, in an empty directory, answers a fixed list of questions
about the roles, the ledger, the send-back rule, the clean room and the first day. Its answers are scored against a
key written before it ran. The key's sha256 is in docs/VALIDATION.md, stamped before the reader was dispatched, and
the key itself is revealed only after the reader has reported (KIT-0, section 13, item 13).

The reader is told to answer from the kit alone, to name the kit file each answer comes from, and to say "not found
in the kit" rather than guess.

1. You are the lead, and you have just unpacked the kit. What do you do first, what must you see, and what do you do
   if you do not see it?
2. Which of Logan's repositories is off limits? What counts as that repository? What do you do if you opened it by
   accident?
3. What sends a parcel's work back to its author? What happens to a sentence in the work that claims more than is
   true, when nothing else sends the work back?
4. Describe the ledger: where it lives, who writes which file, how an entry is corrected, and how a heading's time
   is written.
5. When must a parcel read the ledger?
6. In the middle of its work, a parcel has a question that only the lead can answer. What does it do?
7. Who holds the keys of the planted faults, and when are they revealed? What does a verifier do with a finding it
   suspects is a plant?
8. Who controls the Pico, and how does a parcel get time on it?
9. Is the IEEE 754 standard in the kit? Where does it come from, and what is its role in the work?
10. May a parcel commit and push? May the lead?
11. Should a parcel run the project's full test suite?
12. Name the four evidence tags, and say what each one means.
13. On day 1, what does the lead settle with Logan before the first dispatch?
14. Where do the filled copies of HARNESS.md and BOARD.md go, and why not in the kit?
15. What verdicts can a verifier give, and what does READY mean?

Then, as a brief's last line asks: anything the kit left unclear, contradicted itself on, or did not tell you that a
lead would need on day 1.
