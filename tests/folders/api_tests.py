from tests.base_api_tests import ApiOwnersTestCaseMixin
from tests.base_tests import SupersetTestCase

class DashboardApiTests(SupersetTestCase, ApiOwnersTestCaseMixin):
    resource_name = "folder"

    def __init__(self, *args, **kwargs):
        super(DashboardApiTests, self).__init__(*args, **kwargs)


    def test_info_dashboard(self):
        """
    Dashboard API: Test info
    """
        self.login(username="admin")
        uri = f"api/v1/folders/_info"
        rv = self.get_assert_metric(uri, "info")
        self.assertEqual(rv.status_code, 200)