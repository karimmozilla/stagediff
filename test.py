import unittest
from pxr import Usd, Sdf, Kind
import stagediff

class TestStageDiff(unittest.TestCase):

    @unittest.skip
    def testStageMetadataChanged(self):
        pass

    @unittest.skip
    def testSubLayerAdded(self):
        pass

    @unittest.skip
    def testSubLayerRemoved(self):
        pass

    def testPrimAdded(self):
        stage1 = Usd.Stage.CreateInMemory()
        stage2 = Usd.Stage.CreateInMemory()
        stage2.DefinePrim("/root")

        self.result = stagediff.analyseStage(stage1, stage2)
        self.assertEqual(self.result[0].changeType, "primAdded")

    def testPrimRemoved(self):
        stage1 = Usd.Stage.CreateInMemory()
        stage1.DefinePrim("/root")
        stage2 = Usd.Stage.CreateInMemory()
        
        self.result = stagediff.analyseStage(stage1, stage2)
        self.assertEqual(self.result[0].changeType, "primRemoved")

    def testPrimTypeChanged(self):
        stage1 = Usd.Stage.CreateInMemory()
        stage1.DefinePrim("/root")

        stage2 = Usd.Stage.CreateInMemory()
        newType = "Xform"
        stage2.DefinePrim("/root", newType)

        self.result = stagediff.analyseStage(stage1, stage2)
        # print([[getattr(f, i) for i in dir(f)if not "__"in i] for f in self.result])
        self.assertEqual(self.result[0].changeType, "primTypeChanged")


    def testPrimKindChanged(self):
        stage1 = Usd.Stage.CreateInMemory()
        prim = stage1.DefinePrim("/root")
        Usd.ModelAPI(prim).SetKind(Kind.Tokens.component)

        stage2 = Usd.Stage.CreateInMemory()
        prim = stage2.DefinePrim("/root")
        newKind = Kind.Tokens.subcomponent
        Usd.ModelAPI(prim).SetKind(newKind)
        
        self.result = stagediff.analyseStage(stage1, stage2)
        self.assertEqual(self.result[0].changeType, "primKindChanged")

    def testPrimPathChanged(self):
        stage1 = Usd.Stage.CreateInMemory()
        stage1.DefinePrim("/root/parent/child")

        stage2 = Usd.Stage.CreateInMemory()
        stage2.DefinePrim("/root/child")
        
        self.result = stagediff.analyseStage(stage1, stage2)
        self.assertEqual(self.result[0].changeType, "primPathChanged")

    def testAttributeAdded(self):
        stage1 = Usd.Stage.CreateInMemory()
        stage1.DefinePrim("/root")

        stage2 = Usd.Stage.CreateInMemory()
        prim = stage2.DefinePrim("/root")
        prim.CreateAttribute("test", Sdf.ValueTypeNames.Int)
        
        self.result = stagediff.analyseStage(stage1, stage2)
        self.assertEqual(self.result[0].changeType, "attrAdded")

    def testAttributeRemoved(self):
        stage1 = Usd.Stage.CreateInMemory()
        prim = stage1.DefinePrim("/root")
        prim.CreateAttribute("test", Sdf.ValueTypeNames.Int)

        stage2 = Usd.Stage.CreateInMemory()
        stage2.DefinePrim("/root")

        self.result = stagediff.analyseStage(stage1, stage2)
        self.assertEqual(self.result[0].changeType, "attrRemoved")


    def testAttributeValueChanged(self):
        stage1 = Usd.Stage.CreateInMemory()
        prim = stage1.DefinePrim("/root")
        attr = prim.CreateAttribute("test", Sdf.ValueTypeNames.Int)
        attr.Set(8)

        stage2 = Usd.Stage.CreateInMemory()
        prim = stage2.DefinePrim("/root")
        attr = prim.CreateAttribute("test", Sdf.ValueTypeNames.Int)
        attr.Set(9)

        self.result = stagediff.analyseStage(stage1, stage2)
        self.assertEqual(self.result[0].changeType, "attrValueChanged")

    def testAttributeTypeChanged(self):
        stage1 = Usd.Stage.CreateInMemory()
        prim = stage1.DefinePrim("/root")
        prim.CreateAttribute("test", Sdf.ValueTypeNames.Int)

        stage2 = Usd.Stage.CreateInMemory()
        prim = stage2.DefinePrim("/root")
        prim.CreateAttribute("test", Sdf.ValueTypeNames.Float)

        self.result = stagediff.analyseStage(stage1, stage2)
        self.assertEqual(self.result[0].changeType, "attrTypeChanged")

    @unittest.skip
    def testAttributeLengthChanged(self):
        pass
    
    @unittest.skip
    def testAttributeBlocked(self):
        pass
    
    @unittest.skip
    def testReferenceAdded(self):
        pass    
    
    @unittest.skip
    def testReferenceRemoved(self):
        pass    

    @unittest.skip
    def testReferenceValueChanged(self):
        pass
    
    @unittest.skip
    def testPayloadAdded(self):
        pass    
    
    @unittest.skip
    def testPayloadRemoved(self):
        pass    

    @unittest.skip
    def testPayloadValueChanged(self):
        pass
    
if __name__ == '__main__':
    unittest.main()