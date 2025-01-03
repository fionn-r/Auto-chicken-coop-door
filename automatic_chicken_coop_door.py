import time

from machine import Pin, deepsleep

DEBOUNCE_TIME_SECONDS = 1 * 60  # 1 minute

# Pin Definitions
STEP_PIN = 18
DIR_PIN = 19
INPUT_PIN = 25

# Stepper motor parameters
STEPS_PER_REV = 200
NUM_ROTATIONS = 10
STEPS_TO_MOVE = STEPS_PER_REV * NUM_ROTATIONS

step = Pin(STEP_PIN, Pin.OUT)
direction = Pin(DIR_PIN, Pin.OUT)
input_pin = Pin(INPUT_PIN, Pin.IN, Pin.PULL_DOWN)

is_door_currently_up: bool = False  # Always assume door is down at boot


def rotate_motor(steps: int, *, is_cw: bool) -> None:
    direction.value(is_cw)  # Set direction: 1 for CW, 0 for CCW
    for _ in range(steps):
        step.on()
        time.sleep_us(500)  # Adjust this delay to control speed (e.g., 500 µs)
        step.off()
        time.sleep_us(500)


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
    global is_door_currently_up
    # Clear IRQ while handling existing one
    input_pin.irq()

    print("Starting debounce check...")
    stable_state = debounce_input()

    if stable_state == is_door_currently_up:
        print("Door is already in desired position")
    else:
        if stable_state:
            print("Input stable at HIGH: Rotating CW")
            rotate_motor(steps=STEPS_TO_MOVE, is_cw=True)
        else:
            print("Input stable at LOW: Rotating CCW")
            rotate_motor(steps=STEPS_TO_MOVE, is_cw=False)
        is_door_currently_up = bool(stable_state)

    print("Entering deep sleep...")
    input_pin.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING)
    deepsleep()


main()
