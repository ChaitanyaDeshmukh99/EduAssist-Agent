import json
import streamlit as st
from prompts import QUIZ_GENERATOR_PROMPT, EVALUATOR_PROMPT

class QuizSystem:
    def __init__(self, tutor_client):
        self.tutor_client = tutor_client

    def generate_quiz(self, topic, profile):
        """Generates a JSON quiz based on topic and user profile."""
        if not self.tutor_client.client:
            return None

        prompt = QUIZ_GENERATOR_PROMPT.format(
            topic=topic,
            skill_level=profile.get("skill_level", "Beginner"),
            weak_topics=", ".join(profile.get("weak_topics", [])) or "None"
        )

        try:
            response = self.tutor_client.client.chat.completions.create(
                model=self.tutor_client.model,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            st.error(f"Error generating quiz: {str(e)}")
            return None

    def evaluate_quiz(self, quiz_data, user_answers, profile):
        """Evaluates quiz answers and provides feedback."""
        if not self.tutor_client.client:
            return "⚠️ LLM not available for evaluation."

        prompt = EVALUATOR_PROMPT.format(
            questions=json.dumps(quiz_data.get("questions", [])),
            user_answers=json.dumps(user_answers),
            skill_level=profile.get("skill_level", "Beginner")
        )

        try:
            response = self.tutor_client.client.chat.completions.create(
                model=self.tutor_client.model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ Error evaluating quiz: {str(e)}"
