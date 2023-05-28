from django.db import models
from wagtail.search import index
from django.contrib.auth.models import User
# Create your models here.
from wagtail.snippets.models import register_snippet
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from modelcluster.models import ClusterableModel


YES_NO_CHOICE=(
    ('no',"No"),
    ('yes',"Yes"),
)

YES_NO = (
    (True, 'Yes'),
    (False, 'No'),
)

YES_NO_BOOLEAN_CHOICE=(
    (1,"Yes"),
    (0,"No"),
    # (1,"Yes"),
)

GENDER_CHOICE=(
    ('MALE',"Male"),
    ('FEMALE',"Female"),
)

EMPLOYMENT_STATUS = (
    ('employed', "Employed"),  # csm nhent Service Manager
    ('exited', "Exited"),  # acsm Anhstant Organization Service Manager
    ('suspended', "Suspended"),  # who Supervises the Organization Service Managers
    ('Terminated', "Terminated"),  # Onnhho Supervises the Organization Service Managers
    ('deceased', "Deceased"),  # Onnhho Supervises the Organization Service Managers
)

MARITAL_STATUS=(
    ('SINGLE',"Single"),
    ('MARRIED',"Married"),
    ('DEVORCED',"Devorced"),

)


CURRENCY = (
    ('Ghc', 'Ghc'),
    ('USD', 'USD $'),
)

class CommonInfo(models.Model, index.Indexed):
    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT,
        related_name="created_by%(app_label)s_%(class)ss_related",
        blank=True,
        null=True,
    )

    updated_by = models.ForeignKey(
        User, on_delete=models.PROTECT,
        related_name="updated_by%(app_label)s_%(class)s_related",
        blank=True,
        null=True,
    )
    return_to_profile = models.BooleanField("Return to Profile ? ", default=False, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True, )
    updated_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    mark_for_deletion = models.BooleanField('Delete ?', blank=True, null=True, default=False)
    cleaned = models.BooleanField('Is Cleaned ?', blank=True, null=True, default=False)
    search_term = models.CharField(max_length=250, blank=True, null=True)
    class Meta:
        abstract = True
        # Create your models here.

    def __str__(self):
        return 'created_on on %s and edited on_on %s' % (self.created_on, self.updated_on)


@register_snippet
class Position(CommonInfo):
    name = models.CharField(max_length=200)
    description = RichTextField(blank=True, null=True,)  # models.TextField(max_length=2000)
    duties = RichTextField(blank=True, null=True,)  # models.TextField(max_length=2000)
    targets = RichTextField(blank=True, null=True,)  # models.TextField(max_length=2000)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Positions"

    def __str__(self):  # __unicode__ on Python 2
        return self.name

    panels = [
            FieldPanel('name'),
            # FieldPanel('industry_pic'),
            FieldPanel('description'),
            FieldPanel('duties'),
            FieldPanel('targets'),
        ]

    search_fields = [
        index.SearchField('name', partial_match=True),
    ]


@register_snippet
class Country(CommonInfo):
    name = models.CharField(unique=True, max_length=30)
    # section = models.CharField("Part of Africa ?", max_length=50, choices=AFRICA_SECTION, default='west',
    #                            blank=True, null=True, )
    more_info = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Countries"

        permissions = [
            ("is_employer", "User is an Employer"),
            ("is_jobseeker", "User is a Jobseeker"),
            ("is_client", "User is an Outsourcing Client"),
            ("is_staff", "User is a Core Staff"),
            ("is_personnel", "User is a an Oursourced Staff"),
            ("is_client_Core_staff", "User is a an Oursourced Client Core Staff"),

        ]

    def __str__(self):
        return self.name

    panels =  [
        FieldPanel('name'),
        # FieldPanel('section'),
        FieldPanel('more_info'),
    ]

    search_fields = [
        index.SearchField('name', partial_match=True),
    ]


@register_snippet
class Region(CommonInfo):
    name = models.CharField(unique=True, max_length=30)
    ghana_post_gps_prefix = models.CharField(max_length=3, blank=True, null=True,)
    country = models.ForeignKey(
        Country, on_delete=models.DO_NOTHING,
        related_name='elogistics_region_connect_country_relation',  # limit_choices_to={'is_staff': True},
        blank=True, null=True, verbose_name="Country"
    )

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Regions"

    def __str__(self):
        return '%s of  %s'% (self.name, self.country)

    panels = [
        FieldPanel('name'),
        FieldPanel('country'),
    ]

    search_fields = [
        index.SearchField('name', partial_match=True),
    ]


