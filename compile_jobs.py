import os
import subprocess
import yaml

# Path to the YAML file
yaml_file = "/app/latex_jobs.yaml"

# Load the YAML file
with open(yaml_file, "r") as file:
    config = yaml.safe_load(file)

# Iterate over each job in the YAML file
for job in config.get("item", []):
    jobname = job.get("jobname") if job.get("jobname") else ""
    compile = job.get("compile", False)
    file = job.get("file")
    compiler = job.get("latex_compiler", "pdflatex")
    draft = job.get("draft", False)
    out_dir = job.get("output_dir", "/app/")
    output_format = job.get("output_format", "pdf")
    lua_script = job.get("lua_script", "")
    extra_args = job.get("extra_args", "") if job.get("extra_args") else ""

    if compile:
        print(f"Compiling {file} with {compiler}...")
        os.makedirs(out_dir, exist_ok=True)

        extra_args += "-interaction=nonstopmode"

        # Add draft mode if enabled
        if draft:
            extra_args += " --draftmode"

        if jobname != "":
            extra_args += f" --jobname='{jobname}'"

        # Add output format argument
        if output_format.lower() == "dvi":
            extra_args += " --output-format='dvi'"
        else:
            extra_args += " --output-format='pdf'"

        # Add Lua script if LuaLatex is used
        if compiler.lower() == "lualatex" and lua_script:
            extra_args += f" --lua={lua_script}"

        extra_args += f" --output-directory='{out_dir}'"

        # Compile the LaTeX file
        command = f"{compiler} {extra_args} '{file}'"
        log_file = f"{out_dir}/{jobname}.log"
        try:
            with subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            ) as process:
                for line in process.stdout:
                    print(line, end="")
                for line in process.stderr:
                    print(line, end="")
                process.wait()

            if process.returncode != 0:
                print(
                    f"Error compiling {file}. Check the stderr log for details."
                )
            else:
                print(f"Compilation of {file} completed successfully.")

            error_warning_file = f"/app/{out_dir}/{jobname}_error.log"
            # Extract warnings and errors from the log file
            warnings_errors = []
            try:
                with open(log_file, "r") as f:
                    for line in f:
                        if "Warning" in line or "Error" in line:
                            warnings_errors.append(line.strip())
            except FileNotFoundError:
                print(f"Log file {log_file} not found.")

            # Write warnings and errors to the new file
            if warnings_errors:
                with open(error_warning_file, "a") as ew_file:
                    ew_file.write(f"Job: {jobname}, File: {file}\n")
                    for line in warnings_errors:
                        ew_file.write(line + "\n")
                    ew_file.write("\n")

        except Exception as e:
            print(f"Exception occurred: {e}")
    else:
        print(f"Skipping {file} (compile option is false).")
