from pxr import Usd, Sdf


class LayerExtractor:
    layer = Sdf.Layer.CreateAnonymous()

    def __init__(self, events) -> None:
        for event in events:
            getattr(self, event.changeType)(event)

    def primAdded(self, event):
        srcLayer = event.prim.GetStage().GetRootLayer()
        Sdf.CopySpec(srcLayer, event.prim.GetPath(), self.layer, event.prim.GetPath())