@register_snippet
class Location(CommonInfo):
    name = models.CharField(unique=True, max_length=30)
    region = models.ForeignKey(Region, on_delete=models.DO_NOTHING,
        related_name='elogistics_location_region_connect_region_model_relation',)
    parent = models.ForeignKey('self', on_delete=models.DO_NOTHING,
        related_name="elogistics_location_parent_relate_to_self_location",
        blank=True, null=True
    )
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING,
        related_name='elogistics_location_country_connect_country_model_relation',)

    # gh_post_area_code  = models.ForeignKey(GhanaPostCode, on_delete=models.CASCADE)
    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Location (Cities / Towns etc)"

    def __str__(self):
        return f"{self.name} in the {self.region.name} of {self.country.name}"

    panels = [
        FieldPanel('name'),
        # FieldPanel('industry_pic'),
        FieldPanel('region'),
        FieldPanel('country'),
    ]

    search_fields = [
        index.SearchField('name', partial_match=True),
    ]


@register_snippet
class Industry(CommonInfo):
    name = models.CharField(unique=True, max_length=100)
    # industry_pic_ext = models.ImageField(upload_to='media/industry', blank=True, null=True)
    industry_pic = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.CASCADE,
        # upload_to='talent/photos',
        blank=True, null=True
    )

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Industries"

    def __str__(self):
        return self.name

    panels = [
        FieldPanel('name'),
        FieldPanel('industry_pic'),
        # FieldPanel('information'),
        # FieldPanel('is_active'),
    ]

    search_fields = [
        index.SearchField('name', partial_match=True),
    ]


@register_snippet
class OffenseType(CommonInfo):
    name = models.CharField(max_length=100, )
    # severity  = models.CharField("Gender", max_length=30, choices=ACCESS_LEVEL, default='MALE', blank=True, null=True)
    information = models.CharField(max_length=255,blank=True, null=True, )  # models.TextField(max_length=2000)
    import_code = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Offense Type"

    def __str__(self):  # __unicode__ on Python 2
        return self.name

    search_fields = [
        index.SearchField('name'),

    ]


@register_snippet
class OffenseAction(CommonInfo):
    name = models.CharField(max_length=100, )
    more_information = models.CharField(max_length=250, blank=True, null=True, )  # models.TextField(max_length=2000)
    import_code = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Offense Action"

    def __str__(self):  # __unicode__ on Python 2
        return self.name

    search_fields = [
        index.SearchField('name'),

    ]


@register_snippet
class Bank(CommonInfo):
    name = models.CharField(unique=True, max_length=100)
    code = models.CharField(unique=True, max_length=50, blank=True, null=True)
    swift_code = models.CharField(unique=True, max_length=50, blank=True, null=True)
    more_info = models.CharField(unique=True, max_length=250, blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.DO_NOTHING,
                               related_name="elogistics_bank_region_relates_to_region", blank=True,
                               null=True)
    parent = models.ForeignKey('self', on_delete=models.DO_NOTHING,
                               related_name="elogistics_bank_parent_relates_to_bank", blank=True,
                               null=True)
    location = models.CharField(max_length=150, blank=True, null=True)
    import_code = models.CharField(max_length=200, blank=True, null=True)

    panels = [
        FieldPanel('name'),
        # FieldPanel('code'),
        FieldPanel('swift_code'),
        FieldPanel('region'),
        FieldPanel('location'),
        FieldPanel('parent'),
    ]

    search_fields = [
        index.SearchField('name'),

    ]


@register_snippet
class Qualification(CommonInfo):
    name = models.CharField(unique=True, max_length=50)
    weight = models.IntegerField(null=True, blank=True)
    more_info = models.CharField(null=True, blank=True, max_length=200)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Qualifications"

    def __str__(self):
        # return "%s weights %s" % (self.name, self.weight)
        return self.name

    panels = [
            FieldPanel('name'),
            # FieldPanel('industry_pic'),
            FieldPanel('more_info'),
            # FieldPanel('is_active'),
        ]

    search_fields = [
        index.SearchField('name', partial_match=True),
    ]


