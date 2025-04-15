from rest_framework_nested import routers
from .views import (
    AssignmentViewSet
)


router=routers.DefaultRouter()
router.register('assignments',AssignmentViewSet,basename='assignments')

urlpatterns = router.urls