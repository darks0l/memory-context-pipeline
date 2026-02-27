import unittest

from skill.scripts.context_router import decide, estimate_tokens


class TestContextRouter(unittest.TestCase):
    def test_estimate_tokens_minimum(self):
        self.assertEqual(estimate_tokens(0), 1)

    def test_premium_default_for_general_small_input(self):
        result = decide(task="general", chars=4000, threshold=10000)
        self.assertEqual(result["route"], "premium")
        self.assertEqual(result["model"], "opus")
        self.assertEqual(result["fallback_chain"], ["opus"])

    def test_local_for_known_local_task(self):
        result = decide(task="summarize", chars=1200, threshold=10000)
        self.assertEqual(result["route"], "local")
        self.assertEqual(result["model"], "lfm2")
        self.assertIn("task:summarize", result["decision_trace"])

    def test_local_for_threshold_trigger(self):
        # 40000 chars ~= 10800 tokens via heuristic
        result = decide(task="general", chars=40000, threshold=10000)
        self.assertEqual(result["route"], "local")
        self.assertEqual(result["model"], "lfm2")
        self.assertTrue(any("token_threshold" in r for r in result["decision_trace"]))

    def test_vision_route_on_has_image(self):
        result = decide(task="general", chars=800, threshold=10000, has_image=True)
        self.assertEqual(result["route"], "local")
        self.assertEqual(result["model"], "qwen3-vl")
        self.assertIn("multimodal_branch", result["decision_trace"])

    def test_vision_route_on_vision_task(self):
        result = decide(task="ocr-extract", chars=600, threshold=10000)
        self.assertEqual(result["route"], "local")
        self.assertEqual(result["model"], "qwen3-vl")


if __name__ == "__main__":
    unittest.main()
