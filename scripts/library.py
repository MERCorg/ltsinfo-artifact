import os
import re
import subprocess
from run_process import RunProcess, TimeExceededError, MemoryExceededError, ToolNotFoundError, ToolRuntimeError

MEMORY_REGEX = re.compile(r"\s*Maximum resident set size \(kbytes\): (.*)")
TOTAL_TIME_REGEX = re.compile(r"\s*User time \(seconds\): (.*)")

def run_experiment(arguments, env=None, timeout=600):

    output = []
    result_time = float('nan')
    result_memory = float('nan')

    if timeout is not None:
        # Use RunProcess with timeout
        try:
            if os.name != 'nt':
                # This is only available on linux and macos.
                # When using /usr/bin/time, we need to construct the full command properly
                tool = "/usr/bin/time"
                process_args = ["-v"] + arguments
            else:
                # On Windows, use the first argument as tool and rest as arguments
                tool = arguments[0] if arguments else ""
                process_args = arguments[1:] if len(arguments) > 1 else []
                
            if not tool:
                raise RuntimeError("No command provided")
                
            run_proc = RunProcess(tool, process_args, env, max_time=timeout)
            
            output = run_proc.stdout.splitlines(keepends=True)
            result_time = run_proc.user_time
            result_memory = run_proc.max_memory * 1024  # Convert MB to KB
            
            # Parse time and memory from output if available
            for line in output:
                result = TOTAL_TIME_REGEX.match(line)
                if result is not None:
                    time = float(result.group(1))
                    result_time = time

                result = MEMORY_REGEX.match(line)
                if result is not None:
                    memory = int(result.group(1))
                    result_memory = memory
                    
        except TimeExceededError:
            # Return NaN when timeout is hit
            return (["timeout"], float('nan'), float('nan'))
        except MemoryExceededError:
            return (["memory limit exceeded"], float('nan'), float('nan'))
        except (ToolNotFoundError, ToolRuntimeError) as e:
            return ([str(e)], float('nan'), float('nan'))
         
    return (output, result_time, result_memory)
