from odoo import fields, models, api
import base64
import csv
import io
import xlrd
from odoo.exceptions import UserError  # type: ignore


class ImportChecklistWizard(models.TransientModel):
    _name = "sh.import.checklist"
    _description = "Import checklist Data"

    name = fields.Char()
    import_file_type = fields.Selection(
        [("csv", "CSV File"), ("exl", "Excel File")], default="csv"
    )
    company_id = fields.Many2one(
        "res.company", string="company", default=lambda self: self.env.company.id
    )
    file = fields.Binary(string="File")

    def process_file(self):
        if self.file:
            if self.import_file_type == "csv":
                self._process_csv()
            elif self.import_file_type == "exl":
                self._process_excel()
            else:
                raise UserError(
                    "Unsupported file format. Please upload CSV or Excel file."
                )
        else:
            raise UserError("Please enter the file")

    def _process_csv(self):
        decoded_file = base64.b64decode(self.file)

        try:
            file_io = io.StringIO(decoded_file.decode("utf-8"))
            reader = csv.DictReader(file_io)
        except Exception as e:
            raise UserError(f"Failed to read CSV content: {str(e)}")

        for row in reader:
            print('\n\n\n-----row.get("name")------->', row.get("Name"))
            self.env["sh.manufacturing.checklist"].create(
                {
                    "name": row.get("Name"),
                    "description": row.get("Description"),
                    "company_id": self.company_id.id,
                }
            )
        self.env["bus.bus"]._sendone(
            self.env.user.partner_id,
            "simple_notification",
            {
                "type": "success",
                "title": "success",
                "message": "Data imported successfully from CSV file",
            },
        )

    def _process_excel(self):
        decoded_file = base64.b64decode(self.file)
        if self.import_file_type == "exl":
            workbook = xlrd.open_workbook(file_contents=decoded_file)
            sheet = workbook.sheet_by_index(0)
            headers = sheet.row_values(0)

            for row_idx in range(1, sheet.nrows):
                row = sheet.row_values(row_idx)
                data = dict(zip(headers, row))
                print(f"Row {row_idx}: {row}")

                self.env["sh.manufacturing.checklist"].create(
                    {
                        "name": data.get("Name"),
                        "description": data.get("Description"),
                        "company_id": self.company_id.id,
                    }
                )
            self.env["bus.bus"]._sendone(
            self.env.user.partner_id,
            "simple_notification",
            {
                "type": "success",
                "title": "success",
                "message": "Data imported successfully from Excel file",
            },
        )

