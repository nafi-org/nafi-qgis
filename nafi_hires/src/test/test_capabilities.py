# import unittest

# import os
# import os.path as path

# from nafi_hires.src.widgets.dock_widget.mapping_widget.mapping_manager import Mapping
# from nafi_hires.src.models.project import Project
# from nafi_hires.src.workspace import WorkspaceService
# from nafi_hires.src.utils import getRemoteWorkspaceUrl

# TEST_CAPS = path.normpath(
#     path.join(
#         path.dirname(__file__),
#         os.pardir,
#         os.pardir,
#         "nafi_hires_data",
#         "test",
#         "test_caps.xml",
#     )
# )


# class TestCapabilities(unittest.TestCase):
#     def test_read_caps(self):
#         reader = WorkspaceService()

#         with open(TEST_CAPS, "r") as capsFile:
#             wmsXml = capsFile.read()
#             caps = reader.parseCapabilities(getRemoteWorkspaceUrl(), wmsXml)
#             self.assertTrue(isinstance(caps, Project))

#             # Two regions: Darwin, Katherine
#             self.assertEqual(len(caps.mappings), 2)

#             firstName = next(iter(caps.mappings))
#             self.assertTrue(isinstance(firstName, str))

#             firstRegion = caps.mappings[firstName]
#             self.assertTrue(isinstance(firstRegion, Mapping))
