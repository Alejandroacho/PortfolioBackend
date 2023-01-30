import pytest

from Certifications.factories import CertificationFactory
from Certifications.fakers import CertificationFaker
from Certifications.models import Certification
from Images.fakers import ImageFaker


@pytest.mark.django_db
class TestCertificationModel:
    def test_model_keys(self) -> None:
        certification: Certification = CertificationFaker()
        assert hasattr(certification, "id")
        assert hasattr(certification, "name")
        assert hasattr(certification, "description")
        assert hasattr(certification, "tags")
        assert hasattr(certification, "url")
        assert hasattr(certification, "image")
        assert hasattr(certification, "file")

    def test_str_representation(self) -> None:
        certification: Certification = CertificationFaker()
        assert (
            str(certification) == f"{certification.id} | {certification.name}"
        )


@pytest.mark.django_db
class TestCertificationFactory:
    def test_factory_creates_an_instance(self) -> None:
        assert Certification.objects.count() == 0
        certification: Certification = CertificationFactory(
            name="TEST",
            description="This is a test certification",
            image=ImageFaker(),
            file="certification.pdf",
            url="https://www.appname.com",
            tags=["test", "test2", "test3"],
        )
        assert isinstance(certification, Certification)
        assert Certification.objects.count() == 1


@pytest.mark.django_db
class TestCertificationFaker:
    def test_faker_create_the_default_python_instance(self) -> None:
        assert Certification.objects.count() == 0
        certification: Certification = CertificationFaker()
        assert isinstance(certification, Certification)
        assert Certification.objects.count() == 1
        assert certification.name == "Fake"
        assert certification.description == "This is a fake certification"
        assert certification.tags == ["test", "test2", "test3"]
        assert certification.url == "https://www.appname.com"
        assert "certification_documents" in certification.file.name
        assert "image" in certification.image.image.name
