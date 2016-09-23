import pytest

from capybara.exceptions import Ambiguous, ElementNotFound


class FindFieldTestCase:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/form")


class TestFindField(FindFieldTestCase):
    def test_finds_any_field(self, session):
        assert session.find_field("Dog").value == "dog"
        assert session.find_field("form_description").text == "Descriptive text goes here"
        assert session.find_field("Region")["name"] == "form[region]"

    def test_raises_an_error_if_the_field_does_not_exist(self, session):
        with pytest.raises(ElementNotFound):
            session.find_field("Does not exist")

    def test_raises_an_error_if_the_field_is_disabled(self, session):
        with pytest.raises(ElementNotFound):
            session.find_field("Disabled Checkbox")

    def test_finds_an_approximately_matching_field(self, session):
        assert session.find_field("Explanation")["name"] == "form[name_explanation]"

    def test_does_not_find_an_approximately_matching_field_when_exact_is_true(self, session):
        with pytest.raises(ElementNotFound):
            session.find_field("Explanation", exact=True)


class TestFindFieldDisabled(FindFieldTestCase):
    def test_does_not_find_disabled_fields_when_false(self, session):
        with pytest.raises(ElementNotFound):
            session.find_field("Disabled Checkbox", disabled=False)

    def test_finds_enabled_fields_when_false(self, session):
        field = session.find_field("Dog", disabled=False)
        assert field.value == "dog"

    def test_finds_disabled_fields_when_true(self, session):
        field = session.find_field("Disabled Checkbox", disabled=True)
        assert field["name"] == "form[disabled_checkbox]"

    def test_does_not_find_enabled_fields_when_true(self, session):
        with pytest.raises(ElementNotFound):
            session.find_field("Dog", disabled=True)

    def test_finds_disabled_fields_when_all(self, session):
        field = session.find_field("Disabled Checkbox", disabled="all")
        assert field["name"] == "form[disabled_checkbox]"

    def test_finds_enabled_fields_when_all(self, session):
        field = session.find_field("Dog", disabled="all")
        assert field.value == "dog"


class TestFindFieldReadonly(FindFieldTestCase):
    def test_finds_readonly_fields_when_true(self, session):
        assert session.find_field("form[readonly_test]", readonly=True)["id"] == "readonly"

    def test_does_not_find_readonly_fields_when_false(self, session):
        assert session.find_field("form[readonly_test]", readonly=False)["id"] == "not_readonly"

    def test_ignores_readonly_by_default(self, session):
        with pytest.raises(Ambiguous) as excinfo:
            session.find_field("form[readonly_test]")
        assert "found 2 elements" in str(excinfo.value)
