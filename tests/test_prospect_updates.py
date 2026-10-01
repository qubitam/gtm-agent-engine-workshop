import os
import unittest

os.environ.setdefault("OPENAI_API_KEY", "test-key")
os.environ.setdefault("LANGSMITH_TRACING", "false")

from gtm_agent import data_service
from gtm_agent.gtm_agent import build_prospect_profile


class ProspectUpdateTest(unittest.TestCase):
    def setUp(self):
        self.prospect_id = "LEAD-39002"
        self.original_tech_stack = list(data_service.PROSPECTS[self.prospect_id]["tech_stack"])
        data_service._PROFILES.pop(self.prospect_id, None)

    def tearDown(self):
        data_service.PROSPECTS[self.prospect_id]["tech_stack"] = self.original_tech_stack
        data_service._PROFILES.pop(self.prospect_id, None)

    def test_update_persists_through_fetch_and_profile_build(self):
        build_prospect_profile.invoke({"prospect_id": self.prospect_id})

        result = data_service.update_prospect_info(self.prospect_id, "Terraform")

        self.assertIn("Terraform", result["tech_stack"])
        self.assertIn("Terraform", data_service.fetch_tech_stack(self.prospect_id))
        profile = build_prospect_profile.invoke({"prospect_id": self.prospect_id})
        self.assertIn("Terraform", profile["prospect_profile"]["tech_stack"])


if __name__ == "__main__":
    unittest.main()
