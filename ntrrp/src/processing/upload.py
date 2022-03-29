import processing

from ..utils import qgsDebug

class Upload:
    @staticmethod
    def run(approvedBurntAreas, region, attributedBurntAreas):
        layer = approvedBurntAreas # load the layer as you want
    
        params = {
            'ApprovedBurntAreas': approvedBurntAreas,
            'Region': region,
            'Comments':'Created by the NAFI Burnt Areas Mapping plug-in',
            'Extent': layer.extent(),
            'AttributedBurntAreas': attributedBurntAreas
        }
        
        results = processing.run("BurntAreas:Full Burnt Areas Process", params)

        return results
