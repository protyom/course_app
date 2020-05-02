from rest_framework import routers

from course_app.api.v1.viewsets import AccountViewSet, DetailAccountViewSet


router = routers.SimpleRouter()

router.register('account', AccountViewSet)
router.register('detail_account', DetailAccountViewSet)

urlpatterns = router.urls