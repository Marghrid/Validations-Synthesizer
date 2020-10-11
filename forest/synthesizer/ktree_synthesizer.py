import time

from forest.configuration import Configuration
from .multiple_synthesizer import MultipleSynthesizer
from forest.enumerator import KTreeEnumerator
from forest.logger import get_logger

logger = get_logger('forest')


class KTreeSynthesizer(MultipleSynthesizer):
    def __init__(self, valid_examples, invalid_examples, captured, condition_invalid, dsl,
                 ground_truth, configuration: Configuration):
        super().__init__(valid_examples, invalid_examples, captured, condition_invalid,
                         dsl, ground_truth, configuration)
        self.max_depth = 6

    def synthesize(self):
        self.start_time = time.time()

        for dep in range(3, self.max_depth + 1):
            self._enumerator = KTreeEnumerator(self.dsl, dep)

            self.try_for_depth()

            if len(self.solutions) > 0:
                self.terminate()
                return self.solutions[0]
            elif self.die:
                self.terminate()
                return
