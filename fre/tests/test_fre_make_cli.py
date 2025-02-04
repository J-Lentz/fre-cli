''' test "fre make" calls '''

from click.testing import CliRunner
from pathlib import Path
import os
import shutil
from fre import fre

runner = CliRunner()

def test_cli_fre_make():
    ''' fre make '''
    result = runner.invoke(fre.fre, args=["make"])
    assert result.exit_code == 0

def test_cli_fre_make_help():
    ''' fre make --help '''
    result = runner.invoke(fre.fre, args=["make", "--help"])
    assert result.exit_code == 0

def test_cli_fre_make_opt_dne():
    ''' fre make optionDNE '''
    result = runner.invoke(fre.fre, args=["make", "optionDNE"])
    assert result.exit_code == 2

TEST_DIR = Path("fre/tests")
OUT_PATH=f"{TEST_DIR}/test_files/fremake_out"
def test_cli_fre_make_create_checkout_baremetal():
    ''' fre make create-checkout -y am5.yaml -p ncrc5.intel23 -t debug'''
    # remove the created script to re-create it, if it exists
    #if Path(f"{OUT_PATH}/fremake_canopy/test/am5/src/checkout.sh").exists():
    #    Path(f"{OUT_PATH}/fremake_canopy/test/am5/src/checkout.sh").unlink()

    # Set paths and click options
    yamlfile = Path("fre/make/tests/null_example/")
    platform = "ncrc5.intel23"
    target = "debug"

    # Create output path to test that files exist
    Path(OUT_PATH).mkdir(parents=True,exist_ok=True)

    # Set HOME for modelRoot location (output location) in fre make
    old_home = os.environ["HOME"]
    os.environ["HOME"]=str(Path(OUT_PATH))

    # run create-checkout
    result = runner.invoke(fre.fre, args=["make", "create-checkout", "-y", f"{yamlfile}/null_model.yaml", "-p", platform, "-t", target])

    os.environ["HOME"] = old_home

    # Check for successful command, creation of checkout script, and that script is executable
    # os.access - checks is file has specific access mode, os.X_OK - checks executable permission
    assert all ([result.exit_code == 0,
                 Path(f"{OUT_PATH}/fremake_canopy/test/null_model_full/src/checkout.sh").exists(),
                 os.access(Path(f"{OUT_PATH}/fremake_canopy/test/null_model_full/src/checkout.sh"), os.X_OK)])

def test_cli_fre_make_create_checkout_container():
    ''' fre make create-checkout -y null_model.yaml -p hpcme.2023 -t debug'''
    # Set paths and click options
    yamlfile = Path("fre/make/tests/null_example/")
    platform = "hpcme.2023"
    target = "debug"

    # Set HOME for modelRoot location (output location) in fre make
    old_home = os.environ["HOME"]
    os.environ["HOME"]=str(Path(OUT_PATH))

    # run create-checkout
    result = runner.invoke(fre.fre, args=["make", "create-checkout", "-y", f"{yamlfile}/null_model.yaml", "-p", platform, "-t", target])

    os.environ["HOME"] = old_home

    # Check for successful command, creation of checkout script, and that script is executable
    # os.access - checks is file has specific access mode, os.X_OK - checks executable permission
    assert all ([result.exit_code == 0,
                 Path(f"tmp/{platform}/checkout.sh").exists(),
                 os.access(Path(f"tmp/{platform}/checkout.sh"), os.X_OK) == False ])

def test_cli_fre_make_create_checkout_cleanup():
    ''' make sure the checked out code doesnt stick around to mess up another pytest call '''
    assert Path(OUT_PATH).exists()
    shutil.rmtree(OUT_PATH)
    assert not Path(OUT_PATH).exists()
