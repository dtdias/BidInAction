import os
import unittest

from utils.resources import resource_path


class ResourcePathTests(unittest.TestCase):
    def test_banner_resolves_from_project_root(self):
        self.assertTrue(os.path.isfile(resource_path("assets/logo_vitrine_de_joias.png")))


if __name__ == "__main__":
    unittest.main()
