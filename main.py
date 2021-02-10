"""uPython Traffic Light State Machine"""

__author__ = "Howard C Lovatt"
__copyright__ = "Howard C Lovatt, 2021 onwards."
__license__ = "MIT https://opensource.org/licenses/MIT."
__repository__ = "https://github.com/hlovatt/upythonstatmechex"
__description__ = "``statmach`` traffic light example for MicroPython."
__version__ = "0.0.0"  # Version set by https://github.com/hlovatt/tag2ver

from statmach import StateWithValue, Machine


def main():
    class Inputs:  # 1. The inputs.
        RED_TIMEOUT = 0
        AMBER_TIMEOUT = 1
        GREEN_TIMEOUT = 2
        ERROR = 3

    class Outputs:  # 2. The outputs.
        RED = 0
        AMBER = 1
        GREEN = 2
        FLASHING_RED = 3

    flashing_red = StateWithValue(ident='flashing_red', value=Outputs.FLASHING_RED)  # 3. The states.
    red = StateWithValue(ident='red', value=Outputs.RED)
    amber = StateWithValue(ident='amber', value=Outputs.AMBER)
    green = StateWithValue(ident='green', value=Outputs.GREEN)

    red.actions[Inputs.RED_TIMEOUT] = green.action  # 4a. The *state* actions.
    green.actions[Inputs.GREEN_TIMEOUT] = amber.action
    amber.actions[Inputs.AMBER_TIMEOUT] = red.action

    with Machine(initial_state=red) as machine:  # 5. The machine.
        machine.actions[Inputs.RED_TIMEOUT] = flashing_red.action  # 4b. The *machine* actions.
        machine.actions[Inputs.AMBER_TIMEOUT] = flashing_red.action
        machine.actions[Inputs.GREEN_TIMEOUT] = flashing_red.action
        machine.actions[Inputs.ERROR] = flashing_red.action

        assert machine.state is red
        assert machine.fire(event=Inputs.RED_TIMEOUT) is Outputs.GREEN  # 6. Fire events and obtain outputs.
        assert machine.state is green
        assert machine.fire(event=Inputs.GREEN_TIMEOUT) is Outputs.AMBER
        assert machine.state is amber
        assert machine.fire(event=Inputs.AMBER_TIMEOUT) is Outputs.RED
        assert machine.state is red
        assert machine.fire(event=Inputs.AMBER_TIMEOUT) is Outputs.FLASHING_RED
        assert machine.state is flashing_red
        assert machine.fire(event=Inputs.ERROR) is Outputs.FLASHING_RED
        assert machine.state is flashing_red


if __name__ == '__main__':
    main()
