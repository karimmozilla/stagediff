# from pxr import Usd


class StageDiff:
    def analyse(self, stage1, stage2):
        result = []
        
        primNames = {f.GetName():f for f in stage1.Traverse()}
            
        for prim in stage2.Traverse():
            changesForPrims=False
            primName = prim.GetName()
            if primName in primNames:

                oldType, newType = primNames[primName].GetTypeName(), prim.GetTypeName()
                if oldType != newType:
                    result.append(Status("primTypeChanged", prim=prim, oldType=oldType, newType=newType))
                    changesForPrims=True

                oldKind, newKind = primNames[primName].GetKind(), prim.GetKind()
                if oldKind != newKind:
                    result.append(Status("primKindChanged", prim=prim, oldKind=oldKind, newKind=newKind))
                    changesForPrims=True

                oldPath = primNames[primName].GetPath()
                if prim.GetPath() != oldPath:
                    result.append(Status("primPathChanged", prim=prim, oldPath=oldPath))                    
                    changesForPrims=True

                if not changesForPrims:
                    attrs = {f.GetName(): f for f in primNames[primName].GetAttributes()}
                    for attr in prim.GetAttributes():
                        attrName=attr.GetName()
                        if attrName in attrs:
                            srcAttr = attrs[attrName]
                            #TODO: Handle attr time sample values
                            oldValue, newValue = attr.Get(), srcAttr.Get()
                            if oldValue != newValue:
                                result.append(Status("attrValueChanged", attr=attr, oldValue = oldValue, newValue = newValue))
                            oldType, newType = attr.GetTypeName(), srcAttr.GetTypeName()
                            if oldType != newType:
                                result.append(Status("attrTypeChanged", attr=attr, oldType = oldType, newType = newType))

                            attrs.pop(attrName)
                        else:
                            result.append(Status("attrAdded", attr=attr))
                        
                    for attrName in attrs:
                        result.append(Status("attrRemoved", attr=attrs[attrName]))

                primNames.pop(primName)
            else:
                result.append(Status("primAdded", prim=prim))

        for prim in primNames:
            result.append(Status("primRemoved", prim=primNames[prim]))

        return result

def analyseStage(stage1, stage2):
    cls = StageDiff()
    return cls.analyse(stage1, stage2)
    


class Status:
    changeType=None


    def __init__(self, state, *args, **kwargs) -> None:
        self.changeType = state
        for arg in kwargs:
            setattr(self, arg, kwargs[arg])