from .fastread.parameter_read import _output_directories
import matplotlib.pyplot as plt
import os

try:
    import seaborn as sns
    imported_seaborn = True
except ImportError:
    print("""
    Cannot find seaborn module. Plots will be drawn according to the
    standard matplotlib style.
        """)
    imported_seaborn = False
finally:
    pass

try:
    import f90nml
    imported_f90nml = True
except ImportError:
    print("""
    Cannot find f90nml module.
    Namelist will be read via a standard text interpreter.
        """)
    imported_f90nml = False


class Simulation(object):
    """
    Main class with all the simulation information.

    From here, all the diagnostic can be accessed.
    To initialize the class, after having imported the package lampy,
    call

    >>> s=lampy.Simulation(path).

    In all the package documentation, the previous sintax for the
    simulation import will be assumed, so we will refer to the object
    'Simulation' as 's'.

    Parameters
    --------
    path : str, optional
        Path where all the simulation data are stored.
        If not given, by default '.' is passed

    Returns
    --------
    s.params : dict
        Dictionary containing all the parameters
    s.path : str
        Path of the main simulation folder
    s.directories : list
        List of all the output folders
    s.outputs : list
        List of all the available generated outputs
    s.Field : class
        Class containing all the methods to manipulate fields data.
        Check the information about the Field class
        by typing

        >>> help(s.Field)

    s.Particles : class
        Class containing all the methods to manipulate particle data.
        Check the information about the Particles class
        by typing

        >>> help(s.Particles)

    s.Diagnostic : class
        Class containing all the methods to manipulate diagnostic files.
        Check the information about the Particles class
        by typing

        >>> help(s.Diagnostics)
    """

    def __init__(self, path=os.getcwd()):
        """
        Constructor for the Simulation class.

        It checks the datas, finds the data folders and then
        generates the simulation parameters

        Returns
        --------
        params : dict
            Dictionary containing all the parameters
        path : str
            Path of the main simulation folder
        directories : list
            List of all the output folders
        s.outputs : list
            List of all the available generated outputs
        """
        from .datas.Field import Field, _Field_list
        from .datas.Parts import Particles
        from .datas.Diag import Diagnostics

        plt.ion()

        if imported_seaborn:
            sns.set()
            sns.set_style('ticks')

        if len(path) == 0:
            path = os.getcwd()
        path = os.path.abspath(path)

        if not os.path.exists(path):
            raise NotADirectoryError('Directory {} does not exist'
                                     .format(path))
        self.params = self._open_folder(path)
        self.dx = self.params['dx']
        if 'dz' in self.params.keys():
            self.dz = self.params['dz']
        if 'dy' in self.params.keys():
            self.dy = self.params['dy']
        self.nx = self.params['nx']
        self.ny = self.params['ny']
        self.nz = self.params['nz']
        self._dimensions = self.params['n_dimensions']
        self._a_from_imaginary = False
        self.path = os.path.abspath(path)
        self._Directories = Directories(self)
        self.directories = self._Directories._show()
        self._timesteps = self._collect_timesteps()
        self.outputs = self._collect_outputs()
        self.Field = Field(self, _Field_list)
        self.Particles = Particles(self)
        self._box_limits = self.Field._box_limits
        self.Diagnostics = Diagnostics(self)

    def _collect_outputs(self, *args):

        from .utilities.Utility import _translated_filenames

        if len(args) > 0:
            directory = args[0]
        else:
            directory = self.directories[-1]

        output_list = list()

        for elem in self._Directories._filelist([directory]):
            for key, value in _translated_filenames.items():
                if value in elem:
                    output_list += [key]
                    break

        if 'Ey' in output_list and 'Bz' in output_list:
            output_list += ['Fy']
        if 'Ez' in output_list and 'By' in output_list:
            output_list += ['Fz']
        if 'ReA' in output_list and 'ImA' in output_list \
                and 'A' not in output_list:
            output_list += ['A']
            self._a_from_imaginary = True
        if 'ReA' in output_list and 'ImA' in output_list:
            output_list += ['E_laser', 'E_envelope']

        return output_list

    def _collect_timesteps(self):

        from .utilities.Utility import _total_filenamelist
        from .fastread.parameter_read import _read_file_timestep

        _timesteps = dict()
        for directory in self.directories:
            for filename in _total_filenamelist:
                for elem in self._Directories._filelist([directory]):
                    if filename in elem:
                        break
                file_timestep_path = os.path.join(self.path, directory, elem)
                _timesteps[directory] = _read_file_timestep(file_timestep_path)
                _timesteps[directory] = round(_timesteps[directory], 2)
                break
        return _timesteps

    def _derive_file_path(self, field_name, timestep):

        from .utilities.Utility import _translate_filename

        filename = _translate_filename(field_name)
        for key, value in self._timesteps.items():
            if timestep == value:
                folder = key
        filename = filename+folder[-2:]
        file_path = os.path.join(self.path, folder, filename)

        return file_path

    def _nearest_time(self, timestep):

        times = list()
        times += [time for time in self._timesteps.values()]

        if timestep in times:
            return timestep
        else:
            mintime = min(times, key=lambda x: abs(x-timestep))
            print("""
    WARNING: Requested time {} is not available.
    Output is retrieved at time {}""".format(timestep,
                                             mintime))
            return mintime

    def _open_folder(self, path):

        from .utilities.Utility import _read_simulation_nml,\
            _compute_physical_parameters, _compute_simulation_parameters,\
            _read_simulation_without_nml

        if imported_f90nml:
            params = _read_simulation_nml(path)
        else:
            params = _read_simulation_without_nml(path)

        _compute_physical_parameters(params)
        _compute_simulation_parameters(params)

        return params

    def show_files(self, *args):
        """
        Method to show the available output files in a given folder.

        Params
        --------
        directory : str (list), optional
            A single, or multiple directories where to check the outputs.
            By default, all the available output directories are checked.
        """
        if len(args) > 0:
            if type(args[0]) == str:
                directories = [args[0]]
            elif type(args[0]) == list:
                directories = args[0]
            else:
                print("""Argument of show_files must be either a folder name
                or a list of folders""")
                return
        else:
            directories = self.directories

        for directory in directories:
            files = os.listdir(os.path.join(self.path, directory))
            print('Directory '+str(directory)+' contains:')
            print('')
            print(files)
            print('')

    def box(self):
        """
        Method that prints the simulation box informations
        """
        nx = self.nx
        ny = self.ny
        nz = self.nz
        dx = self.dx
        if 'dz' in self.params.keys():
            dz = self.params['dz']
        if 'dy' in self.params.keys():
            dy = self.params['dy']
        nd = self.params['n_dimensions']
        str_flag = self.params['str_flag']
        print("""
        Running the simulation in a {}D box.
        """.format(nd))
        print("""
        Nx = {} <==> dx = {} p.p.m
        """.format(nx, dx))
        if nd > 1:
            print("""
        Ny = {} <==> dy = {} p.p.m
        """.format(ny, dy))
        if nd > 2:
            print("""
        Nz = {} <==> dz = {} p.p.m
        """.format(nz, dz))
        if str_flag > 0:
            print("""
        The grid is transversally stretched with a stretching flag {}
        """.format(str_flag))

    def show_times(self):
        """
        Method to show the output times (in microns)
        corresponding to every folder.
        """
        for key, value in self._timesteps.items():
            print('Directory '+str(key)+' contains output at time '+str(value))

    def show_outputs(self):
        """
        Method that returns a list of the available
        outputs.
        """
        print(self.outputs)


class Directories(object):

    def __init__(self, Simulation):

        self._path = Simulation.path
        self._listdir = _output_directories(self._path)

    def _filelist(self, *args):
        if len(args) > 0:
            listdir = args[0]
        else:
            listdir = self._listdir
        self._listfile = list()
        for directory in listdir:
            templist = os.listdir(os.path.join(self._path, directory))
            for elem in templist[:]:
                if '.dat' in elem:
                    templist.remove(elem)
            self._listfile += templist

        return self._listfile

    def _show(self):
        return self._listdir