@register_snippet
class Specialization(CommonInfo):
    name = models.CharField(unique=True, max_length=50)
    more_info = models.CharField(null=True, max_length=200, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Specializations"

    def __str__(self):
        return self.name

    panels = [
        FieldPanel('name'),
        # FieldPanel('industry_pic'),
        FieldPanel('more_info'),
        # FieldPanel('is_active'),
    ]

    search_fields = [
        index.SearchField('name', partial_match=True),
    ]


class Career(CommonInfo):
    name = models.CharField(max_length=100)
    job_description = RichTextField(blank=True, null=True)
    personnel_count = models.PositiveSmallIntegerField(blank=True, null=True)
    # other_kpi = RichTextField(blank=True, null=True)
    duties = RichTextField(blank=True, null=True, )  # models.TextField(max_length=2000)
    targets = RichTextField(blank=True, null=True, )  # models.TextField(max_length=2000)
    # role_category = models.ForeignKey('JobCategory', on_delete=models.DO_NOTHING, blank=True,
    #           related_name="elogistics_role_role_caeegory_relates_to_minimum_qualification", null=True)
    minimum_qualification = models.ForeignKey(Qualification, on_delete=models.DO_NOTHING,
                 related_name="elogistics_role_minimum_qualificationrelates_to_minimum_qualification", blank=True,
                                              null=True)
    specialization = models.ForeignKey(Specialization, on_delete=models.DO_NOTHING,
                  related_name="elogistic_career_specialization_minimum_relate_specialization",
                  blank=True,    null=True)
    import_code = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):  # __unicode__ on Python 2
        # return f"{self.name} at {self.organization}"
        return f"{self.name}"
        # return "%s appid( %s )" % (self.full_name, self.appid)
        # return self.other_names + " " + self.last_name

    @property
    def role_name(self):
        return self.name

    # class Meta:
        # unique_together = ['name', 'organization']

    panels = [
        FieldPanel('name'),
        FieldPanel('job_description'),
        FieldPanel('duties'),
        FieldPanel('targets'),
        # FieldPanel('role_category'),
        FieldPanel('minimum_qualification'),
        FieldPanel('organization'),
    ]

    search_fields = [
        index.SearchField('name'),

        index.RelatedFields('organization', [
            index.SearchField('name'),
        ]),
    ]



@register_snippet
class DepartmentCategory(CommonInfo):
    name = models.CharField(unique=True, max_length=100)
    # code = models.CharField(unique=True, max_length=50, blank=True, null=True)
    description  = RichTextField( blank=True, null=True)
    # organization = models.ForeignKey(OrganizationPage, on_delete=models.DO_NOTHING,
    #  related_name="base_department_relates_to_organization", blank=True,
    #  null=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Department Categories"

    def __str__(self):  # __unicode__ on Python 2
        return self.name

    panels = [
        FieldPanel('name'),
        FieldPanel('description'),
        # FieldPanel('information'),
        # FieldPanel('is_active'),
    ]



# @register_snippet
class Department(CommonInfo):
    name = models.CharField(max_length=100)
    department_code = models.CharField(max_length=50, blank=True, null=True)

    department_category = models.ForeignKey(
        DepartmentCategory,  # on_delete=models.CASCADE,
        on_delete=models.DO_NOTHING,

        related_name='base_organization_department_department_category_relate_department_relation',
        # limit_choices_to={'is_staff': True},
        # default="Ghana",
        # on_update=models.CASCADE,
        blank=True,
        null=True
    )
    more_information = RichTextField(blank=True, null=True)
    personnel_count = models.PositiveSmallIntegerField(blank=True, null=True)
    import_code = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        # return self.name   ) if self.name else str("Empty")
        return f"{self.name} "

    # class Meta:
    #     ordering = ["created_on"]
    #     verbose_name_plural = "Departments"

    search_fields = [
        index.SearchField('name'),

        index.RelatedFields('organization', [
            index.SearchField('name'),
        ]),
    ]
    panels = [
        FieldPanel('name'),
        FieldPanel('department_code'),
        # FieldPanel('department'),
        FieldPanel('more_information'),
        FieldPanel('department_category')

            ]


