import unittest

import os.path as path

from src.ntrrp_capabilities_reader import NtrrpCapabilitiesReader
from src.ntrrp_capabilities import NtrrpCapabilities
from src.ntrrp_region import NtrrpRegion
from src.utils import getNtrrpWmsUrl

TEST_CAPS = path.normpath(path.join(path.dirname(__file__), "data", "test_caps.xml"))

class TestCapabilities(unittest.TestCase):

    def test_read_caps(self):
        reader = NtrrpCapabilitiesReader()

        with open(TEST_CAPS, "r") as capsFile:
            wmsXml = capsFile.read()
            caps = reader.parseCapabilities(getNtrrpWmsUrl(), wmsXml)
            self.assertTrue(isinstance(caps, NtrrpCapabilities))

            # Two regions: Darwin, Katherine
            self.assertEqual(len(caps.regions), 2)

            firstName = next(iter(caps.regions))
            self.assertTrue(isinstance(firstName, str))

            firstRegion = caps.regions[firstName]
            self.assertTrue(isinstance(firstRegion, NtrrpRegion))

        

