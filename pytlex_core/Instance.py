# Written by: rgarc461
# Last Updated by: vfern124


from dataclasses import dataclass, field
from pytlex_core import Signal, Event

"""

Class to construct Instance objects with attributes of event_instance_id, event, tense, aspect, pos, polarity,
modality, signal, and cardinality. 

"""

@dataclass
class Instance:
    event_instance_id: int
    event: Event
    tense: str
    aspect: str
    pos: str
    polarity: str
    modality: str = field(default=None)
    signal: Signal = field(default=None)
    cardinality: str = field(default=None)

    def __post_init__(self):
        if self.event_instance_id < 1:
            raise ValueError("Event instance id cannot be less than 1.")

        if self.event is None:
            raise TypeError("Event can not be None")

        accepted_tenses = {"PAST", "PRESENT", "FUTURE", "NONE",	"INFINITIVE", "PRESPART", "PASTPART"}
        if self.tense not in accepted_tenses:
            raise TypeError(self.tense + " is not an acceptable tense.")

        accepted_aspects = {"PROGRESSIVE", "PERFECTIVE", "PERFECTIVE_PROGRESSIVE", "NONE"}
        if self.aspect not in accepted_aspects:
            raise TypeError(self.aspect + " is not an acceptable aspect.")

        accepted_pos = {"ADJECTIVE", "NOUN", "VERB", "PREPOSITION", "OTHER"}
        if self.pos not in accepted_pos:
            raise TypeError(self.pos + " is not an acceptable pos.")

        accepted_polarity = {"POS", "NEG"}
        if self.polarity not in accepted_polarity:
            raise TypeError(self.polarity + " is not an acceptable polarity")

        if self.modality is not None:
            self.modality = self.modality.strip()
            if len(self.modality) == 0:
                raise ValueError("Modality can not be empty string or all whitespace")

    def get_type(self):
        return self.get_event().get_event_class()

    def get_id_str(self):
        return "eiid" + str(self.event_instance_id)

    def to_json(self):
        ret = "{\"id\":\"" + self.get_id_str()
        ret += "\", \"tense\":\"" + self.tense
        ret += "\", \"aspect\":\"" + self.aspect
        ret += "\", \"partOfSpeech\":\"" + self.pos
        ret += "\", \"polarity\":\"" + self.polarity

        ret += "\", \"modality\":"
        if self.modality is not None:
            ret += self.modality
        else:
            ret += "null"

        ret += ", \"cardinality\":"
        if self.cardinality is not None:
            ret += self.cardinality
        else:
            ret += "null"

        ret += ", \"signal\":"
        if self.signal is not None:
            ret += self.get_signal().to_json()
        else:
            ret += "null"

        ret += ", \"event\":" + self.event.to_json() + "}"

        return ret

    def __hash__(self):
        return hash(self.get_id_str())


