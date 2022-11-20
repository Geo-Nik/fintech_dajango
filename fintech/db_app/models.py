from django.db import models

# Create your models here.
class User_Restrictions(models.Model):
    bank_id = models.PositiveIntegerField('Bank_id')
    account_id = models.PositiveIntegerField('Account_id')
    branch_id = models.PositiveIntegerField('Branch_id')
    isrestricted =models.BooleanField('Is_Restricted')
    expiration_date =models.DateField('Expiration_Date', null=True, blank=True)


    def __str__(self):
        return str(self.account_id)

    class Meta:
        verbose_name = "User_Restriction"
        verbose_name_plural = "User_Restrictions"

 