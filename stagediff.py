from pxr import Usd


class StageDiff:
    result = []
    def analyiz(self, stage1, stage2):
        
        primNames = {f.GetName():f for f in stage1.Traverse()}
            
        for prim in stage2.Traverse():
            primName = prim.GetName()
            if primName in primNames:
                # check other

                if prim.GetTypeName() != primNames[prim.GetName()].GetTypeName():
                    self.result.append(Status().primTypeChanged)

                if prim.GetKind() != primNames[prim.GetName()].GetKind():
                    self.result.append(Status().primKindChanged)

                if prim.GetPath() != primNames[prim.GetName()].GetPath():
                    self.result.append(Status().primPathChanged)                    

                attrs1 = {f.GetName(): f for f in primNames[prim.GetName()].GetAttributes()}
                for attr in prim.GetAttributes():
                    if attr.GetName() in attrs1:
                        #TODO: Handle attr time sample values
                        srcAttr = attrs1[attr.GetName()]
                        if attr.Get() != srcAttr.Get():
                            self.result.append(Status().attrValueChanged)
                        if attr.GetTypeName() != srcAttr.GetTypeName():
                            self.result.append(Status().attrTypeChanged)

                        attrs1.pop(attr.GetName())
                    else:
                        self.result.append(Status().attrAdded)
                    
                for attrName in attrs1:
                    self.result.append(Status().attrRemoved)

                primNames.pop(primName)
            else:
                self.result.append(Status().primAdded)

        for prim in primNames:
            self.result.append(Status().primRemoved)



def analyisStage(stage1, stage2):
    cls = StageDiff()
    cls.analyiz(stage1, stage2)
    return cls.result


class Status:

    primAdded = "primAdded"
    primRemoved = "primRemoved"
    primTypeChanged = "primTypeChanged"
    primKindChanged = "primKindChanged"
    primPathChanged = "primPathChanged"
    attrAdded = "attrAdded"
    attrRemoved = "attrRemoved"
    attrValueChanged = "attrValueChanged"
    attrTypeChanged = "attrTypeChanged"