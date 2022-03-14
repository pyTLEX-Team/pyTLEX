"""
Represents the EVENT Tag.

We consider “events” a cover term for situations that happen or occur.
Events can be punctual or last for a period of time. We also
consider as events those predicates describing states or circumstances in
which something obtains or holds true. Not all stative predicates will be
marked up, however.

Written by: asing118
Last Updated by: vfern124
"""
from dataclasses import dataclass, field


@dataclass()
class Event:
    """
    May represent one of the following event classes:

    REPORTING - Describes the action of a person or an organization declaring something, narrating an event,
    informing about an event, etc.

    PERCEPTION - Events involving the physical perception of another event. Such events are typically
    expressed by verbs like: see, watch, glimpse, behold, view, hear, listen, overhear.

    ASPECTUAL - Grammatical device of aspectual predication.

    I_ACTION - An I_ACTION is an Intensional Action. An I ACTION introduces an event argument (which must be in the
    text explicitly) describing an action or situation from which we can infer something given its relation with
    the I_ACTION. Explicit performative predicates are also included here. Note that the I_ACTION class does not cover
    states.

    I_STATE - This class includes states that refer to alternative or possible worlds, (delimited by square brackets
    in the examples below), which can be introduced by subordinated clauses, nominalizations, or untensed VPs.

    STATE - States describe circumstances in which something obtains or holds true.

    OCCURRENCE - This class includes all the many other kinds of events describing something that happens or occurs
    in the world.
    """
    eid: int
    event_class: str
    stem: str = field(default=None)

    def __post_init__(self):
        if self.eid < 1:
            raise Exception("EventID cannot be less than 1.")

        if self.event_class is None:
            raise Exception("Event Class needs to be defined")

        accepted_event_classes = {"REPORTING", "PERCEPTION", "ASPECTUAL", "I_ACTION", "I_STATE", "STATE", "OCCURRENCE"}
        if self.event_class not in accepted_event_classes:
            raise Exception("That is not a valid Event Class - " + self.event_class)

        if self.stem is not None:
            self.stem = self.stem.strip()
            if len(self.stem) == 0:
                raise Exception("Stem cannot be empty or all whitespace.")

    # This is not necessary
    def get_id(self):
        """
        Returns the integer part of the eventId.
        Each event has to be identified by a unique ID number and String.
        """
        return self.eid

    def get_id_str(self):
        """
        Returns the full string representation of the eventID.
        Each event has to be identified by a unique ID number and String.
        """
        eid_str = "e" + str(self.eid)
        return eid_str

    # This is not necessary
    def get_stem(self):
        """
        Returns the stem of the event.
        """
        return self.stem

    # This is not necessary
    def get_event_class(self):
        """
        Returns the event class to which the object belongs.
        """
        return self.event_class

    def to_string(self):
        """
        Returns the Event information as a String.
        """
        event_string = "EVENT: eid = " + self.get_id_str() + ", class = " + str(self.get_event_class()) + ", stem = " \
                       + str(self.get_stem())
        return event_string

    def to_json(self):
        """
        Returns the JSON (RFC 8259) representation of the event.
        """
        if self.get_stem() is None:
            stem = "None"
        else:
            stem = self.get_stem()
        return "{\"id\":\"" + self.get_id_str() + "\", \"eventClass\":\"" + self.get_event_class() + \
               "\", \"stem\":\"" + stem + "\"}"
