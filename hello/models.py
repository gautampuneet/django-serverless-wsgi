from datetime import datetime
from django.utils import timezone

from django.db import models
import uuid


class TimestampMixin(models.Model):
    current_time = datetime.max.replace(tzinfo=timezone.utc)
    id = models.UUIDField(primary_key=True, db_index=True, default=uuid.uuid4())
    created_on = models.DateTimeField(default=current_time)
    modified_on = models.DateTimeField(default=current_time)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


def instance_to_dict(model_instance, required_fields):
    data = {}
    for field in required_fields:
        data[field] = model_instance.__getattribute__(field)
    return data


class CountryModel(models.Model):
    """
        Country Model
    """
    current_time = datetime.max.replace(tzinfo=timezone.utc)
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=128)
    iso3 = models.CharField(max_length=3)
    iso2 = models.CharField(max_length=2)
    phone_code = models.CharField(max_length=16)
    currency = models.CharField(max_length=8)
    currency_symbol = models.CharField(max_length=8)
    created_on = models.DateTimeField(default=current_time)
    modified_on = models.DateTimeField(default=current_time)
    is_deleted = models.BooleanField(default=False)

    objects = models.Manager()

    class Meta:
        db_table = "countries"
        ordering = ['name']


class StateModel(models.Model):
    current_time = datetime.max.replace(tzinfo=timezone.utc)
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=128)
    country = models.ForeignKey(CountryModel, on_delete=models.CASCADE, related_name="countries")
    state_code = models.CharField(max_length=128)
    created_on = models.DateTimeField(default=current_time)
    modified_on = models.DateTimeField(default=current_time)
    is_deleted = models.BooleanField(default=False)

    objects = models.Manager()

    class Meta:
        db_table = "states"
        ordering = ['name']


class CityModel(models.Model):
    current_time = datetime.max.replace(tzinfo=timezone.utc)
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=128)
    state = models.ForeignKey(StateModel, on_delete=models.CASCADE, related_name="states")
    country = models.ForeignKey(CountryModel, on_delete=models.CASCADE, related_name="city_countries")
    created_on = models.DateTimeField(default=current_time)
    modified_on = models.DateTimeField(default=current_time)
    is_deleted = models.BooleanField(default=False)

    objects = models.Manager()

    class Meta:
        db_table = "cities"
        ordering = ['name']


class UserProfileModel(TimestampMixin):

    name = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=16, null=True, blank=True)
    job_title = models.CharField(max_length=128, null=True, blank=True)
    company = models.CharField(max_length=128, null=True, blank=True)
    email = models.EmailField(max_length=64, null=False)
    line1 = models.CharField(max_length=256, null=True, blank=True)
    line2 = models.CharField(max_length=256, null=True, blank=True)
    country = models.ForeignKey(CountryModel, on_delete=models.CASCADE, related_name="user_countries", null=True, blank=True)
    state = models.ForeignKey(StateModel, on_delete=models.CASCADE, related_name="user_states", null=True, blank=True)
    city = models.ForeignKey(CityModel, on_delete=models.CASCADE, related_name="user_cities", null=True, blank=True)
    zipcode = models.CharField(max_length=32, null=True, blank=True)
    profile_picture = models.TextField(null=True, blank=True)

    objects = models.Manager()

    class Meta:
        db_table = "user_profiles"
        ordering = ['name']


class UserNamesModel(TimestampMixin):

    name = models.CharField(max_length=50, null=False)
    provider = models.IntegerField(null=False)
    user = models.ForeignKey(UserProfileModel, on_delete=models.CASCADE, related_name="user_profiles")

    objects = models.Manager()

    class Meta:
        db_table = "user_names"


class DatacentersModel(TimestampMixin):

    location = models.CharField(max_length=56, null=False)
    code = models.CharField(max_length=8)
    region = models.CharField(max_length=64)

    objects = models.Manager()

    class Meta:
        db_table = "datacenters"


class WorkspaceModel(TimestampMixin):

    name = models.CharField(max_length=128)
    owner = models.ForeignKey(UserProfileModel, on_delete=models.CASCADE, related_name="owner")
    datacenter = models.ForeignKey(DatacentersModel, on_delete=models.CASCADE, related_name="datacenters")

    objects = models.Manager()

    class Meta:
        db_table = "workspaces"
        ordering = ['name']


class UserWorkspaceModel(TimestampMixin):

    user = models.ForeignKey(UserProfileModel, on_delete=models.CASCADE, related_name="workspace_user")
    workspace = models.ForeignKey(WorkspaceModel, on_delete=models.CASCADE, related_name="workspace")

    objects = models.Manager()

    class Meta:
        db_table = "user_workspaces"
