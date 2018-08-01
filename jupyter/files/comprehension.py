def my_func(arg1, arg2):
    list_var = [str(x) for x in arg1 if x > 10
                for y in arg2]
    dict_var = {str(x): 4 for x in arg1 if x <= 4}
    set_var = {str(x) for x in arg1 if x == 5}
    return list_var + ['test'], dict_var, set_var
