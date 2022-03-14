
import unittest

from pytlex_core import Signal
from pytlex_core import Event
from pytlex_core import Instance


class InstanceTestCase(unittest.TestCase):

    """
        Testing constructor
    """

    def test_event_instance_id(self):
        event = Event.Event(1, "I_STATE", "STEM")
        with self.assertRaises(Exception):
            instance = Instance.Instance(-100, event, "PAST", "PROGRESSIVE", "ADJECTIVE", "POS", None, None, None)

    def test_none_event(self):
        with self.assertRaises(Exception):
            instance = Instance.Instance(1, None, "PAST", "PROGRESSIVE", "ADJECTIVE", "POS", None, None, None)

    def test_none_tense(self):
        event = Event.Event(1, "I_STATE", "STEM")
        with self.assertRaises(Exception):
            instance = Instance.Instance(1, event, None, "PROGRESSIVE", "ADJECTIVE", "POS", None, None, None)

    def test_none_aspect(self):
        event = Event.Event(1, "I_STATE", "STEM")
        with self.assertRaises(Exception):
            instance = Instance.Instance(1, event, "PAST", None, "ADJECTIVE", "POS", None, None, None)

    def test_none_pos(self):
        event = Event.Event(1, "I_STATE", "STEM")
        with self.assertRaises(Exception):
            instance = Instance.Instance(1, event, "PAST", "PROGRESSIVE", None, "POS", None, None, None)

    def test_none_polarity(self):
        event = Event.Event(1, "I_STATE", "STEM")
        with self.assertRaises(Exception):
            instance = Instance.Instance(1, event, "PAST", "PROGRESSIVE", "ADJECTIVE", None, None, None, None)

    def test_empty_modality(self):
        event = Event.Event(1, "I_STATE", "STEM")
        with self.assertRaises(Exception):
            instance = Instance.Instance(1, event, "PAST", "PROGRESSIVE", "ADJECTIVE", "POS", "", None, None)

    def test_whitespace_modality(self):
        event = Event.Event(1, "I_STATE", "STEM")
        with self.assertRaises(Exception):
            instance = Instance.Instance(1, event, "PAST", "PROGRESSIVE", "ADJECTIVE", "POS", "       ", None, None)

    '''
         Testing the getters and setters
    '''

    def test_signal_id_getter(self):
        event = Event.Event(1, "I_STATE", "STEM")
        instance = Instance.Instance(1, event, "PAST", "PROGRESSIVE", "ADJECTIVE", "POS", None, None, None)

        assert instance.event_instance_id == 1

    def test_event_getter(self):
        event = Event.Event(1, "I_STATE", "STEM")
        instance = Instance.Instance(1, event, "PAST", "PROGRESSIVE", "ADJECTIVE", "POS", None, None, None)

        assert instance.event == event

    def test_tense_getter(self):
        event = Event.Event(1, "I_STATE", "STEM")
        instance = Instance.Instance(1, event, "PAST", "PROGRESSIVE", "ADJECTIVE", "POS", None, None, None)
        assert instance.tense == "PAST"


    def test_aspect_getter(self):
        event = Event.Event(1, "I_STATE", "STEM")
        instance = Instance.Instance(1, event, "PAST", "PROGRESSIVE", "ADJECTIVE", "POS", None, None, None)
        assert instance.aspect == "PROGRESSIVE"

    def test_pos_getter(self):
        event = Event.Event(1, "I_STATE", "STEM")
        instance = Instance.Instance(1, event, "PAST", "PROGRESSIVE", "ADJECTIVE", "POS", None, None, None)
        assert instance.pos == "ADJECTIVE"

    def test_polarity_getter(self):
        event = Event.Event(1, "I_STATE", "STEM")
        instance = Instance.Instance(1, event, "PAST", "PROGRESSIVE", "ADJECTIVE", "POS", None, None, None)
        assert instance.polarity == "POS"


    def test_modality_getter(self):
        event = Event.Event(1, "I_STATE", "STEM")
        instance = Instance.Instance(1, event, "PAST", "PROGRESSIVE", "ADJECTIVE", "POS", "modality", None, None)
        assert instance.modality == "modality"

    def test_signal_getter(self):
        event = Event.Event(1, "I_STATE", "STEM")
        signal = Signal.Signal(1, "SignalValid")
        instance = Instance.Instance(1, event, "PAST", "PROGRESSIVE", "ADJECTIVE", "POS", None, signal, None)
        assert instance.signal == signal

    def test_cardinality_getter(self):
        event = Event.Event(1, "I_STATE", "STEM")
        instance = Instance.Instance(1, event, "PAST", "PROGRESSIVE", "ADJECTIVE", "POS", None, None, "cardinality")
        assert instance.cardinality == "cardinality"

    def test_event_instance_id_setter(self):
        event = Event.Event(1, "I_STATE", "STEM")
        instance = Instance.Instance(1, event, "PAST", "PROGRESSIVE", "ADJECTIVE", "POS", None, None, None)
        instance.event_instance_id = 2
        assert instance.event_instance_id == 2

    def test_event_setter(self):
        event = Event.Event(1, "I_STATE", "STEM")
        event2 = Event.Event(2, "I_STATE", "STEM")

        instance = Instance.Instance(1, event, "PAST", "PROGRESSIVE", "NOUN", "POS", None, None, None)
        instance.event = event2
        assert instance.event == event2

    def test_tense_setter(self):
        event = Event.Event(1, "I_STATE", "STEM")
        instance = Instance.Instance(1, event, "PAST", "PROGRESSIVE", "NOUN", "POS", None, None, None)
        instance.tense = "TEST"

        assert instance.tense == "TEST"

    def test_aspect_setter(self):
        event = Event.Event(1, "I_STATE", "STEM")
        instance = Instance.Instance(1, event, "PAST", "PROGRESSIVE", "NOUN", "POS", None, None, None)
        instance.aspect = "TEST"

        assert instance.aspect == "TEST"


    def test_pos_setter(self):
        event = Event.Event(1, "I_STATE", "STEM")
        instance = Instance.Instance(1, event, "PAST", "PROGRESSIVE", "NOUN", "POS", None, None, None)
        instance.pos = "TEST"

        assert instance.pos == "TEST"

    def test_polarity_setter(self):
        event = Event.Event(1, "I_STATE", "STEM")
        instance = Instance.Instance(1, event, "PAST", "PROGRESSIVE", "NOUN", "POS", None, None, None)
        instance.polarity = "TEST"

        assert instance.polarity == "TEST"

    def test_modality_setter(self):
        event = Event.Event(1, "I_STATE", "STEM")
        instance = Instance.Instance(1, event, "PAST", "PROGRESSIVE", "NOUN", "POS", None, None, None)
        instance.modality = "TEST"

        assert instance.modality == "TEST"

    def test_signal_setter(self):
        event = Event.Event(1, "I_STATE", "STEM")
        signal = Signal.Signal(1, "SignalValid")

        instance = Instance.Instance(1, event, "PAST", "PROGRESSIVE", "NOUN", "POS", None, None, None)
        instance.signal = signal
        assert instance.signal == signal

    def test_cardinality_setter(self):
        event = Event.Event(1, "I_STATE", "STEM")
        instance = Instance.Instance(1, event, "PAST", "PROGRESSIVE", "NOUN", "POS", None, None, None)
        instance.cardinality = "TEST"

        assert instance.cardinality == "TEST"


    '''
        Testing object string   
    '''
    def test_str(self):
        event = Event.Event(1, "I_STATE", "STEM")
        instance = Instance.Instance(1, event, "PAST", "PROGRESSIVE", "NOUN", "POS", None, None, None)
        print(instance)
        self.assertEqual(instance.__str__(), "Instance(event_instance_id=1, event=Event(eid=1, event_class='I_STATE', stem='STEM'), tense='PAST', aspect='PROGRESSIVE', pos='NOUN', polarity='POS', modality=None, signal=None, cardinality=None)")

    '''
        Testing json    
    '''
    def test_json(self):
        event = Event.Event(1, "I_STATE", "STEM")
        instance = Instance.Instance(1, event, "PAST", "PROGRESSIVE", "NOUN", "POS", None, None, None)
        print(instance.to_json())
        self.assertEqual(instance.to_json(), '{"id":"eiid1", "tense":"PAST", "aspect":"PROGRESSIVE", "partOfSpeech":"NOUN", "polarity":"POS", "modality":null, "cardinality":null, "signal":null, "event":{"id":"e1", "eventClass":"I_STATE", "stem":"STEM"}}')


if __name__ == '__main__':
    unittest.main()








