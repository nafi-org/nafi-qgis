import processing

class Upload:
    @staticmethod
    def run(approvedBurntAreas, fsid, region, attributedBurntAreas):
        params = {
            'ApprovedBurntAreas': approvedBurntAreas,
            'FSID': fsid,
            'Region': region,
            'Comments':'Created by the NAFI Burnt Areas Mapping plug-in',
            'AttributedBurntAreas': attributedBurntAreas
        }
        
        results = processing.run("BurntAreas:Full Burnt Areas Process", params)

        return results
