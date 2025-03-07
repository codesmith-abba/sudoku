import sys

# from sudoku import (
#     initial_state,
#     actions,
#     transition_model,
#     solved,
#     select_unassigned_var,
#     domain_values,
#     consistent,
#     backtrack
# )

def main():
    # Check for proper Usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 log.py logs")
    logs = load_logs(sys.argv[1])

def load_logs(file):
    pass

if __name__ == "__main__":
    main()

