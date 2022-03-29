# -*- coding: utf-8 -*-
class NtrrpFsidRecord:
    def __init__(self, fsidJson):
        """Constructor."""

        self.id = fsidJson["id"]
        self.fsid = fsidJson["fsid"]
        self.startDate = fsidJson["start_date"]
        self.endDate = fsidJson["end_date"]
        self.month = fsidJson["month"]
        self.region = fsidJson["region"]
        self.uploadDate = fsidJson["upload_date"]
        self.author = fsidJson["author"]
        self.comment = fsidJson["comment"]


# Sample data showing structure
# [
#   {
#     "id": 1,
#     "fsid": 27,
#     "start_date": "2021-04-14",
#     "end_date": "2021-04-19",
#     "month": 4,
#     "region": "darwin",
#     "upload_date": "2021-04-21",
#     "author": "Angus Farlam",
#     "comment": ""
#   },
#   {
#     "id": 2,
#     "fsid": 28,
#     "start_date": "2021-04-19",
#     "end_date": "2021-04-24",
#     "month": 4,
#     "region": "darwin",
#     "upload_date": "2021-04-26",
#     "author": "Patrice Weber",
#     "comment": ""
#   },
#   {
#     "id": 3,
#     "fsid": 29,
#     "start_date": "2021-04-24",
#     "end_date": "2021-04-29",
#     "month": 4,
#     "region": "darwin",
#     "upload_date": "2021-05-03",
#     "author": "Patrice Weber",
#     "comment": ""
#   },
#   {
#     "id": 4,
#     "fsid": 37,
#     "start_date": "2021-04-29",
#     "end_date": "2021-05-04",
#     "month": 5,
#     "region": "darwin",
#     "upload_date": "2021-05-07",
#     "author": "Patrice Weber",
#     "comment": ""
#   },
#   {
#     "id": 5,
#     "fsid": 38,
#     "start_date": "2021-05-04",
#     "end_date": "2021-05-09",
#     "month": 5,
#     "region": "darwin",
#     "upload_date": "2021-05-11",
#     "author": "Maggie Towers",
#     "comment": ""
#   },
#   {
#     "id": 6,
#     "fsid": 39,
#     "start_date": "2021-05-09",
#     "end_date": "2021-05-14",
#     "month": 5,
#     "region": "darwin",
#     "upload_date": "2021-05-15",
#     "author": "Angus Farlam",
#     "comment": ""
#   },
#   {
#     "id": 7,
#     "fsid": 40,
#     "start_date": "2021-05-14",
#     "end_date": "2021-05-19",
#     "month": 5,
#     "region": "darwin",
#     "upload_date": "2021-05-21",
#     "author": "Angus Farlam",
#     "comment": ""
#   }
# ]