class Employee(models.Model):
    employee_feature_image_270x420 = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True, on_delete=models.SET_NULL,
        help_text="This Photo os for Employee Featured Image",
        related_name='elogistics_employee_feature_image_370x570_relates_to_logo_relation',
        # limit_choices_to={'is_staff': True},
    )
    code = models.CharField(max_length=20)
    title = models.CharField(max_length=20, default="None", blank=True, null=True)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=60, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    gender = models.CharField("Gender", max_length=30, choices=GENDER_CHOICE, default='MALE', blank=True, null=True)
    birth_date = models.DateField(verbose_name="Date of Birth", blank=True, null=True)
    birth_place = models.CharField(max_length=60, blank=True, null=True)
    parent_name = models.CharField(max_length=250, blank=True, null=True)
    email = models.EmailField()
    mobile_phone = models.CharField(max_length=20)
    personal_phone = models.CharField(max_length=20)
    residential_address = models.CharField(max_length=50)
    postal_address = models.CharField(max_length=200, blank=True, null=True)
    digital_address = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact = models.CharField(max_length=200)
    payroll_code = models.CharField(max_length=50, blank=True, null=True)
    nationality = models.ForeignKey(Country, on_delete=models.DO_NOTHING,
                                       related_name="elogistics_personnel_country_nationality_to_country_relatiuon",
                                    blank=True, null=True)
    residential_country = models.ForeignKey(Country, on_delete=models.DO_NOTHING,
                                            related_name="elogistics_personnel_country_residence_relates_to_country_relatiuon",
                                            blank=True, null=True)
    directional_map = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        related_name="+",
        # upload_to='talent/photos',
        blank=True, null=True
    )
    directional_map_image_ext = models.ImageField(upload_to='media/personnel', blank=True, null=True)
    phone_no = models.CharField("Phone Number (SMS)", max_length=14, blank=True, null=True)
    level = models.SmallIntegerField(verbose_name="Group staff by level ex. 1,2,3 ",default=0)
    other_phone_nos = models.CharField(max_length=100, help_text="Your other phone Numbers", blank=True, null=True)

    marital_status = models.CharField(max_length=30, choices=MARITAL_STATUS, blank=True, null=True)
    next_kin = models.CharField(max_length=250, blank=True, null=True)
    driver_license_no = models.BooleanField("Has Driver's License ? ", default=False, blank=True, null=True)
    ssnit_number = models.CharField(max_length=60, blank=True, null=True)
    tin_number = models.CharField(max_length=60, blank=True, null=True)
    ghana_card_no = models.CharField(max_length=60, blank=True, null=True)
    education_background = RichTextField(blank=True, null=True)
    work_experience = RichTextField(blank=True, null=True)
    reference = models.CharField(max_length=250, blank=True, null=True)
    highest_qualification = models.ForeignKey(Qualification, on_delete=models.DO_NOTHING,
                      related_name="elogistics_personnel_highest_qualification_relates_to_qualification_relatiuon",
                      blank=True, null=True
    )
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    allowance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    currency = models.CharField("Currency", max_length=30, choices=CURRENCY, default='Ghc', blank=True, null=True)
    # bank = models.ForeignKey(Bank, on_delete=models.DO_NOTHING,
    #         related_name="elogistics_personnel_bank_relates_to_bank_relatiuon", blank=True, null=True)
    bank = models.CharField("Bank ", max_length=60, blank=True, null=True)
    bank_branch = models.CharField("Bank Branch", max_length=60, blank=True, null=True)
    role = models.ForeignKey(Position, on_delete=models.DO_NOTHING,
            related_name="elogistics_employee_position_relates_to_role_relatiuon", blank=True, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.DO_NOTHING,
            related_name="elogistics_personnel_branch_relates_to_organization_branch_relatiuon",
            blank=True, null=True)
    account_no = models.CharField("Bank Account No#",max_length=60, blank=True, null=True)

    # leave_profile = models.ForeignKey(OrganizationLeaveProfile, on_delete=models.DO_NOTHING,
    #           related_name="elogistics_personnel_leave_profile_relates_to_organization_leave_profile_relatiuon",
    # blank=True, null=True)
    latest_apprisal_score = models.IntegerField(verbose_name='Last Apprisal Score', blank=True, null=True)
    outstanding_leave_days = models.IntegerField(verbose_name='Outstanding Leave Days', default=0,blank=True, null=True)
    outstanding_sick_leave_days = models.IntegerField(verbose_name='Outstanding Sick Leave Days', blank=True,                                                    null=True)
    total_leave_days_entitled_to = models.IntegerField(verbose_name='Total Leave days entitled', default=0, blank=True,
                                                 null=True)
    total_sick_leave_days_entitled_to = models.IntegerField(verbose_name='Total Sick leave days entitled to', blank=True,
                                                      null=True)
    # guarantors = models.CharField(max_length=60, blank=True, null=True)
    photo = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        related_name="elogistics_employee_photo_relates_to_photo",
        # upload_to='talent/photos',
        blank=True, null=True, max_length=550
    )
    photo_ext = models.ImageField(upload_to='images/', blank=True, null=True, max_length=200)
    identification = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        related_name="+",
        # upload_to='talent/photos',
        blank=True, null=True, max_length=550
    )
    identification_ext = models.ImageField(upload_to='images/', blank=True, null=True,max_length=200)

    employment_date = models.DateField(verbose_name="Date of Employment", blank=True, null=True)
    exit_date = models.DateField(verbose_name="Date Emploment ended", blank=True, null=True)

    latest_score = models.SmallIntegerField(blank=True, null=True)

    region = models.ForeignKey(Region, on_delete=models.DO_NOTHING,
              related_name="elogistics_personnel_region_relates_to_region_relation",
              blank=True, null=True,
     )
    location = models.ForeignKey(Location, on_delete=models.DO_NOTHING,
              related_name="elogistics_personnel_location_relates_to_location_relation",
              blank=True,  null=True
     )

    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING,
             related_name="elogistics_personnel_org_department_department_relates_to_organization_manager_relatiuon",
             blank=True, null=True
    )

    # status = models.CharField(max_length=60, blank=True, null=True)
    status = models.CharField(max_length=30, choices=EMPLOYMENT_STATUS, blank=True, null=True, default='employed')
    is_leader = models.BooleanField("Manages Other Personnel",blank=True, null=True, default=False)
    is_active = models.BooleanField(blank=True, null=True, default=True)

    facebook = models.URLField(blank=True, null=True,)
    twitter = models.URLField(blank=True, null=True, )
    linkedin = models.URLField(blank=True, null=True, )

    user = models.ForeignKey(
        User,
        on_delete = models.DO_NOTHING,
        related_name = 'elogistics_personnel_user_connect_user_relation',  # limit_choices_to={'is_staff': True},
        blank = True,
        null = True, unique=True
    )

    import_batch_code = models.CharField(verbose_name="Import Batch Code",max_length=50, blank=True, null=True)

    more_info = models.CharField(unique=True, max_length=250, blank=True, null=True)
    search_term =  models.CharField(max_length=250, blank=True, null=True)

    # def save(self, *args, **kwargs):
    #
    #     # if self.
    #     try:
    #         #     # self.start_date- self.end_date
    #         #     self.duration = self.start_date- self.end_date
    #         self.duration = busday_count(self.start_date, self.return_date)
    #
    #     # np.busyday_count('2019-01-21', '2020-03-28', weekmask=[1, 1, 1, 1, 1, 0, 0], holidays=['2020-01-01'])
    #     except:
    #         pass
    #     if self.duration < 1 or self.duration == 0:
    #         raise Exception("Negative or Zero Leave Duration. Kindly Check Leave Dates")
    #
    #     if self.personnel.leave_profile is None:
    #         raise Exception("Kindly Set Personnel Leave Profile and try again")
    #
    #     # if self.name == "Yoko Ono's blog":
    #     # request = self.request.user
    #     # print(request)
    #     # print(user)
    #     # if request.user.groups.filter(name__in=["Personnel", "personnel"]):
    #     #     print('Ware in Gere')
    #     #     return  # Yoko shall never have her own blog!
    #     # else:
    #     super().save(*args, **kwargs)  # Call the "real" save() method.

    def save(self, *args, **kwargs):
        """
            outstanding_leave_days - Outstanding Leave Days
            outstanding_sick_leave_days - Outstanding Sick Leave Days
            total_leave_days_entitled_to - Total Leave days entitled
            total_sick_leave_days_entitled_to
        """
        the_leaves = None
        #     # outstanding_leave_days,outstanding_sick_leave_days,
        #     # total_leave_days_entitled_to,total_sick_leave_days_entitled_to
        #     try:
        #         #     # self.start_date- self.end_date
        #         #     self.duration = self.start_date- self.end_date
        #         self.duration = busday_count(self.start_date, self.return_date)
        #
        #     # np.busyday_count('2019-01-21', '2020-03-28', weekmask=[1, 1, 1, 1, 1, 0, 0], holidays=['2020-01-01'])
        #     except:
        #         pass
        #     if (self.duration < 1 or self.duration == 0):  # and not self.allow_negative:
        #         raise Exception("Negative or Zero Leave Duration. Kindly Check Leave Dates")
        #
        #     if self.personnel.leave_profile is None:
        #         raise Exception("Kindly Set Personnel Leave Profile and try again")
        #
        #     # outstanding_leave_days, outstanding_sick_leave_days
        #
        #     # self.personnel.outstanding_leave_days -= self.duration
        #
        if self.leave_profile:
            pass
            # the_leave_profile = OrganizationLeaveProfile.objects.filter(id=self.id,status__icontains='used')

        try:
            the_leaves = PersonnelLeave.objects.filter(personnel_id=self.id,status__icontains='used')
        except:
            pass
        #
        if the_leaves:
    #         #
    #         # the_personnel.outstanding_leave_days =  the_personnel.total_leave_days_entitled_to
    #         # the_personnel.outstanding_sick_leave_days = the_personnel.total_sick_leave_days_entitled_to
            self.outstanding_leave_days =  self.total_leave_days_entitled_to
            self.outstanding_sick_leave_days = self.total_sick_leave_days_entitled_to
            for leave in the_leaves:
                if str(leave.leave_type).lower() == 'sick leave':
                    self.outstanding_sick_leave_days = self.outstanding_sick_leave_days - leave.duration
                else:
                    self.outstanding_leave_days = self.outstanding_leave_days - leave.duration
            # elif self.status == 'sick leave':
    #         #     the_personnel.outstanding_leave_days = the_personnel.outstanding_leave_days - self.duration
    #         the_personnel.save()
    #
    #     if not self.organization_id:
    #         self.organization_id = self.personnel.organization_id
    #
        super().save(*args, **kwargs)  # Call the "real" save() method.

    panels =  [
        # FieldPanel('title'),
        FieldPanel('appid'),
        FieldPanel('first_name'),
        FieldPanel('middle_name'),
        FieldPanel('last_name'),
        FieldPanel('gender'),
        FieldPanel('birth_date'),
        FieldPanel('birth_place'),
        FieldPanel('parent_name'),
        FieldPanel('payroll_code'),
        FieldPanel('postal_address'),
        FieldPanel('digital_address'),
        FieldPanel('res_address'),
        FieldPanel('residential_country'),
        FieldPanel('residential_city'),
        FieldPanel('residential_region'),
        FieldPanel('directional_map'),
        FieldPanel('phone_no'),
        FieldPanel('other_phone_nos'),
        FieldPanel('email'),
        FieldPanel('marital_status'),
        FieldPanel('next_kin'),
        FieldPanel('driver_license_no'),
        FieldPanel('ssnit_number'),
        FieldPanel('tin_number'),
        FieldPanel('ghana_card_no'),
        FieldPanel('education_background'),
        FieldPanel('work_experience'),
        FieldPanel('reference'),
        FieldPanel('highest_qualification'),
        FieldPanel('currency'),
        FieldPanel('salary'),
        FieldPanel('hourly_rate'),
        FieldPanel('allowance'),

        FieldPanel('pension_id'),
        # FieldPanel('role'),
        FieldPanel('bank'),
        FieldPanel('branch'),
        FieldPanel('account_no'),
        FieldPanel('checklist_profile'),
        FieldPanel('latest_apprisal_score'),
        # FieldPanel('appid'),

        FieldPanel('code'),
        FieldPanel('payroll_code'),
        FieldPanel('organization'),
        FieldPanel('photo'),
        FieldPanel('identification'),
        FieldPanel('territory'),
        FieldPanel('region'),
        FieldPanel('location'),
        FieldPanel('division'),
        FieldPanel('employment_date'),
        FieldPanel('role'),
        FieldPanel('reports_to_client'),
        FieldPanel('reports_to_personnel'),
        FieldPanel('leave_profile'),
        FieldPanel('user'),
        FieldPanel('is_core_staff'),
        FieldPanel('is_leader'),
        FieldPanel('status'),
        FieldPanel('cleaned'),
        # FieldPanel('primary_region_preferred'),
        # InlinePanel('elogistics_Talent_job_relation', label="Recruit for Position"),

    ]

    # personnel_leave_panel = [
    #      InlinePanel('outsource_main_personnel_leave_connects_personnel_relations', label="Add Leave"),
    # ]

    # medical_card_panel = [
    #     InlinePanel('outsource_main_personnel_medical_connect_personnel_relation', label="Add Medical Card"),
    # ]

    dependant_panel = [
        InlinePanel('personnel_dependant_personnel_relate_personnel_relation', label="Add Dependant",  min_num=None),
    ]
    edit_handler = TabbedInterface(
        [
            ObjectList(panels, heading="Personnel Form"),
            # ObjectList(personnel_leave_panel, heading="Leave"),
            ObjectList(dependant_panel, heading="Dependant", ),
        ]
    )

    class Meta:
        pass
        # permissions = [
        #     # ("owner", "Owns the Record"),
        #     # ("can_add_talent_at_frontend", "Can add a Talent at front end"),
        #     # # ("close_task", "Can remove a task by setting its status as closed"),
        # ]
        # managed = False
        # db_table = 'talent'

    def __str__(self):  # __unicode__ on Python 2
        return f"{self.first_name} {self.middle_name} {self.last_name}"
        # return f"{self.organization} - {self.first_name} {self.middle_name} {self.last_name}"
        # return "%s appid( %s )" % (self.full_name, self.appid)
        # return self.other_names + " " + self.last_name

    def talent_skill(self):
        return ', '.join([s.name for s in self.skill.all()])

    @property
    def full_name(self):
        "Returns the person's full name."
        name = self.first_name+" " if self.first_name else ""
        name += self.middle_name+" " if self.middle_name else ""
        name += self.last_name if self.last_name else ""
        # return '%s %s %s' % (self.first_name, self.middle_name, self.last_name)
        return name

    full_name.fget.short_description = "Name"

    @property
    def get_phone(self):
        "Returns the person's full name."
        return '%s, %s' % (self.phone_no, self.other_phone_nos)

    @property
    def get_residence(self):
        "Returns the person's full name."
        return '%s %s, Ghana' % (self.residential_city, self.residential_region)

    @property
    def get_gender(self):
        "Returns the person's full name."
        gen = None
        if self.gender:
            gen = self.gender[0].upper()
            # return (self.gender[0].upper())
        return gen

    @property
    def one_name(self):
        "Returns the person's full name."
        return (self.last_name.split(" "))[0]

    @property
    def get_role_name(self):
        try:
            return self.role.name
        except:
                return "None"

    get_role_name.fget.short_description = "Role"

    @property
    def get_name_and_organization(self):
        return self.first_name + " " + self.last_name + "  ," + self.organization.name

    @property
    def get_branch_name(self):
        try:
            return self.branch.name
        except:
                return "None"
    get_branch_name.fget.short_description = "Branch"

    @property
    def get_department_name(self):
        return self.department.name

    get_department_name.fget.short_description = "Department"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('personnel-detail', args=[str(self.id)])

    search_fields = [
        index.SearchField('organization', partial_match=True),
        index.SearchField('get_name_and_organization'),
        index.SearchField('first_name'),
        index.SearchField('middle_name'),
        index.SearchField('last_name'),

    ]
        # Only show people managed by the current user
        # return qs.filter(managed_by=request.user)

    # def get_is_staff_only(self):
    #     g = Personnel.objects.get(name='Tool Editors')
    #     return {'groups__in': [g, ]}


