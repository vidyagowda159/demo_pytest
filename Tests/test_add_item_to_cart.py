import pytest

from Library.read_excel import ReadExcel
from POM.add_item_to_cart import addtocart


class TestAddToCart:

    td = ReadExcel()
    data = td.login_details()

    @pytest.mark.parametrize("u_name, pswd", data)
    def test_msg(self, u_name, pswd, init_driver):
        n = addtocart(init_driver)
        n.enter_username(u_name)
        n.enter_pswd(pswd)
        n.click_on_login()
        n.click_on_add_to_cart()

