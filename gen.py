import os, sys, time

builtin_print = __builtins__.print
def print(*args, **kwargs):
    """Overrides print to add a prefix before each print."""
    global print_prefix
    builtin_print(print_prefix,end='')
    return builtin_print(*args, **kwargs)
__builtins__.print = print


print_prefix = ""
sys.path.append(sys.path[0]+"/generators")
moduleNames = os.listdir("./generators")
os.chdir("./generators")
errored = []
times = {}
start_total = time.time()
for module in moduleNames:
    if module.endswith(".py") and not module.startswith("_"):
        module_name = module[:-3]
        print("Generating mod: " + module_name)
        start_time = time.time()
        print_prefix = "[" + module_name + "] "
        imported_module = __import__(module_name)
        try:
            imported_module.generateMod()
            elapsed_time = time.time()-start_time
            print(f"Took {elapsed_time:.2f} seconds")
            times[module_name] = elapsed_time
        except Exception as e:
            print("Error when generating mod: " + module_name)
            print(e)
            errored.append(module_name)
        print_prefix = ""
elapsed_total = time.time() - start_total
print(f"Took {elapsed_total:.2f} seconds total.")

for tim in times:
    print(f"\t[{tim}] took {times[tim]:.2f} seconds")

if len(errored) > 0:
    print("Errored mods: ")
    for i in errored:
        print("\t"+i)
