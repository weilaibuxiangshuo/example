# -*- coding:utf-8 -*-
from tornado.web import URLSpec

from apps.record.handlers import ManagementHandler, ManagementStatusHandler, EventProcessHandler, \
    EventProcessConfirmHandler,EventProcessStatusHandler,DisplaystandHandler,FailSearchHandler,EventProcessFailHandler

urlpatterns = [
    URLSpec('/management/', ManagementHandler),
    URLSpec('/management/(\d+)/(\d+)/', ManagementHandler),
    URLSpec('/management/status/', ManagementStatusHandler),
    URLSpec('/eventprocess/confirm/', EventProcessConfirmHandler),
    URLSpec('/eventprocess/(\d+)/(\d+)/', EventProcessHandler),
    URLSpec('/eventprocess/status/', EventProcessStatusHandler),
    URLSpec('/eventprocess/fail/', EventProcessFailHandler),
    URLSpec('/displaystand/', DisplaystandHandler),
    URLSpec('/displaystand/(\d+)/(\d+)/', DisplaystandHandler),
    URLSpec('/failsearch/(\d+)/(\d+)/', FailSearchHandler),
]
