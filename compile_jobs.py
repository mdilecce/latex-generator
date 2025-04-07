import os
import subprocess
import yaml

# Path to the YAML file
yaml_file = "/home/argonauta/Projects/latex-generator/latex_jobs.yaml"

# Load the YAML file
with open(yaml_file, "r") as file:
    config = yaml.safe_load(file)

# Iterate over each job in the YAML file
for job in config.get("item", []):
    compile = job.get("compile", False)
    file = job.get("file")
    compiler = job.get("latex_compiler", "pdflatex")
    draft = job.get("draft", False)
    out_dir = job.get("out_dir", "./")
    extra_args = job.get("extra_args", "")
    lua_script = job.get("lua_script", "")
    jobname = job.get("jobname", "job")

    if compile:
        stdout_log = os.path.join(out_dir, f"{jobname}_stdout.log")
        stderr_log = os.path.join(out_dir, f"{jobname}_stderr.log")

        print(f"Compiling {file} with {compiler}...")
        with open(stdout_log, "a") as log:
            log.write(f"Compiling {file} with {compiler}...\n")
        os.makedirs(out_dir, exist_ok=True)

        # Add draft mode if enabled
        if draft:
            extra_args += " --draftmode"

        # Add Lua script if LuaLatex is used
        if compiler.lower() == "lualatex" and lua_script:
            extra_args += f" --lua={lua_script}"

        # Compile the LaTeX file
        command = (
            f"{compiler} {extra_args} --output-directory={out_dir} {file}"
        )
        try:
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True
            )
            with open(stdout_log, "a") as log:
                log.write(result.stdout)
            with open(stderr_log, "a") as log:
                log.write(result.stderr)
            if result.returncode != 0:
                print(
                    f"Error compiling {file}. Check the stderr log for details."
                )
                with open(stderr_log, "a") as log:
                    log.write(f"Error compiling {file}.\n")
            else:
                print(f"Compilation of {file} completed successfully.")
                with open(stdout_log, "a") as log:
                    log.write(
                        f"Compilation of {file} completed successfully.\n"
                    )
        except Exception as e:
            print(f"Exception occurred: {e}")
            with open(stderr_log, "a") as log:
                log.write(f"Exception occurred: {e}\n")
    else:
        print(f"Skipping {file} (compile option is false).")
        with open(stdout_log, "a") as log:
            log.write(f"Skipping {file} (compile option is false).\n")
