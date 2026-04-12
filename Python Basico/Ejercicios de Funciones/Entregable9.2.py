global_scope = 10

def local_function():
    local_scope = 5
    global global_scope
    global_scope = 33

#print(local_scope)
print(f"Variable global antes cambio: {global_scope}")
local_function()
print(f"Variable global despues cambio: {global_scope}")