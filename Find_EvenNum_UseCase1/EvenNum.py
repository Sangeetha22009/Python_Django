
def get_even_numbers(lst: list[int]) -> list[int]:    
    list_evennumbers = []
    for num in lst:
        if num % 2 == 0:
            list_evennumbers.append(num)
        else:
            pass          
    print(list_evennumbers)

get_even_numbers([1, 2, 3, 4, 5, 6])