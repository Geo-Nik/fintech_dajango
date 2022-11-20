import openpyxl
import logging


def format_data_in_tuple(tuple_):
    list_ = [
        tuple_item.strip() if isinstance(tuple_item, str) else tuple_item
        for tuple_item in tuple_
    ]
    return tuple(list_)


def are_ends_of_range_int(ends_of_range: dict):
    if isinstance(ends_of_range['min'], int) and isinstance(
                    ends_of_range['max'], int):
        return True
    else:
        logging.error(f"The ends of the range {ends_of_range} are not integer.")
        return False


def are_ends_of_range_positive(ends_of_range: dict):
    if ends_of_range['min'] >= 0 and ends_of_range['max'] >= 0:
        return True
    else:
        return False


def is_max_more_than_min(ends_of_range: dict):
    if ends_of_range['max'] >= ends_of_range['min']:
        return True
    else:
        return False


def is_list_contains(List1, List2):
    set1 = set(List1)
    set2 = set(List2)
    if set1.intersection(set2) == set1:
        return True
    else:
        return False


class Work_Book:
    def __init__(self, path):
        self.path = path

    def load(self):
        try:
            # Define variable to load the wookbook
            workbook = openpyxl.load_workbook(self.path)
        except FileNotFoundError as err:
            logging.error(f"Error: File not found. Details:{err}")
            return
        except OSError as err:
            logging.error(f"Error: Can not open file. Details:{err}")
            return
        return workbook


class WorkSheet:
    def __init__(self, workbook_obj, worksheet_name=None):
        self.worksheet_name = worksheet_name
        self.workbook_obj = workbook_obj

    def read_worksheet(self):
        self.workbook = self.workbook_obj.load()
        if not self.workbook:
            return
        if self.worksheet_name:
            try:
                worksheet = self.workbook[self.worksheet_name]
            except KeyError as err:
                logging.error(f"KeyError:{err}")
                return
        else:
            worksheet = self.workbook.active
        return worksheet


class Range:
    def __init__(self, auto_ends: dict, custum_ends: dict = None):
        self.custum_ends = custum_ends
        self.auto_ends = auto_ends

    def _get_custom_range(self):
        custom_range = range(self.custum_ends['min'],
                             self.custum_ends['max'] + 1)
        auto_range = range(self.auto_ends['min'], self.auto_ends['max'] + 1)
        if is_list_contains(list(custom_range), list(auto_range)):
            return self.custum_ends
        else:
            logging.warning(f"The custom range [{self.custum_ends['min']},"
                            f"{self.custum_ends['max']}] exceeds hard limit"
                            f"[{self.auto_ends['min']},{self.auto_ends['max']}]"
                            ". Was returned automatic values based on current "
                            "worksheet instead.")
            return self.auto_ends

    def set_range(self):
        assert_comment1 = "The custom range should be positive."
        assert_comment2 = "The max of range should be more than min."
        assert are_ends_of_range_positive(self.auto_ends), assert_comment1
        assert is_max_more_than_min(self.auto_ends), assert_comment2

        if are_ends_of_range_int(self.auto_ends):
            if self.custum_ends is None:
                return self.auto_ends
            elif are_ends_of_range_int(self.custum_ends):
                return self._get_custom_range()


class TableRanges:
    def __init__(self, worksheet, row_col_ranges_dict: dict = None):
        if row_col_ranges_dict:
            try:
                self.row_custom_ends = {
                                        'min': row_col_ranges_dict["min_row"],
                                        'max': row_col_ranges_dict["max_row"],
                                        }
                self.col_custom_ends = {
                                        'min': row_col_ranges_dict["min_col"],
                                        'max': row_col_ranges_dict["max_col"],
                                        }
            except KeyError as err:
                logging.warning("KeyError: The key of row_col_ranges_dict "
                                f"variable is not correct:{err}. "
                                "Was returned automatic "
                                "values based on current worksheet instead.")
                self.row_custom_ends = None
                self.col_custom_ends = None

        else:
            self.row_custom_ends = None
            self.col_custom_ends = None

        self.row_auto_ends = {
                              'min': worksheet.min_row,
                              'max': worksheet.max_row,
                              }
        self.col_auto_ends = {
                              'min': worksheet.min_column,
                              'max': worksheet.max_column,
                              }

    def get_ranges(self):
        row = Range(self.row_auto_ends, self.row_custom_ends)
        col = Range(self.col_auto_ends, self.col_custom_ends)
        row_range_dict = row.set_range()
        col_range_dict = col.set_range()
        if row_range_dict and col_range_dict:
            return {'row': row_range_dict, 'col': col_range_dict}


class TableData:
    def __init__(self, worksheet_obj, row_col_ranges_dict: dict = None):
        self.row_col_ranges_dict = row_col_ranges_dict
        self.worksheet_obj = worksheet_obj

    def get_data_from_worksheet(self):
        worksheet = self.worksheet_obj.read_worksheet()
        if not worksheet:
            return

        worksheet_ranges_obj = TableRanges(worksheet, self.row_col_ranges_dict)
        worksheet_ranges = worksheet_ranges_obj.get_ranges()
        if not worksheet_ranges:
            return
        worksheet_iterator = worksheet.iter_rows(
            min_row=worksheet_ranges['row']['min'],
            max_row=worksheet_ranges['row']['max'],
            min_col=worksheet_ranges['col']['min'],
            max_col=worksheet_ranges['col']['max'],
            values_only=True,
        )

        table_head = next(worksheet_iterator)
        table_head = format_data_in_tuple(table_head)
        data_list_of_dicts = []
        for value in worksheet_iterator:
            value = format_data_in_tuple(value)
            new_dict = dict(zip(table_head, value))
            data_list_of_dicts.append(new_dict)

        return data_list_of_dicts


if __name__ == "__main__":
    path = "data/accounts.xlsx"
    workbook_obj = Work_Book(path)
    worksheet_obj = WorkSheet(workbook_obj)
    data_object = TableData(worksheet_obj)
    data = data_object.get_data_from_worksheet()
    print(data)

