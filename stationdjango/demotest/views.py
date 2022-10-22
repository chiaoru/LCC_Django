from django.shortcuts import render

# Create your views here.

def test(request):
    
    name = "John"
    age = 20
    
    score = 70
    
    listdata = range(1,10)
    
    student1 = {"name":"陳美麗","age":18,"phone":"02-23456789"}
    student2 = {"name":"林聰明","age":20,"phone":"07-27475673"}
    student3 = {"name":"林小燕","age":18,"phone":"04-22223343"}
    students = [student1,student2,student3]
    
    
    return render(request, 'base.html', locals())
