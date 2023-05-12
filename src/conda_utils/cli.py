import argparse
import logging
import sys

from conda_utils import __version__
from conda_utils.envfile import env_to_yaml

__author__ = "t-silvers"
__copyright__ = "t-silvers"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


def parse_args(args):
    """Parse command line parameters
    
    TODO: CLI not set up yet. This is just a copy of the cookiecutter template.

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="Generate an environment file from a conda environment.")
    
    # TODO: env output_dir overwrite
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"conda-utils {__version__}",
    )
    parser.add_argument(dest="n", help="Generate an environment file from a conda environment.", type=int, metavar="INT")
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    return parser.parse_args(args)


def setup_logging(loglevel):
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def main(args):
    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.debug("Starting crazy calculations...")
    env_to_yaml(args.env, args.output_dir, args.overwrite)
    _logger.info("Script ends here")


def run():
    main(sys.argv[1:])


if __name__ == "__main__":
    run()