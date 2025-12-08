import unittest
from unittest.mock import patch
import SmartGroceryApp.utils.gpt_helpers as gpt_helpers

class TestGPTHelpers(unittest.TestCase):

    @patch("SmartGroceryApp.utils.gpt_helpers.client.chat.completions.create")
    def test_generate_recipes_from_ingredients(self, mock_create):
        mock_create.return_value = type("obj", (object,), {
            "choices": [
                type("msg", (object,), {
                    "message": type("content", (object,), {
                        "content": (
                            "**Recipe 1: Pasta Primavera**\n\nIngredients:\n- Pasta\n- Onion\n\n"
                            "Instructions:\n1. Cook pasta.\n\n"
                            "**Recipe 2: Stir Fry**\n\nIngredients:\n- Rice\n\nInstructions:\n1. Fry veggies."
                        )
                    })()
                })
            ]
        })()

        ingredients = ["carrot", "pasta", "onion"]
        result = gpt_helpers.generate_recipes_from_ingredients(ingredients)

        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(r, str) for r in result))
        self.assertGreaterEqual(len(result), 1)

if __name__ == "__main__":
    unittest.main()
