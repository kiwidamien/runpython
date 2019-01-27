from pathlib import Path
import yaml


DEFAULT_CONFIG_PATH = Path('~/.run_python/config.yaml').expanduser()


def _load_yaml(filename):
    with open(filename) as yaml_handle:
        yaml_contents = yaml.load(yaml_handle)
    return yaml_contents


class Config():
    """Represent configuration for running python scripts."""
    def __init__(self):
        """Create sensible default values.

        Used when no other config is present.
        """
        self.__dict__ = {
            'timeout': 600,
            'summary':  True,
            'detail': True,
            'summary_file': '.error_log_summary',
            'detail_file': '.error_log_detail',
            'kernel_name': None,
        }

    def load_config_from_file(self, filename,
                              error_on_new_attributes=False):
        """Load configuration from file.

        This will overwrite existing attributes in the configuration.
        Attributes not mentioned will not be changed.

        Parameters
        ----------
        filename : string or Path
            Location of the configuration file
        error_on_new_attribute: bool
            Indicates whether an unknown attribute will raise an error

        Returns
        -------
        bool
            Indicates whether the file was successfully found and loaded.
            If the file cannot be found, returns False (doesn't raise an error)

        Raises
        ------
        ValueError
            If error_on_new_attribute is True and the config file contains a
            new attribute, a ValueError is raised.
        """
        filename = Path(filename).expanduser()
        if not filename.exists():
            return False
        yaml_settings = _load_yaml(filename)
        for setting in yaml_settings:
            if error_on_new_attributes and (setting not in self.__dict__):
                raise ValueError(f'Trying to set unknown attribute {setting}')
            self.__dict__[setting] = yaml_settings[setting]
        return True

    def load_default_config(self):
        """Loads the users default config."""
        return self.load_config_from_file(DEFAULT_CONFIG_PATH)

    def write_config(self, filename):
        """Write config to file."""
        with open(filename, 'w') as config_out:
            yaml.dump(self.__dict__, config_out)
