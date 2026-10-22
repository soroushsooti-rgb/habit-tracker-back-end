"""مدل‌های ردیابی عادت.

این ماژول مدل‌های دیتابیس را برای مدیریت عادات کاربر و پیگیری لاگ‌های تکمیل آن‌ها
بر اساس تناوب‌های مختلف (روزانه، هفتگی، ماهانه) تعریف می‌کند.
"""


from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
"""نگاشت عددی (0-6) به روزهای هفته، مطابق با متد weekday در پایتون."""

DAYS_OF_WEEK = (
    (0, 'Monday'),
    (1, 'Tuesday'),
    (2, 'Wednesday'),
    (3, 'Thursday'),
    (4, 'Friday'),
    (5, 'Saturday'),
    (6, 'Sunday'),
)

"""نماینده یک عادت تکرارپذیر کاربر با تنظیمات تناوب و یادآور.

ویژگی‌ها:
    name (str): عنوان توصیفی عادت.
    user (ForeignKey): ارجاع به مالک عادت (AUTH_USER_MODEL).
    frequency (str): دوره تکرار (DAILY, WEEKLY, یا MONTHLY).
    day_of_week (int | None): اندیس روز هدف (0-6) برای عادات هفتگی.
    day_of_month (int | None): روز تقویمی هدف (1-31) برای عادات ماهانه.
    reminder_time (time | None): زمان یادآور روزانه تنظیم‌شده.
    created_at (datetime): برچسب زمانی ایجاد رکورد عادت.
"""


class Habit(models.Model):

    """شمارشی از تناوب‌های پشتیبانی‌شده برای تکرار عادت."""

    class Frequency(models.TextChoices):
        DAILY = 'DAILY'
        WEEKLY = 'WEEKLY'
        MONTHLY = 'MONTHLY'

    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,

    )
    frequency = models.CharField(
        max_length=10,
        choices=Frequency.choices,
        default=Frequency.DAILY,
        verbose_name='loop'
    )
    day_of_week = models.PositiveSmallIntegerField(
        choices=DAYS_OF_WEEK,
        null=True,
        blank=True,
    )
    day_of_month = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )
    reminder_time = models.TimeField(
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):

        super().clean()
        """اعتبارسنجی فیلدهای زمان‌بندی متناقض بر اساس تناوب انتخابی.

            قوانین زمان‌بندی را به شرح زیر اعمال می‌کند:
                - روزانه (DAILY): به `reminder_time` نیاز دارد؛ فیلدهای `day_of_week` و `day_of_month` را خالی می‌کند.
                - هفتگی (WEEKLY): به `day_of_week` نیاز دارد؛ فیلدهای `reminder_time` و `day_of_month` را خالی می‌کند.
                - ماهانه (MONTHLY): به `day_of_month` (1-31) نیاز دارد؛ فیلدهای `reminder_time` و `day_of_week` را خالی می‌کند.

            خطاها:
                ValidationError: اگر فیلدهای زمان‌بندی مورد نیاز برای تناوب انتخابی موجود نباشند یا نامعتبر باشند.
            """
        if self.frequency == self.Frequency.DAILY:
            if not self.reminder_time:
                raise ValidationError(
                    'You must specify a time for daily habits.')
            self.day_of_week = None
            self.day_of_month = None

        elif self.frequency == self.Frequency.WEEKLY:
            if self.day_of_week is None:
                raise ValidationError(
                    'You must select a day of the week for weekly habits.')
            self.reminder_time = None
            self.day_of_month = None

        elif self.frequency == self.Frequency.MONTHLY:
            if not self.day_of_month:
                raise ValidationError(
                    'You must specify a day of the month for monthly habits.')
            if not (1 <= self.day_of_month <= 31):
                raise ValidationError(
                    'The day of the month must be between 1 and 31.')
            self.reminder_time = None
            self.day_of_week = None

    """ذخیره‌سازی نمونه عادت پس از اجرای اعتبارسنجی‌های مدل.

قبل از ذخیره در دیتابیس، `full_clean()` را فراخوانی می‌کند تا قوانین تجاری تعریف شده در `clean()` اعمال شوند.

آرگومان‌ها:
    *args: آرگومان‌های پوزیشنال ارسالی به `models.Model.save`.
    **kwargs: آرگومان‌های کلیدی ارسالی به `models.Model.save`.
"""

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    """متادیتا و محدودیت‌های مدل Habit."""

    class Meta:
        """متادیتا و محدودیت‌های مدل Habit."""
        unique_together = [('user', 'name')]
        indexes = [
            models.Index(fields=['user', 'name'], name='idx_habit_date'),
        ]
        ordering = ['user', 'frequency']

    """بازگرداندن رشته نمایش دهنده عادت.

خروجی:
    str: نام عادت.
"""

    def __str__(self):
        return f"{self.name}"


class HabitCheck(models.Model):
    """نماینده یک رکورد اجرایی که تأیید می‌کند عادت در تاریخ مشخصی تکمیل شده است.

    ویژگی‌ها:
        habit (ForeignKey): ارجاع به نمونه Habit مرتبط.
        checked_date (date): تاریخ تقویمی که عادت در آن به عنوان تکمیل‌شده علامت‌گذاری شده است.
    """
    habit = models.ForeignKey(
        Habit,
        on_delete=models.CASCADE,

    )
    checked_date = models.DateField(default=timezone.now)
    """اعتبارسنجی انطباق تاریخ تکمیل با قوانین تناوب عادت.

اطمینان حاصل می‌کند که:
    - عادات هفتگی فقط در `day_of_week` پیکربندی‌شده قابل بررسی هستند.
    - عادات ماهانه فقط در `day_of_month` پیکربندی‌شده قابل بررسی هستند.

خطاها:
    ValidationError: اگر `checked_date` با محدودیت‌های تناوب عادت مرتبط مطابقت نداشته باشد.
"""

    def clean(self):
        super().clean()
        if not hasattr(self, 'habit'):
            return

        if self.habit.frequency == Habit.Frequency.WEEKLY:
            if self.checked_date.weekday() != self.habit.day_of_week:
                raise ValidationError(
                    'This habit can only be checked on the selected day of the week.')

        elif self.habit.frequency == Habit.Frequency.MONTHLY:
            if self.checked_date.day != self.habit.day_of_month:
                raise ValidationError(
                    'This habit can only be checked on the selected day of the month.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    """متادیتا و محدودیت‌های مدل HabitCheck."""

    class Meta:
        """متادیتا و محدودیت‌های مدل HabitCheck."""
        unique_together = [('habit', 'checked_date')]
        indexes = [
            models.Index(fields=['habit', 'checked_date'],
                         name='idx_checked_date'),
        ]
        ordering = ['-checked_date']

    """بازگرداندن رشته نمایش دهنده رویداد بررسی عادت.

خروجی:
    str: ترکیب نام عادت و تاریخ بررسی.
"""

    def __str__(self):
        return f"{self.habit.name} - {self.checked_date}"
