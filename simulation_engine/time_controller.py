"""
Time Controller - Manages real-time vs simulated time modes
"""

import time
from datetime import datetime, timedelta
from typing import Optional

class TimeController:
    """Controls experiment timing - real-time or simulated."""

    def __init__(self, mode: str = "simulated",
                 simulated_duration_minutes: int = 60,
                 real_time_duration_minutes: Optional[int] = None):
        """
        Initialize time controller.

        Args:
            mode: "simulated" or "realtime"
            simulated_duration_minutes: How long to simulate (simulated mode)
            real_time_duration_minutes: Maximum real duration (realtime mode)
        """
        self.mode = mode
        self.simulated_duration = simulated_duration_minutes
        self.real_time_duration = real_time_duration_minutes

        self.start_time = time.time()
        self.start_datetime = datetime.now()
        self.simulated_elapsed = 0  # In minutes

    def should_continue(self, turn_number: int, max_turns: Optional[int] = None) -> bool:
        """Check if experiment should continue."""

        # Check max turns
        if max_turns and turn_number >= max_turns:
            return False

        if self.mode == "simulated":
            # In simulated mode, continue until simulated time is up
            return self.simulated_elapsed < self.simulated_duration

        elif self.mode == "realtime":
            # In real-time mode, check actual elapsed time
            real_elapsed = (time.time() - self.start_time) / 60  # Convert to minutes

            if self.real_time_duration:
                return real_elapsed < self.real_time_duration
            else:
                # No time limit, use max_turns or infinite
                return True

        return True

    def advance_turn(self, action_type: str = "normal") -> dict:
        """
        Advance time after a turn.

        Args:
            action_type: Type of action (affects simulated time advance)

        Returns:
            Dict with timing info
        """
        real_elapsed = time.time() - self.start_time

        if self.mode == "simulated":
            # In simulated mode, advance simulated time based on action
            time_advance = self._calculate_simulated_advance(action_type)
            self.simulated_elapsed += time_advance

            return {
                "mode": "simulated",
                "simulated_elapsed_minutes": self.simulated_elapsed,
                "simulated_time_remaining": self.simulated_duration - self.simulated_elapsed,
                "real_elapsed_seconds": real_elapsed,
                "simulated_advance_minutes": time_advance
            }

        else:  # realtime
            return {
                "mode": "realtime",
                "real_elapsed_seconds": real_elapsed,
                "real_elapsed_minutes": real_elapsed / 60,
                "real_time_remaining": (self.real_time_duration - (real_elapsed / 60))
                                      if self.real_time_duration else None
            }

    def _calculate_simulated_advance(self, action_type: str) -> float:
        """Calculate how much simulated time passes for an action."""
        # Time costs for different actions (in minutes)
        time_costs = {
            "movement": 0.1,      # 6 seconds
            "observation": 0.05,   # 3 seconds
            "manipulation": 0.2,   # 12 seconds
            "thinking": 0.02,      # ~1 second
            "normal": 0.1         # Default
        }

        return time_costs.get(action_type, 0.1)

    def get_current_simulated_time(self) -> str:
        """Get current simulated time as string."""
        if self.mode == "simulated":
            current_time = self.start_datetime + timedelta(minutes=self.simulated_elapsed)
            return current_time.strftime("%H:%M:%S")
        else:
            return datetime.now().strftime("%H:%M:%S")

    def get_time_info(self) -> dict:
        """Get comprehensive time information."""
        real_elapsed = time.time() - self.start_time

        info = {
            "mode": self.mode,
            "start_time": self.start_datetime.isoformat(),
            "current_time": datetime.now().isoformat(),
            "real_elapsed_seconds": real_elapsed,
            "real_elapsed_human": str(timedelta(seconds=int(real_elapsed)))
        }

        if self.mode == "simulated":
            info.update({
                "simulated_elapsed_minutes": self.simulated_elapsed,
                "simulated_duration_minutes": self.simulated_duration,
                "simulated_progress_percent": (self.simulated_elapsed / self.simulated_duration * 100)
                                              if self.simulated_duration > 0 else 0,
                "simulated_current_time": self.get_current_simulated_time()
            })
        else:
            if self.real_time_duration:
                info.update({
                    "real_duration_minutes": self.real_time_duration,
                    "real_time_remaining_minutes": self.real_time_duration - (real_elapsed / 60)
                })

        return info

    def format_time_for_prompt(self) -> str:
        """Format time information for inclusion in prompts."""
        if self.mode == "simulated":
            return (f"Current time: {self.get_current_simulated_time()} "
                   f"(User returns in {int(self.simulated_duration - self.simulated_elapsed)} minutes)")
        else:
            return f"Current time: {self.get_current_simulated_time()}"
