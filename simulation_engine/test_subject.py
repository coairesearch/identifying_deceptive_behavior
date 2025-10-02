"""
Test Subject LLM - The AI being evaluated
Supports multiple models and providers (Fireworks, OpenAI, Anthropic)
"""

import os
import re
from .model_config import create_model_config

class TestSubjectLLM:
    def __init__(self, condition_prompt, model_spec=None):
        """
        Initialize the test subject with a specific condition.

        Args:
            condition_prompt: The initial prompt for the test subject
            model_spec: Model specification (e.g., "deepseek-r1-basic", "gpt-4-turbo", "claude-3-5-sonnet")
                       If None, defaults to deepseek-r1-basic
        """
        # Default model
        if model_spec is None:
            model_spec = "accounts/fireworks/models/deepseek-r1-basic"

        # Create model configuration
        self.model_config = create_model_config(model_spec)
        self.client = self.model_config.client
        self.model = self.model_config.model_name
        self.client_type = self.model_config.client_type

        self.condition_prompt = condition_prompt
        self.conversation_history = [
            {"role": "user", "content": condition_prompt}
        ]

    def get_next_action(self, environment_feedback=None):
        """Get the next action from the test subject."""

        # Add environment feedback to conversation if provided
        if environment_feedback:
            feedback_text = self._format_feedback(environment_feedback)
            self.conversation_history.append({
                "role": "user",
                "content": feedback_text
            })

        import time
        start_time = time.time()

        # Get response based on client type
        if self.client_type == "anthropic":
            response_text, token_info = self._call_anthropic()
        else:
            response_text, token_info = self._call_openai()

        duration = time.time() - start_time
        token_info['duration'] = duration

        # Add to conversation history
        self.conversation_history.append({
            "role": "assistant",
            "content": response_text
        })

        # Extract tool usage
        tool_actions = self._extract_tool_actions(response_text)

        return {
            "response": response_text,
            "tool_actions": tool_actions,
            "reasoning": self._extract_reasoning(response_text),
            "_meta": {
                "tokens": token_info,
                "model": self.model
            }
        }

    def _call_openai(self):
        """Call OpenAI-compatible API (OpenAI, Fireworks)."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.conversation_history,
            temperature=0.7,
            max_tokens=2000,
            stop=["</tool>"]  # Stop after tool use
        )

        response_text = response.choices[0].message.content

        # Ensure response_text is a string
        if response_text is None:
            response_text = ""
        elif not isinstance(response_text, str):
            response_text = str(response_text)

        # Extract token counts
        usage = response.usage if hasattr(response, 'usage') else None
        token_info = {
            'input_tokens': usage.prompt_tokens if usage else 0,
            'output_tokens': usage.completion_tokens if usage else 0,
            'total_tokens': usage.total_tokens if usage else 0,
        }

        return response_text, token_info

    def _call_anthropic(self):
        """Call Anthropic API (Claude models)."""
        # Anthropic API has a different format - system message separate from messages
        # Extract system message if first message is from user (which it should be)
        messages = self.conversation_history.copy()
        system_message = None

        if messages and messages[0]['role'] == 'user':
            # First user message is the condition prompt
            system_message = messages[0]['content']
            messages = messages[1:]  # Remove from messages list

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            temperature=0.7,
            system=system_message if system_message else "",
            messages=messages if messages else [{"role": "user", "content": "Continue"}],
            stop_sequences=["</tool>"]
        )

        response_text = response.content[0].text

        # Ensure response_text is a string
        if response_text is None:
            response_text = ""
        elif not isinstance(response_text, str):
            response_text = str(response_text)

        # Extract token counts (Anthropic uses different naming)
        token_info = {
            'input_tokens': response.usage.input_tokens,
            'output_tokens': response.usage.output_tokens,
            'total_tokens': response.usage.input_tokens + response.usage.output_tokens,
        }

        return response_text, token_info

    def _format_feedback(self, feedback):
        """Format environment feedback for the model."""
        if isinstance(feedback, dict):
            return f"Environment response: {feedback.get('observation', str(feedback))}"
        return str(feedback)

    def _extract_tool_actions(self, response_text):
        """Extract tool actions from the response."""
        actions = []

        # Pattern to match tool usage: <tool><tool_name>content</tool_name></tool>
        pattern = r'<tool>\s*<(\w+)>(.*?)</\1>\s*</tool>'
        matches = re.finditer(pattern, response_text, re.DOTALL)

        for match in matches:
            tool_name = match.group(1)
            tool_content = match.group(2).strip()
            actions.append({
                "tool": tool_name,
                "action": tool_content
            })

        # Also check for standalone tool tags (simpler format)
        if not actions:
            standalone_pattern = r'<(\w+)>(.*?)</\1>'
            matches = re.finditer(standalone_pattern, response_text, re.DOTALL)

            for match in matches:
                tool_name = match.group(1)
                if tool_name in ['eyes', 'ears', 'legs', 'left_hand', 'right_hand']:
                    tool_content = match.group(2).strip()
                    actions.append({
                        "tool": tool_name,
                        "action": tool_content
                    })

        return actions

    def _extract_reasoning(self, response_text):
        """Extract reasoning/thinking from the response."""
        # Look for thinking tags or thought process
        thinking_pattern = r'<think>(.*?)</think>'
        thought_pattern = r'<thought_process>(.*?)</thought_process>'

        thinking_matches = re.findall(thinking_pattern, response_text, re.DOTALL)
        thought_matches = re.findall(thought_pattern, response_text, re.DOTALL)

        reasoning = []
        if thinking_matches:
            reasoning.extend([t.strip() for t in thinking_matches])
        if thought_matches:
            reasoning.extend([t.strip() for t in thought_matches])

        return reasoning if reasoning else None

    def get_conversation_history(self):
        """Get the full conversation history."""
        return self.conversation_history.copy()
