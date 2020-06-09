import time

from .multiple_synthesizer import MultipleSynthesizer
from ..enumerator import KTreeEnumerator
from ..logger import get_logger

logger = get_logger('forest.synthesizer')


class KTreeSynthesizer(MultipleSynthesizer):
    def __init__(self, valid_examples, invalid_examples, dsl, ground_truth,  pruning=True, auto_interaction=False):
        super().__init__(valid_examples, invalid_examples, dsl, ground_truth, pruning, auto_interaction)
        self.max_depth = 6

    def synthesize(self):
        self.start_time = time.time()

        for dep in range(3, self.max_depth + 1):
            logger.info(f'Synthesizing programs of depth {dep}...')
            self._enumerator = KTreeEnumerator(self.dsl, dep)

            self.try_for_depth()

            if len(self.programs) > 0:
                return self.programs[0]