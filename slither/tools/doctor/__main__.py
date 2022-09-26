import argparse
import logging
from pathlib import Path

from crytic_compile import cryticparser
import crytic_compile.crytic_compile as crytic_compile
from slither.utils.colors import red, yellow, green


def parse_args():
    """
    Parse the underlying arguments for the program.
    :return: Returns the arguments for the program.
    """
    parser = argparse.ArgumentParser(
        description="Troubleshoot running Slither on your project",
        usage="slither-doctor project",
    )

    parser.add_argument("project", help="The codebase to be tested.")

    # Add default arguments from crytic-compile
    cryticparser.init(parser)

    return parser.parse_args()


def detect_platform(project: str, **kwargs):
    print("## Project platform")
    print()

    path = Path(project)
    if path.is_file():
        print(
            yellow(
                f"{project!r} is a file. Using it as target will manually compile your code with solc and _not_ use a compilation framework. Is that what you meant to do?"
            )
        )
        return

    print(f"Trying to detect project type for {project!r}")

    supported_platforms = crytic_compile.get_platforms()
    skip_platforms = {"solc", "solc-json", "archive", "standard", "etherscan"}
    detected_platforms = {
        platform.NAME: platform.is_supported(project, **kwargs)
        for platform in supported_platforms
        if platform.NAME.lower() not in skip_platforms
    }
    platform_qty = len([platform for platform, state in detected_platforms.items() if state])

    print("Is this project using...")
    for platform, state in detected_platforms.items():
        print(f"    =>  {platform + '?':<15}{state and green('Yes') or red('No')}")
    print()

    if platform_qty == 0:
        print(red("No platform was detected! This doesn't sound right."))
        print(
            yellow(
                "Are you trying to analyze a folder with standalone solidity files, without using a compilation framework? If that's the case, then this is okay."
            )
        )
    elif platform_qty > 1:
        print(red("More than one platform was detected! This doesn't sound right."))
        print(
            red("Please use `--compile-force-framework` in Slither to force the correct framework.")
        )
    else:
        print(green("A single platform was detected."), yellow("Is it the one you expected?"))

    print(end="\n\n")


def compile_project(project: str, **kwargs):
    print("## Project compilation")
    print()

    print("Invoking crytic-compile on the project, please wait...")

    try:
        crytic_compile.CryticCompile(project, **kwargs)
    except Exception as e:
        print(red("Project compilation failed :( The following error was generated:"), end="\n\n")
        print(yellow("---- snip 8< ----"))
        logging.exception(e)
        print(yellow("---- >8 snip ----"))

    print(end="\n\n")


def main():
    args = parse_args()

    kwargs = vars(args)

    detect_platform(**kwargs)
    compile_project(**kwargs)

    # TODO other checks


if __name__ == "__main__":
    main()
