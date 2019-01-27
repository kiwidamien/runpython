import json


class Cell(object):
    def __init__(self, cell_dict):
        self.raw = cell_dict
        self.cell_type = cell_dict['cell_type']
        self.execution_count = cell_dict.get('execution_count')
        if isinstance(cell_dict['source'], list):
            self.source = ''.join(cell_dict['source'])
        else:
            self.source = cell_dict['source']
        self.errors = []
        for output in cell_dict.get('outputs', []):
            if output['output_type'] == 'error':
                error_obj = {key: output[key]
                             for key in ['ename', 'evalue', 'traceback']}
                self.errors.append(error_obj)

    def get_type(self):
        return self.cell_type

    def number_of_errors(self):
        return len(self.errors)

    def contains_errors(self):
        return (self.number_of_errors() > 0)

    def first_error_message(self):
        if self.errors:
            first_error = self.errors[0]
            return f"{first_error['ename']}: {first_error['evalue']}"
        return ""

    def __str__(self):
        msg = f"(self.cell_type) [{self.execution_count}]: {self.source[:20]}"
        return msg

    def __repr__(self):
        msg = f"""Cell {self.cell_type} ({len(self.errors)} errors)"""
        return msg


class Notebook(object):
    def __init__(self, contents):
        if isinstance(contents, str):
            contents = json.loads(contents)
        self.nb_raw = contents
        self.cells = [Cell(cell) for cell in contents.get('cells', [])]
        self.error_summary = [(index, cell.execution_count,
                               cell.first_error_message(),
                               cell.number_of_errors())
                              for index, cell in enumerate(self.cells)
                              if cell.number_of_errors()]

    def number_of_errors(self):
        return sum([entry[3] for entry in self.error_summary])

    def execution_number_of_cells_with_errors(self):
        return [entry[1] for entry in self.error_summary]

    def contains_errors(self):
        return (self.number_of_errors() > 0)

    def summarize_errors(self):
        error_strings = [f'[{o[1]}] {o[2]}' for o in self.error_summary]
        return '\n'.join(error_strings)
