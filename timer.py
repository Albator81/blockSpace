"""
# Timer Module

A module for a Timer class that provides functionality to manage a countdown timer.
## Classes:
- Timer: A class to create and manage a countdown timer with various time units.

## Methods:
```python
def __init__(self, *, milliseconds: float = 0., seconds: float = 0., minutes: float = 0.):
    # Initializes the Timer with the given time in milliseconds, seconds, and/or minutes.
def seconds_to_milliseconds(seconds: float) -> float:
    # Converts seconds to milliseconds.
def milliseconds_to_seconds(milliseconds: float) -> float:
    # Converts milliseconds to seconds.
def milliseconds_to_minutes(milliseconds: float) -> float:
    # Converts milliseconds to minutes.
def seconds_to_minutes(seconds: float) -> float:
    # Converts seconds to minutes.
def minutes_to_seconds(minutes: float) -> float:
    # Converts minutes to seconds.
def minutes_to_milliseconds(minutes: float) -> float:
    # Converts minutes to milliseconds.
def nanoseconds_to_milliseconds(nanoseconds: float) -> float:
    # Converts nanoseconds to milliseconds.
def check(self) -> None:
    # Checks if the timer has ended.
def start(self) -> None:
    # Starts or unpauses the timer.
def pause(self) -> None:
    # Pauses the timer.
def end(self) -> None:
    # Ends the timer.
def reset(self) -> None:
    # Resets the timer to its original time.
def restart(self) -> None:
    # Restarts the timer by resetting and starting it.
def is_running(self) -> bool:
    # Checks if the timer can be updated.
def manual_update(self, milliseconds_passed: float) -> None:
    # Manually updates the timer by subtracting the passed milliseconds.
def auto_update(self) -> None:
    # Automatically updates the timer based on the elapsed time.
def time_left_str(self) -> str:
    # Returns the remaining time as a formatted string.
```
"""
import time

class Timer:
    """
    ## Classes:
    - Timer: A class to create and manage a countdown timer with various time units.

    ## Methods:
    ```python
    def __init__(self, *, milliseconds: float = 0., seconds: float = 0., minutes: float = 0.):
        # Initializes the Timer with the given time in milliseconds, seconds, and/or minutes.
    def seconds_to_milliseconds(seconds: float) -> float:
        # Converts seconds to milliseconds.
    def milliseconds_to_seconds(milliseconds: float) -> float:
        # Converts milliseconds to seconds.
    def milliseconds_to_minutes(milliseconds: float) -> float:
        # Converts milliseconds to minutes.
    def seconds_to_minutes(seconds: float) -> float:
        # Converts seconds to minutes.
    def minutes_to_seconds(minutes: float) -> float:
        # Converts minutes to seconds.
    def minutes_to_milliseconds(minutes: float) -> float:
        # Converts minutes to milliseconds.
    def nanoseconds_to_milliseconds(nanoseconds: float) -> float:
        # Converts nanoseconds to milliseconds.
    def check(self) -> None:
        # Checks if the timer has ended.
    def start(self) -> None:
        # Starts or unpauses the timer.
    def pause(self) -> None:
        # Pauses the timer.
    def end(self) -> None:
        # Ends the timer.
    def reset(self) -> None:
        # Resets the timer to its original time.
    def restart(self) -> None:
        # Restarts the timer by resetting and starting it.
    def is_running(self) -> bool:
        # Checks if the timer can be updated.
    def manual_update(self, milliseconds_passed: float) -> None:
        # Manually updates the timer by subtracting the passed milliseconds.
    def auto_update(self) -> None:
        # Automatically updates the timer based on the elapsed time.
    def time_left_str(self) -> str:
        # Returns the remaining time as a formatted string.
    ```
    """
    def __init__(self, *, milliseconds: float = 0., seconds: float = 0., minutes: float = 0.):
        self._original_time = self.minutes_to_milliseconds(minutes) + self.seconds_to_milliseconds(seconds) + milliseconds
        self.reset()

    @staticmethod
    def seconds_to_milliseconds(seconds: float) -> float:
        return seconds * 1000
    @staticmethod
    def milliseconds_to_seconds(milliseconds: float) -> float:
        return milliseconds / 1000
    @staticmethod
    def milliseconds_to_minutes(milliseconds: float) -> float:
        return milliseconds / (1000 * 60)
    @staticmethod
    def seconds_to_minutes(seconds: float) -> float:
        return seconds / 60
    @staticmethod
    def minutes_to_seconds(minutes: float) -> float:
        return minutes * 60
    @staticmethod
    def minutes_to_milliseconds(minutes: float) -> float:
        return minutes * 60 * 1000
    @staticmethod
    def nanoseconds_to_milliseconds(nanoseconds: float) -> float:
        return nanoseconds / 1_000_000

    def check(self) -> None:
        if self._t_left < 0:
            self.has_ended = True

    def start(self) -> None:
        self._last_time = time.time_ns()
        """
        Start/Unpause the timer.
        """
        self.has_started = True
        self.is_paused = False
    def pause(self) -> None:
        """
        Pause the timer.
        """
        self.is_paused = True
    def end(self) -> None:
        """
        End the timer.
        """
        self.has_ended = True
        self._t_left = 0.
    def reset(self) -> None:
        self._t_left = self._original_time
        self.has_ended = False
        self.has_started = False
        self.is_paused = False
    def restart(self) -> None:
        self.reset()
        self.start()

    def is_running(self) -> bool:
        return self.has_started and not self.has_ended and not self.is_paused

    def manual_update(self, milliseconds_passed: float) -> None:
        if self.is_running():
            self._t_left -= milliseconds_passed
            self.check()
    def auto_update(self) -> None:
        if self.is_running():
            current_time = time.time_ns()
            elapsed_time = current_time - self._last_time
            self._last_time = current_time
            self._t_left -= self.nanoseconds_to_milliseconds(elapsed_time)
            self.check()

    def time_left_str(self) -> str:
        if self._t_left < 0:
            return "00:00:00:000"
        hours, milliseconds = divmod(self._t_left, 60 * 60 * 1000)
        minutes, milliseconds = divmod(milliseconds, 60 * 1000)
        seconds, milliseconds = divmod(milliseconds, 1000)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}:{int(milliseconds):03}"
