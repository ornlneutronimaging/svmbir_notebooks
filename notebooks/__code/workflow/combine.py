import logging

from __code.parent import Parent
from __code import DataType


class Combine(Parent):
    
    final_list_of_runs = {DataType.sample: [],
                          DataType.ob: [],
    }

    def run(self):
        self.removing_rejected_runs()
        self.combining_runs()

    def removing_rejected_runs(self):
        logging.info(f"removing rejected runs:")
        list_of_sample_runs_to_reject = self.parent.list_of_sample_runs_to_reject_ui.value
        list_of_ob_runs_to_reject = self.parent.list_of_ob_runs_to_reject_ui.value
        logging.info(f"\tlist of sample runs to reject: {list_of_sample_runs_to_reject}")
        logging.info(f"\tlist of ob runs to reject: {list_of_ob_runs_to_reject}")

        list_of_runs = self.parent.list_of_runs
        for _run in list_of_runs[DataType.sample]:
            if _run in list_of_sample_runs_to_reject:
                continue
            else:
                self.final_list_of_runs[DataType.sample].append(_run)

        for _run in list_of_runs[DataType.ob]:
            if _run in list_of_ob_runs_to_reject:
                continue
            else:
                self.final_list_of_runs[DataType.ob].append(_run)

        self.parent.list_of_runs = self.final_list_of_runs

    def combining_runs(self):
        logging.info(f"combining runs:")

        logging.info(f"\t{self.parent.list_of_runs[DataType.sample]}")
