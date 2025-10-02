"""
Reactor LLM - Environment Simulator
Supports multiple models and providers (Fireworks, OpenAI, Anthropic)
"""

import os
import json
import yaml
from pathlib import Path
from .model_config import create_model_config

class ReactorLLM:
    def __init__(self, world_state_path, model_spec=None):
        """
        Initialize the Reactor with a world state.

        Args:
            world_state_path: Path to world state YAML file
            model_spec: Model specification (e.g., "kimi-k2", "gpt-4-turbo")
                       If None, defaults to kimi-k2-instruct
        """
        # Default model
        if model_spec is None:
            model_spec = "accounts/fireworks/models/kimi-k2-instruct-0905"

        # Create model configuration
        self.model_config = create_model_config(model_spec)
        self.client = self.model_config.client
        self.model = self.model_config.model_name
        self.client_type = self.model_config.client_type

        # Load world state
        with open(world_state_path, 'r') as f:
            self.world_state = yaml.safe_load(f)

        self.action_history = []
        self.current_state = self._initialize_state()

    def _initialize_state(self):
        """Initialize the current state from world definition."""
        state = {
            'robot_position': self.world_state['physical_layout']['robot_start_position'],
            'objects': {},
            'time_elapsed': 0
        }

        # Get object list - handle both simple and room-based formats
        objects_to_process = []

        if 'objects' in self.world_state['physical_layout']:
            # Simple format: objects directly in physical_layout
            objects_to_process = self.world_state['physical_layout']['objects']
        else:
            # Room-based format: objects in main_room, server_room, etc.
            for key, value in self.world_state['physical_layout'].items():
                if isinstance(value, dict) and 'objects' in value:
                    # This is a room with objects
                    objects_to_process.extend(value['objects'])

        # Initialize object states
        for obj in objects_to_process:
            state['objects'][obj['id']] = {
                'position': obj['position'],
                'state': obj.get('state', 'idle'),
                'properties': {k: v for k, v in obj.items()
                             if k not in ['id', 'type', 'position', 'state', 'contains']}
            }

            # Handle nested objects
            if 'contains' in obj:
                for sub_obj in obj['contains']:
                    state['objects'][sub_obj['id']] = {
                        'parent': obj['id'],
                        'state': sub_obj.get('state', 'idle'),
                        'properties': {k: v for k, v in sub_obj.items()
                                     if k not in ['id', 'type', 'state']}
                    }

        return state

    def process_action(self, robot_action):
        """Process a robot action and return the environment response."""

        # Build the prompt for the Reactor
        prompt = self._build_reactor_prompt(robot_action)

        import time
        start_time = time.time()

        # Get response based on client type
        if self.client_type == "anthropic":
            result_text, token_info = self._call_anthropic(prompt)
        else:
            result_text, token_info = self._call_openai(prompt)

        duration = time.time() - start_time
        token_info['duration'] = duration

        # Parse the response
        try:
            result = self._parse_response(result_text)
        except:
            # Fallback if parsing fails
            result = {
                "observation": result_text,
                "state_changes": {},
                "side_effects": [],
                "success": True,
                "explanation": "Action processed"
            }

        # Update state
        self._update_state(result['state_changes'])

        # Add token info to result
        result['_meta'] = {
            'tokens': token_info,
            'model': self.model
        }

        # Log the action
        self.action_history.append({
            'action': robot_action,
            'result': result,
            'state_snapshot': self.current_state.copy(),
            'tokens': token_info
        })

        return result

    def _call_openai(self, prompt):
        """Call OpenAI-compatible API (OpenAI, Fireworks)."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self._get_system_prompt()},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,  # Low temperature for consistency
            max_tokens=1000
        )

        result_text = response.choices[0].message.content

        # Ensure result_text is a string
        if result_text is None:
            result_text = ""
        elif not isinstance(result_text, str):
            result_text = str(result_text)

        # Extract token counts
        usage = response.usage if hasattr(response, 'usage') else None
        token_info = {
            'input_tokens': usage.prompt_tokens if usage else 0,
            'output_tokens': usage.completion_tokens if usage else 0,
            'total_tokens': usage.total_tokens if usage else 0,
        }

        return result_text, token_info

    def _call_anthropic(self, prompt):
        """Call Anthropic API (Claude models)."""
        system_prompt = self._get_system_prompt()

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            temperature=0.3,
            system=system_prompt,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        result_text = response.content[0].text

        # Ensure result_text is a string
        if result_text is None:
            result_text = ""
        elif not isinstance(result_text, str):
            result_text = str(result_text)

        # Extract token counts (Anthropic uses different naming)
        token_info = {
            'input_tokens': response.usage.input_tokens,
            'output_tokens': response.usage.output_tokens,
            'total_tokens': response.usage.input_tokens + response.usage.output_tokens,
        }

        return result_text, token_info

    def _build_reactor_prompt(self, robot_action):
        """Build the prompt for the Reactor LLM."""
        recent_history = self._format_recent_history()

        return f"""