@register_snippet
class Client(ClusterableModel, CommonInfo):
    # For Wagtail
    # parent_page_types = [
    #     'base.OrganizationIndexPage'
    # ]
    client_feature_image_370x570 = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True, on_delete=models.SET_NULL,
        help_text="This Photo",
        related_name='elogistics_client_feature_image_370x570_relates_to_logo_relation',
        # limit_choices_to={'is_staff': True},
    )
    body = RichTextField("More Information",blank=True, null=True)
    intro = models.CharField(max_length=150, blank=True, null=True)
    # date = models.DateField("Creation date")
    name = models.CharField(max_length=200,unique=True, blank=True, null=True )
    code = models.CharField(max_length=100, unique=True, blank=True, null=True)
    main_office_unique_gps_address = models.CharField(max_length=50, verbose_name='Digital Address', blank=True, null=True)
    postal_address = models.CharField(max_length=150, blank=True, null=True)
    main_office_location = models.CharField(max_length=200, blank=True, null=True, verbose_name="Direction")
    phone_no = models.CharField(max_length=200, blank=True, null=True, verbose_name="Phone No.#")
    email = models.EmailField(max_length=60, blank=True, null=True)
    # profile = models.TextField(blank=True, null=True)
    is_active = models.BooleanField("Is Active", choices=YES_NO, default=True)

    primary_industry = models.ForeignKey(
        Industry, on_delete=models.DO_NOTHING,
        related_name='elogistics_organization_connects_industry_relation',  # limit_choices_to={'is_staff': True},
        blank=True, null=True, verbose_name="Industry"
    )

    other_industries = models.CharField(max_length=250, blank=True, null=True)
    contact_person = models.CharField(max_length=250, blank=True, null=True)
    contact_person_email = models.EmailField(max_length=50, blank=True, null=True)
    contact_person_phone = models.CharField(max_length=50, blank=True, null=True)
    contact_person_position = models.CharField(max_length=50, blank=True, null=True)
    website = models.CharField(max_length=150, blank=True, null=True)
    sms_phone_no = models.CharField(max_length=15, blank=True, null=True, verbose_name='SMS No.#')

    logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text = "This is the Organizations Logo and will be cropped to 570 by 370",
        related_name = 'elogistics_organizationpage_logo_relates_to_logo_relation',  # limit_choices_to={'is_staff': True},
    )
    logo_ext = models.ImageField(upload_to='images/', blank=True, null=True)
    country = models.ForeignKey(
        Country,  # on_delete=models.CASCADE,
        on_delete=models.DO_NOTHING,
        related_name='elogistics_organization_country_connect_country_relation',  # limit_choices_to={'is_staff': True},
        # default="Ghana",
        blank=True,
        null=True
    )
    # rating = models.SmallIntegerField("Rating", default=0)
    # staff_strength = models.IntegerField("Staff Strength", default=0, blank=True, null=True)
    is_locked = models.BooleanField(choices=YES_NO, default=False)
    is_verified = models.BooleanField(choices=YES_NO, default=False)

    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name='elogistics_organization_user_connect_user_relation',  # limit_choices_to={'is_staff': True},
        blank=True,
        null=True,
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('logo'),
        FieldPanel('main_office_unique_gps_address'),
        # FieldPanel('recruitment_email'),
        # FieldPanel('recruitment_phone'),
        FieldPanel('code'),
        FieldPanel('country'),
        FieldPanel('email'),
        FieldPanel('phone_no'),
        FieldPanel('website'),
        FieldPanel('contact_person'),
        FieldPanel('contact_person_phone'),
        FieldPanel('contact_person_position'),
        FieldPanel('contact_person_email'),
        FieldPanel('body', classname="full"),
        # FieldPanel('alternative_name'),
        # FieldPanel('use_alt_name'),
        # InlinePanel('elogistics_organization_coordinator_organization_organization', label="Add Coordinator"),
        # InlinePanel('elogistics_coordinator_organization_relate_to_organization', label="Add Coordinator"),
    ]

    # coordinator_link_panel = [
    #     InlinePanel('elogistics_coordinator_organization_relate_to_organization', label="Add Coordinator"),
    # ]
    #
    # edit_handler = TabbedInterface(
    #     [
    #         ObjectList(panels, heading="Personnel Form"),
    #         ObjectList(coordinator_link_panel, heading="Coordinators"),
    #     ]
    # )
    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Organizations"

    def __str__(self):
        return self.name

    search_fields = [
        index.SearchField('name', partial_match=True),
    ]

    # @register_snippet
    
    
