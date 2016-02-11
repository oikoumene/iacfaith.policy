from collective.grok import gs
from iacfaith.policy import MessageFactory as _

@gs.importstep(
    name=u'iacfaith.policy', 
    title=_('iacfaith.policy import handler'),
    description=_(''))
def setupVarious(context):
    if context.readDataFile('iacfaith.policy.marker.txt') is None:
        return
    portal = context.getSite()

    # do anything here
