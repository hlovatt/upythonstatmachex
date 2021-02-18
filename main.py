"""uPython Traffic Light State Machine."""

__author__ = "Howard C Lovatt"
__copyright__ = "Howard C Lovatt, 2021 onwards."
__license__ = "MIT https://opensource.org/licenses/MIT."
__repository__ = "https://github.com/hlovatt/upythonstatmachex"
__description__ = "``statmach`` traffic light example for MicroPython."
__version__ = "1.0.3"  # Version set by https://github.com/hlovatt/tag2ver

from statmach import State, Machine
from pyb import LED, Timer, wfi, Switch
from micropython import alloc_emergency_exception_buf, schedule

alloc_emergency_exception_buf(200)


def main():
    print('Traffic lights running ...')

    class Events:
        RED_TIMEOUT = 1
        AMBER_TIMEOUT = 2
        GREEN_TIMEOUT = 3
        ERROR = 4
        START = 5

    start = State(ident='start')  # Special start state to allow for initialization before operation.

    timer0 = 10

    class FlashingRed(State):  # Special fault state that should never exit.
        def __init__(self):
            super().__init__(ident='error')
            self.timer = Timer(timer0 + 4)
            self.led = LED(1)

            # noinspection PyUnusedLocal
            def toggle_with_arg(not_used):  # Toggle func that accepts an arg, because ``schedule`` *needs* an arg.
                self.led.toggle()

            self.led_tog_ref = toggle_with_arg  # Store the function reference locally to avoid allocation in interrupt.

        def __enter__(self):
            self.timer.init(freq=2, callback=lambda _: schedule(self.led_tog_ref, None))
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.led.off()
            self.timer.deinit()

    flashing_red = FlashingRed()

    traffic_lights = Machine(initial_state=start)  # The traffic light machine.
    traffic_lights.actions[Events.RED_TIMEOUT] = flashing_red.action  # Catch anything unexpected.
    traffic_lights.actions[Events.AMBER_TIMEOUT] = flashing_red.action
    traffic_lights.actions[Events.GREEN_TIMEOUT] = flashing_red.action
    traffic_lights.actions[Events.ERROR] = flashing_red.action
    traffic_lights.actions[Events.START] = flashing_red.action

    tl_fire_ref = traffic_lights.fire  # Store the function reference locally to avoid allocation in interrupt.
    error = Switch()
    error.callback(lambda: schedule(tl_fire_ref, Events.ERROR))

    class LEDState(State):  # Output is determined by ``__enter__`` and ``__exit__`` (common in embedded machines).
        def __init__(self, led_num, time_on, event):
            super().__init__(ident=led_num)  # Use the LED num as the ident.
            self.led = LED(self.ident)  # The LED to use.
            self.timer = Timer(timer0 + self.ident)  # The timer to use.
            self.timeout = time_on  # Time to wait before firing event.
            self.event = event  # Event to fire at end of time_on.

        def __enter__(self):
            self.led.on()
            self.timer.init(freq=1 / self.timeout, callback=lambda _: schedule(tl_fire_ref, self.event))
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            self.led.off()
            self.timer.deinit()
            return False

    red = LEDState(led_num=1, time_on=3, event=Events.RED_TIMEOUT)
    green = LEDState(led_num=2, time_on=3, event=Events.GREEN_TIMEOUT)
    amber = LEDState(led_num=3, time_on=0.5, event=Events.AMBER_TIMEOUT)

    red.actions[Events.RED_TIMEOUT] = green.action
    green.actions[Events.GREEN_TIMEOUT] = amber.action
    amber.actions[Events.AMBER_TIMEOUT] = red.action
    start.actions[Events.START] = red.action

    with traffic_lights:
        _ = traffic_lights.fire(event=Events.START)  # Start the machine once all the setup is complete.
        while True:  # Keep running timers (and other peripherals), but otherwise do nothing.
            wfi()


if __name__ == '__main__':
    main()