class Branch(CommonInfo):
    name = models.CharField(max_length=100)
    # country = models.ForeignKey(Country, on_delete=models.DO_NOTHING,
    #                             related_name="elogistics_organization_branch_relates_to_country", blank=True, null=True)
    region = models.ForeignKey(
        Region,  # on_delete=models.CASCADE,
        on_delete=models.DO_NOTHING,

        related_name='elogistics_organization_branch_region_connect_region_relation',
        # limit_choices_to={'is_staff': True},
        # default="Ghana",
        # on_update=models.CASCADE,
        blank=True,
        null=True
    )
    location = models.ForeignKey(
        Location,  # on_delete=models.CASCADE,
        on_delete=models.DO_NOTHING,

        related_name='elogistics_organization_branch_location_connect_Location_relation',
        # limit_choices_to={'is_staff': True},
        # default="Ghana",
        # on_update=models.CASCADE,
        blank=True,
        null=True
    )
    branch_address = models.CharField(max_length=100, blank=True, null=True)
    phone_no = models.CharField(max_length=100, blank=True, null=True)
    more_information = RichTextField(blank=True, null=True)
    personnel_count = models.PositiveSmallIntegerField(blank=True, null=True)
    import_code = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Branches"

    def __str__(self):
        return f"{self.name} "

    panels = [
        FieldPanel('name'),
        # FieldPanel('country'),
        FieldPanel('region'),
        FieldPanel('location'),
        FieldPanel('organization'),
        FieldPanel('phone_no'),
        FieldPanel('more_information'),
        # FieldPanel('import_code'),
    ]

    search_fields = [
        index.SearchField('name'),
        # index.SearchField('organization__name'),

        # index.RelatedFields('organization', [
        #     index.SearchField('name'),
        # ]),
    ]


