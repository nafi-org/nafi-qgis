from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterVectorLayer,
)
import processing


class DissolveBurntAreas(QgsProcessingAlgorithm):
    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                "BurntAreas",
                "Your burnt areas",
                types=[QgsProcessing.TypeVectorPolygon],
                defaultValue=None,
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                "DissolvedBurntAreas",
                "Dissolved burnt areas",
                type=QgsProcessing.TypeVectorAnyGeometry,
                createByDefault=True,
                defaultValue=None,
            )
        )

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(1, model_feedback)
        results = {}
        outputs = {}

        # Fix geometries
        alg_params = {
            "INPUT": parameters["BurntAreas"],
            "OUTPUT": QgsProcessing.TEMPORARY_OUTPUT,
        }
        outputs["FixGeometries"] = processing.run(
            "native:fixgeometries",
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        # Dissolve
        alg_params = {
            "FIELD": [""],
            "INPUT": outputs["FixGeometries"]["OUTPUT"],
            "OUTPUT": parameters["DissolvedBurntAreas"],
        }

        processing.ProcessingConfig.setSettingValue("IGNORE_INVALID_FEATURES", 1)
        outputs["Dissolve"] = processing.run(
            "native:dissolve",
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )
        results["DissolvedBurntAreas"] = outputs["Dissolve"]["OUTPUT"]
        return results

    def name(self):
        return "DissolveBurntAreas"

    def displayName(self):
        return "Dissolve Burnt Areas"

    def group(self):
        return ""

    def groupId(self):
        return ""

    def createInstance(self):
        return DissolveBurntAreas()
