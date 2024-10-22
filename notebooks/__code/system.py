from __code import config
import getpass
import glob
import os
from ipywidgets import widgets
from IPython.display import display
from IPython.core.display import HTML
from IPython.display import clear_output
import subprocess

from __code.utilities.folder import find_first_real_dir

list_instrument_per_facility = {'SNS': ['VENUS', 'SNAP'],
'HFIR': ['CG1D'],
                                }


class System:

    working_dir = ''
    start_path = ''

    @classmethod
    def select_working_dir(cls, debugger_folder='', system_folder='',
                           facility='SNS',
                           instrument='VENUS',
                           notebook="N/A",
                           hfir_only=True):

        # try:

        debugging = config.debugging
        if debugging:
            print("** Using Debugging Mode! **")

        display(HTML("""
                   <style>
                   .result_label {
                      font-style: bold;
                      color: red;
                      font-size: 18px;
                   }
                   </style>
                   """))

        if not hfir_only:
            full_list_instruments = cls.get_full_list_instrument()
        else:
            full_list_instruments = ['CG1D']

        start_path = cls.get_start_path(debugger_folder=debugger_folder,
                                        system_folder=system_folder,
                                        instrument=full_list_instruments[0])

        cls.start_path = start_path

        if not hfir_only:
            select_instrument_ui = widgets.HBox([widgets.Label("Select Instrument",
                                                            layout=widgets.Layout(width='20%')),
                                                widgets.Select(options=full_list_instruments,
                                                                value=full_list_instruments[0],
                                                                layout=widgets.Layout(width='20%'))])
            cls.instrument_ui = select_instrument_ui.children[1]
            cls.instrument_ui.observe(cls.check_instrument_input, names='value')
        else:
            select_instrument_ui = widgets.HTML("<b>Instrument</b>: MARS (CG1D)<br><hr>")

        help_ui = widgets.Button(description="HELP",
                                 button_style='info')
        help_ui.on_click(cls.select_ipts_help)

        top_hbox = widgets.HBox([widgets.Label("IPTS-"),
                                 widgets.Text(value="",
                                              layout=widgets.Layout(width='10%')),
                                 widgets.Label("DOES NOT EXIST!",
                                               layout=widgets.Layout(width='20%'))])
        cls.result_label = top_hbox.children[2]
        cls.ipts_number = top_hbox.children[1]
        cls.result_label.add_class("result_label")
        or_label = widgets.Label("OR")

        list_and_default_folders = cls.get_list_folders(start_path=start_path)
        user_list_folders = list_and_default_folders['user_list_folders']
        default_value = list_and_default_folders['default_value']

        bottom_hbox = widgets.HBox([widgets.Label("Select Folder",
                                                  layout=widgets.Layout(width="20%")),
                                    widgets.Select(options=user_list_folders,
                                                   value=default_value,
                                                   layout=widgets.Layout(height='300px')),
                                    ])
        cls.user_list_folders = user_list_folders      
        box = widgets.VBox([select_instrument_ui, top_hbox, or_label, bottom_hbox, help_ui])
        display(box)

        cls.working_dir_ui = bottom_hbox.children[1]
        cls.manual_ipts_entry_ui = top_hbox.children[1]
        cls.manual_ipts_entry_ui.observe(cls.check_ipts_input, names='value')

        cls.result_label.value = ""

        # except:
        #     cls.working_dir = os.path.expanduser("~")
        #     display(HTML('<span style="font-size: 15px; color:blue">working dir set to -> ' + cls.working_dir +
        #                  '</span>'))

        # cls.log_use(notebook=notebook)

    @classmethod
    def get_full_list_instrument(cls):

        list_instrument = []
        for _key in list_instrument_per_facility.keys():
            _facility_list_instrument = list_instrument_per_facility[_key]
            for _instr in _facility_list_instrument:
                list_instrument.append(_instr)
        return list_instrument

    @classmethod
    def get_list_folders(cls, start_path=''):
        debugging = config.debugging

        if debugging:
            instrument = cls.get_instrument_selected()
            cls.start_path = "~/"
            for path in config.debugger_instrument_folder[instrument]:
                if os.path.exists(path):
                    cls.start_path = start_path

        list_folders = sorted(glob.glob(os.path.join(start_path, '*')))
        short_list_folders = [os.path.basename(_folder) for _folder in list_folders if os.path.isdir(_folder)]
        # short_list_folders = sorted(short_list_folders)

        # if user mode, only display folder user can access
        default_value = ''
        if not debugging:
            user_list_folders = [os.path.basename(_folder) for _folder in list_folders if os.access(_folder, os.R_OK)]
            user_list_folders.sort(reverse=True)
            if len(user_list_folders) > 0:
                default_value = user_list_folders[0]
        else:  # debugging
            user_list_folders = short_list_folders
            default_value = config.project_folder
            if not (default_value in user_list_folders):
                if len(user_list_folders) > 0:
                    default_value = user_list_folders[0]

        return {'user_list_folders': user_list_folders,
                'default_value': default_value}

    @classmethod
    def get_facility_from_instrument(cls, instrument='CG1D'):

        for _facility in list_instrument_per_facility:
            list_instrument = list_instrument_per_facility[_facility]
            if instrument in list_instrument:
                return _facility

        return 'HFIR'

    @classmethod
    def get_instrument_selected(cls):
        return cls.instrument_ui.value

    @classmethod
    def get_facility_selected(cls):
        return cls.get_facility_from_instrument(instrument=cls.get_instrument_selected())

    @classmethod
    def get_start_path(cls, debugger_folder='', system_folder='', instrument=''):

        facility = cls.get_facility_from_instrument(instrument=instrument)

        username = getpass.getuser()

        debugging = config.debugging
        debugger_username = config.debugger_username

        found_a_folder = False
        if debugger_folder == '':
            for _folder in config.debugger_folder:
                if os.path.exists(_folder):
                    debugger_folder = _folder
                    found_a_folder = True
                    break

        if not found_a_folder:
            debugger_folder = './'

        if debugging and (username == debugger_username):
            # print("** Using Debugging Mode! **")

            # check that in debugging mode, on analysis machine, default folder exists
            import socket

            if socket.gethostname() == config.analysis_machine:
                if not os.path.exists(debugger_folder):
                    debugging = False

            start_path = debugger_folder
        else:
            if system_folder == '':
                start_path = "/{}/{}/".format(facility, instrument)
            else:
                start_path = system_folder
            import warnings
            warnings.filterwarnings('ignore')

        return start_path

    @classmethod
    def select_ipts_help(cls, value):
        import webbrowser
        webbrowser.open("https://neutronimaging.pages.ornl.gov/tutorial/notebooks/select_ipts/")

    @classmethod
    def check_instrument_input(cls, value_dict):
        instrument = value_dict['new']

        start_path = cls.get_start_path(instrument=instrument)
        cls.start_path = start_path
        list_and_default_folders = cls.get_list_folders(start_path=start_path)
        user_list_folders = list_and_default_folders['user_list_folders']
        default_value = list_and_default_folders['default_value']

        cls.working_dir_ui.options = user_list_folders
        cls.working_dir_ui.value = default_value

        cls.ipts_number.value = ''
        cls.result_label.value = ''

    @classmethod
    def check_ipts_input(cls, value):
        ipts = value['new']
        full_ipts = 'IPTS-{}'.format(ipts)
        if os.path.exists(os.path.join(cls.start_path, full_ipts)):
            # display(HTML("""
            #            <style>
            #            .result_label {
            #               font-style: bold;
            #               color: green;
            #               font-size: 18px;
            #            }
            #            </style>
            #            """))
            cls.result_label.value = "OK"
            #select IPTS folder defined
            cls.working_dir_ui.value = full_ipts

        else:
            # display(HTML("""
            #            <style>
            #            .result_label {
            #               font-style: bold;
            #               color: red;
            #               font-size: 18px;
            #            }
            #            </style>
            #            """))
            cls.result_label.value = "DOES NOT EXIST!"

    @classmethod
    def get_working_dir(cls):
        if cls.working_dir:
            return find_first_real_dir(cls.working_dir)
        else:
            return find_first_real_dir(os.path.join(cls.start_path, cls.working_dir_ui.value))


    @classmethod
    def get_number_of_gpu(cls):
        try:
            str_list_gpu = subprocess.run(["nvidia-smi", "-L"], stdout=subprocess.PIPE)
            list_gpu = str_list_gpu.stdout.decode("utf-8").split("\n")
            nbr_gpu = 0
            for _gpu in list_gpu:
                if not (_gpu == ""):
                    nbr_gpu += 1
            return nbr_gpu

        except FileNotFoundError:
            return 1
