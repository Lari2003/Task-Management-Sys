class Sequencer:
    """
    Generates unique IDs across the system.
    """
    _current_id = 1

    @classmethod
    def generate_sequence(cls):
        unique_id = cls._current_id
        cls._current_id += 1
        return unique_id

    @classmethod
    def reset(cls):
        cls._current_id = 1
