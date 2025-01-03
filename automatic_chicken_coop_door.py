import time

from machine import Pin, deepsleep
from stepper import Stepper

DEBOUNCE_TIME_SECONDS = 1 * 60  # 1 minute

# Pin Definitions
STEP_PIN = 18
DIR_PIN = 19
INPUT_PIN = 25

# Stepper motor parameters
STEPS_PER_REV = 200
NUM_ROTATIONS = 10
STEPS_TO_MOVE = STEPS_PER_REV * NUM_ROTATIONS

stepper = Stepper(STEP_PIN, DIR_PIN, steps_per_rev=STEPS_PER_REV, speed_sps=50)

input_pin = Pin(INPUT_PIN, Pin.IN, Pin.PULL_DOWN)


def rotate_motor(steps: int, *, is_cw: bool) -> None:
    if is_cw:
        stepper.step(steps)
    else:
        stepper.step(-steps)


def debounce_input() -> int:
    initial_state = input_pin.value()
    start_time = time.time()

    while time.time() - start_time < DEBOUNCE_TIME_SECONDS:
        if input_pin.value() != initial_state:
            print(
                "Input state changed during debounce period. Resetting debounce timer."
            )
            start_time = time.time()

    return input_pin.value()


def main() -> None:
    # Clear IRQ while handling existing one
    input_pin.irq()

    print("Starting debounce check...")
    stable_state = debounce_input()

    if stable_state:
        print("Input stable at HIGH: Rotating CW")
        rotate_motor(steps=STEPS_TO_MOVE, is_cw=True)
    else:
        print("Input stable at LOW: Rotating CCW")
        rotate_motor(steps=STEPS_TO_MOVE, is_cw=False)

    print("Entering deep sleep...")
    input_pin.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING)
    deepsleep()


main()
