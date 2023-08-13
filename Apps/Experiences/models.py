import datetime
from typing import List

from dateutil.relativedelta import relativedelta
from django.db.models import CASCADE
from django.db.models import BooleanField
from django.db.models import CharField
from django.db.models import ForeignKey
from django.db.models import ManyToManyField
from django.db.models import Model
from django.db.models.fields import DateField

from Images.models import Image
from Technologies.models import Technology


class Experience(Model):
    company: str = CharField(max_length=100)
    position: str = CharField(max_length=100)
    description: str = CharField(max_length=1000)
    url: str = CharField(max_length=1000, null=True, blank=True)
    current: bool = BooleanField(default=False)
    start_date: datetime.date = DateField(auto_now=False, auto_now_add=False)
    end_date: datetime.date = DateField(
        auto_now=False, auto_now_add=False, null=True, blank=True
    )
    logo: Image = ForeignKey(
        Image,
        null=True,
        on_delete=CASCADE,
    )
    technologies: List[Technology] = ManyToManyField(
        Technology, related_name="experiences"
    )

    def __str__(self) -> str:
        return f"{self.id} | {self.company}"

    @property
    def time_of_experience(self) -> str:
        if self.current:
            delta: relativedelta = relativedelta(
                datetime.date.today(), self.start_date
            )
        else:
            delta: relativedelta = relativedelta(self.end_date, self.start_date)
        if delta.years == 0:
            return f"{delta.months} months"
        if delta.months == 0:
            return f"{delta.years} years"
        return f"{delta.years} years, {delta.months} months"