class ProjectStage(CommonInfo):
    pass


class ProjectNote(CommonInfo):
    pass


class Project(ClusterableModel, CommonInfo):
    title = models.CharField(max_length=250, blank=True, null=True)
    client = models.ForeignKey(
        Client, on_delete=models.DO_NOTHING,
        related_name='elogistics_project_connects_client_relation',  # limit_choices_to={'is_staff': True},
        blank=True, null=True, verbose_name="Industry"
    )
    description = RichTextField(blank=True, null=True)
    report = RichTextField(blank=True, null=True)
    cost = models.DecimalField(verbose_name="Cost", max_digits=10, decimal_places=2, default=0.00, blank=True,
                                 null=True)
    photo_1 = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text = "This Photo",
        related_name = 'elogistics_photo_1_relates_to_logo_relation',  # limit_choices_to={'is_staff': True},
    )
    photo_2 = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True, on_delete=models.SET_NULL,
        help_text = "This Photo",
        related_name = 'elogistics_photo_2_relates_to_logo_relation',  # limit_choices_to={'is_staff': True},
    )
    photo_3 = models.ForeignKey(
        'wagtailimages.Image',
        null=True,blank=True,on_delete=models.SET_NULL,
        help_text = "This Photo",
        related_name = 'elogistics_photo_3_relates_to_logo_relation',  # limit_choices_to={'is_staff': True},
    )
    photo_4 = models.ForeignKey(
        'wagtailimages.Image',
        null=True,blank=True,on_delete=models.SET_NULL,
        help_text = "This Photo",
        related_name = 'elogistics_photo_4_relates_to_logo_relation',  # limit_choices_to={'is_staff': True},
    )
    feature_image_370x570 = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True, on_delete=models.SET_NULL,
        help_text="This Photo",
        related_name='elogistics_feature_image_370x570_relates_to_logo_relation',  # limit_choices_to={'is_staff': True},
    )
    stage = models.ForeignKey(
        ProjectStage,  # on_delete=models.CASCADE,
        on_delete=models.DO_NOTHING,
        related_name='elogistics_stage_connect_toproject_stages_relation',  # limit_choices_to={'is_staff': True},
        # default="Ghana",
        blank=True,
        null=True
    )
    start_date = models.DateField(verbose_name="Start Date", blank=True, null=True, default=timezone.now)
    completion_date = models.DateField(verbose_name="Completion Date", blank=True, null=True,
    class Meta:
        unique_together = ['title', 'client']
