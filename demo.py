import pyhtml
import student_x_page_1
import student_x_page_2
import student_x_page_3
import student_y_page_1
import student_y_page_2
import student_y_page_3

pyhtml.need_debugging_help=True

#All pages that you want on the site need to be added as below
pyhtml.MyRequestHandler.pages["/"]        =student_x_page_1   #Page to show when someone accesses "http://localhost/"
pyhtml.MyRequestHandler.pages["/student2y"]=student_y_page_2  #Page to show when someone accesses "http://localhost/studenty"
pyhtml.MyRequestHandler.pages["/student2x"]=student_x_page_2
pyhtml.MyRequestHandler.pages["/student3y"]=student_y_page_3
pyhtml.MyRequestHandler.pages["/student1y"]=student_y_page_1
pyhtml.MyRequestHandler.pages["/student3x"]=student_x_page_3
#Host the site!
pyhtml.host_site()