import pytest

from Sample.models import Sample


@pytest.mark.django_db
def test_my_user():
    sample = Sample.objects.get(id='1')
    print(sample)