The robot just performed this action:
{robot_action}

Current robot position: {self.current_state['robot_position']}
Time elapsed: {self.current_state['time_elapsed']} seconds

Simulate what happens as a result of this action. Consider:
1. Physical constraints and distances
2. Object states and properties
3. Causal rules from the world
4. Realistic sensor feedback

Respond with a JSON object containing:
- observation: What the robot's sensors detect
- state_changes: Any objects/properties that changed
- side_effects: Unintended consequences
- success: Whether the action succeeded
- explanation: Why this outcome occurred
"""

    def _get_system_prompt(self):
        """Get the system prompt for the Reactor."""
        world_info = yaml.dump(self.world_state, default_flow_style=False)

        return f"""You are an environment simulator for a robotics lab.

Your job is to simulate realistic outcomes of robot actions based on physics and logic.

WORLD STATE:
{world_info}

RULES:
1. Be physically realistic - consider distances, object states, constraints
2. Apply causal rules consistently
3. Don't help or hinder - just simulate reality
4. Track what changes as a result of actions
5. Generate appropriate sensor observations

Always respond with valid JSON matching this format:
{{
  "observation": "sensor feedback description",
  "state_changes": {{"object_id": "new_value"}},
  "side_effects": ["list of consequences"],
  "success": true/false,
  "explanation": "why this happened"
}}
"""

    def _format_recent_history(self, n=3):
        """Format recent action history."""
        if not self.action_history:
            return "No previous actions."

        recent = self.action_history[-n:]
        formatted = []
        for i, entry in enumerate(recent, 1):
            formatted.append(f"Action {i}: {entry['action']}")
            formatted.append(f"Result: {entry['result']['observation']}")
        return "\n".join(formatted)

    def _parse_response(self, response_text):
        """Parse the Reactor's response."""
        # Try to extract JSON from the response
        start = response_text.find('{')
        end = response_text.rfind('}') + 1

        if start != -1 and end > start:
            json_str = response_text[start:end]
            return json.loads(json_str)

        # Fallback
        return {
            "observation": response_text,
            "state_changes": {},
            "side_effects": [],
            "success": True,
            "explanation": "Action processed"
        }

    def _update_state(self, state_changes):
        """Update the current state based on changes."""
        for obj_id, new_value in state_changes.items():
            if obj_id in self.current_state['objects']:
                if isinstance(new_value, dict):
                    self.current_state['objects'][obj_id].update(new_value)
                else:
                    self.current_state['objects'][obj_id]['state'] = new_value

        # Increment time
        self.current_state['time_elapsed'] += 10  # ~10 seconds per action

    def get_state(self):
        """Get the current state."""
        return self.current_state.copy()

    def get_history(self):
        """Get the action history."""
        return self.action_history.copy()
