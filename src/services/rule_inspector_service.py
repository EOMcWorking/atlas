from src.services.architecture_service import (
    analyze_architecture
)

from src.services.circular_dependency_service import (
    find_circular_dependencies
)

from src.services.dead_code_service import (
    find_dead_code
)

from src.services.large_file_service import (
    find_large_files
)


def inspect_architecture():

    strengths = []
    weaknesses = []
    priorities = []

    architecture = (
        analyze_architecture()
    )

    dead_code = (
        find_dead_code()
    )

    cycles = (
        find_circular_dependencies()
        .get("cycles", [])
    )

    large_files = (
        find_large_files()
        .get("large_files", [])
    )

    most_connected = architecture.get(
        "most_connected",
        []
    )

    isolated = architecture.get(
        "isolated",
        []
    )

    dead_files = dead_code.get(
        "dead_code_candidates",
        []
    )

    # High Coupling

    if most_connected:

        top_count = most_connected[0][0]
        top_file = most_connected[0][1]

        if top_count > 20:

            weaknesses.append(
                f"High coupling detected in "
                f"{top_file} ({top_count} imports)"
            )

            priorities.append(
                f"Split responsibilities in "
                f"{top_file}"
            )

        elif top_count > 15:

            weaknesses.append(
                f"{top_file} imports "
                f"{top_count} modules"
            )

            priorities.append(
                f"Reduce coupling in "
                f"{top_file}"
            )

    # Circular Dependencies

    if cycles:

        weaknesses.append(
            f"{len(cycles)} circular "
            "dependencies detected"
        )

        priorities.append(
            "Remove circular dependencies"
        )

    # Large Files

    if large_files:

        weaknesses.append(
            f"{len(large_files)} large "
            "files detected"
        )

        priorities.append(
            "Split large files"
        )

    else:

        strengths.append(
            "No oversized files detected"
        )

    # Dead Code

    if dead_files:

        weaknesses.append(
            f"{len(dead_files)} dead code "
            "candidates detected"
        )

        priorities.append(
            "Review dead code candidates"
        )

    if len(dead_files) < 5:

        strengths.append(
            "Low number of dead code "
            "candidates"
        )

    # Isolated Modules

    if len(isolated) > 5:

        weaknesses.append(
            f"{len(isolated)} isolated "
            "modules detected"
        )

        priorities.append(
            "Review isolated modules"
        )

    # General Strengths

    strengths.append(
        "Dependency graph available"
    )

    strengths.append(
        "Architecture analysis available"
    )

    return {
        "strengths": strengths,
        "weaknesses": weaknesses,
        "priorities": priorities,
        "dead_code": dead_files,
        "cycles": cycles,
        "large_files": large_files
    }