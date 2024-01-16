import cgi
import sys

form = cgi.FieldStorage()

coffee_type = form.getvalue("coffee_type", "Американо")
extras = form.getlist("extras")
quantity = form.getvalue("quantity", "1")
sys.stdout.write("Content-type: text/html; charset=utf-8\n\n")
print("<html>")
print("<head><title>Магазин кави</title></head>")
print("<link rel='stylesheet' href='../style/style.css'>")
print("<body>")
print("<center>")
print("<br>")
print("<h1>Ваше замовлення:</h1>")
print("<form>")
print("<p>Кава: {}</p>".format(coffee_type))
print("<p>Додатки: {}</p>".format(extras))
print("<p>Кількість: {}</p>".format(quantity))
print("</form>")
print("</center>")
print("</body>")
print("</html>")
