from django.core.management.base import BaseCommand
from db_app.models import User_Restrictions
from db_app.management.commands.restrictions import DataUpdater
import db_app.management.commands.FAO as FAO

PATH = "data/accounts.xlsx"

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        workbook_obj = FAO.Work_Book(PATH)
        worksheet_obj = FAO.WorkSheet(workbook_obj)
        data_object = FAO.TableData(worksheet_obj)
        updated_data_obj = DataUpdater(data_object)
        updated_data = updated_data_obj.update_data_dict()
        for data in updated_data:
            models = User_Restrictions(bank_id = data['bank'], account_id = data['account'], branch_id = data['branch'], isrestricted = data['isrestricted'], expiration_date = data['expiration_date'])
            models.save()
