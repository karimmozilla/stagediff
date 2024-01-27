import unittest
from pxr import Usd, Sdf, Kind
import stagediff

class TestStageDiff(unittest.TestCase):

    @unittest.skip
    def testStageMetadataChanged(self):
        pass

    def testPrimAdded(self):
        stage1 = Usd.Stage.CreateInMemory()
        stage2 = Usd.Stage.CreateInMemory()
        stage2.DefinePrim("/root")

        result = stagediff.analyisStage(stage1, stage2)
        self.assertEqual(result[0], stagediff.Status().primAdded)

    def testPrimRemoved(self):
        stage1 = Usd.Stage.CreateInMemory()
        stage1.DefinePrim("/root")
        stage2 = Usd.Stage.CreateInMemory()
        
        result = stagediff.analyisStage(stage1, stage2)
        self.assertEqual(result[0], stagediff.Status().primRemoved)

    def testPrimTypeChanged(self):
        stage1 = Usd.Stage.CreateInMemory()
        stage1.DefinePrim("/root")

        stage2 = Usd.Stage.CreateInMemory()
        stage2.DefinePrim("/root", "Xform")
        
        result = stagediff.analyisStage(stage1, stage2)
        self.assertEqual(result[0], stagediff.Status().primTypeChanged)

    def testPrimKindChanged(self):
        stage1 = Usd.Stage.CreateInMemory()
        prim = stage1.DefinePrim("/root")
        Usd.ModelAPI(prim).SetKind(Kind.Tokens.component)

        stage2 = Usd.Stage.CreateInMemory()
        prim = stage2.DefinePrim("/root")
        Usd.ModelAPI(prim).SetKind(Kind.Tokens.subcomponent)
        
        result = stagediff.analyisStage(stage1, stage2)
        self.assertEqual(result[0], stagediff.Status().primKindChanged)

    def testPrimPathChanged(self):
        stage1 = Usd.Stage.CreateInMemory()
        stage1.DefinePrim("/root/parent/child")

        stage2 = Usd.Stage.CreateInMemory()
        stage2.DefinePrim("/root/child")
        
        result = stagediff.analyisStage(stage1, stage2)
        self.assertEqual(result[0], stagediff.Status().primPathChanged)

    def testAttributeAdded(self):
        stage1 = Usd.Stage.CreateInMemory()
        stage1.DefinePrim("/root")

        stage2 = Usd.Stage.CreateInMemory()
        prim = stage2.DefinePrim("/root")
        prim.CreateAttribute("test", Sdf.ValueTypeNames.Int)
        
        result = stagediff.analyisStage(stage1, stage2)
        self.assertEqual(result[0], stagediff.Status().attrAdded)

    def testAttributeRemoved(self):
        stage1 = Usd.Stage.CreateInMemory()
        prim = stage1.DefinePrim("/root")
        prim.CreateAttribute("test", Sdf.ValueTypeNames.Int)

        stage2 = Usd.Stage.CreateInMemory()
        stage2.DefinePrim("/root")

        result = stagediff.analyisStage(stage1, stage2)
        self.assertEqual(result[0], stagediff.Status().attrRemoved)


    def testAttributeValueChanged(self):
        stage1 = Usd.Stage.CreateInMemory()
        prim = stage1.DefinePrim("/root")
        attr = prim.CreateAttribute("test", Sdf.ValueTypeNames.Int)
        attr.Set(8)

        stage2 = Usd.Stage.CreateInMemory()
        prim = stage2.DefinePrim("/root")
        attr = prim.CreateAttribute("test", Sdf.ValueTypeNames.Int)
        attr.Set(9)

        result = stagediff.analyisStage(stage1, stage2)
        self.assertEqual(result[0], stagediff.Status().attrValueChanged)

    def testAttributeTypeChanged(self):
        stage1 = Usd.Stage.CreateInMemory()
        prim = stage1.DefinePrim("/root")
        prim.CreateAttribute("test", Sdf.ValueTypeNames.Int)

        stage2 = Usd.Stage.CreateInMemory()
        prim = stage2.DefinePrim("/root")
        prim.CreateAttribute("test", Sdf.ValueTypeNames.Float)

        result = stagediff.analyisStage(stage1, stage2)
        self.assertEqual(result[0], stagediff.Status().attrTypeChanged)

    @unittest.skip
    def testAttributeLengthChanged(self):
        pass
    
    @unittest.skip
    def testAttributeBlocked(self):
        pass


if __name__ == '__main__':
    unittest.main()