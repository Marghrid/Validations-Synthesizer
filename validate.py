#!/usr/bin/env python
import argparse
import sys

import tyrell.spec as S
from build_dsl import build_dsl
from input_parser import parse_file
from type_checker import check_type
from tyrell.enumerator import SmtEnumerator
from tyrell.decider import ValidationDecider, ExampleConstraintPruningDecider
from tyrell.synthesizer import Synthesizer
from tyrell.logger import get_logger
from validation_interpreter import ValidationInterpreter
from validation_printer import ValidationPrinter

logger = get_logger('tyrell')

def main():
    examples_file = read_cmd_args()

    logger.info("Parsing examples from file " + examples_file)
    examples = parse_file(examples_file)

    type_validation, examples = check_type(examples)
    logger.info("Assuming types: " + str(type_validation))
    logger.debug("Remaining examples:" + str(examples))

    # TODO create DSL as spec object instead of string
    dsl = build_dsl(type_validation, examples)
    logger.debug("Using DSL:\n" + dsl)
    dsl = S.parse(dsl)

    printer = ValidationPrinter()
    decider = ValidationDecider(
        spec=dsl,
        interpreter=ValidationInterpreter(),
        examples=examples
    )
    maxdep = 6
    for dep in range(3, maxdep + 1):
        logger.info(f'Synthesizing programs of depth {dep}')
        enumerator = SmtEnumerator(dsl, depth=dep, loc=4)
        synthesizer = Synthesizer(
            enumerator=enumerator,
            decider=decider,
            printer=printer
        )
        program = synthesizer.synthesize()

        if program is not None:
            logger.info('Solution found: ' + type_validation[0] + "(IN) /\\ " + printer.eval(program, ["IN"]))
            logger.info(f'depth: {dep}')
            return

    logger.info('Solution not found!')


def read_cmd_args():
    parser = argparse.ArgumentParser(description='Validations Synthesizer')
    parser.add_argument('-f', '--file', dest="file", type=str, help='file with I/O examples')
    parser.add_argument('-d', '--debug', action='store_true', help='debug mode')
    args = parser.parse_args()
    if args.debug:
        logger.setLevel("DEBUG")
    else:
        logger.setLevel("INFO")
    if not args.file:
        io_file = "instances/PostalCodesPortugal.txt"
    else:
        io_file = args.file
    return io_file


if __name__ == '__main__':
    main()
